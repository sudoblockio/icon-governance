from icon_governance.utils.details import get_details


def test_utils_details():
    details = get_details(
        "https://icon-staking-details.s3.us-west-2.amazonaws.com/hugobyte/details.json"
    )

    assert "logo_256" in details
    assert "location" not in details
