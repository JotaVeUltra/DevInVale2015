# coding: utf-8

from sqlite3 import connect, IntegrityError, OperationalError

from constants import DATABASE


def __create_score_table():
    con = connect(DATABASE)
    try:
        with con:
            con.execute('CREATE TABLE scores (player TEXT, score INTEGER)')
            con.execute('CREATE UNIQUE INDEX scores_player_score_uindex ON scores (player ASC, score DESC)')
    except OperationalError:
        pass
    con.close()


def save_score(player, score):
    __create_score_table()
    values = (player, score)
    con = connect(DATABASE)
    try:
        with con:
            con.execute('INSERT INTO scores VALUES (?, ?)', values)
    except IntegrityError:
        pass
    con.close()


def scores():
    __create_score_table()
    con = connect(DATABASE)
    with con:
        top_scores = con.execute('SELECT * FROM scores ORDER BY score DESC').fetchmany(size=10)
    con.close()
    return top_scores
