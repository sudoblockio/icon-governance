from sqlmodel import select

from icon_governance.log import logger
from icon_governance.metrics import prom_metrics
from icon_governance.models.preps import Prep
from icon_governance.utils.rpc import getPRep


def run_get_prep(session):
    """
    This cron runs through all the records in the db and calls a getPRep on the address
     which will include information like `grade` which when the prep is unregistered
     will go from 0x0 to 0x3 and no longer be included in the list of preps
    """
    logger.info("Starting get prep cron...")

    result = session.execute(select(Prep))
    preps = result.scalars().all()

    for p in preps:
        r = getPRep(address=p.address)
        if r.status_code != 200:
            continue
        prep = r.json()["result"]

        if p.grade != prep["grade"]:
            p.grade = prep["grade"]
            session.merge(p)
    session.commit()

    prom_metrics.preps_base_cron_ran.inc()
    logger.info("Ending get prep cron")


if __name__ == "__main__":
    from icon_governance.db import session_factory

    with session_factory() as session:
        run_get_prep(session=session)
