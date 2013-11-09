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

def compile_training_data():
    curr.execute("SELECT sum(spam) + sum(good) FROM training_words")

    zum = curr.fetchone()
    zum = zum[0]

    curr.execute("SELECT word, spam, good FROM training_words")
    for row in curr.fetchall():
        curr.execute("INSERT (word, p_spam, p_good) INTO classifier_cache VALUES \
                (:word, :spam/:sum, :good/:sum)",
                {"word" : row[0], "spam":row[1], "good":row[2]})
    conn.commit()

def get_diff_for_diffid(diffid):
    return "This is a test diff"
