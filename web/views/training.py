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
        addedlines = " ".join(re.findall(r'diff-addedline"><div>[.\n\r]*diffchange-inline">([.\n\r]*?)</span></div>', diff))
        deledlines = " ".join(re.findall(r'diff-deletedline"><div>[.\n\r]*diffchange-inline">([.\n\r]*?)</span></div>', diff))
        print addedlines
        print deledlines
        cur.execute("INSERT INTO training_diffs (added, deled, is_good) VALUES (%s, %s, %s)", (addedlines, deledlines, constructive))
        conn.commit()

    revid = randint(57000000, 58500000)
    c = urlopen("http://en.wikipedia.org/w/api.php?action=query&prop=revisions&format=json&rvdiffto=prev&revids=%s" % revid).read()
    c = json.loads(c)
    if "pages" not in c["query"]:
        return "omg pls exist<br/><a href=\"/train/\">pls refresh</a>"
    pages = c["query"]["pages"]
    diff = pages.values()[0]["revisions"][0]["diff"]["*"]
    comment = pages.values()[0]["revisions"][0]["comment"]
    print comment
    return render_template("train.html", diff=diff, diffid=revid, editsummary=comment)
