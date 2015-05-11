#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   fibonacci.py
Author:     Chen Yanfei
@contact:   fasionchan@gmail.com
@version:   $Id$

Description:

Changelog:

'''

import sys


def fibonacci(n):
    a, b = 1, 0
    for x in xrange(n):
        a, b = b, a + b
    return b

if __name__ == '__main__':
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        n = int(line.strip())
        print fibonacci(n)
