__author__ = '1m2i3_000'
import sqlite3 as lite
import sys

scores = {
    ("290626", 2500),
    ("654538", 4500),
    ("2050"  ,  500),
    ("186234", 2500)
}

con = lite.connect('scores.db')

with con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS charities")
    cur.execute("CREATE TABLE charities(char_id TEXT, amount INT)")
    cur.executemany("INSERT INTO charities VALUES(?,?)",scores)
