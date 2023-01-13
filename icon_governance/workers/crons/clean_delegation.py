from sqlmodel import delete

from icon_governance.log import logger
from icon_governance.models.delegations import Delegation

delegation_delete_count = 0


def clean_delegations(session):
    logger.info("Deleting zero delegations.")
    statement = delete(Delegation).where(Delegation.value == 0)
    session.execute(statement)
    session.commit()


if __name__ == "__main__":
    from icon_governance.db import session_factory

    clean_delegations(session_factory())
