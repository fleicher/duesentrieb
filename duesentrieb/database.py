import sqlite3
from random import randint
from typing import List

from duesentrieb.constants import DB_NAME


class Element:
    def __init__(self, topic, id, rank=0):
        # type: (str, int, int) -> None

        with sqlite3.connect(DB_NAME) as con:
            c = "SELECT type, fronts, intents FROM structure WHERE id='{id}' AND topic='{topic}';".format(
                topic=topic, id=id
            )
            row = con.execute(c).fetchone()
            # there should be only one row
            self.type = row[0]
            self.fronts = [] if (row[1] == "None" or row[1] is None) else [
                int(i) for i in row[1].split(",")]  # type: List[int]
            self.intents = [] if (row[2] == "None" or row[2] is None) else row[2].split(",")  # type: List[str]

            c = "SELECT description, rank, name FROM content WHERE id='{id}' AND topic='{topic}' ORDER BY rank;".format(
                topic=topic, id=id
            )
            res = list(con.execute(c).fetchall())

            rank %= len(res)
            row = res[rank]
            self.description = row[0]
            self.rank = row[1]
            self.name = int(row[2])

    def addRang(self, val):
        with sqlite3.connect(DB_NAME) as con:
            self.rank += val
            c = "UPDATE content (rank) VALUES ('{rank}');".format(
                rank=self.rank
            )
            con.execute(c)

# DataBase Formats
# structure (topic, id, type, fronts, intents)
# content (topic, message, id, rank)


def setup_database():
    with sqlite3.connect(DB_NAME) as con:
        con.execute("CREATE TABLE IF NOT EXISTS structure "
                    "(topic VARCHAR, id INT, type VARCHAR, fronts VARCHAR, intents VARCHAR);")
        con.execute("CREATE TABLE IF NOT EXISTS content "
                    "(topic VARCHAR, id INT, name INT, description TEXT, rank FLOAT);")


def insert_element(topic, description, id=None, type="statement", fronts=None, intents=None, add_structure=True):
    if id is None:
        id = randint(1, 1000000)
    name = randint(1, 1000000)

    with sqlite3.connect(DB_NAME) as con:
        # c = "SELECT EXISTS(SELECT * FROM structure WHERE topic='{topic}' AND id='{id}');"
        if add_structure:  # not con.execute(c).fetchone()[0]:
            c = "INSERT INTO structure (topic, id, type, fronts, intents) VALUES ('{topic}', '{id}', '{type}', " \
                "'{fronts}', '{intents}');".format(
                topic=topic, id=id, desc=description, type=type, fronts=fronts, intents=intents
            )
            con.execute(c)

        c = "INSERT INTO content (topic, id, name, description, rank) VALUES ('{topic}', '{id}', '{name}', '{desc}', '{rank}');".format(
            topic=topic, id=id, desc=description, rank=0.0, name=name
        )
        con.execute(c)


# def update_element(table_name, description, back, id, type="statement", fronts=None, intents=None):
#     with sqlite3.connect(DB_NAME) as con:
#         c = "UPDATE {table} (id, description, back, type, fronts, intents) VALUES ({id}, '{desc}', '{back}', '{type}', '{fronts}', '{intents}');".format(
#             table=table_name, id=id, desc=description, back=back, type=type, fronts=fronts, intents=intents
#         )
#         con.execute(c)


def show_table(table_name):
    with sqlite3.connect(DB_NAME) as con:
        c = "SELECT * FROM {table};".format(table=table_name)
        res = con.execute(c)
        for row in res:
            print(row)


def remove_table(table_name):
    with sqlite3.connect(DB_NAME) as con:
        con.execute("DROP TABLE {table}".format(table=table_name))


def has_topic(topic_name):
    with sqlite3.connect(DB_NAME) as con:
        res = con.execute("SELECT EXISTS(SELECT * FROM structure WHERE topic='{topic}');".format(topic=topic_name))
        row = res.fetchone()
        return True if row[0] else False