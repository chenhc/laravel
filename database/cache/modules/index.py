#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   index.py
Author:     Chen Yanfei
            Liu Dongqiang
@contact:   fasionchan@gmail.com
@version:   $Id$

Description:

Changelog:

'''

import json
import logging

class HashByNameDict(dict):

    def __hash__(self):
        return hash(self['name'])


class IndexCacher(object):

    def __init__(self, mysqldb, redisdb):
        self.mysqldb = mysqldb
        self.redisdb = redisdb

    def build_tag_item_index(self, tag_set, tag_item_map, data):
        # 食材标签集{tag_set}
        # SADD "material_tags" "水果" "维生素C"

        # 菜谱标签集{tag_set}
        # SADD 'recipe_taste' '甜味' '麻辣味'
        # SADD 'recipe_tags' '云贵菜' '粤菜' '早餐' '山东小吃'
        # SADD 'recipe_classifications' '家常菜谱' '国家' '各地小吃'
        for tag in data:
            self.redisdb.sadd(tag_set, tag)

        # 写食材{tag_item_map}:{tag}索引
        # RPUSH "tag2material:维生素C" '{"name": "苹果", "hash": "xxxx", "hash_image": "xxxx", "alias": "xxxx"}' '{"name": "橙子", "hash": "xxxx"}'

        # 写菜谱{tag_item_map}:{tag}索引
        # RPUSH "tag2recipe:云贵菜" '{"taste":"其他口味", "hash": "515ac3ab55d9e1c1bca3fb6ce4b08fb4", "name": "菠萝鸡肉丁", "area": "云贵菜"}'
        # RPUSH "taste2recipe:麻辣味" '{"taste":"麻辣味","hash":"d67946b81c5cc02a14dec89284408b65","name":"麻辣猪血糕", "area":"港台菜"}'
        # RPUSH "classification2category:家常菜谱" '凉菜'
        for tag, item_list in data.iteritems():
            key = '%s:%s' % (tag_item_map, tag)
            for item in item_list:
                self.redisdb.rpush(key, json.dumps(item))

        # json序列化item_list
        for tag, item_list in data.iteritems():
            data[tag] = json.dumps(list(item_list))

        # 写食材{tag_item_map}索引
        # HMSET "tag2material" "维生素C" '[{"name": "苹果", "hash": "xxxx", "image_hash", "xxxx", "alias": "xxxx"}, {"name": "橙子", "hash" "xxxx"}]'

        # 写菜谱{tag_item_map}索引
        # HMSET "taste2recipe" "麻辣味" '[{"taste": "麻辣味","hash":"xxxx", "name": "麻辣风爪", "area": null},{"taste":麻辣味,"hash":"xxx", "name": "麻辣猪血糕","area": "港台菜"}]'
        # HMSET "tag2recipe" "云贵菜" '[{"taste":"其他口味", "hash": "515ac3ab55d9e1c1bca3fb6ce4b08fb4", "name": "菠萝鸡肉丁", "area": "云贵菜"}']'
        # HMSET "classification2category" "家常菜谱" '["凉菜","素食"]'
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

    def build_food_recipe_cache(self, food_recipes, classification_category):
        recipe_infos = {}
        # 标签:云贵菜 粤菜 早餐 山东小吃
        tag2recipe = {}
        # 味道:甜味 麻辣味
        taste2recipe = {}

        # 总纲:家常菜谱 国家 各地小吃
        classification2category = {}

        for recipe in food_recipes:
            # 菜谱简单介绍
            recipe_info = {
                    'hash' : recipe['hash'],
                    'area' : recipe['area'],
                    'taste' : recipe['taste'],
                    # 'procedure' : recipe['procedure']
                    }
            recipe_infos[recipe['name']] = json.dumps(recipe_info)
            recipe_info['name'] = recipe['name']
            # 标签
            for tag in (recipe['tags'] or '').split(','):
                if tag:
                    tag2recipe.setdefault(tag, set()).add( \
                            HashByNameDict(recipe_info))

            # 味道
            taste = recipe['taste']
            taste2recipe.setdefault(taste, set()).add( \
                    HashByNameDict(recipe_info))

        # 写food_recipe索引
        # HMSET "food_recipe" "麻辣风爪" '{"hash": "xxxx", "area": "xxxx", "taste": "xxxx"}'
        self.redisdb.hmset('food_recipe', recipe_infos)

        # 味道索引
        self.build_tag_item_index(tag_set = 'recipe_taste', \
                tag_item_map = 'taste2recipe', data = taste2recipe)

        # 标签索引
        self.build_tag_item_index(tag_set = 'recipe_tags', \
                tag_item_map = 'tag2recipe', data = tag2recipe)

        for item in classification_category:
            classification = item['classification']
            category = item['category']
            categories = category.split(',')
            for item in categories:
                classification2category.setdefault(classification, set()).add( \
                    item)

        # 总纲索引
        self.build_tag_item_index(tag_set = 'recipe_classifications', \
                tag_item_map = 'classification2category',
                data = classification2category)

    def build(self):
        cursor = self.mysqldb.cursor()
        # 食材
        cursor.execute('SELECT * FROM `food_material`')
        food_materials = cursor.fetchall()

        self.build_food_material_cache(food_materials)
        logging.info('build food_material cache success')

        # 食谱
        cursor.execute('SELECT * FROM `food_recipe`;')
        food_recipes = cursor.fetchall()
        cursor.execute('SELECT * FROM `fr_classification_category`;')
        classification_category = cursor.fetchall()

        self.build_food_recipe_cache(food_recipes, \
                classification_category)
        logging.info('build food_recipe cache success')
