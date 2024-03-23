from typing import Callable, TypedDict

from apscheduler.schedulers.background import BlockingScheduler
from loguru import logger
from prometheus_client import start_http_server

from icon_governance.config import settings
from icon_governance.db import session_factory
from icon_governance.workers.crons import (  # preps_missed_blocks,
    address_stake,
    apy_time,
    clean_delegation,
    cps,
    commission_time,
    prep_attributes,
    preps_base,
    preps_failed_blocks,
    preps_ip,
    preps_iscore,
    preps_public_key,
    preps_rewards,
    preps_single,
    preps_stake,
    preps_state,
    proposals,
    stats,
)


class Cron(TypedDict):
    func: Callable
    interval: int


CRONS: list[Cron] = [
    {
        "func": preps_base.run_preps_base,
        "interval": 600,
    },
    {
        "func": prep_attributes.run_prep_attributes,
        "interval": 120,
    },
    {
        "func": cps.run_cps,
        "interval": 3600,
    },
    {
        "func": clean_delegation.clean_delegations,
        "interval": 86400,
    },
    {
        "func": preps_ip.run_prep_ip,
        "interval": 900,
    },
    {
        "func": preps_state.run_prep_state,
        "interval": 30,
    },
    {
        "func": preps_single.run_get_prep,
        "interval": 86400,
    },
    {
        "func": proposals.run_proposals,
        "interval": 600,
    },
    {
        "func": preps_iscore.run_prep_iscore,
        "interval": 600,
    },
    {
        "func": preps_rewards.run_get_prep_rewards,
        "interval": 600,
    },
    {
        "func": preps_stake.run_prep_stake,
        "interval": 600,
    },
    {
        "func": preps_failed_blocks.run_failed_blocks,
        "interval": 30,
    },
    {
        "func": address_stake.run_address_stake,
        "interval": 3600,
    },
    {
        "func": preps_public_key.run_prep_public_key,
        "interval": 3600,
    },
    {
        "func": apy_time.run_apy_time,
        "interval": 3600 * 12,  # 12 hours
    },
    {
        "func": stats.run_stats,
        "interval": 3600,  # 1 hour
    },
    {
        "func": commission_time.run_commission_time,
        "interval": 86400 / 4,
    },
]


def run_cron_with_session(cron: Callable):
    with session_factory() as session:
        cron(session=session)


def main():
    logger.info("Starting metrics server.")
    start_http_server(settings.METRICS_PORT, settings.METRICS_ADDRESS)

    sched = BlockingScheduler()

    for i in CRONS:
        # Run the jobs immediately in order
        run_cron_with_session(i["func"])

        # Then run them in the scheduler
        sched.add_job(
            func=run_cron_with_session,
            trigger="interval",
            args=[i["func"]],
            seconds=i["interval"],
            id=i["func"].__name__,
        )

    sched.start()


if __name__ == "__main__":
    main()
