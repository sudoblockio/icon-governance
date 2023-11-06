from json import JSONDecodeError

import requests

from icon_governance.config import settings
from icon_governance.log import logger


def get_block_from_timestamp(timestamp: int):
    r = requests.get(settings.COMMUNITY_API_ENDPOINT + f"/api/v1/blocks/timestamp/{str(timestamp)}")
    if r.status_code == 200:
        try:
            response = r.json()
        except JSONDecodeError:
            logger.info(
                f"Invalid response from get_block_from_timestamp, with " f"timestamp = {timestamp}."
            )
            return None
        return response["number"] + 1
    else:
        logger.info(
            f"Invalid status code={r.status_code} from "
            f"get_block_from_timestamp, with timestamp = {timestamp}."
        )
        raise requests.exceptions.RequestException


def get_timestamp_from_block(block: int):
    r = requests.get(settings.COMMUNITY_API_ENDPOINT + f"/api/v1/blocks/{str(block)}")
    if r.status_code == 200:
        try:
            response = r.json()
        except JSONDecodeError:
            logger.info("Invalid response from get_timestamp_from_block, check url.")
            return None
        return response["timestamp"]
    else:
        logger.info("Invalid status code from get_timestamp_from_block, check url.")
