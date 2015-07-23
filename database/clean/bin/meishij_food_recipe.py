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
from modules.recipe_cleaner import FoodRecipeCleaner


def parse_args():
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option('-r', '--recipe-file', dest='recipe_file',
            type='string', action='callback', callback=opt_ensure_file)
    parser.add_option('-c','--classificaton_category-file', dest='classification_category_file',
            type='string', action='callback', callback=opt_ensure_file)
    parser.add_option('-e','--effect_detail-file',dest='effect_detail_file',
            type='string', action='callback', callback=opt_ensure_file)
    parser.add_option('-m', '--mysql-uri', dest='mysql_uri', type='string')
    parser.add_option('-i', '--image-dir', dest='image_dir', type='string')

    options, args =  parser.parse_args()

    recipe_file = options.recipe_file
    if not recipe_file:
        parser.error('-r|--recipe-file not specified')

    classification_category_file = options.classification_category_file
    if not classification_category_file:
        parser.error('-c|--classification_category-file not specified')
    
    effect_detail_file = options.effect_detail_file
    if not effect_detail_file:
        parser.error('-e|--effect_detail-file not specified')

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
                parser.error('can not create dirctory %s' % (image_dir,))

    return recipe_file, classification_category_file, effect_detail_file, mysql_uri, image_dir


def main():
    import logging
    logging.basicConfig(level=logging.INFO)
    recipe_file, classificaton_category_file, effect_detail_file, mysql_uri,image_dir = parse_args()
    FoodRecipeCleaner(recipe_file=file(recipe_file),
            classification_category_file=file(classificaton_category_file),
            effect_detail_file=file(effect_detail_file),
            mysqldb=uri2service(mysql_uri), img_dir=image_dir).process()

if __name__ == '__main__':
    main()
