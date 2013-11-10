from flask import redirect, flash, request
from db import conn


def verifye():
    if not request.args or not "key" in request.args:
        return redirect("/")
    cur = conn.cursor()
    cur.execute("SELECT reguuid, username, enabled FROM users where reguuid=%s", (request.args["key"],))
    results = cur.fetchall()
    if not results:
        flash("UUID not found in database; if you came here from a registration email, please check that you have entered the URL correctly.", "danger")
        return redirect("/")
    elif results[2] == 1:
        flash("Account already enabled.", "warning")
        return redirect("/")
    cur.execute("UPDATE users SET enabled=%s WHERE reguuid=%s", (True, results[0]))
    conn.commit()
    cur.close()
    flash("%s, your account has been successfully activated. Please log in." % (results[1]), "success")
    return redirect("/login")
