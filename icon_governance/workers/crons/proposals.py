from time import sleep

from sqlmodel import select

from icon_governance.config import settings
from icon_governance.db import session
from icon_governance.log import logger
from icon_governance.models.preps import Prep
from icon_governance.models.proposals import Proposal
from icon_governance.utils.rpc import convert_hex_int, getProposals, post_rpc_json


def proposals_cron():

    while True:
        logger.info("")
        proposals = post_rpc_json(getProposals())
        if proposals is None:
            logger.info("No proposals found from rpc. Chilling for a bit.")
            sleep(60)
            continue

        proposals_db = session.execute(select(Proposal)).scalars().all()

        titles = [i.title for i in proposals_db]

        for p in proposals["proposals"]:
            if p["contents"]["title"] in titles:
                # If it is in DB continue
                continue
            else:
                proposal = Proposal()

            proposal.proposer = p["proposer"]
            proposal.proposer_name = p["proposerName"]
            proposal.status = p["status"]

            proposal.contents_json = p["contents"]
            proposal.title = p["contents"]["title"]
            proposal.description = p["contents"]["description"]
            proposal.type = p["contents"]["type"]

            # TODO: Fix json into db
            # from psycopg2.extras import Json
            # proposal.value = Json(p["contents"]["value"])

            proposal.start_block_height = convert_hex_int(p["startBlockHeight"])
            proposal.end_block_height = convert_hex_int(p["endBlockHeight"])

            proposal.agree_amount = convert_hex_int(p["vote"]["agree"]["amount"]) / 1e18
            proposal.disagree_amount = convert_hex_int(p["vote"]["disagree"]["amount"]) / 1e18
            proposal.no_vote_amount = convert_hex_int(p["vote"]["noVote"]["amount"]) / 1e18
            proposal.agree_count = convert_hex_int(p["vote"]["agree"]["count"]) / 1e18
            proposal.disagree_count = convert_hex_int(p["vote"]["disagree"]["count"]) / 1e18
            proposal.no_vote_count = convert_hex_int(p["vote"]["noVote"]["count"]) / 1e18

            session.merge(proposal)
            session.commit()

        logger.info("Proposals cron ran.")
        sleep(settings.CRON_SLEEP_SEC)


if __name__ == "__main__":
    proposals_cron()