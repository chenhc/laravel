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

from pylib.util.common import encoded_dict, encoded_jsonic_object
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

        cursor = self.mysqldb.cursor()
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
        #self.process_fm()


class FoodRecipeCleaner(object):

    def __init__(self, recipe_file, category_file, classification_file,
            effect_file, mysqldb, image_dir=None):

        self.recipe_file = recipe_file
        self.category_file = category_file
        self.classification_file = classification_file
        self.effect_file = effect_file
        self.mysqldb = mysqldb
        self.image_dir = image_dir

        self.classifications = set()
        self.categories = set()
        self.category2id = {}

        self.recipes = set()
        self.recipe_list = []
        self.recipe2id = {}

        self.health_tips = {}

        self.classification2category = OrderedDict()
        self.category2recipe = {}

        self.fr_table = 'food_recipe'
        self.frm_table = 'food_recipe_material'
        self.frcc_table = 'fr_classification_category'
        self.ht_table = 'health_tip'
        self.frcm_table = 'fr_category_map'

        # 食材数据
        self.materials = dict()
        cursor = self.mysqldb.cursor()
        cursor.execute('SELECT * FROM `food_material`')
        for material in cursor.fetchall():
            name = material['name']
            self.materials[name] = material

    def process_frcc(self):
        # classification/category对应关系
        for line in self.classification_file:
            pair = encoded_jsonic_object(json.loads(line.strip()))
            classification = pair['classification']
            category = pair['category']
            self.classifications.add(classification)
            self.categories.add(category)

            category_list = self.classification2category\
                    .setdefault(classification, list())
            if category not in category_list:
                    category_list.append(category)

        # 表结构
        table_clause = format_table_clause(self.frcc_table)

        fields = ['classification','category']
        field_clause = format_field_clause(fields)

        # 写入数据
        cursor = self.mysqldb.cursor()
        for classification, categories in \
                self.classification2category.iteritems():

            for category in categories:
                values = [classification, category]
                value_clause = format_value_clause(values)

                sql = 'INSERT INTO %s (%s) VALUE (%s)' % \
                        (table_clause, field_clause, value_clause)

                cursor.execute(sql)
                category_id = self.mysqldb.insert_id()
                self.mysqldb.commit()

                self.category2id[category] = category_id

    def process_ht(self):
        bad_materials = set()
        MATERIAL_BASE_URL = 'http://www.meishij.net/'
        def fixed_material_list(material_list):
            result = []
            for material in material_list:
                url =  material.get('url')
                if url == '####':
                    continue

                if url.startswith(MATERIAL_BASE_URL):
                    name = url[len(MATERIAL_BASE_URL):]

                    material = self.materials.get(name)
                    if material is None:
                        bad_materials.add(name)
                        logging.warn('bad material: name=%s bads=%d' % \
                                (name, len(bad_materials)))

                        result.append(dict(name=name))
                    else:
                        result.append(dict(name=name, hash=material['hash'],
                            image_hash=material['image_hash']))

                    continue

                logging.warn('unknown url: url=%s' % (url,))

            return result

        # 预处理健康小贴士数据
        for line in self.effect_file:
            health_tip = encoded_jsonic_object(json.loads(line.strip()))
            health_tip['topic'] = topic = health_tip.pop('category')

            health_tip['suit_food_materials'] = \
                    json.dumps(fixed_material_list(health_tip.pop('suit_material_list')))
            health_tip['avoid_food_materials'] = \
                    json.dumps(fixed_material_list(health_tip.pop('avoid_material_list')))

            if topic not in self.health_tips:
                self.health_tips[topic] = health_tip
            else:
                duplicate = health_tip == self.health_tips[topic]

                logging.warn('duplicate effect_detail: topic=%s duplicate=%s' % \
                        (topic, duplicate))

        # 表结构
        table_clause = format_table_clause(self.ht_table)

        fields = ['topic','brief','suit_tips',
                  'avoid_tips','suit_food_materials',
                  'avoid_food_materials']
        field_clause = format_field_clause(fields)

        # 写入数据
        cursor = self.mysqldb.cursor()
        for topic, health_tip in self.health_tips.items():
            logging.info('import health tips: topic=%s' % (topic,))

            values = [health_tip.get(field) for field in fields]
            value_clause = format_value_clause(values)

            sql = 'INSERT INTO %s (%s) VALUES (%s)' % \
                    (table_clause, field_clause, value_clause)

            cursor.execute(sql)
            self.mysqldb.commit()

        for name in bad_materials:
            logging.warn('bad material: name=%s' % (name,))

    def process_frm(self):
        # 表结构
        table_clause = format_table_clause(self.frm_table)

        fields = ['recipe_id', 'material_id', 'role']
        field_clause = format_field_clause(fields)

        # 写入数据
        cursor = self.mysqldb.cursor()
        for recipe in self.recipe_list:
            recipe_id = str(recipe['id'])
            for fusage_id, role in (('primary_ids', 'PRIMARY'),
                    ('accessory_ids', 'ACCESSORY')):
                for material_id in recipe.get(fusage_id, ()):
                    material_id = str(material_id)
                    values = [recipe_id, material_id, role]
                    value_clause = format_value_clause(values)

                    sql = 'INSERT INTO %s (%s) VALUES (%s)' % \
                            (table_clause, field_clause, value_clause)

                    cursor.execute(sql)
                    self.mysqldb.commit()

    def process_fr(self):
        # 字段集合定义
        areas = set()
        all_tags = set()
        methods = set()
        difficulties = set()
        amounts = set()
        tastes = set()
        setup_times = set()
        cook_times = set()
        all_primaries = set()
        all_accessories = set()
        bad_materials = set()

        # 用料列表加工
        def process_material_list(recipe, fusage, fusage_id, dataset):
            material_list = []
            for name in recipe.get(fusage, '').split(','):
                dataset.add(name)

                material = self.materials.get(name)
                if material is not None:
                    material_list.append(dict(name=material['name'],
                        hash=material['hash'],
                        image_hash=material['image_hash']))
                    recipe.setdefault(fusage_id, []).append(material['id'])
                else:
                    material_list.append(dict(name=name))
                    bad_materials.add(name)
            return material_list

        # 预处理食谱列表
        for line in self.recipe_file:
            recipe = encoded_jsonic_object(json.loads(line.strip()))
            name = recipe['name']

            # 生成哈希值
            name_md5 = hashlib.md5(name + HASH_SALT).hexdigest()
            recipe['hash'] = name_md5

            # 地域字段集合
            areas.add(recipe.get('area', None))

            # 便签集合
            for tag in recipe.get('tags', '').split(','):
                all_tags.add(tag)

            # 做法字段集合
            methods.add(recipe.get('method', ''))

            # 难度字段
            difficulties.add(recipe.get('difficulty', ''))

            # 分量字段
            amount = recipe.get('amount', '')
            amounts.add(amount)

            amount = amount.replace('未知', '').replace('人份', '')
            if not amount:
                amount = 0
            else:
                amount = int(amount)
            recipe['amount'] = str(amount)

            # 口味字段
            tastes.add(recipe.get('taste', ''))

            # 准备时间
            setup_times.add(recipe.get('setup_time', ''))

            # 烹饪时间
            cook_time = recipe['cook_time']
            cook_times.add(cook_time)
            if 'img' in cook_time or 'src' in cook_time:
                recipe['cook_time'] = None

            # 分享者
            recipe['sharer'] = None

            # 主料
            recipe['primaries'] = json.dumps(process_material_list(recipe,
                'primaries', 'primary_ids', all_primaries))

            # 辅料
            recipe['accessories'] = json.dumps(process_material_list(recipe,
                'accessories', 'accessory_ids', all_accessories))

            self.recipes.add(name)
            self.recipe_list.append(recipe)

        # 表结构
        table_clause = format_table_clause(self.fr_table)

        fields = ['name', 'source', 'hash', 'area', 'tags', 'method',
                'difficulty', 'sharer', 'amount', 'taste', 'setup_time',
                'cook_time', 'primaries', 'accessories',
                'procedure']
        field_clause = format_field_clause(fields)

        # 写入数据
        cursor = self.mysqldb.cursor()
        self.recipe_list = self.recipe_list[:10]
        for recipe in self.recipe_list:
            name = recipe['name']
            logging.info('importing recipe: name=%s' % (name,))

            # 整理做法步骤
            procedure = recipe['procedure'].split('\n')
            for i in xrange(len(procedure)):
                url = procedure[i]
                if 'http' in url or 'jpg' in url:
                    logging.info('getting image: name=%s url=%s' % (name, url))

                    # 请求图片
                    image_res = None
                    for x in xrange(5):
                        try:
                            image_res = requests_with_random_ip.get(url,
                                    timeout=3*x)
                            break
                        except Exception as err:
                            logging.warn('requests error: %s' % (err,))

                    if image_res:
                        image_raw = image_res.content
                        image_md5 = hashlib.md5(image_raw).hexdigest()

                        # 图片写入文件
                        image_file = '%s/%s.jpg' % (self.image_dir, image_md5)
                        file(image_file, 'w+').write(image_raw)

                        # 记录图片哈希值
                        procedure[i] = image_md5 + '.jpg'
                    else:
                        logging.warn('requests image fail: name=%s url=%s' % \
                                (name, url))

            recipe['procedure'] = '\n'.join(procedure)

            values = [recipe.get(field) for field in fields]
            value_clause = format_value_clause(values)

            sql = 'INSERT INTO %s (%s) VALUES (%s)' % \
                    (table_clause, field_clause, value_clause)

            cursor.execute(sql)
            recipe['id'] = recipe_id = self.mysqldb.insert_id()
            self.mysqldb.commit()

            self.recipe2id.setdefault(name, []).append(recipe_id)

        self.process_frm()

        return

        # 显示缺失食材
        for name in bad_materials:
            logging.warn('bad material: name=%s' % (name,))

        # 显示辅料全集
        for accessory in all_accessories:
            logging.info('accessory: %s' % (accessory,))

        # 显示主料全集
        for primary in all_primaries:
            logging.info('primary: %s' % (primary,))

        # 显示准备时间全集
        for setup_time in setup_times:
            logging.info('setup_time: %s' % (setup_time,))

        # 显示口味全集
        for taste in tastes:
            logging.info('taste: %s' % (taste,))

        # 显示分量全集
        for amount in amounts:
            logging.info('amount: %s' % (amount,))

        # 显示难度全集
        for difficulty in difficulties:
            logging.info('difficulty: %s' % (difficulty,))

        # 显示便签全集
        for tag in all_tags:
            logging.info('tag: %s' % (tag,))

        # 显示做法全集
        for method in methods:
            logging.info('method: %s' % (method,))

        # 显示地域全集
        for area in areas:
            logging.info('area: %s' % (area,))

        # 显示cook_time全集
        for cook_time in cook_times:
            logging.info('cook time: %s' % (cook_time,))

    def process_frc(self):
        # 表结构
        table_clause = format_table_clause(self.frcm_table)

        fields = ['category_id', 'recipe_id']
        field_clause = format_field_clause(fields)

        # category/recipe对应关系
        cursor = self.mysqldb.cursor()
        for line in self.category_file:
            pair = encoded_jsonic_object(json.loads(line.strip()))

            recipe = pair['recipe']
            category = pair['category']
            category_id = str(self.category2id[category])

            for recipe_id in self.recipe2id.get(recipe, ()):
                values = [category_id, str(recipe_id)]
                value_clause = format_value_clause(values)

                sql = 'INSERT INTO %s (%s) VALUES (%s)' % \
                        (table_clause, field_clause, value_clause)

                cursor.execute(sql)
                self.mysqldb.commit()

    def process(self):
        self.process_ht()
        self.process_frcc()
        self.process_fr()
        self.process_frc()
