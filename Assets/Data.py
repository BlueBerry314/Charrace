__author__ = '1m2i3_000'

import sqlite3 as lite
import sys

scores = {
    ("290626", 100),
    ("654538", 25),
    ("2050"  ,  125),
    ("186234", 35)
}

con = lite.connect('scores.db')

with con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS charities")
    cur.execute("CREATE TABLE charities(char_id TEXT, amount INT)")
    cur.executemany("INSERT INTO charities VALUES(?,?)",scores)