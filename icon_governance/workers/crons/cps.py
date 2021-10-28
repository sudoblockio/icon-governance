from time import sleep

from icon_governance.config import settings

# from icon_governance.db import session
from icon_governance.log import logger
from icon_governance.models.preps import Prep
from icon_governance.models.proposals import Proposal
from icon_governance.utils.rpc import (
    convert_hex_int,
    get_sponsors_record,
    post_rpc_json,
)


def cps_cron(session):
    while True:
        logger.info("Starting cps cron")
        sponsors = post_rpc_json(get_sponsors_record())

        if sponsors is None:
            logger.info("No sponsors found from rpc. Chilling for a bit.")
            sleep(60)
            continue

        for k, v in sponsors.items():
            prep = session.get(Prep, k)
            if prep is None:
                logger.info("No preps found in db? Should not ever happen cuz of db_init.")
                continue

            prep.sponsored_cps_grants = convert_hex_int(v)

            session.add(prep)
            try:
                session.commit()
                session.refresh()
            except:
                session.rollback()
                raise
            finally:
                session.close()

        logger.info("CPS cron ran.")
        sleep(settings.CRON_SLEEP_SEC * 10)


if __name__ == "__main__":
    from icon_governance.db import session_factory

    cps_cron(session_factory())
