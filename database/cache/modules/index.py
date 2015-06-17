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
        category = []
        for material in food_materials:
            category.append(material['category'])
            infos[material['name']] = json.dumps({
                'hash': material['hash'],
                'image_hash': material['image_hash'],
                'alias': material['alias']
            })
        category_set = set(category)
        category = list(category_set)
        self.redisdb.hmset('food_material', infos)
        
        tags = {}
        for item in category:
            for material in food_materials:	
                if material['tags']: 
	                if item in material['tags']:
	                    if item not in infos.keys():
	                        tags[item] = []
	                    tags[item].append(material['id'])
        	tags[item] = json.dumps(tags[item])
        self.redisdb.hmset('food_material_tag', tags)

    def build(self):     
        cursor = self.mysqldb.cursor()
        cursor.execute('SELECT * FROM `food_material`')
        food_materials = cursor.fetchall()
        self.build_food_material_cache(food_materials)        
        
