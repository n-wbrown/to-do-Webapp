import sqlite3

from flask import current_app, g
from typing import Union, List


def row_to_dict(input: sqlite3.Row) -> dict:
    return {
        "id": input[0],
        "item": input[1],
        "status": input[2],
    }


def get_db(db_path: Union[str, None] = None) -> sqlite3.Connection:
    if db_path is None:
        if 'db' not in g:
            print(current_app.config['DATABASE'])
            if type(current_app.config['DATABASE']) is tuple:
                db_location = current_app.config['DATABASE'][0]
            else:
                db_location = current_app.config['DATABASE']
            g.db = sqlite3.connect(
                db_location,
                detect_types=sqlite3.PARSE_DECLTYPES
            )
            g.db.row_factory = sqlite3.Row
            current_app.logger.debug("Opening connection to database")
            g.cursor = g.db.cursor()
        return g.db
    else:
        db = sqlite3.connect(
            db_path,
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        db.row_factory = sqlite3.Row
        return db


def close_db(db: Union[sqlite3.Connection, None] = None):
    if db is None:
        db = g.pop('db', None)
        if db is not None:
            db.commit()
            current_app.logger.debug("Closing connection to database")
            db.close()

        cursor = g.pop('cursor', None)
        if cursor is not None:
            del cursor
    else:
        db.commit()
        db.close()


def use_db_wrapper(f):
    def wrapped(*args, **kwargs):
        db_path = kwargs.get("db_path", None)
        db = get_db()
        output = f(*args, db=db, **kwargs)
        close_db()
        return output
    return wrapped


@use_db_wrapper
def list_tables(db: sqlite3.Connection):
    cursor = db.cursor()
    output = cursor.execute('''SELECT name FROM sqlite_master 
        WHERE type IN ('table','view')
        AND name NOT LIKE 'sqlite_%'
        ORDER BY 1;''')
    result = []
    for line in output:
        result.append(tuple(line))
    return result


@use_db_wrapper
def init_db(db: sqlite3.Connection):
    cur = db.cursor()
    try:
        # if this is an empty database with no table, create the table
        cur.execute('''CREATE TABLE todo
                    (id integer primary key, item text, status text)
                    ''')
        current_app.logger.info("Adding table to database")
    except sqlite3.OperationalError:
        # if the table already exists in the database, do nothing
        current_app.logger.debug("Database table already created")


@use_db_wrapper
def create(item: str, status: str, db: sqlite3.Connection) -> int:
    cursor = db.cursor()
    assert type(item) == str
    assert type(status) == str
    cursor.execute(
        '''INSERT INTO todo(item, status) VALUES (?, ?)''',
        (item, status)
    )
    return cursor.lastrowid


@use_db_wrapper
def read(id: int, db: sqlite3.Connection) -> Union[sqlite3.Row, None]:
    cursor = db.cursor()
    output = cursor.execute("SELECT * FROM todo where id=:id", {"id": id})
    result = []
    for line in output:
        result.append(tuple(line))
    if len(result) == 0:
        return None
    elif len(result) == 1:
        return result[0]
    else:
        assert False


@use_db_wrapper
def read_all(db: sqlite3.Connection) -> List[sqlite3.Row]:
    cursor = db.cursor()
    rows = []
    for row in cursor.execute('SELECT * FROM todo ORDER BY id'):
        rows.append(row)
    return rows


@use_db_wrapper
def update(
    id: int, item: Union[str, None],
    status: Union[str, None], db: sqlite3.Connection
):
    cursor = db.cursor()
    assert (type(item) == str) or (item is None)
    assert (type(status) == str) or (status is None)
    if item is not None:
        cursor.execute(
            '''UPDATE todo SET item=:item WHERE id=:id''',
            {"id": id, "item": item}
        )
    if status is not None:
        cursor.execute(
            '''UPDATE todo SET status=:status WHERE id=:id''',
            {"id": id, "status": status}
        )


@use_db_wrapper
def delete(id: int, db: sqlite3.Connection):
    cursor = db.cursor()
    cursor.execute(
        '''DELETE FROM todo WHERE id=:id''',
        {"id": id},
    )
