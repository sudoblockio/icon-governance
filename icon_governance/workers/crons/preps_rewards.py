from sqlmodel import select

from icon_governance.log import logger
from icon_governance.metrics import prom_metrics
from icon_governance.models.preps import Prep
from icon_governance.utils.rpc import get_band_price, get_network_info


def run_get_prep_rewards(session):
    """Cron to get the rewards from the preps."""
    logger.info(f"Starting {__name__} cron")

    result = session.execute(select(Prep))
    preps = result.scalars().all()

    icx_usd_price = get_band_price()
    network_info = get_network_info()

    total_power = int(network_info["totalPower"], 16)  # / 10 ** 18
    i_global = int(network_info["rewardFund"]["Iglobal"], 16) / 10**18
    if "Iwage" in network_info["rewardFund"]:
        i_prep = int(network_info["rewardFund"]["Iprep"], 16) / 100 / 100
        i_wage = int(network_info["rewardFund"]["Iwage"], 16) / 100 / 100
    else:
        # TODO: Remove this post rev 25
        i_wage = None
        i_prep = int(network_info["rewardFund"]["Iprep"], 16) / 100

    for prep in preps:
        if prep.power is None:
            # Nodes with grade = 0x3 have null power
            prep.power = 0
        if prep.commission_rate is None:
            commission_rate = 0
        else:
            commission_rate = prep.commission_rate

        if prep.jail_flags is not None and prep.jail_flags != "0x0":
            # Nodes in jail get not rewards
            prep.reward_monthly = 0
            prep.reward_monthly_usd = 0
            prep.reward_daily = 0
            prep.reward_daily_usd = 0
        else:
            if i_wage is None:
                # TODO: Remove this post rev 25
                prep.reward_monthly = (prep.power / total_power) * (i_global * i_prep)
            else:
                prep.reward_monthly = (prep.power / total_power) * (
                    i_global * i_prep * commission_rate / 100
                ) + (prep.power / total_power) * (i_global * i_wage)
            prep.reward_monthly_usd = prep.reward_monthly * icx_usd_price
            # prep.reward_daily = (prep.reward_monthly * 12) / 365
            prep.reward_daily = prep.reward_monthly / 30  # Month = 30 days
            prep.reward_daily_usd = prep.reward_daily * icx_usd_price

        session.merge(prep)
    session.commit()

    prom_metrics.preps_rewards_cron_ran.inc()
    logger.info(f"Ending {__name__} cron")


if __name__ == "__main__":
    from icon_governance.db import session_factory

    with session_factory() as session:
        run_get_prep_rewards(session=session)
