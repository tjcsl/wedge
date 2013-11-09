import web
from web.views import *


def add_view(url, function):
    web.app.add_url_rule(
        url,
        view_func=function,
        methods=["GET", "POST"]
        )


def add_views(views):
    for i in views:
        add_view(i, views[i])


add_views({
    '/': core.index,
    '/train/': training.train 
    '/login/': auth.login,
    '/logout/': auth.logout,
    '/register/': auth.register
})
