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
