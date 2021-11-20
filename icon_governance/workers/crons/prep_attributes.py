from time import sleep

from icon_governance.config import settings
from icon_governance.log import logger
from icon_governance.metrics import prom_metrics
from icon_governance.models.preps import Prep
from icon_governance.utils.rpc import (
    convert_hex_int,
    getDelegation,
    getPReps,
    post_rpc_json,
)


def get_prep_attributes(session):
    preps = post_rpc_json(getPReps())
    if preps is None:
        logger.info("No preps found from rpc.")
        sleep(1)
        return

    for p in preps["preps"]:
        prep = session.get(Prep, p["address"])

        if prep is None:
            logger.info("No preps found in db? Should not ever happen cuz of db_init.")
            continue

        delegation = post_rpc_json(getDelegation(p["address"]))

        prep.voted = convert_hex_int(delegation["totalDelegated"]) / 1e18
        prep.voting_power = convert_hex_int(delegation["votingPower"]) / 1e18

        prep.total_blocks = convert_hex_int(p["totalBlocks"])
        prep.validated_blocks = convert_hex_int(p["validatedBlocks"])
        # prep.unvalidated_sequence_blocks = convert_hex_int(p["unvalidatedSequenceBlocks"])

        prep.bonded = convert_hex_int(p["bonded"])
        prep.bondedDelegation = convert_hex_int(p["bondedDelegation"])

        prep.delegated = convert_hex_int(p["delegated"]) / 1e18

        prep.irep = convert_hex_int(p["irep"]) / 1e18

        prep.grade = p["grade"]
        prep.penalty = p["penalty"]

        session.merge(prep)
        try:
            session.commit()
            session.refresh(prep)
        except:
            session.rollback()
            raise
        finally:
            session.close()


def prep_attributes_cron(session):
    while True:
        logger.info("Starting attributes cron")
        get_prep_attributes(session)
        logger.info("Prep attributes ran.")
        prom_metrics.preps_attributes_cron_ran.inc()
        sleep(settings.CRON_SLEEP_SEC)


if __name__ == "__main__":
    from icon_governance.db import session_factory

    get_prep_attributes(session_factory())
