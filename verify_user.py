from db import conn
from urllib2 import urlopen
from urllib import quote_plus
import hashlib
import json


def verify_user(username, wp_username):
    verifystr = "wedge-verify " + username
    url = "http://en.wikipedia.org/w/api.php?action=query&prop=revisions&format=json&rvprop=content&rvlimit=1&titles=" + quote_plus("User:" + wp_username + "/wedge.js")
    result = urlopen(url).read()
    result = json.loads(result)
    result = result["query"]["pages"].values()[0]
    if "missing" in result:
        return False
    result = result["revisions"][0]["*"]
    if result == verifystr:
        return True
