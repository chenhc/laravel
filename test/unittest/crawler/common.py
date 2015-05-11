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

import os, sys
crawler_root = os.path.abspath(os.path.join(__file__, '../../../../crawler'))
print crawler_root
sys.path.insert(0, crawler_root)
