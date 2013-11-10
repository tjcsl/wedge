from flask import render_template, session, request, flash
from web.auth import loginrequired
from db import conn
import hashlib
curr = conn.cursor()

@loginrequired
def uinfo():
    if request.method == "POST":
        form = request.form
        username = session["username"]
        if "email" in form:
            curr.execute("UPDATE users SET email=%s WHERE username=%s", [form["email"],username])
        else:
            if not "newpassword" in form or not "oldpassword" in form or not "password2" in form:
                flash("Please fill in all three entries to change your password", "danger")
                return render_template("userinfo.html", thispage='userinfo', username=session["username"])
            if form["newpassword"] != form["password2"]:
                flash("Your new and confirmation passwords do not match", "danger")
                return render_template("userinfo.html", thispage='userinfo', username=session["username"])
            curr.execute("SELECT * FROM users WHERE username=%s AND passwd_hash=%s", [username, hashlib.sha256(form["oldpassword"]).hexdigest()])
            if not curr.fetchone():
                flash("Your old password is incorrect", "danger")
                return render_template("userinfo.html", thispage='userinfo', username=session["username"])
            curr.execute("UPDATE users SET passwd_hash=%s WHERE username=%s", [hashlib.sha256(form["newpassword"]).hexdigest(), username])
        conn.commit()
    username = session["username"]
    curr.execute("SELECT * FROM users WHERE username=%s", [username])
    u = curr.fetchone()
    wp_username = u[2]
    email = u[4]
    return render_template("userinfo.html", thispage='userinfo', username=session["username"], wp_username=wp_username, email=email)
