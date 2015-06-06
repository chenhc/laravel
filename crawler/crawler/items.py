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
    #cook_time = scrapy.Field()

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


# 食材列表页面和菜谱列表页面的解析得到的食材或菜谱的item
class ListItem(scrapy.Item):
    # 类别
    category = scrapy.Field()

    # 名字
    name = scrapy.Field()

    # url
    url = scrapy.Field()

class RecipeCategoryListItem(scrapy.Item):
    # 类别 如：家常菜谱，国外菜谱
    category = scrapy.Field()

    # 名字 如：川菜 贵州小吃 美国家常菜 甜品蛋糕
    name = scrapy.Field()

    # url
    url = scrapy.Field()

# 人群膳食页面各种人群和url
class CrowdListItem(scrapy.Item):
    # 人群
    crowd = scrapy.Field()

    # url
    url = scrapy.Field()

# 人群对应的适合以及禁忌的食材，适合的食谱
class CrowdItem(scrapy.Item):
    # 人群 比如：孕妇 小孩
    crowd = scrapy.Field()

    # 适合做的tips 比如：多吃含蛋白质的食物
    suit_tips = scrapy.Field()

    # 适宜食材名字&url的列表
    suit_material_list = scrapy.Field()

    # 不推荐做的tips 比如：不能喝酒
    avoid_tips = scrapy.Field()

    # 禁忌食材&url的列表
    avoid_material_list = scrapy.Field()

    # 适合的食谱&url的列表
    suit_recipe_list = scrapy.Field()

    # 下一页链接，方便解析往后的推荐食用菜谱
    nxtpage = scrapy.Field()

class IllListItem(scrapy.Item):
    # 疾病名字
    ill = scrapy.Field()

    # url
    url = scrapy.Field()


class IllItem(scrapy.Item):
    # 疾病
    ill = scrapy.Field()

    # 适合做的tips 比如：多吃含蛋白质的食物
    suit_tips = scrapy.Field()

    # 适宜食材名字适宜食材url的列表
    suit_material_list = scrapy.Field()

    # 不推荐做的tips 比如：不能喝酒
    avoid_tips = scrapy.Field()

    # 禁忌食材禁忌食材url的列表
    avoid_material_list = scrapy.Field()

    # 适合的食谱&url对应的列表
    suit_recipe_list = scrapy.Field()

    # 下一页链接，方便解析往后的推荐食用菜谱
    nxtpage = scrapy.Field()

class FunctionalityListItem(scrapy.Item):
    # 功能
    functionality = scrapy.Field()

    # url
    url = scrapy.Field()


class FunctionalityItem(scrapy.Item):
    # 功能 比如：美容 减肥
    functionality = scrapy.Field()

    # 适合做的tips 比如：多吃含蛋白质的食物
    suit_tips = scrapy.Field()

    # 适宜食材名字适宜食材url的列表
    suit_material_list = scrapy.Field()

    # 不推荐做的tips 比如：不能喝酒
    avoid_tips = scrapy.Field()

    # 禁忌食材禁忌食材url的列表
    avoid_material_list = scrapy.Field()

    # 适合的食谱&url对应的列表
    suit_recipe_list = scrapy.Field()

    # 下一页链接，方便解析往后的推荐食用菜谱
    nxtpage = scrapy.Field()


class OrganEfctListItem(scrapy.Item):
    # 功效 例如：补心， 胃调养
    effect = scrapy.Field()

    # url
    url = scrapy.Field()


class OrganEfctItem(scrapy.Item):
    # 功效 比如:补肾 补心
    effect = scrapy.Field()

    # 适合做的tips 比如：多吃含蛋白质的食物
    suit_tips = scrapy.Field()

    # 适宜食材名字适宜食材url的列表
    suit_material_list = scrapy.Field()

    # 不推荐做的tips 比如：不能喝酒
    avoid_tips = scrapy.Field()

    # 禁忌食材禁忌食材url的列表
    avoid_material_list = scrapy.Field()

    # 适合的食谱&url对应的列表
    suit_recipe_list = scrapy.Field()

    # 下一页链接，方便解析往后的推荐食用菜谱
    nxtpage = scrapy.Field()


class RecipeItem(scrapy.Item):

    name = scrapy.Field()

    url = scrapy.Field()


class MaterialItem(scrapy.Item):

    name = scrapy.Field()

    url = scrapy.Field()

class CategoryMaterialPairItem(scrapy.Item):

    category = scrapy.Field()

    material = scrapy.Field()
