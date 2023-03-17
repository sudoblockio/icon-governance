from time import sleep

import requests
from sqlmodel import select

from icon_governance.config import settings
from icon_governance.log import logger
from icon_governance.metrics import prom_metrics
from icon_governance.models.preps import Prep
from icon_governance.utils.rpc import get_admin_chain


def p2p_to_rpc_address(p2p_address):
    return p2p_address.split(":")[0], "9000"


def get_prep_address_peers(ip_address: str = "52.26.81.40"):
    admin_metrics = get_admin_chain(ip_address=ip_address)

    peers = []
    for peer in admin_metrics["module"]["network"]["p2p"]["friends"]:
        peers.append({"ip_address": peer["addr"], "public_key": peer["id"]})

    return peers


def scrape_peers(peers):
    neighbor_peers = []
    for peer in peers:
        neighbor_peers.append(get_prep_address_peers(peer["ip_address"].split(":")[0]))
    return neighbor_peers


def get_peers(peer_set: set, added_peers: list = None):
    """
    Function that takes in a set with a tuple of the ip and node_address as a seed to
    then call that node's orphan peers, call those nodes
    """
    if added_peers is None:
        added_peers = []

    old_peer_count = len(added_peers)

    for i in peer_set.copy():
        if i[0] not in added_peers:
            admin_metrics = get_admin_chain(ip_address=i[0])
            added_peers.append(i[0])
        else:
            continue

        if admin_metrics is None:
            continue

        for peer in admin_metrics["module"]["network"]["p2p"]["orphanages"]:

            peer_item = (peer["addr"].split(":")[0], peer["id"])

            if peer_item not in peer_set:
                peer_set.add(peer_item)

    if old_peer_count == len(added_peers):
        return peer_set
    else:
        return get_peers(peer_set, added_peers=added_peers)


def run_prep_ip(session):
    logger.info("Running prep ip cron")

    # Gets a full set of IP addresses
    peers = get_peers({(settings.PEER_SEED_IP, settings.PEER_SEED_ADDRESS)})

    result = session.execute(select(Prep))
    preps = result.scalars().all()

    for prep in preps:
        prep_ip = [i[0] for i in peers if i[1] == prep.node_address]

        if len(prep_ip) == 0:
            # Prep not active in peer set
            prep.node_state = "Inactive"
        else:
            prep_ip = prep_ip[0]
            prep.p2p_endpoint = prep_ip + ":7100"
            prep.api_endpoint = prep_ip + ":9000"

        session.merge(prep)
    session.commit()
    logger.info("Ending prep ip cron")


if __name__ == "__main__":
    from icon_governance.db import session_factory

    with session_factory() as session:
        run_prep_ip(session=session)
