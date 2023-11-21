from loguru import logger
from sqlmodel import select

from icon_governance.models.preps import Prep
from icon_governance.utils.rpc import get_prep_stats, getPReps

# Example schema
# {
#     'fail': '0x272f6',
#     'failCont': '0x0',
#     'grade': '0x0',
#     'lastHeight': '0x3c45213',
#     'lastState': '0x2',
#     'penalties': '0x0',
#     'realFail': '0x272f6',
#     'realFailCont': '0x0',
#     'realTotal': '0x3227c4f',
#     'status': '0x0',
#     'total': '0x321f2e3'
# }


def run_failed_blocks(session):
    """
    Check missed blocks for failures and penalties.

    realFailCont reset when a node votes on a block only.
    1. At Term(n) : Node(A) missed last 2 blocks
    2. At Term(n+1): Node(A) was not elected as a Validator
    3. At Term(n+2): Node(A) missed first 3 blocks til Block(N).
    4. At Block(N): Node(A) got realFailCont: "0x5"
    5. At Block(N+1): If Node(A) votes, realFailCont will be reset
    """
    logger.info(f"Starting {__name__} cron")
    # TODO: Qualify based on whether penalties are active? -> No because we're not doing
    #  business logic here.
    # network_info = get_network_info()

    r = getPReps()
    if r.status_code == 200:
        preps_rpc = r.json()["result"]["preps"]
    else:
        logger.info("Error getting preps in failed blocks.")
        return
    prep_stats = get_prep_stats()["preps"]

    for i, p in enumerate(preps_rpc):
        try:
            stats = prep_stats[i]
        except IndexError:
            logger.info("Mismatch in count between stats and getPreps...")
            return
        # Convert to int
        stats = {k: int(v, 0) for k, v in stats.items() if k != "address"}

        result = session.execute(select(Prep).where(Prep.address == p["address"]))
        prep_db = result.scalars().first()

        prep_db.failure_count = stats["realFailCont"]
        prep_db.penalties = stats["penalties"]

        session.merge(prep_db)
        session.commit()
    logger.info(f"Ending {__name__} cron")


if __name__ == "__main__":
    from icon_governance.db import session_factory

    with session_factory() as session:
        run_failed_blocks(session=session)
