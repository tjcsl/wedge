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


