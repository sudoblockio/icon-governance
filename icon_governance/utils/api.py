from typing import Optional

import requests

from icon_governance.config import settings
from icon_governance.log import logger


def get_max_addresses(is_contract: bool = None) -> Optional[int]:

    endpoint = settings.COMMUNITY_API_ENDPOINT + f"/api/v1/addresses"
    if is_contract:
        endpoint += "/contracts"

    r = requests.head(endpoint)
    if r.status_code == 200:
        total_records = int(dict(r.headers)["x-total-count"])
        return total_records
    else:
        logger.info(f"Could not head addresses")
        return None


def get_addresses(
    max_addresses: int,
    data: list = None,
    skip: int = None,
    limit: int = 100,
    is_contract: bool = None,
) -> list[dict]:
    if data is None:
        data = []
    if skip is None:
        skip = 0
    if skip >= max_addresses:
        return data

    endpoint = settings.COMMUNITY_API_ENDPOINT + f"/api/v1/addresses?skip={skip}&limit={limit}"
    if is_contract is not None:
        endpoint += "&is_contract=true"

    r = requests.get(endpoint)
    if r.status_code == 200:
        data += r.json()
        return get_addresses(max_addresses, data, skip + limit)

    return data
