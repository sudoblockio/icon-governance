import asyncio
import json

import aiohttp

from icon_governance.config import settings
from icon_governance.models.preps import Prep


async def get_pool_stats_async_resp(session, prep: Prep):
    try:
        async with session.get(url=prep.metrics_endpoint, timeout=5) as response:
            resp = await response.read()
    except Exception as e:
        prep.node_state = "Unknown"
        return

    for i in resp.decode("utf-8").split("\n"):
        if i.startswith("goloop_consensus_round_duration"):
            if int(float(i.split()[-1])) > 1500:
                prep.node_state = "Synced"
                return
            elif int(float(i.split()[-1])) < 1500:
                prep.node_state = "BlockSync"
                return
            break
    prep.node_state = "Unknown"


async def get_prep_state(preps: list[Prep]):
    async with aiohttp.ClientSession() as session:
        ret = await asyncio.gather(*[get_pool_stats_async_resp(session, prep=i) for i in preps])
    return ret


async def get_rpc_async_resp(session, method: str, params: dict):
    async with session.post(
        url=settings.ICON_NODE_URL,
        json={
            "jsonrpc": "2.0",
            "method": method,
            "id": 1,
            "params": params,
        },
        timeout=5,
    ) as response:
        r = await response.read()

    response = json.loads(r)
    if "result" in response:
        return response["result"]
    else:
        return response


async def get_delegation(addresses: list[dict]):
    async with aiohttp.ClientSession() as session:
        ret = await asyncio.gather(
            *[
                get_rpc_async_resp(
                    session,
                    method="icx_call",
                    params={
                        "to": "cx0000000000000000000000000000000000000000",
                        "dataType": "call",
                        "data": {"method": "getDelegation", "params": {"address": i["address"]}},
                    },
                )
                for i in addresses
            ]
        )
    return ret
