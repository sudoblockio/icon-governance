from sqlmodel import select

from icon_governance.db import session_factory
from icon_governance.models.delegations import Delegation
from icon_governance.workers.delegations import set_delegation

# def test_set_delegations():
#     data = {
#         "method": "setDelegation",
#         "params": {
#             "delegations": [
#                 {
#                     "address": "hx0b047c751658f7ce1b2595da34d57a0e7dad357d",
#                     "value": "0x388e8c2ac431f14000",
#                 },
#                 {
#                     "address": "hx1cb5883939f2fd478e92da1260438aa1f03440ca",
#                     "value": "0x10c108cecb0e49c000",
#                 },
#                 {
#                     "address": "hxd0d9b0fee857de26fd1e8b15209ca15b14b851b2",
#                     "value": "0x706a0beeca18c0000",
#                 },
#                 {
#                     "address": "hx168d2cfe6d73acb8cb690d3abda54d3af266addf",
#                     "value": "0x33e232938e4e24000",
#                 },
#                 {
#                     "address": "hx262afdeda4eba10fe41fa5ef21796ac2bdcc6629",
#                     "value": "0x7cd0a3fa003c8c000",
#                 },
#             ]
#         },
#     }
#
#     with session_factory() as session:
#         set_delegation(
#             session, data, "hxf55eccb07a95a263a81d79561adb372bc39b3ca8", 1000, "foo-hash"
#         )
#         # Should have no effect
#         set_delegation(
#             session, data, "hxf55eccb07a95a263a81d79561adb372bc39b3ca8", 1000, "foo-hash"
#         )
#         statement = select(Delegation).where(
#             Delegation.address == "hxf55eccb07a95a263a81d79561adb372bc39b3ca8"
#         )
#         result = session.execute(statement)
#         address_delegation = result.scalars().all()
#
#         assert len(address_delegation) == 5
#
#         set_delegation(
#             session, data, "hxf55eccb07a95a263a81d79561adb372bc39b3ca8", 1001, "foo-hash"
#         )
#
#         set_delegation(session, data, "hxf55eccb07a95a263a81d79561adb372bc39b3ca8", 999, "foo-hash")
#
#         assert len(address_delegation) == 5
#
#         result = session.execute(statement)
#         address_delegation = result.scalars().all()
#         blocks = [i.last_updated_block for i in address_delegation]
#         last_updated_block_set = set(blocks)
#
#         assert len(last_updated_block_set) == 1
#         assert blocks[0] == 1001
