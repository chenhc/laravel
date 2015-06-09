# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
from scrapy import log

from crawler.items import FoodMaterialItem, CategoryMaterialPairItem, \
        FoodRecipeItem, CategoryRecipePairItem, RecipeCategoryPairItem, \
        RecipeCategoryDetailItem


class FileStorePipeline(object):

    def __init__(self):
        self.food_material = file('/tmp/food_material', 'w+')
        self.category_material = file('/tmp/category_material','w+')

        self.food_recipe = file('/tmp/food_recipe','w+')
        self.category_recipe = file('/tmp/category_recipe', 'w+')
        self.recipe_category_pair = file('/tmp/recipe_category_pair', 'w+')
        self.recipe_category_detail = file('/tmp/recipe_category_detail', 'w+')


    def store_into(self, item, f):
        f.write(json.dumps(dict(item)))
        f.write('\n')
        f.flush()

    def process_item(self, item, spider):
        if isinstance(item, FoodMaterialItem):
            log.msg('[STORE][file][food_material] name=%s category=%s' %
                    (item['name'], item['category']), level=log.INFO)
            self.store_into(item, self.food_material)

        if isinstance(item, CategoryMaterialPairItem):
            log.msg('[STORE][file][category_material] category=%s material=%s' %
                    (item['category'], item['material']), level=log.INFO)
            self.store_into(item, self.category_material)

        if isinstance(item, FoodRecipeItem):
            log.msg('[STORE][file][food_recipe] name=%s' % (item['name'],),
                    level=log.INFO)
            self.store_into(item, self.food_recipe)

        if isinstance(item, CategoryRecipePairItem):
            log.msg('[STORE][file][category_recipe] category=%s recipe=%s' %
                    (item['category'], item['recipe'],), level=log.INFO)
            self.store_into(item, self.category_recipe)

        if isinstance(item, RecipeCategoryPairItem):
            log.msg('[STORE][file][recipe_category_pair] classification=%s category=%s' %
                    (item['classification'], item['category'],), level=log.INFO)
            self.store_into(item, self.recipe_category_pair)

        if isinstance(item, RecipeCategoryDetailItem):
            log.msg('[STORE][file][recipe_category_detail] category=%s' %
                    (item['category'],), level=log.INFO)
            self.store_into(item, self.recipe_category_detail)

        return item


class CrawlerPipeline(object):
    def process_item(self, item, spider):
        return item
