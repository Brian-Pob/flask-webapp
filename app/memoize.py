memoized_inputs = {}

def memoize(myfunc):
    """
    Memoizes myfunc
    """
    def wrapper(*args, **kw):
        key_tuple = list(kw.items())
        key_tuple = tuple(key_tuple)
        result = memoized_inputs.get(key_tuple, None)
        if result is None:
            result = myfunc(*args, **kw)
            memoized_inputs[key_tuple] = result
        return result
    wrapper.__name__ = myfunc.__name__
    return wrapper
