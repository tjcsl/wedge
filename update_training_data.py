from db import conn
curr = conn.cursor()

def get_word_status(word):
    """ Returns word data in format [a_spam, d_spam, a_good, d_good] """
    curr.execute("SELECT add_spam, add_good, del_spam, del_good FROM training_words WHERE word = :word", (word,))
    row = curr.fetchone()
    return [row[0], row[1], row[2], row[3]]

def compile_training_data():
    curr.execute("SELECT added, deled is_good FROM training_diffs")
    #format {"word": [a_spam, d_spam, a_good, d_good]}
    words = {}
    for row in curr.fetchall():
        added = words[0]
        deled = words[1]
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
    for word in words:
        curr.execute("INSERT INTO training_words (word, add_spam, add_good, del_spam, del_good) \
                VALUES (:word, :aspam, :agood, :dspam, :dgood) WHERE word = :word
                ON DUPLICATE KEY UPDATE add_spam=:aspam, del_spam=:dspam, add_good=:agood, del_good=:dgood",
                {"word":word, "aspam": words[0], "dspam":words[1], "agood":words[2], "dgood":words[3]})


    curr.execute("SELECT sum(add_spam) + sum(add_good) + sum(del_spam) + sum(del_good) FROM training_words LIMIT 1")

    zum = curr.fetchone()
    zum = zum[0]

    curr.execute("SELECT word, add_spam, add_good, del_spam, del_good FROM training_words")
    for row in curr.fetchall():
        curr.execute("INSERT (word, p_add_spam, p_add_good, p_del_spam, p_del_good) INTO classifier_cache VALUES \
                (:word, :aspam/:sum, :agood/:sum, :dspam/:sum, :dgood/:sum)",
                {"word" : row[0], "aspam":row[1], "agood":row[2], "dspam":row[3], "dgood":row[4]})
    conn.commit()

def get_diff_for_diffid(diffid):
    return "This is a test diff"

if __name__ == "__main__": compile_training_data()
