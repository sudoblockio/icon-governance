from typing import Optional

from pydantic import BaseModel

from icon_governance.utils.rpc import get_network_info, get_preps, getIISSInfo


class Apys(BaseModel):
    i_global: float
    i_prep: float
    i_cps: float
    i_relay: float

    # Pre / post iiss 4.0
    i_voter: Optional[float]
    i_wage: Optional[float]

    staking_apy: float
    prep_apy: float
    total_stake: float
    total_delegated: float
    total_bonded: float
    total_power: float

    total_wage: float
    active_preps: int


def get_apys(height: int = None) -> Apys:
    iiss_info = getIISSInfo(height=height)
    network_info = get_network_info(height=height)
    get_preps_info = get_preps(height=height)

    total_stake = int(get_preps_info["totalStake"], 0) / 10**18
    total_delegated = int(get_preps_info["totalDelegated"], 0) / 10**18
    total_bonded = int(network_info["totalBonded"], 0) / 10**18
    total_power = int(network_info["totalPower"], 0) / 10**18

    i_global = int(iiss_info["variable"]["Iglobal"], 0) / 10**18
    i_prep = int(iiss_info["variable"]["Iprep"], 0) / 100
    i_cps = int(iiss_info["variable"]["Icps"], 0) / 100
    i_relay = int(iiss_info["variable"]["Irelay"], 0) / 100

    active_preps = len([i for i in get_preps_info['preps'] if i['grade'] in ['0x0', '0x1']])
    # Proxy for transition to iiss 4.0 where rates are not multiplied by 100
    if int(network_info["iissVersion"], 0) <= 3 or "Iwage" not in iiss_info["variable"]:
        # iiss 3.0
        i_wage = None
        i_voter = int(iiss_info["variable"]["Ivoter"], 0) / 100
        total_wage = 0
        prep_apy = i_prep * i_global * 12 / total_stake
    else:
        # iiss 4.0
        i_wage = int(iiss_info["variable"]["Iwage"], 0) / 100 / 100
        # https://forum.icon.community/t/changes-to-icon-economic-policy-iiss-4/3612
        # Take the sum of the product of each active validators power times the inverse
        # of their commission (ie what each validator is paying out) and then divide
        # that by total power. This is meant to approximate the i_voter which is in
        # IISSv4 null - so now we are just trying get the weighted average of the
        # commissions.
        voter_percent = sum([
            (1 - int(i['commissionRate'], 0) / 100 / 100) * int(i['power'], 0)
            for i in get_preps_info['preps']
            if i['grade'] in ['0x0', '0x1'] and 'commissionRate' in i
        ]) / 1e18 / total_power
        i_voter = i_prep * voter_percent
        total_wage = i_wage * i_global

        prep_apy = (1 - voter_percent) * i_prep * i_global * 12 / total_stake

    staking_apy = i_voter * i_global * 12 / (total_delegated + total_bonded)

    apys = Apys(
        i_global=i_global,
        i_voter=i_voter,
        i_prep=i_prep,
        i_cps=i_cps,
        i_relay=i_relay,
        i_wage=i_wage,
        staking_apy=staking_apy,
        prep_apy=prep_apy,
        total_delegated=total_delegated,
        total_stake=total_stake,
        total_bonded=total_bonded,
        total_power=total_power,
        total_wage=total_wage,
        active_preps=active_preps,
    )

    return apys
