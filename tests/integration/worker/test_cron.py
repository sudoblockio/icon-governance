from icon_governance.workers.crons.cps import get_cps
from icon_governance.workers.crons.prep_attributes import get_prep_attributes
from icon_governance.workers.crons.preps_base import get_preps_base
from icon_governance.workers.crons.preps_stake import get_prep_stake
from icon_governance.workers.crons.proposals import get_proposals
from icon_governance.workers.crons.rewards import get_rewards


def test_preps_cron(db):
    with db as session:
        get_preps_base(session)


def test_cps_cron(db):
    with db as session:
        get_cps(session)


def test_prep_attributes_cron(db):
    with db as session:
        get_prep_attributes(session)


def test_proposals_cron(db):
    with db as session:
        get_proposals(session)


def test_stake_cron(db):
    with db as session:
        get_prep_stake(session)


def test_get_rewards(db):
    with db as session:
        get_rewards(session)
