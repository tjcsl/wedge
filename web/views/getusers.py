from flask import jsonify, url_for
from db import conn


def getusers():
    cur = conn.cursor()
    cur.execute("SELECT username from users")
    users = [i[0] for i in cur.fetchall()]
    userdict = [{'title': i, 'url': url_for('ustats') + '?username=' + i, 'text': i} for i in users]
    return jsonify(dict(results=userdict))
