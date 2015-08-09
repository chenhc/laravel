#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   meishij_food_recipe.py
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

from modules.meishij import FoodRecipeCleaner


def parse_args():
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option('-r', '--recipe-file', dest='recipe_file',
            type='string', action='callback', callback=opt_ensure_file)
    parser.add_option('-c','--category-file', dest='category_file',
            type='string', action='callback', callback=opt_ensure_file)
    parser.add_option('-C', '--classification-file',
            dest='classification_file', type='string', action='callback',
            callback=opt_ensure_file)
    parser.add_option('-e','--effect-file', dest='effect_file',
            type='string', action='callback', callback=opt_ensure_file)
    parser.add_option('-m', '--mysql-uri', dest='mysql_uri', type='string')
    parser.add_option('-i', '--image-dir', dest='image_dir', type='string')

    options, args =  parser.parse_args()

    recipe_file = options.recipe_file
    if not recipe_file:
        parser.error('-r|--recipe-file not specified')

    category_file = options.category_file
    if not category_file:
        parser.error('-c|--category-file not specified')

    classification_file = options.classification_file
    if not classification_file:
        parser.error('-C|--classification-file not specified')

    effect_file = options.effect_file
    if not effect_file:
        parser.error('-e|--effect-file not specified')

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

    return recipe_file, category_file, classification_file, effect_file, \
            mysql_uri, image_dir


def main():
    import logging
    logging.basicConfig(level=logging.INFO)
    recipe_file, category_file, classification_file, effect_file, mysql_uri, \
            image_dir = parse_args()
    FoodRecipeCleaner(recipe_file=file(recipe_file),
            category_file=file(category_file),
            classification_file=file(classification_file),
            effect_file=file(effect_file),
            mysqldb=uri2service(mysql_uri),
            image_dir=image_dir).process()

if __name__ == '__main__':
    main()
