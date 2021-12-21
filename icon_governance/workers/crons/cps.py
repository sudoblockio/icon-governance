from time import sleep

from sqlmodel import select

from icon_governance.config import settings
from icon_governance.log import logger
from icon_governance.models.preps import Prep
from icon_governance.utils.rpc import (
    convert_hex_int,
    get_preps_cps,
    get_sponsors_record,
    post_rpc_json,
)


def get_cps(session):
    sponsors = post_rpc_json(get_sponsors_record())

    if sponsors is None:
        logger.info("No sponsors found from rpc.")
        sleep(1)
        return

    for k, v in sponsors.items():
        prep = session.get(Prep, k)
        if prep is None:
            logger.info("No preps found in db? Should not ever happen cuz of db_init.")
            continue

        prep.sponsored_cps_grants = convert_hex_int(v)

        session.merge(prep)
        session.commit()

    result = session.execute(select(Prep))
    preps = result.scalars().all()

    cps_preps = post_rpc_json(get_preps_cps())
    prep_list = [i["address"] for i in cps_preps]

    for prep in preps:
        if prep.address in prep_list:
            prep.cps_governance = True
        else:
            prep.cps_governance = False

        session.merge(prep)
        session.commit()


def cps_cron(session):
    while True:
        logger.info("Starting cps cron")
        get_cps(session)
        logger.info("CPS cron ran.")
        sleep(settings.CRON_SLEEP_SEC * 10)


if __name__ == "__main__":
    from icon_governance.db import session_factory

    get_cps(session_factory())
