from statistics import mean, median, stdev

from pydantic import BaseModel

from icon_governance.utils.rpc import get_preps


class CommissionStats(BaseModel):
    average: float = 0
    weighted_average: float = 0
    median: float = 0
    max: float = 0
    min: float = 0
    stdev: float = 0
    weighted_stdev: float = 0


def make_stats_from_rate_list(commissions: list, power: list) -> CommissionStats:
    average_commissions = mean(commissions)
    weighted_average_commissions = sum(
        rate * p for rate, p in zip(commissions, power)) / sum(power)
    median_commissions = median(commissions)
    max_commissions = max(commissions)
    min_commissions = min(commissions)
    stdev_commissions = stdev(commissions)
    weighted_stdev_commissions = stdev(
        (rate - weighted_average_commissions) ** 2 * p for rate, p in zip(commissions, power)
    ) / sum(power)

    return CommissionStats(
        average=average_commissions,
        weighted_average=weighted_average_commissions,
        median=median_commissions,
        max=max_commissions,
        min=min_commissions,
        stdev=stdev_commissions,
        weighted_stdev=weighted_stdev_commissions,
    )


def get_commission_stats(height: int) -> dict[str, CommissionStats]:
    preps = get_preps(height)['preps']

    output = {}
    for rate_name in [
        {
            'field_name': 'commissionRate',
            'sql_name': 'commission_rate'
        },
        {
            'field_name': 'maxCommissionChangeRate',
            'sql_name': 'max_commission_change_rate',
        },
        {
            'field_name': 'maxCommissionRate',
            'sql_name': 'max_commission_rate',
        },
    ]:
        power = []
        rates = []
        for p in preps:
            if p['grade'] in ['0x0', '0x1'] and 'commissionRate' in p:
                power.append(int(p['power'], 0) / 1e18)
                rates.append(int(p[rate_name['field_name']], 0) / 100)
        output[rate_name['sql_name']] = make_stats_from_rate_list(rates, power)

    return output  # noqa
