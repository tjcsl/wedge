from flask import render_template


def ustats():
    return render_template("userstats.html", thispage='userstats')
