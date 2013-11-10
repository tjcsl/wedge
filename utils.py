from score import score_funcs
from db import conn
from urllib2 import urlopen
import json
import lxml.html
curr = conn.cursor()


def process_diff(diffiduser):
    try:
        diffid, user = diffiduser
    except:
        return
    diff = get_diff_for_diffid(diffid)
    zum = 0
    for f in score_funcs:
        zum += f(diff)
    print zum, diffid


def get_diff_for_diffid(diffid):
    rev = urlopen("http://en.wikipedia.org/w/api.php?action=query&prop=revisions&format=json&rvdiffto=prev&revids=%s" % diffid).read()
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
    return addedstring, deledstring


def get_is_spam_score(diff):
    return 0


def is_spam(diff):
    return get_is_spam_score(diff) > 0.6
