from score import score_funcs
from db import conn
curr = conn.cursor()


def process_diff(diffiduser):
    try:
        diffid, user = diffiduser
    except:
        return
    diff = get_diff_for_diffid(diffid)
    zum = 0
    for f in score_funcs:
        zum += f(diff)
    print zum, diffid


def get_diff_for_diffid(diffid):
    return "This is a test diff"


def get_is_spam_score(diff):
    return 0


def is_spam(diff):
    return get_is_spam_score(diff) > 0.6
