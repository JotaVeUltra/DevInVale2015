# coding: utf-8

from sqlite3 import *


class DB(object):

    def __init__(self, database):
        self.database = database
        self.__create_score_table()

    def __create_score_table(self):
        with connect(self.database) as con:
            try:
                con.execute('CREATE TABLE scores (player TEXT, score INTEGER)')
            except OperationalError:
                pass
        con.close()

    def save_score(self, player, score):
        values = (player, score, )

        with connect(self.database) as con:
            con.execute("INSERT INTO scores VALUES (?, ?)", values)
        con.close()

    def scores(self):
        with connect(self.database) as con:
            scores = con.execute(
                "SELECT * FROM scores ORDER BY score DESC").fetchmany(size=10)
        con.close()

        return scores
