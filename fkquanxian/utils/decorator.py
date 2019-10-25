from functools import wraps

from flask import session, redirect


def is_login(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if session.get('user'):
            return func(*args, **kwargs)
        else:
            return redirect('/user/login')

    return inner