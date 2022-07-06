# from icon_governance.db import session_factory
# from icon_governance.workers.crons.preps_ip import get_prep_state

# def test_get_prep_state(mocker):
#     from .fixture import peers
#     mocker.patch('icon_governance.workers.crons.preps_ip.get_peers', return_value=peers)
#     get_prep_state(session_factory())
#
#
# def test_get_peers():
#     peer_set = {('174.138.3.225', 'hx6f89b2c25c15f6294c79810221753131067ed3f8')}
#     peers = get_peers(peer_set)
#     assert len(peers) > 50
