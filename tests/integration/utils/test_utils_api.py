from icon_governance.utils.api import get_addresses, get_max_addresses


def test_get_max_addresses():
    max_addresses = get_max_addresses()

    assert isinstance(max_addresses, int)
    assert max_addresses > 1000000


def test_get_addresses():
    addresses = get_addresses(1000500, skip=1000000)

    assert len(addresses) == 500
