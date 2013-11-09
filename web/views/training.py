from flask import request, render_template
from random import randint
from urllib2 import urlopen
import json
from db import conn
import re
cur = conn.cursor()

def train():
    if request.method=="POST":
        form = request.form
        constructive = form["constructive"]
        revid = form["diffid"]
        rev = urlopen("http://en.wikipedia.org/w/api.php?action=query&prop=revisions&format=json&rvdiffto=prev&revids=%s" % revid).read()
        rev = json.loads(rev)
        pages = rev["query"]["pages"]
        diff = pages.values()[0]["revisions"][0]["diff"]["*"]
        addedlines = " ".join(re.findall(r'diff-addedline"><div>(.*)</div>', diff))
        deledlines = " ".join(re.findall(r'diff-deletedline"><div>(.*)</div>', diff))
        print addedlines
        print deledlines
        cur.execute("INSERT INTO training_diffs (added, deled, is_good) VALUES (%s, %s, %s)", (addedlines, deledlines, constructive))
        conn.commit()

    revid = randint(58000000, 58500000)
    c = urlopen("http://en.wikipedia.org/w/api.php?action=query&prop=revisions&format=json&rvdiffto=prev&revids=%s" % revid).read()
    c = json.loads(c)
    pages = c["query"]["pages"]
    diff = pages.values()[0]["revisions"][0]["diff"]["*"]
    return render_template("train.html", diff=diff, diffid=revid)
