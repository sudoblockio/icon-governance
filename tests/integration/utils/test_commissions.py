import pytest

from icon_governance.utils.commissions import get_commission_stats


@pytest.mark.order(3)
@pytest.mark.parametrize(
    "url,height",
    [
        ("https://api.icon.community/api/v3", None),
        ("https://api.berlin.icon.community/api/v3", None),
        ("https://api.lisbon.icon.community/api/v3", None),
        ("https://api.icon.community/api/v3", 77_500_000),
        ("https://api.berlin.icon.community/api/v3", 18_000_000),
        ("https://api.lisbon.icon.community/api/v3", 32_000_000),
    ],
)
def test_get_commission_stats(url, height, tmp_set_settings):
    with tmp_set_settings("ICON_NODE_URL", url):
        stats = get_commission_stats(height=height)

    assert stats['commission_rate'].average
