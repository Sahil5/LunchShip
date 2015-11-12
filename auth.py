# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from functools import wraps
from flask import request, Response, session

import contextlib
import os
import ldap
import secrets


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


def authenticate():
    return Response(
        status=401,
        headers={'WWW-Authenticate': 'Basic realm="Login Required"'},
    )


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        session['username'] = auth.username
        return f(*args, **kwargs)
    return decorated


__all__ = ['requires_auth']
