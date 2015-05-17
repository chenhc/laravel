# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
from scrapy import log

from crawler.items import FoodMaterialItem


class FileStorePipeline(object):

    def __init__(self):
        self.food_material = file('/tmp/food_material', 'w+')

    def store_into(self, item, f):
        f.write(json.dumps(dict(item)))
        f.write('\n')
        f.flush()

    def process_item(self, item, spider):
        if isinstance(item, FoodMaterialItem):
            log.msg('[STORE][file][food_material] name=%s category=%s' %
                    (item['name'], item['category']), level=log.INFO)
            self.store_into(item, self.food_material)
        return item


class CrawlerPipeline(object):
    def process_item(self, item, spider):
        return item
