import hashlib
from db import conn
from flask import session, flash, redirect, url_for
from functools import wraps


def loginrequired(f):
    @wraps(f)
    def wrappedf(*args, **kwargs):
        if 'uid' in session:
            return f()
        flash("You need to be logged in to access this page.", "danger")
        return redirect(url_for("login"))
    return wrappedf


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


def create_account(username, password, email):
    """
    Create an account given a username/password combination.
    """
    cur = conn.cursor()
    cur.execute("SELECT username FROM users")
    usernames = [matching[0] for matching in cur.fetchall()]
    if username in usernames or len(username) < 4:
        return False
    passwd_hash = hashlib.sha256(password).hexdigest()
    cur.execute("INSERT INTO users (username, passwd_hash, email) VALUES (%s,%s, %s)",
                (username, passwd_hash, email))
    conn.commit()
    cur.close()
    return True
