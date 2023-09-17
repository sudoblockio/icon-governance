from loguru import logger
from sqlmodel import select

from icon_governance.metrics import prom_metrics
from icon_governance.models.preps import Prep
from icon_governance.utils.rpc import getPRepNodePublicKey


def run_prep_public_key(session):
    logger.info("Starting preps public key cron")

    result = session.execute(select(Prep))
    preps = result.scalars().all()

    for prep in preps:
        public_key = getPRepNodePublicKey(address=prep.address)

        if public_key is None:
            continue
        prep.public_key = public_key
        session.merge(prep)
        session.commit()

    prom_metrics.preps_public_key_cron_ran.inc()
    logger.info("Ending preps public key cron")


if __name__ == "__main__":
    from icon_governance.db import session_factory

    with session_factory() as session:
        run_prep_public_key(session=session)
