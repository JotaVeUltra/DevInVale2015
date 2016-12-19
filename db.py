# coding: utf-8

from sqlite3 import connect, OperationalError

from constants import DATABASE


def __create_score_table():
    with connect(DATABASE) as con:
        try:
            con.execute('CREATE TABLE scores (player TEXT, score INTEGER)')
        except OperationalError:
            pass
    con.close()


def save_score(player, score):
    __create_score_table()

    values = (player, score)
    with connect(DATABASE) as con:
        con.execute("INSERT INTO scores VALUES (?, ?)", values)
    con.close()


def scores():
    __create_score_table()

    with connect(DATABASE) as con:
        top_scores = con.execute(
            "SELECT * FROM scores ORDER BY score DESC").fetchmany(size=10)
    con.close()
    return top_scores
