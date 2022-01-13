from time import sleep

from loguru import logger
from prometheus_client import start_http_server

from icon_governance.config import settings
from icon_governance.db import session_factory
from icon_governance.metrics import prom_metrics
from icon_governance.workers.crons.cps import get_cps
from icon_governance.workers.crons.prep_attributes import get_prep_attributes
from icon_governance.workers.crons.preps_base import get_preps_base
from icon_governance.workers.crons.preps_ip import get_prep_state
from icon_governance.workers.crons.preps_stake import get_prep_stake
from icon_governance.workers.crons.proposals import get_proposals
from icon_governance.workers.crons.rewards import get_rewards
from icon_governance.workers.kafka import KafkaClient
from icon_governance.workers.transactions import (
    transactions_worker_head,
    transactions_worker_tail,
)


def main(worker_type: str = None):
    logger.info("Starting metrics server.")
    start_http_server(settings.METRICS_PORT, settings.METRICS_ADDRESS)

    logger.info(f"Worker is a {worker_type}.")

    if worker_type == "head":
        transactions_worker_head()
    if worker_type == "tail":
        transactions_worker_tail()

    kafka = KafkaClient()
    with session_factory() as session:
        get_preps_base(session, kafka)

    if worker_type == "cron":
        while True:
            with session_factory() as session:
                logger.info("Starting rewards cron")
                get_rewards(session)
                prom_metrics.rewards_cron_ran.inc()

                logger.info("Starting base cron")
                get_preps_base(session)
                prom_metrics.preps_base_cron_ran.inc()

                logger.info("Starting cps cron")
                get_cps(session)
                prom_metrics.preps_stake_cron_ran.inc()

                logger.info("Starting attributes cron")
                get_prep_attributes(session)
                prom_metrics.preps_attributes_cron_ran.inc()

                logger.info("Starting state cron")
                get_prep_state(session)
                prom_metrics.preps_attributes_cron_ran.inc()

                logger.info("Starting stake cron")
                get_prep_stake(session)
                prom_metrics.preps_attributes_cron_ran.inc()

                logger.info("Starting proposals cron")
                get_proposals(session)
                prom_metrics.preps_attributes_cron_ran.inc()

                logger.info("Sleeping after crons.")
                sleep(settings.CRON_SLEEP_SEC)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Worker type input.")
    parser.add_argument("worker_type", type=str, help="The type of worker")
    args = parser.parse_args()
    main(args.worker_type)
