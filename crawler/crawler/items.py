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


class HackItem(scrapy.Item):
    verifycode_key = scrapy.Field()
    verifycode = scrapy.Field()
    verifycode_shicai = scrapy.Field()
    verify_shicai = scrapy.Field()
    name = scrapy.Field()
    img_src = scrapy.Field()


class PageItem(scrapy.Item):
    # url
    url = scrapy.Field()

    # 类型
    type = scrapy.Field()

    # 其他属性
    kwargs = scrapy.Field()


# 原材料页面解析的item
class FoodMaterialItem(scrapy.Item):
    # 来源
    source = scrapy.Field()

    # 名字
    name = scrapy.Field()

    # 类别
    category = scrapy.Field()

    # 别名
    alias = scrapy.Field()

    # 图片URL
    image_url = scrapy.Field()

    # 建议食量
    amount_rec = scrapy.Field()

    # 适宜人群
    suit_crowds = scrapy.Field()

    # 禁忌人群
    avoid_crowds = scrapy.Field()

    # 适宜体质
    suit_ctcms = scrapy.Field()

    # 禁忌体质
    avoid_ctcms = scrapy.Field()

    # 简介
    brief = scrapy.Field()

    # 营养价值
    nutrient = scrapy.Field()

    # 食用功效
    efficacy = scrapy.Field()

    # 食用禁忌
    taboos = scrapy.Field()

    # 适宜搭配
    suit_mix = scrapy.Field()

    # 禁忌搭配
    avoid_mix = scrapy.Field()

    # 选购技巧
    choose = scrapy.Field()

    # 储藏方法
    store = scrapy.Field()

    # 烹饪小贴士
    tips = scrapy.Field()

# 菜谱页面解析的item
class FoodRecipeItem(scrapy.Item):
    # 来源
    source = scrapy.Field()

    # 名字
    name = scrapy.Field()

    # 菜系
    area = scrapy.Field()

    # 标签
    tags = scrapy.Field()

    # 工艺
    method = scrapy.Field()

    # 难度
    difficulty = scrapy.Field()

    # 分量：人数
    amount = scrapy.Field()

    # 口味
    taste = scrapy.Field()

    # 准备时间
    setup_time = scrapy.Field()

    # 烹饪时间
    cook_time = scrapy.Field()

    # 晒客
    sharer = scrapy.Field()

    # 主料
    primaries = scrapy.Field()

    # 辅料
    accessories = scrapy.Field()

    # 做法
    procedure = scrapy.Field()


# 类别列表的解析的item，url为各种原材料列表页面(如蔬菜)的解析链接入口
class MaterialCategoryItem(scrapy.Item):
    # 类别
    category = scrapy.Field()

    # url
    url = scrapy.Field()

# 原材料列表页面的解析的item，url为各种材料(如菠菜)的解析链接入口
class MaterialListItem(scrapy.Item):
    # 类别
    category = scrapy.Field()

    # 名字
    name = scrapy.Field()

    # url
    url = scrapy.Field()
