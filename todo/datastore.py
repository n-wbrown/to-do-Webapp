import sqlite3

from flask import current_app, g
from typing import Union, List


def row_to_dict(input: sqlite3.Row) -> dict:
    return {
        "id": input[0],
        "item": input[1],
        "status": input[2],
    }

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
        current_app.logger.debug("Opening connection to database")
        g.cursor = g.db.cursor()
    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.commit()
        current_app.logger.debug("Closing connection to database")
        db.close()

    cursor = g.pop('cursor', None)
    if cursor is not None:
        del cursor


def list_tables():
    output = g.cursor.execute('''SELECT name FROM sqlite_master 
        WHERE type IN ('table','view')
        AND name NOT LIKE 'sqlite_%'
        ORDER BY 1;''')
    result = []
    for line in output:
        result.append(tuple(line))
    return result


def init_db():
    con = get_db()
    cur = con.cursor()
    try:
        # if this is an empty database with no table, create the table
        cur.execute('''CREATE TABLE todo
                    (id integer primary key, item text, status text)
                    ''')
        current_app.logger.info("Adding table to database")
    except sqlite3.OperationalError:
        # if the table already exists in the database, do nothing
        current_app.logger.debug("Database table already created")
 

def use_db_wrapper(f):
    def wrapped(*args, **kwargs):
        get_db()
        output = f(*args, **kwargs)
        close_db()
        return output
    return wrapped


@use_db_wrapper
def create(item: str, status: str) -> int:
    assert type(item) == str
    assert type(status) == str
    g.cursor.execute(
        '''INSERT INTO todo(item, status) VALUES (?, ?)''',
        (item, status)
    )
    return g.cursor.lastrowid


@use_db_wrapper
def read(id: int) -> Union[sqlite3.Row, None]:
    output = g.cursor.execute("SELECT * FROM todo where id=:id", {"id": id})
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
def read_all() -> List[sqlite3.Row]:
    rows = []
    for row in g.cursor.execute('SELECT * FROM todo ORDER BY id'):
        rows.append(row)
    return rows


@use_db_wrapper
def update(id: int, item: Union[str, None], status: Union[str, None]):
    assert (type(item) == str) or (item is None)
    assert (type(status) == str) or (status is None)
    if item is not None:
        g.cursor.execute(
            '''UPDATE todo SET item=:item WHERE id=:id''',
            {"id": id, "item": item}
        )
    if status is not None:
        g.cursor.execute(
            '''UPDATE todo SET status=:status WHERE id=:id''',
            {"id": id, "status": status}
        )


@use_db_wrapper
def delete(id: int):
    g.cursor.execute(
        '''DELETE FROM todo WHERE id=:id''',
        {"id": id},
    )
