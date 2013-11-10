from flask import render_template, session, request, flash, redirect
from web.auth import loginrequired
from db import conn


def leaderboard():
    cur = conn.cursor()
    cur.execute("SELECT username, sum(score) FROM edits GROUP BY username ORDER BY sum(score) DESC LIMIT 25")
    users = cur.fetchall()
    return render_template("leaderboard.html",
                           thispage='leaderboard',
                           users=users)
