from flask import render_template
from db import conn


def getusers():
    cur = conn.cursor()
    cur.execute("SELECT username from users")
    users = cur.fetchall()
    return render_template("getusers.html", userl=users, str=str)
