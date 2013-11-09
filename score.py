#list of registered score affecting-functions

score_funcs = []

def test_score_func(diff):
    return 9000
score_funcs.append(test_score_func)

def test_score_func2(diff):
    return len(diff)
score_funcs.append(test_score_func2)
