# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class FoodMaterialItem(scrapy.Item):
    name = scrapy.Field()
    alias = scrapy.Field()
    suit_types = scrapy.Field()
    avoid_types = scrapy.Field()
