import asyncio

import aiohttp
from sqlmodel import select

from icon_governance.log import logger
from icon_governance.metrics import prom_metrics
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


def run_prep_state(session):
    logger.info(f"Starting {__name__} cron")

    result = session.execute(select(Prep))
    preps = result.scalars().all()

    if len(preps) == 0:
        raise Exception("Empty DB.")

    for prep in preps:
        if prep.api_endpoint is None:
            prep.node_state = "Unknown"
            session.merge(prep)
            continue

        prep.metrics_endpoint = prep.api_endpoint + "/metrics"
        if not prep.metrics_endpoint.startswith("http://"):
            prep.metrics_endpoint = "http://" + prep.metrics_endpoint

    asyncio.run(
        get_prep_state(
            preps=preps,
        )
    )

    for prep in preps:
        session.merge(prep)
    session.commit()

    prom_metrics.preps_attributes_cron_ran.inc()
    logger.info(f"Ending {__name__} cron")


if __name__ == "__main__":
    from icon_governance.db import session_factory

    with session_factory() as session:
        run_prep_state(session=session)
