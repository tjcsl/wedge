from flask import render_template


def uinfo():
    return render_template("userinfo.html", thispage='userinfo')
