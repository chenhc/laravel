#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   index.py
Author:     Chen Yanfei
@contact:   fasionchan@gmail.com
@version:   $Id$

Description:

Changelog:

'''

import json


class IndexCacher(object):

    def __init__(self, mysqldb, redisdb):
        self.mysqldb = mysqldb
        self.redisdb = redisdb

    def build_food_material_cache(self, food_materials):
        infos = {}
        for material in food_materials:
            infos[material['name']] = json.dumps({
                'hash': material['hash'],
                'image_hash': material['image_hash'],
            })

        self.redisdb.hmset('food_material', infos)

    def build(self):
        cursor = self.mysqldb.cursor()
        cursor.execute('SELECT * FROM `food_material`')
        food_materials = cursor.fetchall()

        self.build_food_material_cache(food_materials)
