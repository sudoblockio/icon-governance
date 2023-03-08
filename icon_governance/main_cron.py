from typing import Callable, TypedDict

from apscheduler.schedulers.background import BlockingScheduler
from loguru import logger
from prometheus_client import start_http_server

from icon_governance.config import settings
from icon_governance.db import session_factory
from icon_governance.workers.crons import (  # preps_missed_blocks,
    clean_delegation,
    cps,
    prep_attributes,
    preps_base,
    preps_ip,
    preps_stake,
    preps_state,
    proposals,
    rewards,
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
        "interval": 300,
    },
    {
        "func": cps.run_cps,
        "interval": 3600,
    },
    {
        "func": clean_delegation.clean_delegations,
        "interval": 600,
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
        "func": proposals.run_proposals,
        "interval": 600,
    },
    {
        "func": rewards.run_rewards,
        "interval": 600,
    },
    {
        "func": preps_stake.run_prep_stake,
        "interval": 600,
    },
    # {
    #     'func': preps_missed_blocks.get_missed_blocks,
    #     'interval': 600,
    # }
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
