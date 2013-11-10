from flask import render_template
from web.auth import loginrequired

@loginrequired
def uinfo():
    return render_template("userinfo.html", thispage='userinfo')
