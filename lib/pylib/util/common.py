#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   common.py
Author:     Chen Yanfei
@contact:   fasionchan@gmail.com
@version:   $Id$

Description:

Changelog:

'''

def encoded_dict(data, encoding='utf8', key_enable=True):
    return {
        (k.encode(encoding) if key_enable and isinstance(k, unicode) else k):
            (v.encode(encoding) if isinstance(v, unicode) else v)
        for k, v in data.iteritems()
    }
