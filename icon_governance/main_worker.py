from contextlib import ExitStack
from functools import partial
from multiprocessing.pool import ThreadPool
from threading import Thread
from time import sleep

from loguru import logger
from prometheus_client import start_http_server
from sqlalchemy.orm import scoped_session

from icon_governance.config import settings
from icon_governance.db import session_factory
from icon_governance.workers.crons.cps import cps_cron
from icon_governance.workers.crons.prep_attributes import prep_attributes_cron
from icon_governance.workers.crons.preps import preps_cron
from icon_governance.workers.crons.preps_stake import prep_stake_cron
from icon_governance.workers.crons.proposals import proposals_cron
from icon_governance.workers.transactions import transactions_worker_head

logger.info("Starting metrics server.")
metrics_pool = ThreadPool(1)
metrics_pool.apply_async(start_http_server, (settings.METRICS_PORT, settings.METRICS_ADDRESS))


Session = scoped_session(session_factory)

if not settings.IS_TAIL_WORKER:
    # Base
    prep_cron_session = Session()
    prep_cron = Thread(
        target=preps_cron,
        args=(prep_cron_session,),
    )
    prep_cron.start()

    sleep(60)

    # Attributes
    prep_attributes_cron_session = Session()
    prep_attributes_cron = Thread(
        target=prep_attributes_cron,
        args=(prep_attributes_cron_session,),
    )
    prep_attributes_cron.start()

    # CPS
    cps_cron_session = Session()
    cps_cron = Thread(
        target=cps_cron,
        args=(cps_cron_session,),
    )
    cps_cron.start()

    # Proposals
    proposals_cron_session = Session()
    proposals_cron = Thread(
        target=proposals_cron,
        args=(proposals_cron_session,),
    )
    proposals_cron.start()

    # Stake
    prep_stake_cron_session = Session()
    prep_stake_cron = Thread(
        target=prep_stake_cron,
        args=(proposals_cron_session,),
    )
    proposals_cron.start()

    # Kafka
    transactions_worker_head_thread_session = Session()
    transactions_worker_head_thread = Thread(
        target=transactions_worker_head,
        args=(transactions_worker_head_thread_session,),
    )
    transactions_worker_head_thread.start()

else:
    # Kafka
    transactions_worker_head_thread_session = Session()
    transactions_worker_head_thread = Thread(
        target=transactions_worker_head,
        args=(transactions_worker_head_thread_session,),
    )
    transactions_worker_head_thread.start()
