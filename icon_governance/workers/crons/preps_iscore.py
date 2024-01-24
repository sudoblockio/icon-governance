"""
Rewards are Txs with the claim-iscore method but since this service only listens for
new Txs, this job backfills the value and iscore from the logs service.
"""
import json
from time import sleep

from requests import RequestException, get
from sqlalchemy.exc import DataError
from sqlmodel import func, select

from icon_governance.config import settings
from icon_governance.log import logger
from icon_governance.metrics import prom_metrics
from icon_governance.models.rewards import Reward
from icon_governance.utils.rpc import convert_hex_int


def get_iscore_value(tx_hash):
    """Get rewards value and Tx from logs service."""
    try:
        response = get(f"{settings.LOGS_SERVICE_URL}/api/v1/logs?transaction_hash={tx_hash}")
    except RequestException as e:
        logger.info(f"Exception in iscore - \n{e} - \n{tx_hash}")
        # TODO: Add backoff - This should not happen generally
        sleep(0.5)
        return None, None

    if response.status_code == 200:
        try:
            data = json.loads(response.json()[0]["data"])
            return convert_hex_int(data[0]) / 1e18, convert_hex_int(data[1]) / 1e18
        except Exception as e:
            logger.info(f"Exception in iscore - \n{e} - \n{tx_hash}")
            return None, None
    else:
        logger.info(f"Could not find Tx hash from logs service {tx_hash}")
        return None, None


def run_prep_iscore(session):
    """
    Cron to get all the values and iscores for rewards txs. Works by getting all the
     iscore distributions which are picked up by the transactions processor and insert
     them into a DB. The values are then inserted with this cron job by querying for
     rewards that have no value.
    """
    logger.info(f"Starting {__name__} cron")

    count = (
        session.execute(select([func.count(Reward.address)]).where(Reward.value == None))
        .scalars()
        .all()
    )

    logger.info(f"Found {count} number of rewards records.")

    chunk_size = 10
    for i in range(0, int(count[0] / chunk_size) + 1):
        rewards = (
            session.execute(select(Reward).where(Reward.value == None).limit(chunk_size))
            .scalars()
            .all()
        )
        for r in rewards:
            # Get value from logs service
            if r.tx_hash is None:
                continue

            iscore, value = get_iscore_value(tx_hash=r.tx_hash)

            if iscore is None:
                continue

            r.value = value
            r.iscore = iscore

            session.add(r)
            try:
                session.commit()
            except DataError as e:
                if settings.NETWORK_NAME == "mainnet":
                    # Lisbon has been giving issues here
                    # 0x1f48830983c0a4b4a576ec082b23b52833d8bb9ab73a1e88c4938f96a68c633a
                    raise e
                session.rollback()

    prom_metrics.preps_iscore_cron_ran.inc()
    logger.info(f"Ending {__name__} cron")


if __name__ == "__main__":
    from icon_governance.db import session_factory

    with session_factory() as session:
        run_prep_iscore(session=session)
