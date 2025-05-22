from datetime import datetime

from sqlalchemy.orm import Session

from icon_governance.config import settings
from icon_governance.log import logger
from icon_governance.metrics import prom_metrics
from icon_governance.models.apy_time import ApyTime
from icon_governance.utils.apys import get_apys
from icon_governance.utils.time_to_block import (
    get_block_from_timestamp,
    get_timestamp_from_block,
)


def run_apy_time(session: Session):
    logger.info(f"Starting {__name__} cron")

    if settings.NETWORK_NAME in ["lisbon", "berlin"]:
        logger.info("Skipping apytime for testnets")
        return

    last_apy_time = session.query(ApyTime).order_by(ApyTime.timestamp.desc()).first()
    if last_apy_time is None:
        logger.info("Starting new apy time....")
        # This is roughly when the governance stats were started (ie ICON 2.0)
        # if settings.NETWORK_NAME in ["lisbon", "berlin"]:
        #     start_height = 2000000
        # else:
        start_height = settings.apy_start_block
        staking_time = int(get_timestamp_from_block(start_height) / 1e6)
    else:
        staking_time = last_apy_time.timestamp + 86400

    if staking_time >= int(datetime.utcnow().timestamp()):
        logger.info("Last staking apy time is less than 1 day old. Skipping.")
        return

    # Iterate until the staking time is within 1 day of now
    while staking_time < datetime.utcnow().timestamp():
        height = get_block_from_timestamp(int(staking_time * 1e6))

        apys = get_apys(height=height)

        staking_apy_time = ApyTime(
            timestamp=staking_time,
            height=height,
            **apys.model_dump(),
        )
        session.merge(staking_apy_time)
        session.commit()

        staking_time = staking_time + 86400

    prom_metrics.cron_ran.inc()
    logger.info(f"Ending {__name__} cron")


if __name__ == "__main__":
    from icon_governance.db import session_factory

    with session_factory() as session:
        run_apy_time(session=session)
