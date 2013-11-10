from flask import request, render_template
from random import randint
from urllib2 import urlopen
import json
from db import conn
import re
import lxml.html
cur = conn.cursor()

def train(revid=None):
    if request.method=="POST":
        form = request.form
        constructive = form["constructive"]
        revid = form["diffid"]
        rev = urlopen("http://en.wikipedia.org/w/api.php?action=query&prop=revisions&format=json&rvdiffto=prev&revids=%s" % revid).read()
        rev = json.loads(rev)
        pages = rev["query"]["pages"]
        diff = pages.values()[0]["revisions"][0]["diff"]["*"]
        diff = lxml.html.document_fromstring(diff)
        addedlines = diff.xpath("//td[@class='diff-addedline']")
        deledlines = diff.xpath("//td[@class='diff-deletedline']")
        addedstring = ""
        deledstring = ""
        for i in addedlines:
            diffchanges = i.xpath("./span[@class='diffchange diffchange-inline']/text()")
            if not diffchanges:
                addedstring = addedstring + " " + i.text_content()
            else:
                addedstring = addedstring + " " + " ".join(diffchanges)
        for i in deledlines:
            diffchanges = i.xpath("./span[@class='diffchange diffchange-inline']/text()")
            if not diffchanges:
                deledstring = deledstring + " " + i.text_content()
            else:
                deledstring = deledstring + " " + " ".join(diffchanges)
        print addedstring
        print deledstring
        cur.execute("INSERT INTO training_diffs (added, deled, is_good) VALUES (%s, %s, %s)", (addedstring, deledstring, constructive))
        conn.commit()

    if not revid:
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
