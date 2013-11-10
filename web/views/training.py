from flask import request, render_template
from random import randint
from urllib2 import urlopen
from db import conn
from web.auth import loginrequired
import re
import json
from utils import get_diff_for_diffid
cur = conn.cursor()

@loginrequired
def train(revid2=None):
    if request.method=="POST":
        form = request.form
        constructive = form["constructive"]
        revid = form["diffid"]
        addedstring, deledstring, title, summary = get_diff_for_diffid(revid)
        cur.execute("INSERT INTO training_diffs (added, deled, is_good) VALUES (%s, %s, %s)", (addedstring, deledstring, constructive))
        conn.commit()

    while not revid2:
        revid2 = randint(45000000, 58500000)
        c = urlopen("http://en.wikipedia.org/w/api.php?action=query&prop=revisions&format=json&rvdiffto=prev&revids=%s" % revid2).read()
        c = json.loads(c)
        if "pages" not in c["query"]:
            revid2 = None
            continue
        pages = c["query"]["pages"]
        diff = pages.values()[0]["revisions"][0]["diff"]["*"]
        comment = pages.values()[0]["revisions"][0]["comment"]
        print comment
        return render_template("train.html", diff=diff, diffid=revid2, editsummary=comment)
