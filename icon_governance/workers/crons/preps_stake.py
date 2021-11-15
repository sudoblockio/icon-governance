from time import sleep

from sqlmodel import select

from icon_governance.config import settings
from icon_governance.log import logger
from icon_governance.metrics import prom_metrics
from icon_governance.models.preps import Prep
from icon_governance.utils.rpc import convert_hex_int, getStake, post_rpc_json


def prep_stake_cron(session):

    while True:
        logger.info("Starting stake cron")

        result = session.execute(select(Prep))
        preps = result.scalars().all()

        for prep in preps:
            prep.stake = convert_hex_int(post_rpc_json(getStake(prep.address))["stake"]) / 1e18

            session.merge(prep)
            session.commit()

        logger.info("Prep stake ran.")
        prom_metrics.preps_stake_cron_ran.inc()
        sleep(settings.CRON_SLEEP_SEC)


if __name__ == "__main__":
    from icon_governance.db import session_factory

    prep_stake_cron(session_factory())
