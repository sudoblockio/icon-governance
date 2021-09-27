from threading import Thread
from time import sleep
import os

import pytest
from compose.cli.command import project_from_options
from compose.service import ImageType
from icon_governance.db import session
from icon_governance.models.preps import Prep


@pytest.fixture(scope="session")
def db():
    yield session


@pytest.fixture()
def db_migration():
    import alembic.config

    cur_dir = os.path.abspath(os.path.dirname(__file__))
    alembic_dir = os.path.join(cur_dir, '../../icon_governance')
    os.chdir(alembic_dir)

    alembicArgs = [
        '--raiseerr',
        'upgrade', 'head',
    ]
    alembic.config.main(argv=alembicArgs)
    yield

    # from icon_governance.alembic.env import run_migrations_offline
    # run_migrations_offline()


@pytest.fixture()
def get_path_to_file():
    def f(file_name):

        cur_dir = os.getcwd()

        while True:
            file_list = os.listdir(cur_dir)
            parent_dir = os.path.dirname(cur_dir)

            if file_name in file_list:
                return cur_dir
            else:
                if cur_dir == parent_dir:
                    break
                else:
                    cur_dir = parent_dir

    return f


@pytest.fixture()
def get_compose_project(get_path_to_file):
    def f(compose_files=None):
        if compose_files is None:
            compose_files = ['docker-compose.db.yml']

        project_dir = get_path_to_file(compose_files[0])

        project = project_from_options(
            project_dir=str(project_dir),
            options={"--file": compose_files},
        )
        return project

    return f


@pytest.fixture()
def docker_up_block(get_compose_project):
    def f(block, compose_files=None):
        get_compose_project(compose_files)
        os.environ['START_BLOCK'] = block

        project = get_compose_project()
        project.up()

        return project

    return f


@pytest.fixture()
def docker_project_down(get_compose_project):
    def f(project):
        project.down(ImageType.none, "--docker-compose-remove-volumes")

    return f


@pytest.fixture()
def run_process_wait():
    def f(target, timeout: int = 1):
        thread = Thread(
            target=target,
            args=(),
        )
        thread.daemon = True
        thread.start()

        # Let worker work
        sleep(timeout)
        assert thread.is_alive()

    return f
