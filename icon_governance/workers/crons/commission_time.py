from datetime import datetime

from sqlalchemy.orm import Session

from icon_governance.config import settings
from icon_governance.log import logger
from icon_governance.metrics import prom_metrics
from icon_governance.models.commission_time import CommissionTime
from icon_governance.utils.commissions import get_commission_stats, CommissionStats
from icon_governance.utils.time_to_block import (
    get_block_from_timestamp,
    get_timestamp_from_block,
)


def _transpose_dict_keys(commission_dict: dict[str, CommissionStats]) -> dict:
    output = {}
    for sql_name, commission_stat in commission_dict.items():
        for stat_name, stat_value in commission_stat.dict().items():
            output[sql_name + '_' + stat_name] = stat_value
    return output

def run_commission_time(session: Session):
    if settings.NETWORK_NAME in ["lisbon", "berlin"]:
        logger.info(f"Skipping {__name__} cron for testnets")
        return
    logger.info(f"Starting {__name__} cron")

    last_commission_time = session.query(CommissionTime).order_by(
        CommissionTime.timestamp.desc()
    ).first()

    if last_commission_time is None:
        # This is roughly when the governance stats were started (ie ICON 2.0)
        if settings.NETWORK_NAME == "lisbon":
            start_height = 32_000_000
        elif settings.NETWORK_NAME == "berlin":
            start_height = 18_000_000
        else:
            start_height = 77_500_000
        staking_time = int(get_timestamp_from_block(start_height) / 1e6)
    else:
        staking_time = last_commission_time.timestamp + 86400

    if staking_time >= int(datetime.utcnow().timestamp()):
        logger.info("Last staking commission time is less than 1 day old. Skipping.")
        return

    # Iterate until the staking time is within 1 day of now
    while staking_time < datetime.utcnow().timestamp():
        height = get_block_from_timestamp(int(staking_time * 1e6))

        commissions = get_commission_stats(height=height)

        commission_stats = CommissionTime(
            timestamp=staking_time,
            height=height,
            **_transpose_dict_keys(commissions),
        )
        session.merge(commission_stats)
        session.commit()

        staking_time = staking_time + 86400

    prom_metrics.cron_ran.inc()
    logger.info(f"Ending {__name__} cron")


if __name__ == "__main__":
    from icon_governance.db import session_factory

    with session_factory() as session:
        run_commission_time(session=session)
