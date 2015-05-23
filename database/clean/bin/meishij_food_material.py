#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   meishij_food_material.py
Author:     Chen Yanfei
@contact:   fasionchan@gmail.com
@version:   $Id$

Description:

Changelog:

'''

import os

import common

from pylib.server import uri2service
from pylib.util.optargs import opt_ensure_file
from pylib.util.fs import ensure_dir

from modules.meishij import FoodMaterialCleaner


def parse_args():
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option('-j', '--json-file', dest='json_file', type='string',
            action='callback', callback=opt_ensure_file)
    parser.add_option('-m', '--mysql-uri', dest='mysql_uri', type='string',)
    parser.add_option('-i', '--image_dir', dest='image_dir', type='string')

    options, args =  parser.parse_args()

    json_file = options.json_file
    if not json_file:
        parser.error('-j|--json-file not specified')

    mysql_uri = options.mysql_uri
    if not mysql_uri:
        parser.error('mysql uri not specified')

    image_dir = options.image_dir
    if image_dir:
        if os.path.exists(image_dir):
            if not os.path.isdir(image_dir):
                parser.error('%s is not directory' % (image_dir,))
        else:
            if not ensure_dir(image_dir):
                parser.error('can not create directory %s' % (image_dir,))

    return json_file, mysql_uri, image_dir


def main():
    json_file, mysql_uri, image_dir = parse_args()
    FoodMaterialCleaner(source_file=file(json_file), 
            mysqldb=uri2service(mysql_uri), image_dir=image_dir).process()

if __name__ == '__main__':
    main()
