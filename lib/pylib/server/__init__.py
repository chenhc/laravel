#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   __init__.py
Author:     Chen Yanfei
@contact:   fasionchan@gmail.com
@version:   $Id$

Description:
    uri2service

    uri2service('schema://uesrname:password@host:port/path1/path2?arg1=value1&arg2=value2')

    uri2service('mysql://test:test@127.0.0.1:3306/test?charset=utf8&use_unicode=False&cursorclass=DictCursor')
    uri2service('redis://127.0.0.1:6379/0')

Changelog:

'''

import urllib

from copy import deepcopy
from urlparse import urlparse, parse_qsl

URI_SERVICE_SUPPORTED = {}

try:
    import MySQLdb
    import MySQLdb.cursors
    URI_SERVICE_SUPPORTED['mysql'] = (
        MySQLdb.connect,
        {
            'host': 'hostname',
            'port': 'port',
            'user': 'username',
            'passwd': 'password',
            'db': 'args',
            'use_unicode': 'kwargs',
            'cursorclass': 'kwargs',
            '__kwargs__': 'kwargs'
        },
        {
            'port': lambda port: port or 3306,
            'db': lambda args: args[0],
            'use_unicode': lambda kwargs: eval(kwargs.get('use_unicode', 'True')),
            'cursorclass': lambda kwargs: eval('MySQLdb.cursors.' + kwargs.get('cursorclass', 'Cursor')),
        },
    )
except:
    pass

try:
    import redis
    URI_SERVICE_SUPPORTED['redis'] = (
        redis.client.StrictRedis,
        {
            'host': 'hostname',
            'port': 'port',
            'db': 'args',
        },
        {
            'port': lambda port: port or 6379,
            'db': lambda args: args[0],
        },
    )
except:
    pass


def uriparse(uri):
    params = urlparse(uri)
    params.peer = '%s:%s' % (params.hostname, params.port) if params.port \
            else params.hostname
    params.args = map(urllib.unquote_plus, params.path.split('/')[1:])
    params.kwargs = dict(parse_qsl(params.query))
    return params


def uri2service(uri, scheme_conf=None, **kwargs):
    params = uriparse(uri)

    scheme = params.scheme
    scheme_conf = scheme_conf or URI_SERVICE_SUPPORTED.get(scheme)
    if not scheme_conf:
        raise Exception('no scheme conf')

    cls, mapping, converts = scheme_conf
    mapping = deepcopy(mapping)
    converts = deepcopy(converts)
    all_kwargs = getattr(params, mapping.pop('__kwargs__', '__nosuch__'), {})
    for dst, src in mapping.iteritems():
        value = getattr(params, src, None)
        convert = converts.get(dst)
        all_kwargs[dst] = convert(value) if convert else value
    all_kwargs.update(kwargs)

    return cls(**all_kwargs)
