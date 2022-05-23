import json
from typing import Type

from icon_governance.config import settings
from icon_governance.db import session_factory
from icon_governance.log import logger
from icon_governance.metrics import prom_metrics
from icon_governance.models.preps import Prep
from icon_governance.models.rewards import Reward
from icon_governance.schemas.block_etl_pb2 import BlockETL, LogETL, TransactionETL
from icon_governance.utils.details import get_details
from icon_governance.workers.delegations import set_delegation
from icon_governance.workers.kafka import KafkaClient, get_current_offset


class TransactionsWorker(KafkaClient):
    msg_count: int = 0
    preps_created: int = 0
    preps_updated: int = 0

    block: Type[BlockETL] = BlockETL()
    transaction: Type[TransactionETL] = TransactionETL()
    log: Type[LogETL] = LogETL()

    def process_transaction_preps(self, data, method):
        try:
            params = data["params"]
        except KeyError:
            # Must be a failed Tx or something?
            logger.info(f"Skipping Tx - no params {self.transaction.hash}")
            return

        prep = self.session.get(Prep, self.transaction.from_address)

        if prep is not None:
            if method == "unregisterPRep":
                logger.info(f"Prep unregistration tx hash {self.transaction.hash}")
                prep.status = "unregistered"

                self.preps_created += 1
                prom_metrics.preps_created.set(self.preps_created)

                self.session.add(prep)
                self.session.commit()
                return

            if prep.last_updated_block is not None:

                if prep.last_updated_block > self.block.number and method == "setPrep":
                    logger.info(
                        f"Skipping setPrep call in tx_hash {self.transaction.hash} "
                        f"because it has since been updated."
                    )
                    return
        else:
            prep = Prep(
                address=self.transaction.from_address,
            )

        if prep.last_updated_block is None:
            logger.info(f"Prep update registration tx hash {self.transaction.hash}")
            prep.created_block = self.block.number
            # prep.created_timestamp = timestamp

        prep.last_updated_block = self.block.number
        # prep.last_updated_timestamp = timestamp
        prep.name = params["name"]
        prep.email = params["email"]
        prep.city = params["city"]
        prep.website = params["website"]
        prep.country = params["country"]
        prep.details = params["details"]
        prep.p2p_endpoint = params["p2pEndpoint"]

        if "nodeAddress" in params:
            prep.node_address = params["nodeAddress"]

        details = get_details(params["details"])
        # Add information from details
        if details is not None:
            for k, v in details.items():
                try:
                    setattr(prep, k, v)
                except ValueError:
                    continue

        self.preps_updated += 1
        prom_metrics.preps_updated.set(self.preps_updated)

        self.session.add(prep)
        try:
            self.session.commit()
        except:
            self.session.rollback()
            raise

    def process_transaction_rewards(self):
        logger.info(f"set delegation {self.transaction.hash}")
        reward = self.session.get(Reward, self.transaction.hash)
        if reward is None:
            logger.info(f"Creating reward transaction {self.transaction.hash}")
            reward = Reward(
                address=self.transaction.from_address,
                tx_hash=self.transaction.hash,
                block=self.block.number,
                timestamp=self.transaction.timestamp / 1e6,
            )

            self.session.add(reward)
            try:
                self.session.commit()
            except:
                self.session.rollback()
                raise

    def process_transaction(self):
        # Ignore any unsuccessful txs
        if self.transaction.status != "0x1":
            return

        # Ignore anything without a method call like contract creation events
        if self.transaction.data == "":
            return

        data = json.loads(self.transaction.data)

        if "method" not in data:
            return

        method = data["method"]

        # P-Reps
        if method in ["registerPRep", "setPrep"]:
            self.process_transaction_preps(data, method)

        if method in ["unregisterPRep"]:
            # TODO: Handle unregister? Add field (unregistered?) Would need to add it
            #  into api
            print("Skipping for now.")

        # Staking
        elif method == "setStake":
            pass

        elif method == "setDelegation":
            logger.info(f"set delegation {self.transaction.hash}")
            set_delegation(
                session=self.session,
                data=data,
                address=self.transaction.from_address,
                block_height=self.block.number,
                hash=self.transaction.hash,
            )

        elif method == "claimIScore":
            self.process_transaction_rewards()

        elif method == "registerProposal":
            pass

        elif method == "cancelProposal":
            pass

        if method == "voteProposal":
            pass

    def process(self, msg):
        # Deserialize msg
        self.block.ParseFromString(msg.value())

        for tx in self.block.transactions:
            if tx.to_address == settings.governance_address:
                # Skip all Txs not to the gov address
                self.transaction = tx
                self.process_transaction()


def transactions_worker_head():
    with session_factory() as session:
        kafka = TransactionsWorker(
            session=session,
            topic=settings.CONSUMER_TOPIC_BLOCKS,
            consumer_group=settings.CONSUMER_GROUP + "-head",
        )

        kafka.start()


def transactions_worker_tail():
    with session_factory() as session:
        consumer_group, partition_dict = get_current_offset(session)

        kafka = TransactionsWorker(
            session=session,
            topic=settings.CONSUMER_TOPIC_BLOCKS,
            consumer_group=consumer_group,
            partition_dict=partition_dict,
        )

        kafka.start()
