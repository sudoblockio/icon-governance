from loguru import logger
from sqlmodel import select

from icon_governance.metrics import prom_metrics
from icon_governance.models.preps import Prep
from icon_governance.utils.rpc import convert_hex_int, getStake, post_rpc_json


def run_prep_stake(session):
    logger.info("Starting stake cron")

    result = session.execute(select(Prep))
    preps = result.scalars().all()

    for prep in preps:
        prep.stake = convert_hex_int(post_rpc_json(getStake(prep.address))["stake"]) / 1e18

        session.merge(prep)
        session.commit()

    prom_metrics.preps_attributes_cron_ran.inc()
    logger.info("Ending stake cron")


if __name__ == "__main__":
    from icon_governance.db import session_factory

    with session_factory() as session:
        run_prep_stake(session=session)
