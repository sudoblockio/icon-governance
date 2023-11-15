import datetime

from sqlalchemy.orm import Session

from icon_governance.log import logger
from icon_governance.metrics import prom_metrics
from icon_governance.models.stats import Stats


def run_stats(session: Session):
    """This cron scrapes the cmc endpoint for."""
    logger.info(f"Starting {__name__} cron")

    sql = "select count(distinct address) from delegations"
    stakers_count = session.execute(sql).scalar()

    sql = "select count(bonders) from preps"
    bonders_count = session.execute(sql).scalar()

    stats = Stats(
        timestamp=int(datetime.datetime.utcnow().timestamp()),
        stakers=stakers_count,
        bonders=bonders_count,
    )

    session.merge(stats)
    session.commit()

    prom_metrics.cron_ran.inc()
    logger.info(f"Ending {__name__} cron")


if __name__ == "__main__":
    from icon_governance.db import session_factory

    with session_factory() as session:
        run_stats(session=session)
