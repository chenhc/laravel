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


def encoded_jsonic_object(data, encoding='utf8', key_enable=True):
    if isinstance(data, dict):
        return {
            encoded_jsonic_object(k, encoding=encoding, key_enable=key_enable):
                encoded_jsonic_object(v, encoding=encoding, key_enable=key_enable)
            for k, v in data.iteritems()
            }
    elif isinstance(data, list):
        return [
            encoded_jsonic_object(i, encoding=encoding, key_enable=key_enable)
            for i in data
            ]
    elif isinstance(data, tuple):
        return tuple([
            encoded_jsonic_object(i, encoding=encoding, key_enable=key_enable)
            for i in data
            ])
    elif isinstance(data, unicode):
        return data.encode(encoding)
    else:
        return data
