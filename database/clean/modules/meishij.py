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

from pylib.net.http import requests_with_random_ip

from pylib.util.common import encoded_dict
from pylib.util.sql import format_table_clause, format_field_clause, \
    format_value_clause

from config.const import HASH_SALT

class FoodMaterialCleaner(object):

    def __init__(self, source_file, category_file,mysqldb, image_dir=None):
        self.source_file = source_file
        self.category_file = category_file
        self.mysqldb = mysqldb
        self.image_dir = image_dir
        self.materials = {}
        self.tags = {}
        self.table_name = 'food_material'

    def process(self):
        for line in self.source_file:
            material = json.loads(line.strip())
            name = material['name'].encode('utf8')
            if name not in self.materials:
                self.materials[name] = encoded_dict(material)
            else:
                raise Exception('duplicate material: %s' % (name,))
       
        table_clause = format_table_clause(self.table_name)
        fields = [ 'name', 'hash', 'category', 'alias', 'image_hash',
                'amount_rec', 'suit_crowds', 'avoid_crowds', 'suit_ctcms',
                'avoid_ctcms', 'brief', 'nutrient', 'efficacy', 'taboos',
                'suit_mix', 'avoid_mix', 'choose', 'store', 'tips']
        field_clause = format_field_clause(fields)
        
        cursor = self.mysqldb.cursor()
        for name, material in self.materials.iteritems():
            logging.info('importing name=%s' % (name,))
            name_md5 = hashlib.md5(name + HASH_SALT).hexdigest()
            material['hash'] = name_md5
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
            cursor.execute('INSERT INTO `%s` (%s) VALUES (%s)' %
                    (self.table_name, field_clause, value_clause))
            self.mysqldb.commit()
        
        self.category_clean()		
        category = ['蔬菜','水果','薯类淀粉',
                    '菌藻','畜肉','禽肉','鱼虾蟹贝','蛋类',
                    '谷类','干豆','坚果种子',
                    '速食食品','婴幼儿食品','小吃甜饼','糖蜜饯','乳类','软饮料','酒精饮料']
        for key,value in self.tags.iteritems():    
            cursor.execute('UPDATE `food_material` SET `tags`=%s WHERE `name`=%s',(value,key))
            self.mysqldb.commit()       
            for i in category:
                if i in value:
                    cursor.execute('UPDATE `food_material` SET `category`=%s WHERE `name`=%s',(i,key))
                    self.mysqldb.commit()
                    break


    def category_clean(self):
        for line in self.category_file:
            tags = json.loads(line.strip())
            category = tags['category'].encode('utf8')
            material = tags['material'].encode('utf8')
            if material not in self.tags.keys():
                self.tags[material] = category
            else:
                self.tags[material] = self.tags[material]+','+category
				
