from pydantic import BaseModel

from icon_governance.utils.rpc import get_preps, getIISSInfo


class Apys(BaseModel):
    i_global: float
    i_voter: float
    i_prep: float
    i_cps: float
    i_relay: float

    staking_apy: float
    prep_apy: float
    cps_apy: float
    relay_apy: float
    total_stake: float
    total_delegated: float


def get_apys(height: int = None) -> Apys:
    iiss_info = getIISSInfo(height=height)

    get_preps_info = get_preps(height)

    total_stake = int(get_preps_info["totalStake"], 0) / 10**18
    # TODO: Make sure it is all a function of stake - not delegation which is lower
    total_delegated = int(get_preps_info["totalDelegated"], 0) / 10**18

    i_global = int(iiss_info["variable"]["Iglobal"], 0) / 10**18
    i_voter = int(iiss_info["variable"]["Ivoter"], 0) / 100
    i_prep = int(iiss_info["variable"]["Iprep"], 0) / 100
    i_cps = int(iiss_info["variable"]["Icps"], 0) / 100
    i_relay = int(iiss_info["variable"]["Irelay"], 0) / 100

    apys = Apys(
        i_global=i_global,
        i_voter=i_voter,
        i_prep=i_prep,
        i_cps=i_cps,
        i_relay=i_relay,
        staking_apy=i_voter * i_global * 12 / total_stake,
        prep_apy=i_prep * i_global * 12 / total_stake,
        cps_apy=i_cps * i_global * 12 / total_stake,
        relay_apy=i_relay * i_global * 12 / total_stake,
        total_delegated=total_delegated,
        total_stake=total_stake,
    )

    return apys
