from db import conn

def get_user_achievements(user):
    cur = conn.cursor()
    cur.execute("SELECT uid FROM users WHERE username=%s", (user,))
    uid = str(cur.fetchone()[0])
    cur.execute("SELECT name FROM achievements WHERE uid=%s", (uid,))
    achievements = [i[0] for i in cur.fetchall()]
    return achievements
