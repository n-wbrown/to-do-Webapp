import pytest, tempfile, os
from todo import create_app, datastore


@pytest.fixture
def client_empty():
    db_fd, db_path = tempfile.mkstemp()
    app = create_app({'TESTING': True, 'DATABASE': db_path})

    with app.test_client() as client:
        with app.app_context():
            datastore.init_db()
        yield client, app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client_populated():
    db_fd, db_path = tempfile.mkstemp()
    app = create_app({'TESTING': True, 'DATABASE': db_path})

    with app.test_client() as client:
        with app.app_context():
            datastore.init_db()
            datastore.create("buy oranges", "")
            datastore.create("wash car", "done")
            datastore.create("check mail", "started")

        yield client, app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def cli_empty():
    db_fd, db_path = tempfile.mkstemp()

    datastore.init_db(db_path=db_path)
    yield db_path

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def cli_populated():
    db_fd, db_path = tempfile.mkstemp()

    datastore.init_db(db_path=db_path)
    datastore.create("buy oranges", "",db_path=db_path)
    datastore.create("wash car", "done",db_path=db_path)
    datastore.create("check mail", "started",db_path=db_path)

    yield db_path

    os.close(db_fd)
    os.unlink(db_path)
