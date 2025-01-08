from loguru import logger
from sqlalchemy import text
from sqlmodel import select

from icon_governance.metrics import prom_metrics
from icon_governance.models.preps import Prep
from icon_governance.utils.rpc import (
    convert_hex_int,
    get_bond,
    get_bonder_list,
    getStake,
    post_rpc_json,
)


def run_prep_stake(session):
    logger.info(f"Starting {__name__} cron")

    result = session.execute(select(Prep))
    preps = result.scalars().all()

    for prep in preps:
        prep.stake = convert_hex_int(post_rpc_json(getStake(prep.address))["stake"]) / 1e18

        bonders = post_rpc_json(get_bonder_list(prep.address))
        if bonders is not None:
            prep.bonders = 0
            for b in bonders["bonderList"]:
                get_bond_result = post_rpc_json(get_bond(address=b))

                for bond in get_bond_result["bonds"]:
                    if bond["address"] != prep.address:
                        continue
                    bond_amount = int(bond["value"], 0) / 10e18
                    if bond_amount > 0:
                        prep.bonders += 1

        sql = (
            f"select count(distinct address) from delegations where prep_address = '{prep.address}'"
        )
        delegators_count = session.execute(text(sql)).scalar()
        prep.stakers = delegators_count

        session.merge(prep)
        session.commit()

    prom_metrics.preps_attributes_cron_ran.inc()
    logger.info(f"Ending {__name__} cron")


if __name__ == "__main__":
    from icon_governance.db import session_factory

    with session_factory() as session:
        run_prep_stake(session=session)
