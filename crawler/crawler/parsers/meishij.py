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
Content Structure:
    反爬虫页面解析器
        1. HackParser
    食材页面解析器(解析每个食材具体的信息)
        2. FoodMaterialParser
    菜谱页面解析器(解析每个菜谱具体的信息）
        3. FoodRecipeParser
    食材类别解析器(解析各种食材类别，得到食材类别的名字(如:蔬菜)和对应的url)
        4. CategoryListParser
    食材列表页面解析器(解析对每个食材类别(如:蔬菜)的具体食材列表页面，得到具体食材的名字(如:花生)和url)
        5. MaterialListParser
    菜谱类别解析器(解析各种菜系(如:中华菜系),得到类别的名字(如:川菜)和对应的url)
        6. CommonRecipesCategoryListParser
        7. ChineseRecipeCategoryListParser
        8. RegionSnacksCategoryListParser
        9. ForignRercipesCategoryListParser
        10. BakeCategoryParser
    菜谱列表页面解析器(解析对每种菜系类别(如:川菜)的具体菜谱列表页面，得到具体的菜谱名字(如:番茄炒西红柿)和url)
        11. RecipeListParser
    饮食健康标签下各种列表的解析器
        12. CrowdItemListParser # 人群类别列表解析器
        13. IllItemListParser   # 疾病类别列表解析器
        14. FunctionalityItemParser # 功能性调理类别列表解析器
        15. OrganItemListParser     # 脏腑调理类别列表解析器  

'''

if __name__ == '__main__':
    import mainenv

import urlparse

from crawler.items import HackItem, PageItem, FoodMaterialItem, \
        FoodRecipeItem, ListItem, MaterialCategoryItem, \
        CommonRecipesCategoryListItem, ChineseRecipesCategoryListItem, RegionSnacksCategoryListItem, \
        ForeignRecipesCategoryListItem, BakeCategoryListItem, CrowdListItem, CrowdItem, \
        IllListItem, IllItem, FunctionalityListItem, FunctionalityItem, \
        OrganEfctListItem, OrganEfctItem, MaterialItem, RecipeItem

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
            item = ListItem(category=category)

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
            yield PageItem(url=str(next_url), type=ListItem,
                    kwargs=dict(category=category))

# 解析家常菜谱列表，得到各种菜（如：家常菜 私家菜）的页面链接
class CommonRecipesCategoryListParser(object):

    def parse(self, response):
        main_w = response.xpath('//div[@class="main_w clearfix"]')
        listnav = response.xpath('//dl[@class="listnav_dl_style1 w990 bb1 clearfix"]')
        dds = listnav.xpath('./dd')
        for dd in dds:
            name, = dd.xpath('./a/text()').extract()
            url, = dd.xpath('./a/@href').extract()
            yield CommonRecipesCategoryListItem(name = name, url = url)

# 解析中华菜系的列表，得到各种菜系（如：川菜 粤菜）的页面链接
class ChineseRecipesCategoryListParser(object):

    def parse(self, response):
        listnav = response.xpath('//dl[@class="listnav_dl_style1 w990 clearfix"]')
        dds = listnav.xpath('./dd')
        for dd in dds:
            name, = dd.xpath('./a/text()').extract()
            url, = dd.xpath('./a/@href').extract()
            yield ChineseRecipesCategoryListItem(name = name, url = url)

# 解析地方小吃的列表，得到各地小吃的页面链接
class RegionSnacksCategoryListParser(object):
    
    def parse(self, response):
        listnav = response.xpath('//dl[@class="listnav_dl_style1 w990 clearfix"]')
        dds = listnav.xpath('./dd')
        for dd in dds:
            region, = dd.xpath('./a/text()').extract()
            url, = dd.xpath('./a/@href').extract()
            yield RegionSnacksCategoryListItem(region = region, url = url)

# 解析外国菜谱的列表，得到各个国家菜谱的页面链接
class ForeignRecipesCategoryListParser(object):

    def parse(self, response):
        listnav = response.xpath('//dl[@class="listnav_dl_style1 w990 bb1 clearfix"]')
        dds = listnav.xpath('./dd')
        for dd in dds:
            country, = dd.xpath('./a/text()').extract()
            url, = dd.xpath('./a/@href').extract()
            yield ForeignRecipesCategoryListItem(country = country, url = url)

# 解析烘焙的列表，得到烘焙相关的页面链接
class BakeCategoryListParser(object):
        
    def parse(self, response):
        listnav = response.xpath('//dl[@class="listnav_dl_style1 w990 clearfix"]')
        dds = listnav.xpath('./dd')
        for dd in dds:
            name, = dd.xpath('./a/text()').extract()
            # 烘陪工具不需要解析
            if name.rfind(u"工具") != -1:
                continue
            url, = dd.xpath('./a/@href').extract()
            yield BakeCategoryListItem(name = name, url = url)

# 分析菜谱列表, 得到每一道菜的菜名以及url，url可是调用具体菜谱分析器进行分析
class RecipeListParser(object):
 
    def parse(self,response):
        # 菜谱的种类
        dl_style1 = response.xpath('//dl[@class="listnav_dl_style1 w990 bb1 clearfix"]')

        category, = dl_style1.xpath('//dd[@class="current"]//a/text()').extract()
        category = category.encode('utf8')

        # 菜谱列表
        div_listtyle1 = response.xpath('//div[@class="listtyle1"]')
        for l in div_listtyle1:
            # 类别
            item = ListItem(category=category)

            # 名字
            name, = l.xpath('./a[@class="big"]/@title').extract()
            item['name'] = name.encode('utf8')

            # url
            url, = l.xpath('./a[@class="big"]/@href').extract()
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
            yield PageItem(url=str(next_url), type=ListItem,
                    kwargs=dict(category=category))


class CrowdItemListParser(object):

    def parse(self, response):
        dds = response.xpath("//dl[@class='listnav_dl_style1 w990 clearfix']/dd")
        for dd in dds:
            crowd, = dd.xpath('./a/text()').extract()
            crowd = crowd.encode('utf8')
            url, = dd.xpath('./a/@href').extract()
            url = url.encode('utf8')
            yield CrowdListItem(crowd = crowd, url = url)

# 解析人群膳食页面的各个人群的具体信息，得到各种人群适/忌的食材和适合的食谱
class CrowdItemParser(object):

    def parse(self, response):
        listnav = response.xpath("//dl[@class='listnav_dl_style1 w990 clearfix']")
        crowd, = listnav.xpath('./dd[@class="current"]/h1/a/text()').extract()
        crowd = crowd.encode('utf8')
        main_w = response.xpath('//div[@class="main_w clearfix"]')
        slys_con = main_w.xpath('//div[@class="slys_con"]')
        p2s = slys_con.xpath('./p[@class="p2"]')
        suit_tips = []
        suit_material_list = []
        avoid_tips = []
        avoid_material_list = []
        suit_recipe_list = []
        # 解析推荐的tips 以及 不推荐的tips
        for x in xrange(2):
            p2 = p2s[x]
            spans = p2.xpath('./span')
            for span in spans:
                tip, = span.xpath('./text()').extract()
                tip = tip.encode('utf8')
                if x % 2:
                    suit_tips.append(tip)
                else:
                    avoid_tips.append(tip)
        # 解析适宜食用的食材
        uls = slys_con.xpath('//ul[@class="clearfix"]')
        lis = uls[0].xpath('./li')
        for li in lis:
            temp = li.xpath('./a/strong/text()').extract()
            if len(temp):
                name = temp[0].encode('utf8')
            temp = li.xpath('./a/@href').extract()
            if len(temp):
                url = temp[0].encode('utf8')
            item = MaterialItem()
            item['name'] = name
            item['url'] = url
            suit_material_list.append(item)
        # 解析禁忌食用的食材
        lis = uls[1].xpath('./li') 
        for li in lis:
            temp = li.xpath('./a/strong/text()').extract()
            if len(temp):
                name = temp[0].encode('utf8')
            temp = li.xpath('./a/@href').extract()
            if len(temp):
                url = temp[0].encode('utf8')
            item = MaterialItem()
            item['name'] = name
            item['url'] = url
            avoid_material_list.append(item)
        # 解析推荐的菜谱
        listtyle1_list = main_w.xpath('//div[@id="listtyle1_list"] [@class="listtyle1_list clearfix"]')
        divs = listtyle1_list.xpath('./div')
        for div in divs:
            temp = div.xpath('./a/@title').extract()
            if len(temp):
                name = temp[0].encode('utf8')
            temp = div.xpath('./a/@href').extract()
            if len(temp):
                url = temp[0].encode('utf8')
            item = RecipeItem()
            item['name'] = name
            item['url'] = url
            suit_recipe_list.append(item)
            # 下一页的解析
            pageitem = PageItem()
            url, = response.xpath('//a[@class="next"]/@href').extract()
            pageitem['url'] = url
            pageitem['type'] = CrowdItem
            pageitem['kwargs'] = crowd

        yield CrowdItem(crowd = crowd,suit_tips = suit_tips, avoid_tips = avoid_tips, suit_material_list = suit_material_list, \
                avoid_material_list = avoid_material_list, suit_recipe_list = suit_recipe_list, nxtpage = pageitem)

class IllItemListParser(object):

    def parse(self, response):
        dds = response.xpath("//dl[@class='listnav_dl_style1 w990 clearfix']/dd")
        for dd in dds:
            ill, = dd.xpath('./a/text()').extract()
            ill = ill.encode('utf8')
            url, = dd.xpath('./a/@href').extract()
            url = url.encode('utf8')
            yield IllListItem(ill = ill, url = url)

# 解析疾病调理页面里面每个疾病的具体信息，得到各种病患者适/忌的食材和适合的食谱
class IllItemParser(object):

    def parse(self, response):
        listnav = response.xpath("//dl[@class='listnav_dl_style1 w990 clearfix']")
        ill, = listnav.xpath('./dd[@class="current"]/h1/a/text()').extract()
        ill = ill.encode('utf8')
        main_w = response.xpath('//div[@class="main_w clearfix"]')
        slys_con = main_w.xpath('//div[@class="slys_con"]')
        p2s = slys_con.xpath('./p[@class="p2"]')
        suit_tips = []
        suit_material_list = []
        avoid_tips = []
        avoid_material_list = []
        suit_recipe_list = []
        for x in xrange(2):
            p2 = p2s[x]
            spans = p2.xpath('./span')
            for span in spans:
                tip, = span.xpath('./text()').extract()
                tip = tip.encode('utf8')
                if x % 2:
                    suit_tips.append(tip)
                else:
                    avoid_tips.append(tip)

        uls = slys_con.xpath('//ul[@class="clearfix"]')
        lis = uls[0].xpath('./li')
        for li in lis:
            temp = li.xpath('./a/strong/text()').extract()
            if len(temp):
                name = temp[0].encode('utf8')
            temp = li.xpath('./a/@href').extract()
            if len(temp):
                url = temp[0].encode('utf8')
            item = MaterialItem()
            item['name'] = name
            item['url'] = url
            suit_material_list.append(item)
        lis = uls[1].xpath('./li') 
        for li in lis:
            temp = li.xpath('./a/strong/text()').extract()
            if len(temp):
                name = temp[0].encode('utf8')
            temp = li.xpath('./a/@href').extract()
            if len(temp):
                url = temp[0].encode('utf8')
            item = MaterialItem()
            item['name'] = name
            item['url'] = url
            avoid_material_list.append(item)
        listtyle1_list = main_w.xpath('//div[@id="listtyle1_list"] [@class="listtyle1_list clearfix"]')
        divs = listtyle1_list.xpath('./div')
        for div in divs:
            temp = div.xpath('./a/@title').extract()
            if len(temp):
                name = temp[0].encode('utf8')
            temp = div.xpath('./a/@href').extract()
            if len(temp):
                url = temp[0].encode('utf8')
            item = RecipeItem()
            item['name'] = name
            item['url'] = url
            suit_recipe_list.append(item)
            # 下一页的解析
            pageitem = PageItem()
            url, = response.xpath('//a[@class="next"]/@href').extract()
            pageitem['url'] = url
            pageitem['type'] = ill
            pageitem['kwargs'] = IllItem

        yield IllItem(ill = ill,suit_tips = suit_tips, avoid_tips = avoid_tips, suit_material_list = suit_material_list, \
                avoid_material_list = avoid_material_list, suit_recipe_list = suit_recipe_list, nxtpage = pageitem)

class FunctionalityItemListParser(object):

    def parse(self, response):
        dds = response.xpath("//dl[@class='listnav_dl_style1 w990 clearfix']/dd")
        for dd in dds:
            functionality, = dd.xpath('./a/text()').extract()
            functioality = functionality.encode('utf8')
            url, = dd.xpath('./a/@href').extract()
            url = url.encode('utf8')
            yield FunctionalityListItem(functionality = functionality, url = url)

# 解析功能性调理页面里面每个功能性的具体信息，得到各种功效性适/忌的食材和适合的食谱
class FunctionalityItemParser(object):
    def parse(self, response):
        listnav = response.xpath("//dl[@class='listnav_dl_style1 w990 clearfix']")
        functionality, = listnav.xpath('./dd[@class="current"]/h1/a/text()').extract()
        functionality = functionality.encode('utf8')
        main_w = response.xpath('//div[@class="main_w clearfix"]')
        slys_con = main_w.xpath('//div[@class="slys_con"]')
        p2s = slys_con.xpath('./p[@class="p2"]')
        suit_tips = []
        suit_material_list = []
        avoid_tips = []
        avoid_material_list = []
        suit_recipe_list = []
        for x in xrange(2):
            p2 = p2s[x]
            spans = p2.xpath('./span')
            for span in spans:
                tip, = span.xpath('./text()').extract()
                tip = tip.encode('utf8')
                if x % 2:
                    suit_tips.append(tip)
                else:
                    avoid_tips.append(tip)

        uls = slys_con.xpath('//ul[@class="clearfix"]')
        lis = uls[0].xpath('./li')
        for li in lis:
            temp = li.xpath('./a/strong/text()').extract()
            if len(temp):
                name = temp[0].encode('utf8')
            temp = li.xpath('./a/@href').extract()
            if len(temp):
                url = temp[0].encode('utf8')
            item = MaterialItem()
            item['name'] = name
            item['url'] = url
            suit_material_list.append(item)
        lis = uls[1].xpath('./li') 
        for li in lis:
            temp = li.xpath('./a/strong/text()').extract()
            if len(temp):
                name = temp[0].encode('utf8')
            temp = li.xpath('./a/@href').extract()
            if len(temp):
                url = temp[0].encode('utf8')
            item = MaterialItem()
            item['name'] = name
            item['url'] = url
            avoid_material_list.append(item)
        listtyle1_list = main_w.xpath('//div[@id="listtyle1_list"] [@class="listtyle1_list clearfix"]')
        divs = listtyle1_list.xpath('./div')
        for div in divs:
            temp = div.xpath('./a/@title').extract()
            if len(temp):
                name = temp[0].encode('utf8')
            temp = div.xpath('./a/@href').extract()
            if len(temp):
                url = temp[0].encode('utf8')
            item = RecipeItem()
            item['name'] = name
            item['url'] = url
            suit_recipe_list.append(item)
            # 下一页的解析
            pageitem = PageItem()
            url, = response.xpath('//a[@class="next"]/@href').extract()
            pageitem['url'] = url
            pageitem['type'] = FunctionalityItem
            pageitem['kwargs'] = functionality

        yield FunctionalityItem(functionality = functionality,suit_tips = suit_tips, avoid_tips = avoid_tips, \
                suit_material_list = suit_material_list, avoid_material_list = avoid_material_list, \
                suit_recipe_list = suit_recipe_list, nxtpage = pageitem)


class OrganItemListParser(object):
    
    def parse(self, response):
        dds = response.xpath("//dl[@class='listnav_dl_style1 w990 clearfix']/dd")
        for dd in dds:
            effect, = dd.xpath('./a/text()').extract()
            effect = effect.encode('utf8')
            url, = dd.xpath('./a/@href').extract()
            url = url.encode('utf8')
            yield OrganEfctListItem(effect = effect, url = url)

# 解析脏腑调理页面里面每个脏腑功效的具体信息，得到各种脏腑调理适/禁的食材和适合的食谱
class OrganItemParser(object):

    def parse(self, response):
        listnav = response.xpath("//dl[@class='listnav_dl_style1 w990 clearfix']")
        effect, = listnav.xpath('./dd[@class="current"]/h1/a/text()').extract()
        main_w = response.xpath('//div[@class="main_w clearfix"]')
        slys_con = main_w.xpath('//div[@class="slys_con"]')
        p2s = slys_con.xpath('./p[@class="p2"]')
        suit_tips = []
        suit_material_list = []
        avoid_tips = []
        avoid_material_list = []
        suit_recipe_list = []
        for x in xrange(2):
            p2 = p2s[x]
            spans = p2.xpath('./span')
            for span in spans:
                tip, = span.xpath('./text()').extract()
                tip.encode('utf8')
                if x % 2:
                    suit_tips.append(tip)
                else:
                    avoid_tips.append(tip)

        uls = slys_con.xpath('//ul[@class="clearfix"]')
        lis = uls[0].xpath('./li')
        for li in lis:
            temp = li.xpath('./a/strong/text()').extract()
            if len(temp):
                name = temp[0].encode('utf8')
            temp = li.xpath('./a/@href').extract()
            if len(temp):
                url = temp[0].encode('utf8')
            temp = li.xpath('./a/@href').extract()
            item = MaterialItem()
            item['name'] = name
            item['url'] = url
            suit_material_list.append(item)
        lis = uls[1].xpath('./li') 
        for li in lis:
            temp = li.xpath('./a/strong/text()').extract()
            if len(temp):
                name = temp[0].encode('utf8')
            temp = li.xpath('./a/@href').extract()
            if len(temp):
                url = temp[0].encode('utf8')
            item = MaterialItem()
            item['name'] = name
            item['url'] = url
            avoid_material_list.append(item)
        listtyle1_list = main_w.xpath('//div[@id="listtyle1_list"] [@class="listtyle1_list clearfix"]')
        divs = listtyle1_list.xpath('./div')
        for div in divs:
            temp = div.xpath('./a/@title').extract()
            if len(temp):
                name = temp[0].encode('utf8')
            temp = div.xpath('./a/@href').extract()
            if len(temp):
                url = temp[0].encode('utf8')
            item = RecipeItem()
            item['name'] = name
            item['url'] = url
            suit_recipe_list.append(item)
            # 下一页的解析
            pageitem = PageItem()
            url, = response.xpath('//a[@class="next"]/@href').extract()
            pageitem['url'] = url
            pageitem['type'] = OrganEfctItem
            pageitem['kwargs'] = effect

        yield OrganEfctItem(effect = effect, suit_tips = suit_tips, avoid_tips = avoid_tips, suit_material_list = suit_material_list, \
                avoid_material_list = avoid_material_list, suit_recipe_list = suit_recipe_list, nxtpage = pageitem)

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

    def show_recipe_list(url):
        items = RecipeListParser().parse(fetch(url))
        for item in items:
            for attr, value in item.iteritems():
                print '%s=%s' % (attr, value)
            print 
    
    def show_commonrecipes_category_list(url):
        items = CommonRecipesCategoryListParser().parse(fetch(url))
        for item in items:
            for attr, value in item.iteritems():
                print '%s = %s' % (attr, value)
            print 

    def show_chineserecipes_category_list(url):
        items = ChineseRecipesCategoryListParser().parse(fetch(url))
        for item in items:
            for attr, value in item.iteritems():
                print '%s = %s' % (attr, value)
            print 

    def show_regionsnacks_category_list(url):
        items = RegionSnacksCategoryListParser().parse(fetch(url))
        for item in items:
            for attr, value in item.iteritems():
                print '%s = %s' % (attr, value)
            print 

    def show_foreignrecipes_category_list(url):
        items = ForeignRecipesCategoryListParser().parse(fetch(url))
        for item in items:
            for attr, value in item.iteritems():
                print '%s = %s' % (attr, value)
            print

    def show_bake_category_list(url):
        items = BakeCategoryListParser().parse(fetch(url))
        for item in items:
            for attr, value in item.iteritems():
                print '%s = %s' % (attr, value)
            print 

    def show_crowditem(url):
        items = CrowdItemParser().parse(fetch(url))
        for item in items:
            for attr, value in item.iteritems():
                print '%s = %s' % (attr, value)
                print 
            print

    def show_illitem(url):
        items = IllItemParser().parse(fetch(url))
        for item in items:
            for attr, value in item.iteritems():
                print '%s = %s' % (attr, value)
                print 
            print
            
    def show_functionalityitem(url):
        items = FunctionalityItemParser().parse(fetch(url))
        for item in items:
            for attr, value in item.iteritems():
                print '%s = %s' % (attr, value)
                print 
            print

    def show_organefctitem(url):
        items = OrganItemParser().parse(fetch(url))
        for item in items:
            for attr, value in item.iteritems():
                print '%s = %s' % (attr, value)
                print 
            print

    def show_crowd_list_item(url):
        items = CrowdItemListParser().parse(fetch(url))
        for item in items:
            for attr, value in item.iteritems():
                print '%s = %s' % (attr, value)
            print
    
    def show_ill_list_item(url):
        items = IllItemListParser().parse(fetch(url))
        for item in items:
            for attr, value in item.iteritems():
                print '%s = %s' % (attr, value)
            print
                
    def show_functionality_list_item(url):
        items = FunctionalityItemListParser().parse(fetch(url))
        for item in items:
            for attr, value in item.iteritems():
                print '%s = %s' % (attr, value)
            print

    def show_organefct_list_item(url):
        items = OrganItemListParser().parse(fetch(url))
        for item in items:
            for attr, value in item.iteritems():
                print '%s = %s' % (attr, value)
            print



    url = 'http://www.meishij.net/chufang/diy/jiangchangcaipu/'
    show_recipe_list(url)

if False:
    
    url = "http://www.meishij.net/yaoshanshiliao/renqunshanshi/yunfu/"
    show_crowditem(url)
    
    url = "http://www.meishij.net/yaoshanshiliao/jibingtiaoli/qianliexian/"
    show_illitem(url)

    url = "http://www.meishij.net/yaoshanshiliao/gongnengxing/meirong/"
    show_functionalityitem(url)

    url = "http://www.meishij.net/yaoshanshiliao/zangfu/xintiaoli/"
    show_organefctitem(url)
    
    url = "http://www.meishij.net/yaoshanshiliao/renqunshanshi/"
    show_crowd_list_item(url)
    
    url = "http://www.meishij.net/yaoshanshiliao/jibingtiaoli/"
    show_ill_list_item(url)

    url = "http://www.meishij.net/yaoshanshiliao/gongnengxing/"
    show_functionality_list_item(url)

    url = "http://www.meishij.net/yaoshanshiliao/zangfu/"
    show_organefct_list_item(url)

    for m in ('胡萝卜', '葡萄', '香菇', '猪肉'):
        show_food_material(m)
        print

    url = "http://www.meishij.net/shicai/shucai_list"
    show_material_list(url)

    url = "http://meishij.net/zuofa/huotuizhengluyu_1.html"
    show_food_recipe(url)

    url = 'http://www.meishij.net/shicai/'
    show_category_list(url)

    url = "http://www.meishij.net/shicai/list.php?y=5"         
    show_material_list(url)

    url = 'http://www.meishij.net/chufang/diy/'
    show_commonrecipes_category_list(url)

    url = 'http://www.meishij.net/china-food/caixi/'
    show_chineserecipes_category_list(url)

    url = 'http://www.meishij.net/china-food/xiaochi/'
    show_regionsnacks_category_list(url)

    url = 'http://www.meishij.net/chufang/diy/guowaicaipu1/'
    show_foreignrecipes_category_list(url)

    url = 'http://www.meishij.net/hongpei/'
    show_bake_category_list(url)

    url = "http://meishij.net/zuofa/huotuizhengluyu_1.html"
    show_food_recipe(url)
