import pytest

from icon_governance.workers.crons import (
    cps,
    prep_attributes,
    preps_base,
    preps_failed_blocks,
    preps_ip,
    preps_iscore,
    preps_rewards,
    preps_single,
    preps_stake,
    preps_state,
    proposals,
)

CRONS = [
    preps_base.run_preps_base,
    prep_attributes.run_prep_attributes,
    cps.run_cps,
    preps_failed_blocks.run_failed_blocks,
    preps_ip.run_prep_ip,
    preps_stake.run_prep_stake,
    preps_single.run_get_prep,
    preps_state.run_prep_state,
    proposals.run_proposals,
    preps_iscore.run_prep_iscore,
    preps_rewards.run_get_prep_rewards,
]


@pytest.mark.parametrize("cron", CRONS)
def test_preps_cron(db, cron):
    with db as session:
        cron(session)
