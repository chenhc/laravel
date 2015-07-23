#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   recipe_cleaner.py
Author:     Chen Yanfei
@contact:   fasionchan@gmail.com
@version:   $Id$

Description:

Changelog:

'''

import json
import hashlib
import logging
import sys

from pylib.net.http import requests_with_random_ip
from pylib.util.common import encoded_dict
from pylib.util.sql import format_table_clause, format_field_clause, \
    format_value_clause

from config.const import HASH_SALT

reload(sys)
sys.setdefaultencoding('utf8')

class FoodRecipeCleaner(object):

    def __init__(self, recipe_file, classification_category_file, 
                 effect_detail_file,  mysqldb, img_dir=None):
        self.recipe_file = recipe_file
        self.classification_category_file = classification_category_file
        self.effect_detail_file = effect_detail_file
        self.mysqldb = mysqldb
        self.img_dir = img_dir

        self.recipe = {}
        self.category2classification = {}
        self.health_tip = {}

        self.table_name1 = 'food_recipe'
        self.table_name2 = 'fr_classification_category'
        self.table_name3 = 'health_tip'

    def process(self):
        table_clause2 = format_table_clause(self.table_name2)
        table_clause1 = format_table_clause(self.table_name1)
        table_clause3 = format_table_clause(self.table_name3)

        cursor = self.mysqldb.cursor()
        
        # 处理classification_category_file
        fields = ['classification','category']
        field_clause = format_field_clause(fields)

        for line in self.classification_category_file:
            pair = json.loads(line.strip())
            category = pair['category'].encode('utf8')
            classification = pair['classification'].encode('utf8')
            self.category2classification.setdefault(classification, set()).add(category)

        for classification,category in self.category2classification.items():
            category_list = list(category)
            category_list.sort()
            category_string = ','.join(category_list)
            
            values = [classification,category_string]
            value_clause = format_value_clause(values)

            sql = 'INSERT INTO %s(%s) VALUE(%s)' % (table_clause2,field_clause,value_clause)
            cursor.execute(sql)
            self.mysqldb.commit()
        
        num = 0
        # 处理food_recipe
        for line in self.recipe_file:
            recipe = json.loads(line.strip())
            name = recipe['name'].encode('utf8')

            if name not in self.recipe.keys():
                self.recipe[name] = encoded_dict(recipe)
            else:
                #raise Exception('duplicate recipe: %s' % (name,))
                print 'duplicate recipe； %s num: %d' % (name,num)
                num += 1

        fields = [ 'name', 'hash', 'area', 'tags', 'method',
                'difficulty', 'sharer', 'amount', 'taste', 'setup_time',
                'cook_time', 'primaries', 'accessories',
                'procedure']
        field_clause = format_field_clause(fields)
        num = 0
        for name, recipe in self.recipe.items():
            logging.info('importing name=%s' % (name,))
            #hash处理
            name_md5 = hashlib.md5(name + HASH_SALT).hexdigest()
            recipe['hash'] = name_md5
            #cook_time处理   
            if 'img' in recipe['cook_time'] or 'src' in recipe['cook_time']:
                recipe['cook_time'] = ' '
            #sharer处理
            recipe['sharer'] = '小编'
            #分离图片url
            image_res = None
            if  self.img_dir:
                procedure = recipe['procedure'].split('\n')
                for i in xrange(len(procedure)):
                    print procedure[i]
                    if 'http' in procedure[i] or 'jpg' in procedure[i]:
                        logging.info('getting %s url=%s' % (name, procedure[i]))
                        #请求图片
                        for x in xrange(3):
                            try:
                                image_res = requests_with_random_ip.get(procedure[i],timeout=3*x)
                                break
                            except Exception as err:
                                logging.warn('requests error: %s' % (err,))
                        if not image_res:
                            logging.warn('requests image fail: urll=%s' % (procedure[i],))
                    if image_res:
                        image_raw = image_res.content
                        image_md5 = hashlib.md5(image_raw).hexdigest()
                        #图片写入文件
                        image_file = '%s/%s.jpg' % (self.img_dir, image_md5)
                        file(image_file, 'w+').write(image_raw)
                        #记录图片哈希值
                        procedure[i] = image_md5
                recipe['procedure'] = '\n'.join(procedure)
            
            values = [recipe.get(field) for field in fields]
            value_clause = format_value_clause(values)
            sql = 'INSERT INTO %s (%s) VALUES (%s)' % (table_clause1, field_clause, value_clause)
            cursor.execute(sql)
            self.mysqldb.commit()
        
        #处理effect_detail
        avoid_material_set = set()
        suit_material_set = set()
        num = 0
        for line in self.effect_detail_file:
            health_tip = json.loads(line.strip())
            topic = health_tip['category'].encode('utf8')
            if topic not in self.health_tip:
                for avoid_material in health_tip['avoid_material_list']:
                    avoid_material_set.add(avoid_material['name'].encode('utf8'))
                avoid_material_list = list(avoid_material_set)
                avoid_material_list.sort()
                health_tip['avoid_material_list'] = ','.join(avoid_material_list)
            
                for suit_material in health_tip['suit_material_list']:
                    suit_material_set.add(suit_material['name'].encode('utf8'))
                suit_material_list = list(suit_material_set)
                suit_material_list.sort()
                health_tip['suit_material_list'] = ','.join(suit_material_list)
                
                self.health_tip[topic] = encoded_dict(health_tip)
            else:
               # raise Exception('duplicate effect_detail: %s' % (topic,))
                print 'duplicate effect_detail: %s num: %d' %(topic,num)
                num += 1

        fields = ['topic','brief','suit_tips',
                  'avoid_tips','suit_food_materials',
                  'avoid_food_materials']
        fields_file = ['category','brief','suit_tips',
                       'avoid_tips','suit_material_list',
                      'avoid_material_list']
        field_clause = format_field_clause(fields)

        for topic,health_tip in self.health_tip.items():
            logging.info('import topic=%s' % (topic,))
            
            values = [health_tip.get(field) for field in fields_file]
            value_clause = format_value_clause(values)

            sql = 'INSERT INTO %s (%s) VALUES (%s)' % (table_clause3,field_clause,value_clause)
            cursor.execute(sql)
            self.mysqldb.commit()
        




