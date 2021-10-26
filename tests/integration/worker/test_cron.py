from icon_governance.workers.crons.cps import cps_cron
from icon_governance.workers.crons.prep_attributes import prep_attributes_cron
from icon_governance.workers.crons.preps import preps_cron
from icon_governance.workers.crons.proposals import proposals_cron


def test_cron_worker(run_process_wait):
    run_process_wait(cps_cron)
