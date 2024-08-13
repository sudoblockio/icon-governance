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
    get_network_info,
)


def run_prep_attributes(session):
    logger.info(f"Starting {__name__} cron")

    if settings.NETWORK_NAME in ["lisbon", "berlin"]:
        network_info = get_network_info()
        bond_requirement_rate = int(network_info["bondRequirementRate"], 0) / 10_000

    preps_rpc = post_rpc_json(getPReps())
    if preps_rpc is None:
        logger.info("No preps found from rpc.")
        sleep(1)
        return

    for p in preps_rpc["preps"]:
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
        prep.power = convert_hex_int(p["power"])

        prep.delegated = convert_hex_int(p["delegated"]) / 1e18

        if prep.delegated != 0:
            if settings.NETWORK_NAME in ["lisbon", "berlin"]:
                prep.bond_percent = (
                    prep.bonded / bond_requirement_rate / prep.delegated / 1e18
                )
            else:
                prep.bond_percent = 20 * prep.bonded / prep.delegated / 1e18
        else:
            prep.bond_percent = 0

        prep.irep = convert_hex_int(p["irep"]) / 1e18

        prep.grade = p["grade"]
        prep.penalty = p["penalty"]

        # iiss 4
        if "jailFlags" in p:
            prep.jail_flags = p["jailFlags"]
        if "unjailRequestHeight" in p:
            prep.unjail_request_height = int(p["unjailRequestHeight"], 0)
        if "maxCommissionChangeRate" in p:
            prep.max_commission_change_rate = int(p["maxCommissionChangeRate"], 0) / 100
        if "maxCommissionRate" in p:
            prep.max_commission_rate = int(p["maxCommissionRate"], 0) / 100
        if "commissionRate" in p:
            prep.commission_rate = int(p["commissionRate"], 0) / 100
        if "minDoubleSignHeight" in p:
            prep.min_double_sign_height = int(p["minDoubleSignHeight"], 0)
        if "hasPublicKey" in p:
            prep.has_public_key = bool(int(p["hasPublicKey"], 0))

        session.merge(prep)
        try:
            session.commit()
            session.refresh(prep)
        except:
            session.rollback()
            raise
        finally:
            session.close()
    prom_metrics.preps_attributes_cron_ran.inc()
    logger.info(f"Ending {__name__} cron")


if __name__ == "__main__":
    from icon_governance.db import session_factory

    with session_factory() as session:
        run_prep_attributes(session=session)
