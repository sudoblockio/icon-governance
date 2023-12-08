import pytest

from icon_governance.config import settings
from icon_governance.utils.apys import get_apys


def test_get_staking_apy():
    apys = get_apys()

    assert apys.staking_apy > 0


@pytest.mark.parametrize(
    "url,height",
    [
        ("https://api.icon.community/api/v3", 44000000),
        ("https://api.lisbon.icon.community/api/v3", 2000000),
        ("https://api.berlin.icon.community/api/v3", 2000000),
    ],
)
def test_get_staking_apy_height(url, height):
    # height when height base RPC was enabled - this is pre ICON 2.0 so governance stats
    # not available
    # apys = get_apys(height=33518615)
    settings.ICON_NODE_URL = url
    apys = get_apys(height=height)

    assert apys.staking_apy > 0
