from sqlmodel import select

from icon_governance.models.preps import Prep
from icon_governance.utils.rpc import convert_hex_int, getStake, post_rpc_json


def get_prep_stake(session):
    result = session.execute(select(Prep))
    preps = result.scalars().all()

    for prep in preps:
        prep.stake = convert_hex_int(post_rpc_json(getStake(prep.address))["stake"]) / 1e18

        session.merge(prep)
        session.commit()


if __name__ == "__main__":
    from icon_governance.db import session_factory

    get_prep_stake(session_factory())
