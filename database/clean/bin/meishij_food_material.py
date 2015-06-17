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
    parser.add_option('-M', '--material-file', dest='material_file',
            type='string', action='callback', callback=opt_ensure_file)
    parser.add_option('-c','--category-file', dest='category_file',
            type='string', action='callback', callback=opt_ensure_file)
    parser.add_option('-m', '--mysql-uri', dest='mysql_uri', type='string',)
    parser.add_option('-i', '--image_dir', dest='image_dir', type='string')

    options, args =  parser.parse_args()

    material_file = options.material_file
    if not material_file:
        parser.error('-M|--material-file not specified')

    category_file = options.category_file
    if not category_file:
        parser.error('-c|--category-file not specified')

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

    return material_file, category_file, mysql_uri, image_dir

def main():
    import logging
    logging.basicConfig(level=logging.INFO)
    material_file, category_file, mysql_uri, image_dir = parse_args()
    FoodMaterialCleaner(material_file=file(material_file),
            category_file=file(category_file), mysqldb=uri2service(mysql_uri),
            image_dir=image_dir).process()

if __name__ == '__main__':
    main()
