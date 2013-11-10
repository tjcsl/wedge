#does nothing lol
import imp
import importlib
import glob
import os
import os.path
import sys

achievement_checks = []

for f in glob.glob(os.path.dirname(__file__) + "/*.py"):
    mod = os.path.basename(f).split('.')[0]
    mod_name = "achievements." + mod
    if mod_name in sys.modules:
        imp.reload(sys.modules[mod_name])
    else:
        importlib.import_module(mod_name)


class Achievement:
    def __init__(self, check_func, name, icon_url):
        self.check_func = check_func
        self.icon_url = icon_url
        self.name = name
        achievement_checks.append(self)

    def try_award(self, curr, user):
        if self.check_func(curr, user):
            curr.execute("INSERT INTO achievments (username, name) VALUES (%(u)S, %(a)s)",
                    {"u": user, "a":self.name})

def check_all_achievements(curr, user):
    for a in achievement_checks:
        a.try_award(curr, user)
