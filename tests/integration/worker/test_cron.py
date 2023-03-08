from icon_governance.workers.crons.cps import run_cps
from icon_governance.workers.crons.prep_attributes import run_prep_attributes
from icon_governance.workers.crons.preps_base import run_preps_base
from icon_governance.workers.crons.preps_ip import run_prep_ip
from icon_governance.workers.crons.preps_stake import run_prep_stake
from icon_governance.workers.crons.preps_state import run_prep_state
from icon_governance.workers.crons.proposals import run_proposals
from icon_governance.workers.crons.rewards import run_rewards


def test_preps_cron(db):
    with db as session:
        run_preps_base(session)


def test_cps_cron(db):
    with db as session:
        run_cps(session)


def test_prep_attributes_cron(db):
    with db as session:
        run_prep_attributes(session)


def test_proposals_cron(db):
    with db as session:
        run_proposals(session)


def test_stake_cron(db):
    with db as session:
        run_prep_stake(session)


def test_get_rewards(db):
    with db as session:
        run_rewards(session)


def test_get_prep_state(db):
    with db as session:
        run_prep_ip(session)


def test_run_prep_state(db):
    with db as session:
        run_prep_state(session=session)
