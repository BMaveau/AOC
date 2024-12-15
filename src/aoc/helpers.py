def cache_results(func):
    _cache = {}

    def _exec(*args):
        if args in _cache:
            return _cache[args]
        else:
            res = func(*args)
            _cache[args] = res
            return res

    return _exec
