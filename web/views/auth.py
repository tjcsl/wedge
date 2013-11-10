from flask import flash, request, render_template, session, redirect,\
    url_for
import web.auth
from verify_user import verify_user

def login():
    if request.method == "POST":
        response = web.auth.is_valid_login(
                request.form["username"],
                request.form["password"]
                )
        if response:
            session["username"] = response[0]
            session["uid"] = response[1]
            flash("Login success.", "success")
            return redirect(url_for("index"))
        flash("Login failed!", "danger")
    return render_template("auth/login.html")

def register():
    if request.method == "POST":
        if request.form["password"] != request.form["password2"]:
            flash("Error: your passwords didn't match.", "danger")
        elif verify_user(request.form["username"],request.form["wp_username"]):
            if web.auth.create_account(
                request.form["username"],
                request.form["password"],
                request.form["email"],
                request.form["wp_username"].capitalize()
                ):
                flash("Account created. Please login.", "success")
                return render_template("auth/login.html")
            else:
                flash("Account creation failure, please try a different username."
                      , "danger")
        else:
            flash("Your Wikipedia account is not verified. Please follow the instructions located at <a href=\"/verify\">verify</a> to verify your account", "danger")
    return render_template("auth/register.html")

def logout():
    if "username" in session or "uid" in session:
        if "username" in session: session.pop("username")
        if "uid" in session: session.pop("uid")
        flash("Logged out.", "success")
        return redirect(url_for("login"))
    flash("You are already logged out!", "warning")
    return redirect(url_for("logout"))
        
