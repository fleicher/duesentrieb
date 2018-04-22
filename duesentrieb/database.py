"""
Access to sqlite database.
"""
# TODO: use prepared statements -> currently only using format (SQL injection possible)

import sqlite3
from random import randint
from typing import List

from duesentrieb.constants import DB_NAME


class InstructionsElement:
    def __init__(self, topic, id_, cur_alternative=0):
        # type: (str, int, int) -> None
        self.topic = topic  # name of instruction topic
        self.id = id_  # id of current node
        with sqlite3.connect(DB_NAME) as con:
            c = "SELECT type, fronts, intents FROM structure WHERE id='{id}' AND topic='{topic}';".format(
                topic=topic, id=id_
            )
            row = con.execute(c).fetchone()  # there should be only one row as id AND topic is a unique identifier
            self.type = row[0]
            self.fronts = [] if (row[1] == "None" or row[1] is None) else [
                int(i) for i in row[1].split(",")]  # type: List[int]
            self.intents = [] if (row[2] == "None" or row[2] is None) else row[2].split(",")  # type: List[str]

            c = "SELECT description, rank, name FROM content WHERE id='{id}' AND topic='{topic}' ORDER BY rank;".format(
                topic=topic, id=id_
            )
            res = list(con.execute(c).fetchall())

            cur_alternative %= len(res)  # determine which alternative is shown (if several of a step exist)
            row = res[cur_alternative]
            self.description = row[0]
            self.rank = row[1]
            self.name = int(row[2])

    def vote_on_element(self, val):
        # type: (int) -> None
        """ update the rank value of a node """
        assert self.name is not None
        with sqlite3.connect(DB_NAME) as con:
            self.rank += val
            c = "UPDATE content SET rank = '{rank}' WHERE name='{name}';".format(
                rank=int(self.rank), name=self.name
            )
            con.execute(c)

###################################################
# DataBase Formats                                #
# structure (topic, id, type, fronts, intents)    #
# content (topic, message, id, rank)              #
###################################################


def setup_database():
    """ create new database, only necessary once at start of project"""
    with sqlite3.connect(DB_NAME) as con:
        con.execute("CREATE TABLE IF NOT EXISTS structure "
                    "(topic VARCHAR, id INT, type VARCHAR, fronts VARCHAR, intents VARCHAR);")
        con.execute("CREATE TABLE IF NOT EXISTS content "
                    "(topic VARCHAR, id INT, name INT, description TEXT, rank FLOAT);")


def insert_element(topic, description, id_=None, type_="statement", fronts=None, intents=None, add_structure=True):
    if id_ is None:
        id_ = randint(1, 1000000)  # unique id  TODO: match against Primary Key of SQL Table
    name = randint(1, 1000000)

    with sqlite3.connect(DB_NAME) as con:
        if add_structure:  # not con.execute(c).fetchone()[0]:
            c = "INSERT INTO structure (topic, id, type, fronts, intents) VALUES ('{topic}', '{id}', '{type}', " \
                "'{fronts}', '{intents}');".format(
                    topic=topic, id=id_, desc=description, type=type_, fronts=fronts, intents=intents
                    )
            con.execute(c)

        c = "INSERT INTO content (topic, id, name, description, rank)" \
            " VALUES ('{topic}', '{id}', '{name}', '{desc}', '{rank}');".format(
                topic=topic, id=id_, desc=description, rank=0.0, name=name
            )
        con.execute(c)


def show_table(table_name):
    # type: (str) -> None
    """ maintenance function"""
    with sqlite3.connect(DB_NAME) as con:
        c = "SELECT * FROM {table};".format(table=table_name)
        res = con.execute(c)
        for row in res:
            print(row)


def remove_table(table_name):
    # type: (str) -> None
    try:
        with sqlite3.connect(DB_NAME) as con:
            con.execute("DROP TABLE {table}".format(table=table_name))
    except sqlite3.OperationalError:
        pass


def has_topic(topic_name):
    # type: (str) -> bool
    """ check if instructions on the topic provided are in the database """
    with sqlite3.connect(DB_NAME) as con:
        res = con.execute("SELECT EXISTS(SELECT * FROM structure WHERE topic='{topic}');".format(topic=topic_name))
        row = res.fetchone()
        return True if row[0] else False
