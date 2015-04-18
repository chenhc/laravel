# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem


class UniqueSitePipeline(object):
    def __init__(self):
        self.seen_sites = set()

    def process_item(self, item, spider):
        site = item['site']
        if site in self.seen_sites:
            raise DropItem
        else:
            self.seen_sites.add(site)
        return item


class PrintSitePipeline(object):
    def process_item(self, item, spider):
        print item['title'], item['url']
        return item
