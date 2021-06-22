import argparse
from . import datastore
from typing import Union


class CLIerror(Exception):
    pass


def create(db, item: str, status: str, **kwargs) -> int:
    datastore.init_db(db_path=db)
    result = datastore.create(item=item, status=status, db_path=db)
    return {
        "id": result,
        "item": item,
        "status": status,
    }


def read(db, id: Union[str, None] = None, **kwargs) -> Union[dict, None]:
    datastore.init_db(db_path=db)
    if id is not None:
        result = datastore.read(id=id, db_path=db)
        if result is not None:
            output = datastore.row_to_dict(result)
        else:
            raise CLIerror("No entry with that ID exists")
            return

    else:
        result = datastore.read_all(db_path=db)
        output = []
        for line in result:
            output.append(datastore.row_to_dict(line))

    return output


def update(
    db: str, id: int, item: Union[str, None] = None,
    status: Union[str, None] = None, **kwargs,
) -> Union[str, None]:
    datastore.init_db(db_path=db)
    if datastore.read(id=id, db_path=db) is None:
        raise CLIerror("No entry with that ID exists")
        return
    try:
        datastore.update(id=id, item=item, status=status, db_path=db)
    except AssertionError:
        raise CLIerror("Invalid arguments")

    return


def delete(db: str, id: int, **kwargs):
    datastore.init_db(db_path=db)
    if datastore.read(id=id, db_path=db) is None:
        raise CLIerror("No entry with that ID exists")
        return

    datastore.delete(id=id, db_path=db)
    return



def main():
    parser = argparse.ArgumentParser(prog='todo')
    parser.add_argument('--db', required=True, help='select your database')
    subparsers = parser.add_subparsers(
        dest="operation",
        title="Subcommands",
        description="",
        help="",
    )

    # CREATE
    parser_create = subparsers.add_parser(
        'create',
        help='Create a new to-do item'
    )
    parser_create.add_argument(
        '--item', type=str, help='The new to-do item', required=True,
    )
    parser_create.add_argument(
        '--status', type=str, help='The status of the newitem', required=True
    )

    # READ
    parser_read = subparsers.add_parser(
        'read',
        help='Read the data of an existing to-do item'
    )
    parser_read.add_argument(
        '--id', type=int, help='The to-do item to read'
    )

    # UPDATE
    parser_update = subparsers.add_parser(
        'update',
        help='Update an existing to-do item'
    )
    parser_update.add_argument(
        '--id', type=int, help='The id of the to-do item to change',
        required=True
    )
    parser_update.add_argument(
        '--item', type=str, help='The new item text'
    )
    parser_update.add_argument(
        '--status', type=str, help='The new status text'
    )
    # READ
    parser_delete = subparsers.add_parser(
        'delete',
        help='Delete a to-do item'
    )
    parser_delete.add_argument(
        '--id', type=int, help='The id of the to-do item to delete'
    )

    args = vars(parser.parse_args())
    ops = {
        "create": create,
        "read": read,
        "update": update,
        "delete": delete,
    }
    try:
        subcommand = args['operation']
    except KeyError:
        print("An operation is required")
        return 1

    try:
        result = ops[subcommand](**args)
        if result is not None:
            print(result)
    except CLIerror as e:
        print(e)
