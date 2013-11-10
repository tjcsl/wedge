import utils
score_funcs = []


def sf(f):
    score_funcs.append(f)
    return f


@sf
def length(added, deled):
    # +1 point for every 1000 characters modified
    return (len(added) + len(deled))*0.001


@sf
def each_edit(added, deled):
    # +1 point for every edit
    return 1


@sf
def links(added, deled):
    return added.count("[[")*0.5


@sf
def templates(added, deled):
    return added.count("{{") * 0.25


@sf
def get_score(added, deled):
    notspam, spam = utils.classify(added, deled)
    return ((notspam * 20) - (spam * 20))
