from sqlmodel import select

from icon_governance.log import logger
from icon_governance.models.delegations import Delegation
from icon_governance.utils.rpc import convert_hex_int


def set_delegation(session, data, address):
    params = data["params"]

    if "delegations" not in params:
        logger.info(f"Skipping because no delegation field.")
        return

    for d in params["delegations"]:
        prep_address = d["address"]
        value = convert_hex_int(d["value"])

        # Get the delegation from address and to prep_address
        statement = (
            select(Delegation)
            .where(Delegation.address == address)
            .where(Delegation.prep_address == prep_address)
        )

        result = session.execute(statement)
        delegation = result.scalars().all()

        if len(delegation) == 0:
            delegation = Delegation(
                address=address,
                prep_address=d["address"],
                value=convert_hex_int(d["value"]),
            )
        else:
            # There can be only one
            delegation = delegation[0]

        # if value == 0:
        #     # Delete the record
        #     session.delete(delegation)
        # else:
        # Update the record
        delegation.value = value
        session.add(delegation)
        try:
            session.commit()
        except:
            session.rollback()
            raise
