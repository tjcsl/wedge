from flask import request, render_template
from random import randint
from urllib2 import urlopen
from db import conn
import re
import json
from utils import get_diff_for_diffid
cur = conn.cursor()

def train(revid2=None):
    if request.method=="POST":
        form = request.form
        constructive = form["constructive"]
        revid = form["diffid"]
        addedstring, delstring = get_diff_for_diffid(revid)
        cur.execute("INSERT INTO training_diffs (added, deled, is_good) VALUES (%s, %s, %s)", (addedstring, deledstring, constructive))
        conn.commit()

    if not revid2:
        revid2 = randint(57000000, 58500000)
    c = urlopen("http://en.wikipedia.org/w/api.php?action=query&prop=revisions&format=json&rvdiffto=prev&revids=%s" % revid2).read()
    c = json.loads(c)
    if "pages" not in c["query"]:
        return "omg pls exist<br/><a href=\"/train/\">pls refresh</a>"
    pages = c["query"]["pages"]
    diff = pages.values()[0]["revisions"][0]["diff"]["*"]
    comment = pages.values()[0]["revisions"][0]["comment"]
    print comment
    return render_template("train.html", diff=diff, diffid=revid2, editsummary=comment)
