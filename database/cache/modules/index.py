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


class HashByNameDict(dict):

    def __hash__(self):
        return hash(self['name'])


class IndexCacher(object):

    def __init__(self, mysqldb, redisdb):
        self.mysqldb = mysqldb
        self.redisdb = redisdb

    def build_tag_item_index(self, tag_set, tag_item_map, data):
        # 标签集{tag_set}
        # SADD "material_tags" "水果" "维生素C"
        for tag in data:
            self.redisdb.sadd(tag_set, tag)

        # 写{tag_item_map}:{tag}索引
        # RPUSH "tag2material:维生素C" '{"name": "苹果", "hash": "xxxx", "hash_image": "xxxx", "alias": "xxxx"}' '{"name": "橙子", "hash": "xxxx"}'
        for tag, item_list in data.iteritems():
            key = '%s:%s' % (tag_item_map, tag)
            for item in item_list:
                self.redisdb.rpush(key, json.dumps(item))

        # json序列化item_list
        for tag, item_list in data.iteritems():
            data[tag] = json.dumps(list(item_list))

        # 写{tag_item_map}索引
        # HMSET "tag2material" "维生素C" '[{"name": "苹果", "hash": "xxxx", "image_hash", "xxxx", "alias": "xxxx"}, {"name": "橙子", "hash" "xxxx"}]'
        self.redisdb.hmset(tag_item_map, data)

    def build_food_material_cache(self, food_materials):
        material_infos = {}
        classification2material = {}
        category2material = {}
        tag2material = {}
        for material in food_materials:
            # 食材简述
            material_info = {
                'hash': material['hash'],
                'image_hash': material['image_hash'],
                'alias': material['alias'],
            }

            # 更新食材简述字典
            material_infos[material['name']] = json.dumps(material_info)

            # 食材名字
            material_info['name'] = material['name']

            # 分类
            classification = material['classification']
            if classification:
                classification2material.setdefault(classification, set())\
                        .add(HashByNameDict(material_info))

            # 子分类
            category = material['category']
            if category:
                category2material.setdefault(category, set())\
                        .add(HashByNameDict(material_info))

            # 标签
            for tag in (material['tags'] or '').split(','):
                if tag:
                    tag2material.setdefault(tag, set())\
                            .add(HashByNameDict(material_info))

        # 写food_material索引
        # HMSET "food_material" "苹果" '{"hash": "xxxx", "image_hash": "xxxx", "alias": "xxxx"}'
        self.redisdb.hmset('food_material', material_infos)

        # 标签索引
        self.build_tag_item_index(tag_set='material_tags',
                tag_item_map='tag2material', data=tag2material)

        # 分类索引
        self.build_tag_item_index(tag_set='material_classifications',
                tag_item_map='classification2material',
                data=classification2material)

        # 类别索引
        self.build_tag_item_index(tag_set='material_categories',
                tag_item_map='category2material', data=category2material)

    def build(self):
        cursor = self.mysqldb.cursor()
        cursor.execute('SELECT * FROM `food_material`')
        food_materials = cursor.fetchall()

        self.build_food_material_cache(food_materials)
