#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   meishij.py
Author:     Chen Yanfei
@contact:   fasionchan@gmail.com
@version:   $Id$

Description:

Changelog:

'''

import json
import hashlib
import logging

from collections import OrderedDict

from pylib.net.http import requests_with_random_ip

from pylib.util.common import encoded_dict
from pylib.util.sql import format_table_clause, format_field_clause, \
    format_value_clause

from config.const import HASH_SALT

class FoodMaterialCleaner(object):

    def __init__(self, material_file, category_file, mysqldb, image_dir=None):
        self.material_file = material_file
        self.category_file = category_file
        self.mysqldb = mysqldb
        self.image_dir = image_dir

        self.materials = {}
        self.material2category = {}

        self.fm_table = 'food_material'
        self.fmcc_table = 'fm_classification_category'

        self.classification_list = set([
            '蔬菜', '水果', '薯类淀粉', '菌藻',
            '畜肉', '禽肉', '鱼虾蟹贝', '蛋类',
            '谷类', '干豆', '坚果种子',
            '速食食品', '婴幼儿食品', '小吃甜饼', '糖蜜饯', '乳类', '软饮料', '酒精饮料',
        ])

        self.category_list = set([
            '根菜类', '鲜豆类', '茄果、瓜菜类', '葱蒜类', '嫩茎、叶、花菜类', '水生蔬菜类', '薯芋类', '野生蔬菜类',
            '仁果类', '核果类', '浆果类', '柑橘类', '热带、亚热带水果', '瓜果类',
            '薯类', '淀粉类',
            '菌类', '藻类',
            '猪类', '牛类', '羊类', '驴类', '马类', '其它畜肉类',
            '鸡类', '鸭类', '鹅类', '火鸡类', '其它禽肉类',
            '鱼类', '虾类', '蟹类', '贝类', '其它水产类',
            '鸡蛋类', '鸭蛋类', '鹅蛋类', '鹌鹑蛋类',
            '小麦类', '稻米类', '玉米类', '大麦类', '小米、黄米类', '其它谷类',
            '大豆类', '绿豆类', '赤豆类', '芸豆类', '蚕豆类', '其它干豆类',
            '树坚果类', '种子类',
            '快餐食品类', '方便食品类', '休闲食品类',
            '婴幼儿配方粉类', '婴幼儿断奶期辅助', '婴幼儿补充食品类',
            '小吃类', '蛋糕、甜点类',
            '糖类', '糖果类', '蜜饯类',
            '液态乳类', '奶粉类', '酸奶类', '奶酪类', '奶油类', '其它乳类',
            '碳酸饮料类', '果汁及果汁饮料类', '蔬菜汁饮料类', '含乳饮料类', '植物蛋白饮料类', '茶叶及茶饮料类', '固态饮料类', '棒冰、冰激凌类', '其它饮料类',
            '发酵酒类', '蒸馏酒类', '露酒（配制酒类）',
        ])

        self.classification_category = OrderedDict([
            ['蔬菜', ['根菜类', '鲜豆类', '茄果、瓜菜类', '葱蒜类', '嫩茎、叶、花菜类', '水生蔬菜类', '薯芋类', '野生蔬菜类'],],
            ['水果', ['仁果类', '核果类', '浆果类', '柑橘类', '热带、亚热带水果', '瓜果类'],],
            ['薯类淀粉', ['薯类', '淀粉类'],],
            ['菌藻', ['菌类', '藻类'],],
            ['畜肉', ['猪类', '牛类', '羊类', '驴类', '马类', '其它畜肉类'],],
            ['禽肉', ['鸡类', '鸭类', '鹅类', '火鸡类', '其它禽肉类'],],
            ['鱼虾蟹贝', ['鱼类', '虾类', '蟹类', '贝类', '其它水产类'],],
            ['蛋类', ['鸡蛋类', '鸭蛋类', '鹅蛋类', '鹌鹑蛋类'],],
            ['谷类', ['小麦类', '稻米类', '玉米类', '大麦类', '小米、黄米类', '其它谷类'],],
            ['干豆', ['大豆类', '绿豆类', '赤豆类', '芸豆类', '蚕豆类', '其它干豆类'],],
            ['坚果种子', ['树坚果类', '种子类'],],
            ['速食食品', ['快餐食品类', '方便食品类', '休闲食品类'],],
            ['婴幼儿食品', ['婴幼儿配方粉类', '婴幼儿断奶期辅助', '婴幼儿补充食品类'],],
            ['小吃甜饼', ['小吃类', '蛋糕、甜点类'],],
            ['糖蜜饯', ['糖类', '糖果类', '蜜饯类'],],
            ['乳类', ['液态乳类', '奶粉类', '酸奶类', '奶酪类', '奶油类', '其它乳类'],],
            ['软饮料', ['碳酸饮料类', '果汁及果汁饮料类', '蔬菜汁饮料类', '含乳饮料类', '植物蛋白饮料类', '茶叶及茶饮料类', '固态饮料类', '棒冰、冰激凌类', '其它饮料类'],],
            ['酒精饮料', ['发酵酒类', '蒸馏酒类', '露酒（配制酒类）'],],
            ])

    def process_fmcc(self):
        # 处理classification_category
        assert(set(self.classification_category) == self.classification_list)
        assert(set(sum(self.classification_category.values(), [])) == self.category_list)

        fields = ['classification','category']
        field_clause = format_field_clause(fields)
        table_clause = format_table_clause(self.fmcc_table)

        cursor = self.mysqldb.cursor()
        for classification, category_list in self.classification_category.items():
            for category in category_list:
                values = [classification, category]
                value_clause = format_value_clause(values)
                sql = 'INSERT INTO %s (%s) VALUES (%s)' % (table_clause, field_clause, value_clause)
                cursor.execute(sql)
                self.mysqldb.commit()

    def process_fm(self):
        # 处理category_material
        for line in self.category_file:
            pair = json.loads(line.strip())
            category = pair['category'].encode('utf8').replace('，', '、')
            material = pair['material'].encode('utf8')

            self.material2category.setdefault(material, set()).add(category)

        # 处理food_material
        for line in self.material_file:
            material = json.loads(line.strip())
            name = material['name'].encode('utf8')
            if name not in self.materials:
                self.materials[name] = encoded_dict(material)
            else:
                raise Exception('duplicate material: %s' % (name,))

        table_clause = format_table_clause(self.fmcc_table)

        fields = [ 'name', 'hash', 'classification', 'category', 'alias',
                'tags', 'image_hash', 'amount_rec', 'suit_crowds',
                'avoid_crowds', 'suit_ctcms', 'avoid_ctcms', 'brief',
                'nutrient', 'efficacy', 'taboos', 'suit_mix', 'avoid_mix',
                'choose', 'store', 'tips']
        field_clause = format_field_clause(fields)

        for name, material in self.materials.iteritems():
            logging.info('importing name=%s' % (name,))

            name_md5 = hashlib.md5(name + HASH_SALT).hexdigest()
            material['hash'] = name_md5

            # 标签
            tags = list(self.material2category.get(name, ()))
            tags.sort()
            material['tags'] = ','.join(tags)

            # 分类以及子类
            material['category'] = None
            for tag in tags:
                if tag in self.category_list:
                    material['category'] = tag
                elif tag in self.classification_list:
                    material['classification'] = tag

            image_res = None
            if self.image_dir:
                # 取出图片URL
                image_url = material.get('image_url')
                logging.info('getting url=%s' % (image_url,))

                # 请求图片
                for x in xrange(3):
                    try:
                        image_res= requests_with_random_ip.get(image_url, timeout=3*x)
                        break
                    except Exception as err:
                        logging.warn('requests error: %s' % (err,))

                if not image_res:
                    logging.warn('getting image fail: url=%s' % (image_url,))

            if image_res:
                image_raw = image_res.content
                image_md5 = hashlib.md5(image_raw).hexdigest()

                # 图片写入文件
                image_file = '%s/%s.jpg' % (self.image_dir, image_md5)
                file(image_file, 'w+').write(image_raw)

                # 记录图片哈希值
                material['image_hash'] = image_md5

            values = [material.get(field) for field in fields]
            value_clause = format_value_clause(values)

            sql = 'INSERT INTO %s (%s) VALUES (%s)' % \
                    (table_clause, field_clause, value_clause)

            cursor.execute(sql)
            self.mysqldb.commit()

    def process(self):
        self.process_fmcc()
