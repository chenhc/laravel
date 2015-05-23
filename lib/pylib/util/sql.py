#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   sql.py
Author:     Chen Yanfei
@contact:   fasionchan@gmail.com
@version:   $Id$

Description:

Changelog:

'''


def format_table_clause(table):
    return '`%s`' % (table.replace('\\', '\\\\').replace('`', '\\`'),)


def format_field_clause(fields):
    return ', '.join([
        '`%s`' % (field.replace('\\', '\\\\').replace('`', '\\`'),)
        for field in fields
    ])


def format_value_clause(values):
    return ', '.join([
        'NULL' if value is None else \
            '"%s"' % (value.replace('\\', '\\\\').replace('"', '\\"'),)
        for value in values
    ])
