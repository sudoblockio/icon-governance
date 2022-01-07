from icon_governance.db import session_factory
from icon_governance.workers.delegations import set_delegation


def test_set_delegations():
    data = {
        "method": "setDelegation",
        "params": {
            "delegations": [
                {
                    "address": "hx0b047c751658f7ce1b2595da34d57a0e7dad357d",
                    "value": "0x388e8c2ac431f14000",
                },
                {
                    "address": "hx1cb5883939f2fd478e92da1260438aa1f03440ca",
                    "value": "0x10c108cecb0e49c000",
                },
                {
                    "address": "hxd0d9b0fee857de26fd1e8b15209ca15b14b851b2",
                    "value": "0x706a0beeca18c0000",
                },
                {
                    "address": "hx168d2cfe6d73acb8cb690d3abda54d3af266addf",
                    "value": "0x33e232938e4e24000",
                },
                {
                    "address": "hx262afdeda4eba10fe41fa5ef21796ac2bdcc6629",
                    "value": "0x7cd0a3fa003c8c000",
                },
            ]
        },
    }

    with session_factory() as session:
        set_delegation(session, data, "hxf55eccb07a95a263a81d79561adb372bc39b3ca8")
