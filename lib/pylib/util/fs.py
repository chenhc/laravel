#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   fs.py
Author:     Chen Yanfei
@contact:   fasionchan@gmail.com
@version:   $Id$

Description:

Changelog:

'''

import os


def ensure_dir(path):
    path = os.path.abspath(path)
    cursor = '/'
    for entity in path.split('/')[1:]:
        cursor = os.path.join(cursor, entity)
        if os.path.exists(cursor):
            if not os.path.isdir(cursor):
                return False
        else:
            os.mkdir(cursor)
    return True
