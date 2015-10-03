# coding=utf-8


from flask import flash
from flask import redirect, url_for
from flask import session
from functools import wraps


__all__ = ['login_required']

def login_required(fn):
    """
    you can view this:
         http://flask.pocoo.org/docs/patterns/viewdecorators/
    """

    @wraps(fn)
    def decorated_view(*args, **kwargs):
        if 'user_id' not in session.keys():
            return redirect(url_for('manage.manage_login'))
        return fn(*args, **kwargs)
    return decorated_view

def after_login(fn):
    """
    you can view this:
         http://flask.pocoo.org/docs/patterns/viewdecorators/
    """

    @wraps(fn)
    def decorated_view(*args, **kwargs):
        if 'user_id' in session.keys():
            return redirect(url_for('admin.index'))
        return fn(*args, **kwargs)
    return decorated_view
