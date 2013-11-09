import hashlib
import web
from db import conn
from flask import session


def is_valid_login(username, password):
    """
    Checks if a given username/password combination exists. If it does,
    returns a two-tuple (username, user id). If it's not, return False.
    """
    cur = conn.cursor()
    passwd_hash = hashlib.sha256(password).hexdigest()
    cur.execute("SELECT uid FROM users where username=%s and passwd_hash=%s",
                (username, passwd_hash))
    matching = cur.fetchone()
    cur.close()
    if matching is not None:
        return (username, matching[0])
    return False


def create_account(username, password):
    """
    Create an account given a username/password combination.
    """
    cur = conn.cursor()
    cur.execute("SELECT username FROM users")
    usernames = [matching[0] for matching in cur.fetchall()]
    if username in usernames or len(username) < 4:
        return False
    passwd_hash = hashlib.sha256(password).hexdigest()
    cur.execute("INSERT INTO users (username, passwd_hash) VALUES (%s,%s)",
                (username, passwd_hash))
    conn.commit()
    cur.close()
    return True
