from flask import render_template
from db import conn


def index():
    cur = conn.cursor()
    cur.execute("SELECT username, sum(score) FROM edits GROUP BY username ORDER BY sum(score) DESC LIMIT 10")
    users = cur.fetchall()
    return render_template("index.html", thispage='home', lb=users)
