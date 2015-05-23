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

import socket
import random


def random_ip():
    ip = ''.join([chr(random.randint(0, 255)) for x in xrange(4)])
    return socket.inet_ntoa(ip)
