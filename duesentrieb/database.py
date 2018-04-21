import sqlite3
from random import randint
from typing import List

from duesentrieb.constants import DB_NAME


class Element:
    def __init__(self, table_name, id):
        show_table(table_name)
        with sqlite3.connect(DB_NAME) as con:
            c = 'SELECT type, description, back, fronts, intents FROM {table} WHERE id={id};'.format(
                table=table_name, id=id
            )
            res = con.execute(c)
            for row in res:
                # there should be only one row

                self.type = row[0]
                self.description = row[1]
                self.back = None if (row[2] == "None" or row[2] is None) else int(row[2])  # type: List[int]
                self.fronts = [] if (row[3] == "None" or row[3] is None) else [int(i) for i in row[3].split(",")]  # type: List[int]
                self.intents = [] if (row[4] == "None" or row[4] is None) else row[4].split(",")  # type: List[str]


def setup_database(table_name):
    """
    Create the `user_string` table in the database
    on server startup
    """
    with sqlite3.connect(DB_NAME) as con:
        con.execute("CREATE TABLE IF NOT EXISTS {table} "
                    "(id VARCHAR, type INT, description, TEXT, back INT, fronts VARCHAR, intents VARCHAR);".format(table=table_name))


def insert_element(table_name, description, back, id=None, type="statement", fronts=None, intents=None):
    if id is None:
        id = randint(1, 100000)
    with sqlite3.connect(DB_NAME) as con:
        c = "INSERT INTO {table} (id, description, back, type, fronts, intents) VALUES ({id}, '{desc}', '{back}', '{type}', '{fronts}', '{intents}');".format(
            table=table_name, id=id, desc=description, back=back, type=type, fronts=fronts, intents=intents
        )
        print(c)
        con.execute(c)


def update_element(table_name, description, back, id, type="statement", fronts=None, intents=None):
    with sqlite3.connect(DB_NAME) as con:
        c = "UPDATE {table} (id, description, back, type, fronts, intents) VALUES ({id}, '{desc}', '{back}', '{type}', '{fronts}', '{intents}');".format(
            table=table_name, id=id, desc=description, back=back, type=type, fronts=fronts, intents=intents
        )
        print(c)
        con.execute(c)



def show_table(table_name):
    with sqlite3.connect(DB_NAME) as con:
        c = "SELECT * FROM {table};".format(table=table_name)
        print(c)
        res = con.execute(c)
        for row in res:
            print(row)


def cleanup_database(table_name):
    """
    Destroy the `user_string` table from the database
    on server shutdown.
    """
    with sqlite3.connect(DB_NAME) as con:
        con.execute("DROP TABLE ?", [table_name])
