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

    def __init__(self, source_file, mysqldb, image_dir=None):
        self.source_file = source_file
        self.mysqldb = mysqldb
        self.image_dir = image_dir

        self.materials = {}
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

            sql = 'INSERT INTO %s (%s) VALUES (%s)' % \
                    (table_clause, field_clause, value_clause)

            cursor.execute('INSERT INTO `%s` (%s) VALUES (%s)' %
                    (self.table_name, field_clause, value_clause))
            self.mysqldb.commit()
