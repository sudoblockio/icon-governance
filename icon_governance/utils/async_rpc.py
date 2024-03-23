import asyncio
import json

import aiohttp

from icon_governance.config import settings


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
