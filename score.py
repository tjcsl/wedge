import utils
score_funcs = []


def sf(f):
    score_funcs.append(f)
    return f


@sf
def length(diff):
    # +1 point for every 100 characters modified
    return len(diff)*0.01


@sf
def each_edit(diff):
    # +1 point for every edit
    return 1


def get_score(diff):
    if utils.get_is_spam_score(diff)
    score = 0
    for i in score_funcs:
        score += i(diff)
    return score
