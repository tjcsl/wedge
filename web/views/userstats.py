from flask import render_template, session
from web.auth import loginrequired
from db import conn


@loginrequired
def ustats():
    cur = conn.cursor()
    cur.execute("SELECT page_title, summary, score FROM edits WHERE username=(SELECT wp_username from users where uid=%s)", [str(session["uid"])])
    edit = cur.fetchall()
    edits = [{'page': i[0], 'summary': i[1], 'score': i[2]} for i in edit]
    return render_template("userstats.html",
                           thispage='userstats',
                           edits=edits)
