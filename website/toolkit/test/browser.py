#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   browser.py
Author:     Chen Yanfei
@contact:   fasionchan@gmail.com
@version:   $Id$

Description:

Changelog:

'''

import urllib
import urlparse
import requests


class Browser(object):

    def __init__(self, host=None, domain=None):
        self.host = host
        self.domain = domain

        self.token = None
        self.cookies = {}

        for method in ('get', 'post', 'put', 'delete'):
            setattr(self, method, self.catch_token(getattr(requests, method)))

    def catch_token(self, func):
        def method(url, *args, **kwargs):
            # 取出自定义HTTP头
            headers = kwargs.setdefault('headers', {})

            # 带上Token头
            if self.token:
                headers['X-XSRF-TOKEN'] = self.token

            # 带上Host头
            if self.domain:
                headers['Host'] = self.domain

            # 修改请求主机地址
            if self.host:
                url = urlparse.urlparse(url)._replace(netloc=self.host).geturl()

            cookies = dict(self.cookies)
            cookies.update(kwargs.get('cookies', {}))
            kwargs['cookies'] = cookies

            # 发起请求
            res = func(url, *args, **kwargs)

            # 记录cookie
            for name, value in res.cookies.iteritems():
                self.cookies[name] = urllib.unquote(value)

            # 记录Token
            token = self.cookies.pop('XSRF-TOKEN', None)
            if token:
                self.token = urllib.unquote(token)


            return res

        return method
