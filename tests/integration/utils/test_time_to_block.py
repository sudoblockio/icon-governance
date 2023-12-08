import pytest

from icon_governance.config import settings
from icon_governance.utils.time_to_block import get_timestamp_from_block


@pytest.mark.parametrize(
    "url",
    [
        "https://tracker.lisbon.icon.community",
        "https://tracker.berlin.icon.community",
    ],
)
def test_get_timestamp_from_block(url):
    settings.COMMUNITY_API_ENDPOINT = url
    timestamp = get_timestamp_from_block(2)

    assert timestamp > 1000000
