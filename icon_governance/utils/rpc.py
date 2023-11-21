import json
from typing import Optional

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


def get_preps(height: int = None):
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
    if height is not None:
        payload["params"]["height"] = hex(height)

    return unpack_call(post_rpc(payload))


def getPRep(address: str):
    payload = {
        "jsonrpc": "2.0",
        "id": 1234,
        "method": "icx_call",
        "params": {
            "to": "cx0000000000000000000000000000000000000000",
            "dataType": "call",
            "data": {
                "method": "getPRep",
                "params": {"address": address},
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


def get_bonder_list(address: str):
    payload = {
        "jsonrpc": "2.0",
        "id": 1234,
        "method": "icx_call",
        "params": {
            "to": "cx0000000000000000000000000000000000000000",
            "dataType": "call",
            "data": {"method": "getBonderList", "params": {"address": address}},
        },
    }
    return post_rpc(payload)


def get_missed_blocks():
    payload = {
        "jsonrpc": "2.0",
        "id": 1234,
        "method": "icx_call",
        "params": {
            "to": "cx0000000000000000000000000000000000000000",
            "dataType": "call",
            "data": {"method": "getNetworkInfo"},
        },
    }
    return post_rpc(payload)


def get_preps_stats():
    payload = {
        "jsonrpc": "2.0",
        "id": 1234,
        "method": "icx_call",
        "params": {
            "to": "cx0000000000000000000000000000000000000000",
            "dataType": "call",
            "data": {"method": "getPRepStats"},
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


def unpack_call(r: requests.Response) -> Optional[dict]:
    if r.status_code == 200:
        return r.json()["result"]
    return None


def get_network_info(height: int = None):
    payload = {
        "jsonrpc": "2.0",
        "id": 1234,
        "method": "icx_call",
        "params": {
            "to": "cx0000000000000000000000000000000000000000",
            "dataType": "call",
            "data": {"method": "getNetworkInfo"},
        },
    }
    if height is not None:
        payload["params"]["height"] = hex(height)

    return unpack_call(post_rpc(payload))


def get_prep_stats():
    payload = {
        "jsonrpc": "2.0",
        "id": 1234,
        "method": "icx_call",
        "params": {
            "to": "cx0000000000000000000000000000000000000000",
            "dataType": "call",
            "data": {"method": "getPRepStats"},
        },
    }
    return unpack_call(post_rpc(payload))


def getPRepNodePublicKey(address: str):
    payload = {
        "jsonrpc": "2.0",
        "id": 1234,
        "method": "icx_call",
        "params": {
            "to": "cx0000000000000000000000000000000000000000",
            "dataType": "call",
            "data": {"method": "getPRepNodePublicKey", "params": {"address": address}},
        },
    }
    return unpack_call(post_rpc(payload))


def getIISSInfo(height: int = None):
    payload = {
        "jsonrpc": "2.0",
        "id": 1234,
        "method": "icx_call",
        "params": {
            "to": "cx0000000000000000000000000000000000000000",
            "dataType": "call",
            "data": {"method": "getIISSInfo"},
        },
    }
    if height is not None:
        payload["params"]["height"] = hex(height)

    return unpack_call(post_rpc(payload))


def get_band_price(symbol: str = "ICX", height: int = None) -> float:
    """Band contract was updated from python to java at the below block height."""
    if height is None or height > 59878978:
        address = "cxca5faa5a71d986a2e84dd7e6f5ff791d29901ebe"
        method = "getRefData"
        param_name = "symbol"
    else:
        address = "cx087b4164a87fdfb7b714f3bafe9dfb050fd6b132"
        method = "get_ref_data"
        param_name = "_symbol"
    payload = {
        "jsonrpc": "2.0",
        "id": 1234,
        "method": "icx_call",
        "params": {
            "to": address,
            "dataType": "call",
            "data": {"method": method, "params": {param_name: symbol}},
        },
    }
    if height is not None:
        payload["params"]["height"] = hex(height)

    r = post_rpc(payload)

    if r.status_code == 200:
        return int(r.json()["result"]["rate"], 16) / 1e9
    raise Exception(f"Band contract for symbol={symbol} unreachable for get ref...")
