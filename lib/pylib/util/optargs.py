#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   optargs.py
Author:     Chen Yanfei
@contact:   fasionchan@gmail.com
@version:   $Id$

Description:

Changelog:

'''

import os

from optparse import OptionValueError


def opt_ensure_file(option, opt_str, value, parser):
    if not value:
        raise OptionValueError('%s not specified' % (opt_str,))

    if not os.path.exists(value):
        raise OptionValueError('file %s not exists' % (value,))

    if not os.path.isfile(value):
        raise OptionValueError('%s not file' % (value,))

    setattr(parser.values, option.dest, value)
