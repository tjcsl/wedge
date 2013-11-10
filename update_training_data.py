from db import conn
curr = conn.cursor()

def get_word_status(word):
    """ Returns word data in format [a_spam, d_spam, a_good, d_good] """
    curr.execute("SELECT add_spam, add_good, del_spam, del_good FROM training_words WHERE word = %(word)s", {"word":word})
    row = curr.fetchone()
    if row is None: return [0, 0, 0, 0]
    return [row[0], row[1], row[2], row[3]]

def compile_training_data():
    curr.execute("SELECT added, deled, is_good FROM training_diffs")
    #format {"word": [a_spam, d_spam, a_good, d_good]}
    words = {}
    print "Begin commit begin"
    for row in curr.fetchall():
        added = row[0]
        deled = row[1]
        for word in added.split():
            if word not in words:
                words[word] = get_word_status(word)
            if row[2] == 0:
                words[word][0] += 1
            else:
                words[word][2] += 1
        for word in deled .split():
            if word not in words:
                words[word] = get_word_status(word)
            if row[2] == 0:
                words[word][1] += 1
            else:
                words[word][3] += 1
    print "Begin commit word updates"
    curr.execute("DELETE FROM training_words")
    for word in words:
        word_data = words[word]
        curr.execute("INSERT INTO training_words (word, add_spam, add_good, del_spam, del_good) \
                    VALUES (%(word)s, %(aspam)s, %(agood)s, %(dspam)s, %(dgood)s)", 
                {"word":word, "aspam": word_data[0], "dspam":word_data[1], "agood":word_data[2], "dgood":word_data[3]})
        #curr.execute("INSERT INTO training_words (word, add_spam, add_good, del_spam, del_good) \
        #        VALUES (%(word)s, %(aspam)s, %(agood)s, %(dspam)s, %(dgood)s) WHERE word = %(word)s \
        #        ON DUPLICATE KEY UPDATE add_spam=%(aspam)s, del_spam=%(dspam)s, add_good=%(agood)s, del_good=%(dgood)s",
        #        {"word":word, "aspam": word_data[0], "dspam":word_data[1], "agood":word_data[2], "dgood":word_data[3]})
        conn.commit()

    print "Begin commiting probabilities"
    curr.execute("SELECT sum(add_spam) + sum(add_good) + sum(del_spam) + sum(del_good) FROM training_words LIMIT 1")

    zum = curr.fetchone()
    zum = zum[0]

    curr.execute("SELECT word, add_spam, add_good, del_spam, del_good FROM training_words")
    for row in curr.fetchall():
        curr.execute("INSERT INTO classifier_cache (word, p_add_spam, p_add_good, p_del_spam, p_del_good) VALUES \
                (%(word)s, %(aspam)s/%(sum)s, %(agood)s/%(sum)s, %(dspam)s/%(sum)s, %(dgood)s/%(sum)s)",
                {"word" : row[0], "aspam":row[1], "agood":row[2], "dspam":row[3], "dgood":row[4], "sum":zum})
    conn.commit()
    print "Done"

def get_diff_for_diffid(diffid):
    return "This is a test diff"

if __name__ == "__main__": compile_training_data()
