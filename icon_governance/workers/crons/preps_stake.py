from loguru import logger
from sqlmodel import select

from icon_governance.metrics import prom_metrics
from icon_governance.models.preps import Prep
from icon_governance.utils.rpc import (
    convert_hex_int,
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
            prep.bonders = len(bonders["bonderList"])

        sql = (
            f"select count(distinct address) from delegations where prep_address = '{prep.address}'"
        )
        delegators_count = session.execute(sql).scalar()
        prep.stakers = delegators_count

        session.merge(prep)
        session.commit()

    prom_metrics.preps_attributes_cron_ran.inc()
    logger.info(f"Ending {__name__} cron")


if __name__ == "__main__":
    from icon_governance.db import session_factory

    with session_factory() as session:
        run_prep_stake(session=session)
