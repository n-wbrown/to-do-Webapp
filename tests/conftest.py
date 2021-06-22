import pytest, tempfile, os
from todo import create_app, datastore


# @pytest.fixture
# def app_empty():
#     app = create_app()
#     app.config["TESTING"] = True
#     app.config["DATABASE"] = ":memory:"
#     with app.app_context():
#         datastore.init_db()
#     return app
# 
# 
# @pytest.fixture
# def client_empty():
#     app = create_app()
#     app.config["TESTING"] = True
#     app.config["DATABASE"] = ":memory:"
#     with app.test_client() as client:
#         yield client
# 
# 
# @pytest.fixture
# def client_populated():
#     app = create_app()
#     app.config["TESTING"] = True
#     app.config["DATABASE"] = ":memory:"
#     with app.app_context:
#        pass 
#     with app.test_client() as client:
#         yield client


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
