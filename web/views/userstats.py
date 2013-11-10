from flask import render_template
from web.auth import loginrequired

@loginrequired
def ustats():
    return render_template("userstats.html", thispage='userstats')
