from icon_governance.utils.apys import get_apys


def test_get_staking_apy():
    apys = get_apys()

    assert apys.staking_apy > 0


def test_get_staking_apy_height():
    # height when height base RPC was enabled - this is pre ICON 2.0 so governance stats
    # not available
    # apys = get_apys(height=33518615)
    apys = get_apys(height=44000000)

    assert apys.staking_apy > 0
