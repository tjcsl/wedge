from flask import jsonify
from db import conn


def getusers():
    cur = conn.cursor()
    cur.execute("SELECT username from users")
    users = [i[0] for i in cur.fetchall()]
    return jsonify(dict(users=users))
