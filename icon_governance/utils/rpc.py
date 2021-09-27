import json
import requests


def post_rpc(payload: dict):
    uri = "https://icon.geometry-dev.net/api/v3"
    r = requests.post(uri, data=json.dumps(payload)).json()
    return r


def icx_getTransactionResult(txHash: str):
    payload = {
        "jsonrpc": "2.0",
        "method": "icx_getTransactionResult",
        "id": 1234,
        "params": {
            "txHash": txHash
        }
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
                "params": {
                    "startRanking": "0x1",
                    "endRanking": "0xaaa"  # Should be all preps
                }
            }
        }
    }
    return post_rpc(payload)


if __name__ == '__main__':
    x = icx_getTransactionResult('0x3bea9c00f108496a264d6562dfe6f11901cfb76aecb21a1f128eeae514603bd9')
    print()
    # x = getPReps()
    # print()
