from web.auth import loginrequired
from web.ach import *
from flask import session, request, render_template


@loginrequired
def ach():
    name = session["username"] if "username" not in request.args else request.args["username"]
    ach = get_user_achievements(name)
    return render_template("ach.html", name=name, ach=ach)
