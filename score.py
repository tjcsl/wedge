score_funcs = []


def sf(f):
    score_funcs.append(f)
    return f


@sf
def test_score_func(diff):
    return 9000


@sf
def test_score_func2(diff):
    return len(diff)
