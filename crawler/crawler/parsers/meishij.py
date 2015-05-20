#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   meishij.py
Author:     Chen Yanfei
            Liu Dongqiang
@contact:   fasionchan@gmail.com
@version:   $Id$

Description:

Changelog:

'''

if __name__ == '__main__':
    import mainenv

import urlparse

from crawler.items import HackItem, PageItem, FoodMaterialItem, \
        FoodRecipeItem, MaterialListItem, MaterialCategoryItem, \
        CommonRecipesListItem, ChineseRecipesListItem, RegionSnacksListItem, \
        ForeignRecipesListItem, BakeListItem


class HackParser(object):

    def parse(self, response):
        form = response.xpath('//form[@id="hack_form"]')
        verifycode_key, = form.xpath('./input[@name="verifycode_key"]/@value').extract()
        verifycode, = form.xpath('./input[@name="verifycode"]/@value').extract()
        verifycode_shicai, = form.xpath('./input[@name="verifycode_shicai"]/@value').extract()
        verify_shicai, = form.xpath('./input[@name="verify_shicai"]/@value').extract()
        img_src, = form.xpath('.//img/@src').extract()
        img_src = urlparse.urljoin(response.url, img_src)
        name, = form.xpath('.//p[@class="ques_p"]/strong/text()').extract()
        name = name.strip()[1:-1]
        yield HackItem(verifycode_key=verifycode_key, verifycode=verifycode,
                verifycode_shicai=verifycode_shicai,
                verify_shicai=verify_shicai, name=name, img_src=img_src)


class FoodMaterialParser(object):

    def parse(self, response, attr_map={
            u'别名': 'alias',
            u'食量建议': 'amount_rec',
            u'适宜人群': 'suit_crowds',
            u'禁忌人群': 'avoid_crowds',

            u'介绍': 'brief',
            u'营养价值': 'nutrient',
            u'食用效果': 'efficacy',
            u'食用禁忌': 'taboos',
            u'选购': 'choose',
            u'存储': 'store',
            u'烹饪小技巧': 'tips',
            }):
        div_main = response.xpath('//div[@class="main"]')
        div_sc_header = div_main.xpath('.//div[@class="sc_header"]')

        div_sc_header_con1 = div_sc_header.xpath('.//div[@class="sc_header_con1"]')
        name, = div_sc_header_con1.xpath('.//h1/text()').extract()
        image_url, = div_sc_header.xpath('.//img[@class="sc_headerimg"]/@src').extract()

        attrs = {}
        attr_names = div_sc_header_con1.xpath('.//p[@class="p2"]/strong/text()').extract()
        attr_names.reverse()
        for record in div_sc_header_con1.xpath('.//p[@class="p2"]/text()').extract():
            attr_value = record.split(u'：',1)
            if len(attr_value) == 1: 
                continue
            attr, value = attr_value
            attr = attr.strip() or attr_names.pop().strip()
            attr = attr[1:-1]
            value = value.strip()
            attr = attr_map.get(attr)
            if attr:
                attrs[attr] = value.encode('utf8')

        div_sc_header_con2 = div_sc_header.xpath('.//div[@class="sc_header_con2"]')
        suit_types = ','.join(div_sc_header_con2.xpath('.//li[@class="yi"]/a/text()').extract())
        avoid_types = ','.join(div_sc_header_con2.xpath('.//li[@class="ji"]/a/text()').extract())

        div_sccon_right_con = div_main.xpath('.//div[@class="sccon_right_con"]')

        suit_mix = ','.join([mix.replace(' ', '').replace(u'，', ':').strip() for mix in div_sccon_right_con.xpath('.//li[@class="yi"]/p/a/text()').extract()])
        avoid_mix = ','.join([mix.replace(' ', '').replace(u'，', ':').strip() for mix in div_sccon_right_con.xpath('.//li[@class="ji"]/p/text()').extract()])

        attr, values = None, None
        for dom in div_sccon_right_con.xpath('./strong[@class="title2"]|p'):
            if dom._root.tag == 'strong':
                if attr is not None and values is not None:
                    attr = attr_map.get(attr)
                    if attr:
                        attrs[attr] = '\n'.join(values)

                attr, = dom.xpath('./text()').extract()
                attr = attr.replace(name, '').replace(u'的', '')
                values = []

            elif dom._root.tag == 'p':
                for value in dom.xpath('./text()').extract():
                    values.append(value.strip().encode('utf8'))

        else:
            if attr is not None and values is not None:
                attr = attr_map.get(attr)
                if attr:
                    attrs[attr] = '\n'.join(values)

        attrs['alias'] = attrs.get('alias', '').replace('、', ',').strip(',')

        yield FoodMaterialItem(source=response.url, name=name.encode('utf8'),
                image_url=image_url,
                suit_mix=suit_mix.encode('utf8'),
                avoid_mix=avoid_mix.encode('utf8'),
                suit_ctcms=suit_types.encode('utf8'),
                avoid_ctcms=avoid_types.encode('utf8'), **attrs)


class FoodRecipeParser(object):

    def parse(self, response, areas=set([u"川菜", u"湘菜", u"粤菜", u"东北菜",
            u"鲁菜", u"浙菜", u"苏菜", u"清真菜", u"闽菜", u"沪菜", u"京菜",
            u"湖北菜", u"徽菜", u"豫菜", u"西北菜", u"云贵菜", u"江西菜",
            u"山西菜", u"广西菜", u"港台菜", u"其它菜"])):
        recipe = FoodRecipeItem()
        recipe['source'] = response.url

        # 名字
        div_info1 = response.xpath('//div[@class="info1"]')
        name, = div_info1.xpath('.//h1/a/text()').extract()
        recipe['name'] = name.strip().encode('utf8')

        # 标签：热菜、家常菜
        tags = []
        ul_pathstlye1 = response.xpath('//ul[@class="pathstlye1"]')
        for tag in ul_pathstlye1.xpath(".//li/a[@class='curzt']/text()").extract():
            tag = tag.replace('#', '').strip()
            tags.append(tag)

            #菜系
            if tag in areas:
                recipe['area'] = tag.encode('utf8')
        recipe['tags'] = ','.join(tags).encode('utf8')

        # 工艺
        div_info2 = response.xpath('//div[@class="info2"]')
        method, = div_info2.xpath('.//li[1]/a/text()').extract()
        recipe['method'] = method.encode('utf8')

        # 难度
        difficulty, = div_info2.xpath('.//li[2]/div/a/text()').extract()
        recipe['difficulty'] = difficulty.encode('utf8')

        # 份量（人数）
        amount, = div_info2.xpath('//li[3]/div/a/text()').extract()
        recipe['amount'] = amount.encode('utf8')

        # 口味
        taste, = div_info2.xpath('.//li[4]/a/text()').extract()
        recipe['taste'] = taste.encode('utf8')

        # 准备时间
        setup_time, = div_info2.xpath('.//li[5]/div/a/text()').extract() or ['']
        recipe['setup_time'] = setup_time.encode('utf8')

        # 烹饪时间
        cook_time, = div_info2.xpath('.//li[6]/div/a/text').extract() or ['']
        recipe['cook_time'] = cook_time.encode('utf8')

        # 主料
        primaries = []
        div_materials_box = response.xpath('//div[@class="materials_box"]')
        div_zl = div_materials_box.xpath('./div[@class="yl zl clearfix"]')
        for item in div_zl.xpath('./ul/li//a/text()').extract():
            primaries.append(item.strip())
        recipe['primaries'] = ','.join(primaries).encode('utf8')

        # 辅料
        accessories = []
        div_fuliao = div_materials_box.xpath('./div[@class="yl fuliao clearfix"]')
        for item in div_fuliao.xpath('./ul/li//a/text()').extract():
            accessories.append(item.strip())
        recipe['accessories'] = ','.join(accessories).encode('utf8')

        # 做法
        procedure = []
        div_measure = response.xpath('//div[@class="measure"]')
        for step in div_measure.xpath('//div[@class="content clearfix"]/div[@class="c"]/p/text()').extract():
            step = step.strip().encode('utf8')
            procedure.append(step)
        recipe['procedure'] = '\n'.join(procedure)
        yield recipe

# 解析食材百科类别栏 得到每一个类别的名字(如:蔬菜)与对应的链接,对应的链接可用于每种食材类别页面解析的入口,也包括了维生素类别，体质类别的入口
class CategoryListParser(object):

    def parse(self,response):
        div_other_c = response.xpath('//div[@class="other_c listnav_con clearfix"]')
        # 食材分类
        dls = div_other_c.xpath('./dl')
        for dl in dls:
            dt = dl.xpath('./dt/text()').extract()
            dds = dl.xpath('./dd')
            for dd in dds:
                url, = dd.xpath('a/@href').extract()
                category, = dd.xpath('a/text()').extract()
                item = MaterialCategoryItem()
                item['category'] = category.encode('utf8')
                item['url'] = url.encode('utf8')
                yield item

#parse 解析食材类别的页面(如：蔬菜，水果)，解析页面里面的每一个食材(如：菠菜，菠萝)的名字，类型，对应的链接,对应的链接可用于食材页面的解析
class MaterialListParser(object):

    def parse(self,response):
        # 食材类别
        div_other_c = response.xpath('//div[@class="other_c listnav_con clearfix"]')
        category, = div_other_c.xpath('//dd[@class="current"]//a/text()').extract()
        category = category.encode('utf8')

        # 食材列表
        div_listtyle1 = response.xpath('//div[@class="listtyle1"]')
        for l in div_listtyle1:
            # 类别
            item = MaterialListItem(category=category)

            # 名字
            name, = l.xpath('./div[@class="info1"]/h3/a/text()').extract()
            item['name'] = name.encode('utf8')

            # url
            url, = l.xpath('./div[@class="img"]/a/@href').extract()
            item['url'] = url.encode('utf8')
            yield item

        # base url
        base_url = response.url.split(u'?', 1)[0]

        # 下一页解析
        page_w = response.xpath('//div[@class="listtyle1_page_w"]')
        result = page_w.xpath('a[@class="next"]/@href').extract()
        if result:
            nxt, = result
            next_url = base_url + nxt
            yield PageItem(url=str(next_url), type=MaterialListItem,
                    kwargs=dict(category=category))

# 解析家常菜谱列表，得到各种菜（如：家常菜 私家菜）的页面链接
class CommonRecipesListParser(object):

    def parse(self, response):
        main_w = response.xpath('//div[@class="main_w clearfix"]')
        listnav = response.xpath('//dl[@class="listnav_dl_style1 w990 bb1 clearfix"]')
        dds = listnav.xpath('./dd')
        for dd in dds:
            name, = dd.xpath('./a/text()').extract()
            url, = dd.xpath('./a/@href').extract()
            yield CommonRecipesListItem(name = name, url = url)

# 解析中华菜系的列表，得到各种菜系（如：川菜 粤菜）的页面链接
class ChineseRecipesListParser(object):

    def parse(self, response):
        listnav = response.xpath('//dl[@class="listnav_dl_style1 w990 clearfix"]')
        dds = listnav.xpath('./dd')
        for dd in dds:
            name, = dd.xpath('./a/text()').extract()
            url, = dd.xpath('./a/@href').extract()
            yield ChineseRecipesListItem(name = name, url = url)

# 解析地方小吃的列表，得到各地小吃的页面链接
class RegionSnacksListParser(object):
    
    def parse(self, response):
        listnav = response.xpath('//dl[@class="listnav_dl_style1 w990 clearfix"]')
        dds = listnav.xpath('./dd')
        for dd in dds:
            region, = dd.xpath('./a/text()').extract()
            url, = dd.xpath('./a/@href').extract()
            yield RegionSnacksListItem(region = region, url = url)

# 解析外国菜谱的列表，得到各个国家菜谱的页面链接
class ForeignRecipesListParser(object):

    def parse(self, response):
        listnav = response.xpath('//dl[@class="listnav_dl_style1 w990 bb1 clearfix"]')
        dds = listnav.xpath('./dd')
        for dd in dds:
            country, = dd.xpath('./a/text()').extract()
            url, = dd.xpath('./a/@href').extract()
            yield ForeignRecipesListItem(country = country, url = url)

# 解析烘焙的列表，得到烘焙相关的页面链接
class BakeListParser(object):
        
    def parse(self, response):
        listnav = response.xpath('//dl[@class="listnav_dl_style1 w990 clearfix"]')
        dds = listnav.xpath('./dd')
        for dd in dds:
            name, = dd.xpath('./a/text()').extract()
            #烘陪工具不需要解析
            if name.rfind(u"工具") != -1:
                continue
            url, = dd.xpath('./a/@href').extract()
            yield BakeListItem(name = name, url = url)

if __name__ == '__main__':
    from crawler.utils import fetch

    def show_hack():
        url = 'http://www.meishij.net/hack/hack.php'
        item, = HackParser().parse(fetch(url))
        for attr, value in item.iteritems():
            print '%s=%s' % (attr, value)
            print

    def show_food_material(name):
        url = 'http://www.meishij.net/%s' % (name,)
        item, = FoodMaterialParser().parse(fetch(url))
        for attr, value in item.iteritems():
            print '%s=%s' % (attr, value)
            print
            
    def show_food_recipe(url):
        item, = FoodRecipeParser().parse(fetch(url))
        for attr, value in item.iteritems():
            print '%s=%s' % (attr, value)
            print
   
    def show_material_list(url):
        items = MaterialListParser().parse(fetch(url))
        for item in items:
            for attr, value in item.iteritems():
                print '%s=%s' % (attr, value)
            print 

    def show_category_list(url):
        items = CategoryListParser().parse(fetch(url))
        for item in items:
            for attr, value in item.iteritems():
                print '%s = %s' % (attr, value)
            print

    def show_commonrecipes_list(url):
        items = CommonRecipesListParser().parse(fetch(url))
        for item in items:
            for attr, value in item.iteritems():
                print '%s = %s' % (attr, value)
            print 

    def show_chineserecipes_list(url):
        items = ChineseRecipesListParser().parse(fetch(url))
        for item in items:
            for attr, value in item.iteritems():
                print '%s = %s' % (attr, value)
            print 

    def show_regionsnacks_list(url):
        items = RegionSnacksListParser().parse(fetch(url))
        for item in items:
            for attr, value in item.iteritems():
                print '%s = %s' % (attr, value)
            print 

    def show_foreignrecipes_list(url):
        items = ForeignRecipesListParser().parse(fetch(url))
        for item in items:
            for attr, value in item.iteritems():
                print '%s = %s' % (attr, value)
            print

    def show_bake_list(url):
        items = BakeListParser().parse(fetch(url))
        for item in items:
            for attr, value in item.iteritems():
                print '%s = %s' % (attr, value)
            print 

    url = "http://www.meishij.net/shicai/list.php?y=5"
    show_material_list(url)

    url = 'http://www.meishij.net/chufang/diy/'
    show_commonrecipes_list(url)

    url = 'http://www.meishij.net/china-food/caixi/'
    show_chineserecipes_list(url)

    url = 'http://www.meishij.net/china-food/xiaochi/'
    show_regionsnacks_list(url)

    url = 'http://www.meishij.net/chufang/diy/guowaicaipu1/'
    show_foreignrecipes_list(url)

    url = 'http://www.meishij.net/hongpei/'
    show_bake_list(url)

if False:
    for m in ('胡萝卜', '葡萄', '香菇', '猪肉'):
        show_food_material(m)
        print

    url = "http://www.meishij.net/shicai/shucai_list"
    show_material_list(url)

    url = "http://meishij.net/zuofa/huotuizhengluyu_1.html"
    show_food_recipe(url)

    url = 'http://www.meishij.net/shicai/'
    show_category_list(url)
