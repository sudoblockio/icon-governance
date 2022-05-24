import requests
from sqlmodel import select

from icon_governance.log import logger
from icon_governance.models.preps import Prep


def get_prep_state(session):
    logger.info("Getting prep node state")
    result = session.execute(select(Prep))
    preps = result.scalars().all()

    if len(preps) == 0:
        raise Exception("Empty DB.")

    for prep in preps:
        if prep.api_endpoint is None:
            # Prep not active in peer set
            prep.node_state = "Inactive"
        else:
            try:
                endpoint = prep.api_endpoint
                if not prep.api_endpoint.startswith("http://"):
                    endpoint = "http://" + prep.api_endpoint

                r = requests.get(endpoint + "/metrics", timeout=1)
                if r.status_code == 200:
                    for i in r.text.split("\n"):
                        if i.startswith("goloop_consensus_round_duration"):
                            if int(float(i.split()[-1])) > 1500:
                                prep.node_state = "Synced"
                            elif int(float(i.split()[-1])) < 1500:
                                prep.node_state = "BlockSync"
                            break
            except requests.exceptions.RequestException:
                prep.node_state = "Unknown"

        session.merge(prep)
        session.commit()


if __name__ == "__main__":
    from icon_governance.db import session_factory

    get_prep_state(session_factory())
