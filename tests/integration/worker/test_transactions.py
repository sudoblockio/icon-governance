from time import sleep

import pytest
from sqlmodel import select

from icon_governance.models.preps import Prep
from icon_governance.workers.transactions import transactions_worker


@pytest.fixture()
def prep_creation_docker(docker_up_block, docker_project_down):
    project = docker_up_block("36747915")
    sleep(5)
    yield
    docker_project_down(project)


def test_prep_creation(prep_creation_docker, run_process_wait, db, db_migration):
    run_process_wait(transactions_worker)

    preps = db.execute(select(Prep)).scalars().all()

    assert len(preps) > 0
    assert preps[0].name == "HugoByte"


@pytest.fixture()
def prep_creation_docker(docker_up_block, docker_project_down):
    project = docker_up_block("10767242")
    # sleep(5)
    yield
    # docker_project_down(project)


def test_proposal(prep_creation_docker, run_process_wait, db, db_migration):
    # run_process_wait(transactions_worker)

    transactions_worker()

    preps = db.execute(select(Prep)).scalars().all()

    assert len(preps) > 0
    assert preps[0].name == "HugoByte"
