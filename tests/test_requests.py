import json
from todo import datastore


# CREATE


def test_CreateNoData(client_empty):
    client, app = client_empty
    rv = client.post('/todo/create', json={
            "item": "refill gas", "status": "done",
        }
    )
    data = json.loads(rv.data)
    print(data)
    assert data == {'id': 1, 'item': 'refill gas', 'status': 'done'}
    with app.app_context():
        output = datastore.read_all()
        result = []
        for line in output:
            result.append(tuple(line))
        assert result == [(1, 'refill gas', 'done')]


def test_CreateIncompleteInfo(client_empty):
    client, app = client_empty
    rv = client.post('/todo/create', json={
            "item": "refill gas"
        }
    )
    assert rv.status_code == 400


def test_CreateNoInfo(client_empty):
    client, app = client_empty
    rv = client.post('/todo/create')
    assert rv.status_code == 400


# READ


def test_readSingleNoData(client_empty):
    client, _ = client_empty
    rv = client.get('/todo/read/2')
    assert rv.status_code == 410


def test_readSingleHasData(client_populated):
    client, _ = client_populated
    rv = client.get('/todo/read/2')
    data = json.loads(rv.data)
    print(data)
    assert data == {'id': 2, 'item': 'wash car', 'status': 'done'}


def test_readNoData(client_empty):
    client, _ = client_empty
    rv = client.get('/todo/read')
    data = json.loads(rv.data)
    assert len(data) == 0


def test_readHasData(client_populated):
    client, _ = client_populated
    rv = client.get('/todo/read')
    data = json.loads(rv.data)
    print(data)
    assert data == [
        {'id': 1, 'item': 'buy oranges', 'status': ''},
        {'id': 2, 'item': 'wash car', 'status': 'done'},
        {'id': 3, 'item': 'check mail', 'status': 'started'}
    ]


# UPDATE


def test_updateNoMatch(client_empty):
    client, _ = client_empty
    rv = client.post('/todo/update/2', json={
            "item": "refill gas", "status": "done",
        }
    )
    assert rv.status_code == 410


def test_updateHasMatch(client_populated):
    client, app = client_populated
    rv = client.post('/todo/update/2', json={
            "item": "refill gas", "status": "done",
        }
    )
    assert json.loads(rv.data) == {
        "id": 2, "item": "refill gas", "status": "done"
    }
    with app.app_context():
        output = datastore.read_all()
        result = []
        for line in output:
            result.append(tuple(line))
        print(line)
        assert result == [
            (1, 'buy oranges', ''),
            (2, 'refill gas', 'done'),
            (3, 'check mail', 'started'),
        ]


# DELETE


def test_deleteNoMatch(client_empty):
    client, _ = client_empty
    rv = client.post('/todo/delete/2')
    assert rv.status_code == 410


def test_deleteHasMatch(client_populated):
    client, app = client_populated
    rv = client.post('/todo/delete/2')
    assert json.loads(rv.data) == {"id": 2}
    with app.app_context():
        output = datastore.read_all()
        result = []
        for line in output:
            result.append(tuple(line))
        print(line)
        assert result == [
            (1, 'buy oranges', ''),
            (3, 'check mail', 'started'),
        ]
