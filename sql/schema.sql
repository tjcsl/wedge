DROP TABLE IF EXISTS users;
CREATE TABLE users (
    uid serial,
    username varchar(512),
    wp_username varchar(512),
    passwd_hash varchar(128),
    score float
);

DROP TABLE IF EXISTS training_words;
CREATE TABLE training_words (
    wid serial unique,
    word varchar(128),
    add_spam integer,
    add_good integer,
    del_spam integer,
    del_good integer
);

DROP TABLE IF EXISTS classifier_cache;
CREATE TABLE classifier_cache (
    wid serial unique,
    word varchar(128),
    p_add_spam number,
    p_add_good number,
    p_del_spam number,
    p_del_good number
);

DROP TABLE IF EXISTS training_diffs;
CREATE TABLE training_diffs {
    did serial unique,
    added text,
    deled text,
    is_good boolean
);
