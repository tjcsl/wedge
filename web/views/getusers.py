from flask import render_template, request
from db import conn
import json

def getusers():
    cur = conn.cursor()
    cur.execute("SELECT username, wp_username FROM users WHERE wp_username LIKE %(search)s\
            or username LIKE %(search)s LIMIT 10 ", {"search":request.form['search'] + "%"})
    unames = []
    for r in cur.fetchall():
        unames.append({"title":r[0], "url":"/userstats/?username=%s" % r[0], "text":r[1]})
    resp = {}
    resp['results'] = unames
    return json.dumps(resp)
