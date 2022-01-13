"""
Rewards are Txs with the claim-iscore method but since this service only listens for
new Txs, this job backfills the value and iscore from the logs service.
"""
import json

from requests import RequestException, get
from sqlmodel import func, select

from icon_governance.config import settings
from icon_governance.log import logger
from icon_governance.models.rewards import Reward
from icon_governance.utils.rpc import convert_hex_int


def get_iscore_value(tx_hash):
    """Get rewards value and Tx from logs service."""
    try:
        response = get(f"{settings.LOGS_SERVICE_URL}/api/v1/logs?transaction_hash={tx_hash}")
    except RequestException as e:
        logger.info(f"Exception in iscore - \n{e} - \n{tx_hash}")
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


def get_rewards(session):
    """Simple cron to get all the values and iscores for rewards txs."""
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
            iscore, value = get_iscore_value(tx_hash=r.tx_hash)

            if iscore is None:
                continue

            r.value = value
            r.iscore = iscore

            session.add(r)
            try:
                session.commit()
            except:
                session.rollback()
                raise
