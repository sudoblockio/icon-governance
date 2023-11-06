from icon_governance.utils.rpc import (
    convert_hex_int,
    get_bond,
    get_missed_blocks,
    get_preps_cps,
    get_preps_stats,
    get_sponsors_record,
    getDelegation,
    getIISSInfo,
    getPRepNodePublicKey,
    getPReps,
    getProposals,
    getStake,
    post_rpc_json,
)

SKIMPY_ADDRESS = "hxf5a52d659df00ef0517921647516daaf7502a728"
ADDRESS = "hx0cc3a3d55ed55df7c8eee926a4fafb5412d0cca4"


def test_get_preps():
    result = getPReps().json()["result"]
    assert len(result["preps"]) > 50


def test_post_rpc_json():
    delegation = post_rpc_json(getDelegation(ADDRESS))  # Parrot9
    stake = post_rpc_json(getStake(ADDRESS))["stake"]  # Foundation
    stake = int(stake, 16) / 1e18
    assert delegation
    assert stake >= 0


def test_convert_hex_int():
    delegated = convert_hex_int("0x21e19e0c9bab2400000")
    assert delegated == 10000000000000000000000


def test_get_delegation():
    delegation = post_rpc_json(getDelegation(ADDRESS))

    total_delegation = 0
    for d in delegation["delegations"]:
        total_delegation += convert_hex_int(d["value"])

    totalDelegated = convert_hex_int(delegation["totalDelegated"])
    assert totalDelegated == total_delegation


def test_get_sponsors_record():
    sponsors = post_rpc_json(get_sponsors_record())
    assert len(sponsors) > 10


def test_get_preps_cps():
    cps_preps = post_rpc_json(get_preps_cps())
    assert len(cps_preps) > 10

    prep_list = [i["address"] for i in cps_preps]
    assert len(prep_list) > 15


def test_getProposals():
    proposals = post_rpc_json(getProposals())
    assert proposals


def test_get_bond():
    # bond = post_rpc_json(get_bond('hx0b047c751658f7ce1b2595da34d57a0e7dad357d'))
    bond = post_rpc_json(get_bond("hx1e15b53379e5ee634a2da493a43fdc2d03d0c718"))
    assert bond


def test_get_missed_blocks():
    output = get_missed_blocks().json()["result"]
    assert output


def test_get_preps_stats():
    output = get_preps_stats().json()["result"]
    assert output


def test_getPRepNodePublicKey():
    output = getPRepNodePublicKey(address="hxfc56203484921c3b7a4dee9579d8614d8c8daaf5")
    assert output


def test_getIISSInfo():
    output = getIISSInfo()
    assert output
