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
    cur = conn.cursor()
    cur.execute("SELECT wp_username FROM users")
    rusers = [r[0] for r in cur.fetchall()]
    cur.close()
    if user not in rusers:
        return
    diff = get_diff_for_diffid(diffid)
    zum = 0
    for f in score_funcs:
        zum += f(diff[0], diff[1])
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


def is_blacklisted(word):
    return not re.match("[\w]+", word) and word in ['is', 'in', 'the', 'for', 'was', 'and', 'of', 'to', 'a', 'he', 'it', 'if']


def clean_word(word):
    for i in string.punctuation:
        word = word.replace(i, "")
    return word.lower()

def classify(added, deled):
    """ Returns tuple of (good, bad) """
    added_words = added.split()
    added_words = [clean_word(w) for w in added_words]
    deled_words = deled.split()
    deled_words = [clean_word(w) for w in deled_words]

    pspam = 0
    pgood = 0
    for w in added_words:
        if is_blacklisted(w):
            continue
        curr.execute("SELECT p_add_spam, p_add_good WHERE word = %(word)s", {"word":w})
        row = curr.fetchone()
        pspam += curr[0]
        pgood += curr[1]
    for w in added_words:
        if is_blacklisted(w):
            continue
        curr.execute("SELECT p_del_spam, p_del_good WHERE word = %(word)s", {"word":w})
        row = curr.fetchone()
        pspam += curr[0]

    pgood /= len(added_words) + len(deled_words)
    pspam /= len(added_words) + len(deled_words)
    return (pgood, pspam)


def is_spam(diff):
    return get_is_spam_score(diff) > 0.6
