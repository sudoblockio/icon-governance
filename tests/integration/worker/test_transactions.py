from time import sleep

import pytest
from sqlmodel import select

from icon_governance.models.preps import Prep
from icon_governance.workers.transactions import (
    TransactionsWorker,
    transactions_worker_head,
)

# def test_run_worker():
#     transactions_worker_head()


# def test_prep_creation(prep_creation_docker, run_process_wait, db, db_migration):
#     run_process_wait(transactions_worker)
#
#     preps = db.execute(select(Prep).where(Prep.address == "hxfba37e91ccc13ec1dab115811f73e429cde44d48")).scalars().all()
#     preps = db.execute(select(Prep)).scalars().all()
#
#     assert len(preps) > 0
#     assert preps[0].name == "ICX_Station"


# def test_proposal(prep_creation_docker, run_process_wait, db, db_migration):
#     # run_process_wait(transactions_worker)
#
#     transactions_worker()
#
#     preps = db.execute(select(Prep)).scalars().all()
#
#     assert len(preps) > 0
#     assert preps[0].name == "HugoByte"
