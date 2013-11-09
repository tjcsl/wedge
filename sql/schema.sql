CREATE TABLE users (
    uid serial,
    username varchar(512),
    wp_username varchar(512),
    passwd_hash varchar(128),
    score number
);

CREATE TABLE training_words (
    wid serial,
    word varchar(128),
    spam integer,
    good integer
);


