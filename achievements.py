from db import conn
import json


#Format "Name":"Desc"
achievement_metadata = {}

def first_edit(wpusername):
    first_edit.name = "Your First Edit"
    achievement_metadata[first_edit.name] = "Awarded for your first edit after signing up for wedge"
    query = "SELECT score FROM edits WHERE username=%s"
    cur = conn.cursor()
    cur.execute(query, [wpusername])
    meetsreqs = (len(cur.fetchall()) == 1)
    cur.close()
    return meetsreqs

def gen_point_achievement(score, name, desc):
    achievement_metadata[name] = desc
    def ach(wpusername):
        ach.name = name
        cur = conn.cursor()
        cur.execute("SELECT sum(score) FROM edits WHERE username=%s", (wpusername,))
        row = cur.fetchone()
        cur.execute("SELECT 1 FROM achievements WHERE \
                uid=(SELECT uid FROM users WHERE wp_username=%s) AND name=%s", (wpusername, ach.name))
        return row[0] > score and cur.fetchone() is None
    return ach


ACH_FUNCS = [
        first_edit,
        gen_point_achievement(10, "Ten Points", "Awarded for getting 10 points"),
        gen_point_achievement(100, "One Hundred Points", "Awarded for acculating 100 points"),
        gen_point_achievement(500, "Five Hundred Points", "Acquired when you have reached the lofty heights of 500 points"),
        gen_point_achievement(1000, "One Thousand Points", "Awarded for stashing away 1,000 points"),
        gen_point_achievement(9001, "Over 9000", "Get OVER 9000 POINTS")]


def check_all_achievements(wpusername):
    for i in ACH_FUNCS:
        check(i, wpusername)


def check(f, wpusername):
    result = f(wpusername)
    if result:
        name = f.name
        query = "INSERT INTO achievements (uid, name) VALUES ((SELECT uid FROM users WHERE wp_username=%s), %s)"
        cur = conn.cursor()
        cur.execute(query, (wpusername, name))
        conn.commit()
