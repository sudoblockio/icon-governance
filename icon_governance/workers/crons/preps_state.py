import requests
from sqlmodel import select

from icon_governance.log import logger
from icon_governance.metrics import prom_metrics
from icon_governance.models.preps import Prep


def run_prep_state(session):
    logger.info("Running prep ip state")

    result = session.execute(select(Prep))
    preps = result.scalars().all()

    if len(preps) == 0:
        raise Exception("Empty DB.")

    for prep in preps:
        if prep.api_endpoint is None:
            prep.node_state = "Unknown"
            session.merge(prep)
            continue

        rpc_endpoint = prep.api_endpoint + "/metrics"

        if not rpc_endpoint.startswith("http://"):
            rpc_endpoint = "http://" + rpc_endpoint

        try:
            r = requests.get(rpc_endpoint, timeout=1)
        except requests.exceptions.RequestException:
            prep.node_state = "Unknown"
            session.merge(prep)
            continue

        if r.status_code == 200:
            print()
            for i in r.text.split("\n"):
                if i.startswith("goloop_consensus_round_duration"):
                    if int(float(i.split()[-1])) > 1500:
                        prep.node_state = "Synced"
                    elif int(float(i.split()[-1])) < 1500:
                        prep.node_state = "BlockSync"
                    break
        else:
            prep.node_state = "Unknown"

        session.merge(prep)
    session.commit()

    prom_metrics.preps_attributes_cron_ran.inc()
    logger.info("Ending prep node state")


if __name__ == "__main__":
    from icon_governance.db import session_factory

    run_prep_state(session_factory())
