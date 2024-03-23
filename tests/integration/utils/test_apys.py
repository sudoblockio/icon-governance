import pytest

from icon_governance.utils.apys import get_apys


def test_get_staking_apy():
    apys = get_apys()

    assert apys.staking_apy > 0


@pytest.mark.parametrize(
    "url,height,expected_value",
    [
        ("https://api.icon.community/api/v3", 44000000, 7),
        ("https://api.lisbon.icon.community/api/v3", 2000000, 27),
        ("https://api.berlin.icon.community/api/v3", 2000000, 55),
        # iiss 4.0
        ("https://api.icon.community/api/v3", 75000000, 6),
        ("https://api.lisbon.icon.community/api/v3", 33000000, 24),
        ("https://api.berlin.icon.community/api/v3", 19000000, 2389),
        # Broken
        # ("https://api.berlin.icon.community/api/v3", None, 0),
        # ("https://api.lisbon.icon.community/api/v3", None, 0),
    ],
)
def test_get_staking_apy_height(url, height, expected_value, tmp_set_settings):
    # height when height base RPC was enabled - this is pre ICON 2.0 so governance stats
    # not available
    with tmp_set_settings("ICON_NODE_URL", url):
        apys = get_apys(height=height)

    assert int(apys.staking_apy * 100) == expected_value
