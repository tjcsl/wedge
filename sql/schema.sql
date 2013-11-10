CREATE TABLE IF NOT EXISTS users (
    uid serial,
    username varchar(512),
    wp_username varchar(512),
    passwd_hash varchar(128),
    email varchar(512),
    score float default 0
);

CREATE TABLE IF NOT EXISTS training_words (
    wid serial unique,
    word varchar(128) unique,
    add_spam integer,
    add_good integer,
    del_spam integer,
    del_good integer
);

CREATE TABLE IF NOT EXISTS classifier_cache (
    wid serial unique,
    word varchar(128),
    p_add_spam float,
    p_add_good float,
    p_del_spam float,
    p_del_good float
);

CREATE TABLE IF NOT EXISTS edits (
    id serial unique,
    username varchar(512),
    summary text,
    page_title text,
    added text,
    deled text,
    score float
);

CREATE TABLE IF NOT EXISTS training_diffs (
    did serial unique,
    added text,
    deled text,
    is_good boolean
);

CREATE TABLE IF NOT EXISTS achievements (
    id serial unique,
    username varchar(512),
    name text
);
