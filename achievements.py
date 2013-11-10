from db import conn
import json


def first_edit(wpusername):
    __display__ = "Your First Edit"
    query = "SELECT score FROM edits WHERE username=%s"
    cur = conn.cursor()
    cur.execute(query, [wpusername])
    meetsreqs = (len(cur.fetchall()) == 1)
    cur.close()
    return meetsreqs

def onehundred_points(wpusername):
    __display__ = "One Hundred Points"
    cur.execute("SELECT sum(score) FROM edits WHERE username=%s", (wpusername,))
    row = cur.fetchone()
    cur.execute("WITH SELECT uid AS uid FROM users WHERE wp_username=%s\
            SELECT 1 FROM achievements WHERE uid=uid AND name=%s", (wpusername, __display__))
    return row[0] > 100 && cur.fetchone() is None

def always(wpusername):
    __display__ = "Free Achievement"
    return True


ACH_FUNCS = {
    first_edit: 'Your First Edit',
    onehundred_points: 'One Hundred Points'
}

def check_all_achievements(wpusername):
    for i in ACH_FUNCS:
        check(i, wpusername)


def check(f, wpusername):
    result = f(wpusername)
    if result:
        name = ACH_FUNCS[f]
        query = "INSERT INTO achievements (uid, name) VALUES ((SELECT uid FROM users WHERE wp_username=%s), %s)"
        cur = conn.cursor()
        cur.execute(query, (wpusername, name))
        conn.commit()
