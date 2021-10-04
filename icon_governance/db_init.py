from json import JSONDecodeError

import requests
from requests.exceptions import ConnectionError, ConnectTimeout

from icon_governance.db import session
from icon_governance.log import logger
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

        if "api_endpoint" in details["server"]:
            prep.api_endpoint = details["server"]["api_endpoint"]

        if "location" in details["server"]:
            if "country" in details["server"]["location"]:
                prep.server_country = details["server"]["location"]["country"]
            if "city" in details["server"]["location"]:
                prep.server_city = details["server"]["location"]["city"]


def get_initial_preps():
    rpc_preps = getPReps().json()["result"]

    for p in rpc_preps["preps"]:
        prep = session.get(Prep, p["address"])
        logger.info(f"Parsing {p['name']}")
        if prep is None:
            prep = Prep(
                address=p["address"],
                name=p["name"],
                country=p["country"],
                city=p["city"],
                email=p["email"],
                website=p["website"],
                details=p["details"],
                p2p_endpoint=p["p2pEndpoint"],
                node_address=p["nodeAddress"],
                status=p["status"],
            )
        else:
            # Prep is already in DB
            continue

        try:
            r = requests.get(p["details"], timeout=1)
        except (ConnectTimeout, ConnectionError):
            # Details not available so no more parsing
            session.add(prep)
            session.commit()
            continue

        if r.status_code == 200:
            try:
                details = r.json()
                extract_details(details, prep)
            except JSONDecodeError:
                pass

            # if 'representative' in details:
            #     if 'logo' in details['representative']:
            #         if 'logo_256' in details['representative']['logo']:
            #             prep.logo_256 = details['representative']['logo']['logo_256']
            #         if 'logo_1024' in details['representative']['logo']:
            #             prep.logo_1024 = details['representative']['logo']['logo_1024']
            #         if 'logo_svg' in details['representative']['logo']:
            #             prep.logo_svg = details['representative']['logo']['logo_svg']
            #
            #     if 'media' in details['representative']:
            #         if 'steemit' in details['representative']['media']:
            #             prep.steemit = details['representative']['media']['steemit']
            #         if 'twitter' in details['representative']['media']:
            #             prep.twitter = details['representative']['media']['twitter']
            #         if 'youtube' in details['representative']['media']:
            #             prep.youtube = details['representative']['media']['youtube']
            #         if 'facebook' in details['representative']['media']:
            #             prep.facebook = details['representative']['media']['facebook']
            #         if 'github' in details['representative']['media']:
            #             prep.github = details['representative']['media']['github']
            #         if 'reddit' in details['representative']['media']:
            #             prep.reddit = details['representative']['media']['reddit']
            #         if 'keybase' in details['representative']['media']:
            #             prep.keybase = details['representative']['media']['keybase']
            #         if 'telegram' in details['representative']['media']:
            #             prep.telegram = details['representative']['media']['telegram']
            #         if 'wechat' in details['representative']['media']:
            #             prep.wechat = details['representative']['media']['wechat']
            #
            # if 'server' in details:
            #     if 'server_type' in details['server']:
            #         prep.server_type = details['server']['server_type']
            #
            #     if 'api_endpoint' in details['server']:
            #         prep.api_endpoint = details['server']['api_endpoint']
            #
            #     if 'location' in details['server']:
            #         if 'country' in details['server']['location']:
            #             prep.server_country = details['server']['location']['country']
            #         if 'city' in details['server']['location']:
            #             prep.server_city = details['server']['location']['city']
        else:
            pass

        session.add(prep)
        session.commit()


if __name__ == "__main__":
    get_initial_preps()
