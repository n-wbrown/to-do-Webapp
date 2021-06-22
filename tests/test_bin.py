import json
import pytest
from todo import bin as bin_tools
from todo import datastore


# CREATE


def test_CreateNoData(cli_empty):
    db_path = cli_empty
    result = bin_tools.create(db=db_path, item="refill gas", status="done")
    assert result == {'id': 1, 'item': 'refill gas', 'status': 'done'}
    response = []
    output = datastore.read_all(db_path=db_path)
    for row in output:
        response.append(datastore.row_to_dict(row))
    print(response)
    assert response == [{'id': 1, 'item': 'refill gas', 'status': 'done'}]


# READ


def test_ReadNoData(cli_empty):
    db_path = cli_empty
    with pytest.raises(bin_tools.CLIerror):
        bin_tools.read(db=db_path, id=9)


def test_ReadHasData(cli_populated):
    db_path = cli_populated
    result = bin_tools.read(db=db_path, id=2)
    assert result == {'id': 2, 'item': 'wash car', 'status': 'done'}


def test_ReadAllNoData(cli_empty):
    db_path = cli_empty
    result = bin_tools.read(db=db_path)
    assert result == []


def test_ReadAllHasData(cli_populated):
    db_path = cli_populated
    result = bin_tools.read(db=db_path)
    print(result)
    assert result == [
        {'id': 1, 'item': 'buy oranges', 'status': ''},
        {'id': 2, 'item': 'wash car', 'status': 'done'},
        {'id': 3, 'item': 'check mail', 'status': 'started'}
    ]


# UPDATE


def test_UpdateNoData(cli_empty):
    db_path = cli_empty
    with pytest.raises(bin_tools.CLIerror):
        bin_tools.update(db=db_path, id=9)


def test_UpdateHasData(cli_populated):
    db_path = cli_populated
    result = bin_tools.update(
        db=db_path, id=2, item="buy groceries",
        status="scheduled"
    )
    assert result == None

    output = datastore.read_all(db_path=db_path)
    response = []
    for row in output:
        response.append(datastore.row_to_dict(row))
    print(response)
    assert response == [
        {'id': 1, 'item': 'buy oranges', 'status': ''},
        {'id': 2, 'item': 'buy groceries', 'status': 'scheduled'},
        {'id': 3, 'item': 'check mail', 'status': 'started'}
    ]


# DELETE


def test_DeleeNoData(cli_empty):
    db_path = cli_empty
    with pytest.raises(bin_tools.CLIerror):
        bin_tools.delete(db=db_path, id=9)


def test_DeleteHasData(cli_populated):
    db_path = cli_populated
    result = bin_tools.delete(db=db_path, id=2)
    assert result == None

    output = datastore.read_all(db_path=db_path)
    response = []
    for row in output:
        response.append(datastore.row_to_dict(row))
    print(response)
    assert response == [
        {'id': 1, 'item': 'buy oranges', 'status': ''},
        {'id': 3, 'item': 'check mail', 'status': 'started'}
    ]
