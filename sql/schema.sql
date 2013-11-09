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
    spam integer,
    good integer
);

DROP TABLE IF EXISTS classifier_cache;
CREATE TABLE classifier_cache (
    wid serial unique,
    word varchar(128),
    p_spam number,
    p_good number,
);