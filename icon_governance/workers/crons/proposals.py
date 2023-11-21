from time import sleep

from sqlmodel import select

from icon_governance.log import logger
from icon_governance.metrics import prom_metrics
from icon_governance.models.proposals import Proposal
from icon_governance.utils.rpc import convert_hex_int, getProposals, post_rpc_json


def run_proposals(session):
    logger.info(f"Starting {__name__} cron")

    proposals = post_rpc_json(getProposals())
    if proposals is None:
        logger.info("No proposals found from rpc. Chilling for a bit.")
        sleep(1)
        return

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

        session.add(proposal)
        try:
            session.commit()
            session.refresh(proposal)
        except:
            session.rollback()
            raise
        finally:
            session.close()

    prom_metrics.preps_attributes_cron_ran.inc()
    logger.info(f"Ending {__name__} cron")


if __name__ == "__main__":
    from icon_governance.db import session_factory

    with session_factory() as session:
        run_proposals(session=session)
