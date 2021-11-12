from icon_governance.db import session_factory
from icon_governance.workers.crons.cps import cps_cron
from icon_governance.workers.crons.prep_attributes import prep_attributes_cron
from icon_governance.workers.crons.preps import preps_cron
from icon_governance.workers.crons.proposals import proposals_cron


def test_preps_cron(db, run_process_wait):
    with db as session:
        run_process_wait(preps_cron, (session,))


def test_cps_cron(db, run_process_wait):
    with db as session:
        run_process_wait(cps_cron, (session,))


def test_prep_attributes_cron(db, run_process_wait):
    with db as session:
        run_process_wait(prep_attributes_cron, (session,))


def test_proposals_cron(db, run_process_wait):
    with db as session:
        run_process_wait(proposals_cron, (session,))
