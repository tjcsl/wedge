from flask import render_template, session, request
from web.auth import loginrequired
from db import conn


@loginrequired
def ustats():
    cur = conn.cursor()
    if not request.args or not "username" in request.args:
        cur.execute("SELECT page_title, summary, score FROM edits WHERE username=(SELECT wp_username from users where uid=%s)", [str(session["uid"])])
    else:
        cur.execute("SELECT page_title, summary, score FROM edits WHERE username=(SELECT wp_username from users where username=%s)", [request.args["username"]])
    edit = cur.fetchall()
    edits = [{'page': i[0], 'summary': i[1], 'score': i[2]} for i in edit]
    ssum = sum([i["score"] for i in edits])
    return render_template("userstats.html",
                           thispage='userstats',
                           edits=edits,
                           uname=(session["username"] if not "username" in request.args else request.args["username"]))
