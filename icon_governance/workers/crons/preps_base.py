import requests

from icon_governance.log import logger
from icon_governance.metrics import prom_metrics
from icon_governance.models.preps import Prep
from icon_governance.utils.rpc import getPReps


def extract_details(details: dict, prep: Prep):
    if "representative" in details:
        if "logo" in details["representative"]:
            if "logo_256" in details["representative"]["logo"]:
                prep.logo_256 = details["representative"]["logo"]["logo_256"]
            if "logo_1024" in details["representative"]["logo"]:
                prep.logo_1024 = details["representative"]["logo"]["logo_1024"]
            if "logo_svg" in details["representative"]["logo"]:
                prep.logo_svg = details["representative"]["logo"]["logo_svg"]

        if "media" in details["representative"]:
            if "steemit" in details["representative"]["media"]:
                prep.steemit = details["representative"]["media"]["steemit"]
            if "twitter" in details["representative"]["media"]:
                prep.twitter = details["representative"]["media"]["twitter"]
            if "youtube" in details["representative"]["media"]:
                prep.youtube = details["representative"]["media"]["youtube"]
            if "facebook" in details["representative"]["media"]:
                prep.facebook = details["representative"]["media"]["facebook"]
            if "github" in details["representative"]["media"]:
                prep.github = details["representative"]["media"]["github"]
            if "reddit" in details["representative"]["media"]:
                prep.reddit = details["representative"]["media"]["reddit"]
            if "keybase" in details["representative"]["media"]:
                prep.keybase = details["representative"]["media"]["keybase"]
            if "telegram" in details["representative"]["media"]:
                prep.telegram = details["representative"]["media"]["telegram"]
            if "wechat" in details["representative"]["media"]:
                prep.wechat = details["representative"]["media"]["wechat"]

    if "server" in details:
        if "server_type" in details["server"]:
            prep.server_type = details["server"]["server_type"]

        if "location" in details["server"]:
            if "country" in details["server"]["location"]:
                prep.server_country = details["server"]["location"]["country"]
            if "city" in details["server"]["location"]:
                prep.server_city = details["server"]["location"]["city"]


def run_preps_base(session):
    logger.info(f"Starting {__name__} cron")

    rpc_preps = getPReps().json()["result"]

    for p in rpc_preps["preps"]:
        prep = session.get(Prep, p["address"])
        # logger.info(f"Parsing {p['name']}")
        if prep is None:
            prep = Prep(
                address=p["address"],
            )

        prep.name = p["name"]
        prep.country = p["country"]
        prep.city = p["city"]
        prep.email = p["email"]
        prep.website = p["website"]
        prep.details = p["details"]
        prep.p2p_endpoint = p["p2pEndpoint"]
        prep.node_address = p["nodeAddress"]
        prep.status = p["status"]
        prep.grade = p["grade"]
        prep.penalty = p["penalty"]
        # prep.created_block = (convert_hex_int(p["blockHeight"])

        try:
            r = requests.get(
                p["details"],
                timeout=4,
                headers={
                    "Accept": "application/json",
                    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
                },
            )
            if r.status_code == 200:
                details = r.json()
                extract_details(details, prep)

        except Exception:
            # Details not available so no more parsing
            # logger.info(f"error parsing {p['address']}")
            pass

        session.merge(prep)
        session.commit()

    prom_metrics.preps_base_cron_ran.inc()
    logger.info(f"Ending {__name__} cron")


if __name__ == "__main__":
    from icon_governance.db import session_factory

    with session_factory() as session:
        run_preps_base(session=session)
