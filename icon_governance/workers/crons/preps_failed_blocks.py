from sqlmodel import select

from icon_governance.models.preps import Prep
from icon_governance.utils.rpc import get_network_info, get_prep_stats

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
    # TODO: Qualify based on whether penalties are active? -> No because we're not doing
    #  business logic here.
    # network_info = get_network_info()
    prep_stats = get_prep_stats()["preps"]

    # Get all the missed blocks for all the nodes
    result = session.execute(select(Prep).order_by(Prep.power.desc()))
    preps = result.scalars().all()

    for i, p in enumerate(preps):
        stats = prep_stats[i]
        # Convert to int
        stats = {k: int(v, 0) for k, v in stats.items()}

        p.failure_count = stats["realFailCont"]
        p.penalties = stats["penalties"]

        session.merge(p)
    session.commit()


if __name__ == "__main__":
    from icon_governance.db import session_factory

    with session_factory() as session:
        run_failed_blocks(session=session)
