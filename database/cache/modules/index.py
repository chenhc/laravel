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
        material_infos = {}
        classification2material = {}
        category2material = {}
        tag2material = {}
        for material in food_materials:
            material_infos[material['name']] = json.dumps({
                'hash': material['hash'],
                'image_hash': material['image_hash'],
                'alias': material['alias']
            })

            # 分类
            classification = material['classification']
            if classification:
                classification2material.setdefault(classification, set())\
                        .add(material['id'])

            # 子分类
            category = material['category']
            if category:
                category2material.setdefault(category, set())\
                        .add(material['id'])

            # 标签
            for tag in (material['tags'] or '').split(','):
                if tag:
                    tag2material.setdefault(tag, set()).add(material['id'])

        # 写food_material索引
        self.redisdb.hmset('food_material', material_infos)

        # json序列化material_list
        for tag, material_list in tag2material.iteritems():
            tag2material[tag] = json.dumps(list(material_list))

        # 写tag2material索引
        self.redisdb.hmset('tag2material', tag2material)

    def build(self):
        cursor = self.mysqldb.cursor()
        cursor.execute('SELECT * FROM `food_material`')
        food_materials = cursor.fetchall()

        self.build_food_material_cache(food_materials)
