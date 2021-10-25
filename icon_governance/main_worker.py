from multiprocessing.pool import ThreadPool
from threading import Thread
from time import sleep

from loguru import logger
from prometheus_client import start_http_server

from icon_governance.config import settings
from icon_governance.workers.crons.cps import cps_cron
from icon_governance.workers.crons.prep_attributes import prep_attributes_cron
from icon_governance.workers.crons.preps import preps_cron
from icon_governance.workers.crons.proposals import proposals_cron
from icon_governance.workers.transactions import (
    transactions_worker_head,
    transactions_worker_tail,
)

logger.info("Starting metrics server.")
metrics_pool = ThreadPool(1)
metrics_pool.apply_async(start_http_server, (settings.METRICS_PORT, settings.METRICS_ADDRESS))

transactions_worker_head_thread = Thread(
    target=transactions_worker_head,
    args=(),
)

transactions_worker_tail_thread = Thread(
    target=transactions_worker_tail,
    args=(),
)

prep_cron = Thread(
    target=preps_cron,
    args=(),
)

prep_attributes_cron = Thread(
    target=prep_attributes_cron,
    args=(),
)

cps_cron = Thread(
    target=cps_cron,
    args=(),
)

proposals_cron = Thread(
    target=proposals_cron,
    args=(),
)

transactions_worker_head_thread.start()
transactions_worker_tail_thread.start()

prep_cron.start()

sleep(60)

prep_attributes_cron.start()
cps_cron.start()
proposals_cron.start()
