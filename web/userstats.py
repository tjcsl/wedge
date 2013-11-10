# Generic Statistics Thingy
from db import conn


def get_edits(user=None):
    cur = conn.cursor()
    if user is None:
        cur.execute("SELECT score FROM edits")
        edits = cur.fetchall()
    else:
        cur.execute("SELECT score FROM edits WHERE username=(SELECT wp_username from users where uid=%s", [str(uid)])
        edits = len(cur.fetchall())
    cur.close()
    return edits


def get_total_score(user=None):
    edits = get_edits(user)
    return sum([i[0] for i in edits])


def get_avg_score(user=None):
    edits = get_edits(user)
    return sum([i[0] for i in edits])/len(edits)
