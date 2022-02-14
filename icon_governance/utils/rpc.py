import json

import requests

from icon_governance.config import settings
from icon_governance.log import logger


def convert_hex_int(hex_string: str) -> int:
    return int(hex_string, 16)


def post_rpc_json(response):
    if response.status_code != 200:
        return None
    return response.json()["result"]


def post_rpc(payload: dict):
    r = requests.post(settings.ICON_NODE_URL, data=json.dumps(payload))

    if r.status_code != 200:
        logger.info(f"Error {r.status_code} with payload {payload}")
        r = requests.post(settings.BACKUP_ICON_NODE_URL, data=json.dumps(payload))
        if r.status_code != 200:
            logger.info(f"Error {r.status_code} with payload {payload} to backup")
        return r

    return r


def icx_getTransactionResult(txHash: str):
    payload = {
        "jsonrpc": "2.0",
        "method": "icx_getTransactionResult",
        "id": 1234,
        "params": {"txHash": txHash},
    }
    return post_rpc(payload)


def getPReps():
    payload = {
        "jsonrpc": "2.0",
        "id": 1234,
        "method": "icx_call",
        "params": {
            "to": "cx0000000000000000000000000000000000000000",
            "dataType": "call",
            "data": {
                "method": "getPReps",
                "params": {"startRanking": "0x1", "endRanking": "0xaaa"},
            },
        },
    }
    return post_rpc(payload)


def getDelegation(address: str):
    payload = {
        "jsonrpc": "2.0",
        "id": 1234,
        "method": "icx_call",
        "params": {
            "to": "cx0000000000000000000000000000000000000000",
            "dataType": "call",
            "data": {"method": "getDelegation", "params": {"address": address}},
        },
    }
    return post_rpc(payload)


# def get_delegation(address: str):
#     delegation = post_rpc_json(getDelegation(address))
#     if delegation
#     return delegation


def getStake(address: str):
    payload = {
        "jsonrpc": "2.0",
        "id": 1234,
        "method": "icx_call",
        "params": {
            "to": "cx0000000000000000000000000000000000000000",
            "dataType": "call",
            "data": {"method": "getStake", "params": {"address": address}},
        },
    }
    return post_rpc(payload)


def getProposals():
    payload = {
        "jsonrpc": "2.0",
        "id": 100,
        "method": "icx_call",
        "params": {
            "to": "cx0000000000000000000000000000000000000001",
            "dataType": "call",
            "data": {
                "method": "getProposals",
            },
        },
    }
    return post_rpc(payload)


def get_sponsors_record():
    payload = {
        "jsonrpc": "2.0",
        "method": "icx_call",
        "params": {
            "to": "cx9f4ab72f854d3ccdc59aa6f2c3e2215dd62e879f",
            "dataType": "call",
            "data": {"method": "get_sponsors_record"},
        },
        "id": 3205148222,
    }
    return post_rpc(payload)


def get_preps_cps():
    payload = {
        "jsonrpc": "2.0",
        "method": "icx_call",
        "params": {
            "to": "cx9f4ab72f854d3ccdc59aa6f2c3e2215dd62e879f",
            "dataType": "call",
            "data": {"method": "get_PReps"},
        },
        "id": 3746196027,
    }
    return post_rpc(payload)


def get_bond(address: str):
    payload = {
        "jsonrpc": "2.0",
        "id": 1234,
        "method": "icx_call",
        "params": {
            "to": "cx0000000000000000000000000000000000000000",
            "dataType": "call",
            "data": {"method": "getBond", "params": {"address": address}},
        },
    }
    return post_rpc(payload)


def get_admin_chain(ip_address: str):
    """Get the response from the admin API."""
    url = f"http://{ip_address}:9000/admin/chain/0x1"

    try:
        response = requests.get(url, timeout=2)
    except requests.exceptions.RequestException:
        return None

    if response.status_code == 200:
        return response.json()
    else:
        return None
