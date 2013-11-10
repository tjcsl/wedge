from web.ach import *
from flask import render_template
from achievements import achievement_metadata

def ach_all():
    return render_template("ach_all.html", ach=achievement_metadata)
