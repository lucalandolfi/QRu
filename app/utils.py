from flask import session, abort
import requests
import functools
import base64

def cineca(username, password):
    api = 'https://uniparthenope.esse3.cineca.it/e3rest/api/login'
    login = (username + ':' + password).encode('utf-8')
    login = base64.b64encode(login)
    auth_header = {'Authorization': 'Basic ' + login.decode("ascii")}
    response = requests.get(api, headers=auth_header)
    return response

def login_required(type):
    if (type == 'user'):
        # a normal user is required, not admin
        def user_required(route):
            @functools.wraps(route)
            def wrapper(*args, **kwargs):
                if (session.get('username') is None
                        or session.get('password') is None
                        or session.get('data') is None):
                    abort(401)
                return route(*args, **kwargs)
            return wrapper
        return user_required
    elif type == 'admin':
        # a user with admin privileges is required
        def admin_required(route):
            @functools.wraps(route)
            def wrapper(*args, **kwargs):
                if (session.get('username') is None
                        or session.get('password') is None
                        or session.get('admin') is None):
                    abort(401)
                return route(*args, **kwargs)
            return wrapper
        return admin_required
    elif type == 'any':
        # a logged user is enough
        def default(route):
            @functools.wraps(route)
            def wrapper(*args, **kwargs):
                if (session.get('username') is None
                        or session.get('password') is None):
                    abort(401)
                return route(*args, **kwargs)
            return wrapper
        return default
