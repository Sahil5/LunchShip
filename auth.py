# -*- coding: utf-8 -*-
import app
from functools import wraps
from flask import flash, request, Response, session
from flask import render_template
from flask.ext.login import LoginManager, UserMixin, current_user, login_user, logout_user

import contextlib
import os
import ldap
import secrets
from functools import wraps

from helpers.forms import LoginForm

os.environ['LDAPTLS_REQCERT'] = secrets.LDAPTLS_REQCERT
os.environ['LDAPTLS_CACERT'] = secrets.LDAPTLS_CACERT


@contextlib.contextmanager
def ldap_connection(url):
    conn = ldap.initialize(url)
    conn.set_option(ldap.OPT_NETWORK_TIMEOUT, 3)
    conn.set_option(ldap.OPT_REFERRALS, 0)
    conn.set_option(ldap.OPT_PROTOCOL_VERSION, ldap.VERSION3)
    try:
        conn.start_tls_s()
        yield conn
    finally:
        conn.unbind_s()


def check_auth(username, password):
    """Attempts to bind a given username/password pair in LDAP
    and returns whether or not it succeeded.
    """
    dn = secrets.DN_STRING.format(username)
    with ldap_connection(secrets.LDAP_URL) as conn:
        try:
            conn.simple_bind_s(dn, password)
            conn.search_s(secrets.BASE_DN, ldap.SCOPE_ONELEVEL)
        except ldap.LDAPError:
            return False
    return True


class User(UserMixin):
    def __init__(self, username):
        self.id = username


# Flask-Login use this to reload the user object from the user ID stored in the session
@app.login_manager.user_loader
def load_user(username):
    return User(username)


def requires_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return show_login()
        return f(*args, **kwargs)
    return decorated_function


def require_login():
    if not current_user.is_authenticated:
        return show_login()


def show_login():
    login_form = LoginForm(request.form)
    flash('Please login')
    return render_template(
        "login.html",
        login_form=login_form
    )
