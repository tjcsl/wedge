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


def always(wpusername):
    __display__ = "Free Achievement"
    return True


ACH_FUNCS = {
    first_edit: 'Your First Edit'
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
