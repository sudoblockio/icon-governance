from icon_governance.db import session_factory
from icon_governance.workers.crons.cps import cps_cron
from icon_governance.workers.crons.prep_attributes import prep_attributes_cron
from icon_governance.workers.crons.preps import preps_cron
from icon_governance.workers.crons.proposals import proposals_cron


def test_cps_cron(run_process_wait):
    run_process_wait(cps_cron, (session_factory(),))


def test_prep_attributes_cron(run_process_wait):
    run_process_wait(prep_attributes_cron, (session_factory(),))


def test_preps_cron(run_process_wait):
    run_process_wait(preps_cron, (session_factory(),))


def test_proposals_cron(run_process_wait):
    run_process_wait(proposals_cron, (session_factory(),))
