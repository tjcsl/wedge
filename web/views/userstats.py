from flask import render_template, session, request, flash, redirect
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
    cur.execute("SELECT username FROM users")
    users = cur.fetchall()
    rusers = []
    for i in users:
        rusers.append(str(i)[2:len(str(i)) - 3])
    if "username" in request.args:
        if request.args["username"] not in rusers:
            flash("This user doesn't exist.", "danger")
            return str(rusers)
            #return redirect("/userstats")
        elif len(edits) == 0:
            flash("This user doesn't have any edits.", "warning")
            return redirect("/userstats")
    return render_template("userstats.html",
                           thispage='userstats',
                           edits=edits,
                           uname=(session["username"] if not "username" in request.args else request.args["username"]))
