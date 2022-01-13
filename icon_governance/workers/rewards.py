from icon_governance.log import logger
from icon_governance.models.rewards import Reward


def set_rewards(session, value):
    """Insert new rewards Txs into DB.  Cron then inserts values and iscores."""
    reward = session.get(Reward, value.hash)
    if reward is None:
        logger.info(f"Creating reward transaction {value.hash}")
        reward = Reward(
            address=value.from_address,
            tx_hash=value.hash,
            block=value.block_number,
            timestamp=int(value.timestamp, 16) / 1e6,
        )

        session.add(reward)
        try:
            session.commit()
        except:
            session.rollback()
            raise
