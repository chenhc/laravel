#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   __init__.py
Author:     Chen Yanfei
@contact:   fasionchan@gmail.com
@version:   $Id$

Description:

Changelog:

'''

import urllib
import MySQLdb

from urlparse import urlparse, parse_qsl

URI_SERVICE_SUPPORTED = {
    'mysql': (
        MySQLdb.connect,
        {
            'host': 'hostname',
            'port': 'port',
            'user': 'username',
            'passwd': 'password',
            'db': 'args',
            'use_unicode': 'kwargs',
            '__kwargs__': 'kwargs'
        },
        {
            'port': lambda port: port or 3306,
            'db': lambda args: args[0],
            'use_unicode': lambda kwargs: eval(kwargs.get('use_unicode', 'True')),
        },
    ),
    'mongo': (

    ),
    'amqp': (
        
    ),
    'rabbitmq': (

    ),
}


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
    kwargs.update(getattr(params, mapping.pop('__kwargs__', '__nosuch__'), {}))
    for dst, src in mapping.iteritems():
        value = getattr(params, src, None)
        convert = converts.get(dst)
        kwargs[dst] = convert(value) if convert else value

    print kwargs
    return cls(**kwargs)
