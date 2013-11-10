import utils
score_funcs = []


def sf(f):
    score_funcs.append(f)
    return f


@sf
def length(added, deled):
    # +1 point for every 100 characters modified
    return len(added, deled)*0.01


@sf
def each_edit(added, deled):
    # +1 point for every edit
    return 1


def get_score(added, deled):
    scores = utils.classify(added, deled)
    score = 0
    for i in score_funcs:
        score += i(added, deled)
    return score
