from icon_governance.utils.details import get_details


def test_utils_details():
    details = get_details('https://hugobyte-mainnet-aws-us-west-2.s3-us-west-2.amazonaws.com/details.json')

    assert 'logo_256' in details
    assert 'location' not in details
