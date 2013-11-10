import utils
score_funcs = []


def sf(f):
    score_funcs.append(f)
    return f


@sf
def length(added, deled):
    # +1 point for every 100 characters modified
    return (len(added) + len(deled))*0.01


@sf
def each_edit(added, deled):
    # +1 point for every edit
    return 1


def get_score(added, deled):
    notspam, spam = utils.classify(added, deled)
    score = ((notspam * 2) + (spam * 2))
    for i in score_funcs:
        score += i(added, deled)
    return score
