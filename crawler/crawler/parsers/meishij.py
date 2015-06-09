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
        6. RecipeCategoryListParser
    菜谱列表页面解析器(解析对每种菜系类别(如:川菜)的具体菜谱列表页面，得到具体的菜谱名字(如:番茄炒西红柿)和url)
        7. RecipeListParser
    饮食健康标签下各种列表的解析器
        8. CrowdItemListParser # 人群类别列表解析器
        9. IllItemListParser   # 疾病类别列表解析器
        10. FunctionalityItemParser # 功能性调理类别列表解析器
        11. OrganItemListParser     # 脏腑调理类别列表解析器
'''

if __name__ == '__main__':
    import mainenv

import urlparse

from crawler.items import HackItem, PageItem, \
        FoodMaterialItem, MaterialCategoryEntryItem, MaterialEntryItem, \
        FoodRecipeItem, RecipeCategoryEntryItem, RecipeEntryItem, \
        RecipeCategoryDetailItem

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

        body = response.body
        body = body[body.find('icon_pr'):]
        body = body[body.find('<a'):]
        body = body[body.find('>')+1:]
        cook_time = body[:body.find('</a>')]

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
        try:
            difficulty, = div_info2.xpath('.//li[2]/div/a/text()').extract()
        except ValueError:
            difficulty = ""
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
        recipe['cook_time'] = cook_time

        # 简介
        briefs = response.xpath('//div[@class="materials"]/p/text()').extract()
        recipe['brief'] = '\n'.join([b.strip() for b in briefs]).encode('utf8')

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
        p_steps = div_measure.xpath('//div[@class="content clearfix"]/div[@class="c"]/p')
        if len(p_steps) == 0:
            p_steps = div_measure.xpath('//div[@class="edit"]/p')
        for p_step in p_steps:
            steps = p_step.xpath('./text()').extract()
            if not steps:
                steps = p_step.xpath('./img/@src').extract()
            for step in steps:
                step = step.strip().encode('utf8')
                procedure.append(step)
        recipe['procedure'] = '\n'.join(procedure)
        yield recipe

# 解析食材百科类别栏 得到每一个类别的名字(如:蔬菜)与对应的链接,对应的链接可用于每种食材类别页面解析的入口,也包括了维生素类别，体质类别的入口
class MaterialCategoryListParser(object):

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
                item = MaterialCategoryEntryItem()
                item['category'] = category.encode('utf8')
                item['url'] = url.encode('utf8')
                yield item

#parse 解析食材类别的页面(如：蔬菜，水果)，解析页面里面的每一个食材(如：菠菜，菠萝)的名字，类型，对应的链接,对应的链接可用于食材页面的解析
class MaterialListParser(object):

    def parse(self, response):
        # 食材子类别
        div_fliterstyle1 = response.xpath('//div[@class="fliterstyle1"]')
        for a in div_fliterstyle1.xpath('.//dd/a'):
            url, = a.xpath('./@href').extract()
            new_category, = a.xpath('./text()').extract()
            yield MaterialCategoryEntryItem(url=url.encode('utf8'),
                    category=new_category.encode('utf8'))

        # 食材类别
        div_other_c = response.xpath('//div[@class="other_c listnav_con clearfix"]')
        category = getattr(response.request, '_msj_cateogry', '')
        if not category:
            category, = div_other_c.xpath('//dd[@class="current"]//a/text()').extract()[:1] or ['']
            category = category.encode('utf8')

        # 食材列表
        div_listtyle1 = response.xpath('//div[@class="listtyle1"]')
        for l in div_listtyle1:
            # 类别
            item = MaterialEntryItem(category=category)

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
            yield PageItem(url=str(next_url), type=MaterialEntryItem,
                    kwargs=dict(category=category))


# 菜谱类别解析器
class RecipeCategoryListParser(object):

    def parse(self, response):
        menu_div = response.xpath('//div[@class="other_c listnav_con clearfix"]')
        if not len(menu_div):
            menu_div = response.xpath('//div[@class="listnav_con clearfix"]')

        for menu_dl in menu_div.xpath('./dl'):
            classification, = menu_dl.xpath('./dt/text()').extract()

            dds = menu_dl.xpath('./dd')
            for dd in dds:
                category, = dd.xpath('./a/text()').extract()
                url, = dd.xpath('./a/@href').extract()
                yield RecipeCategoryEntryItem(
                        classification=classification.encode('utf8'),
                        category=category.encode('utf8'),
                        url=url.encode('utf8'))


# 分析菜谱列表, 得到每一道菜的菜名以及url，url可是调用具体菜谱分析器进行分析
class RecipeListParser(object):

    def parse(self,response):
        # 菜谱的种类
        dl_style1 = response.xpath('//dl[@class="listnav_dl_style1 w990 bb1 clearfix"]')
        if len(dl_style1) ==0:
            dl_style1 = response.xpath('//dl[@class="listnav_dl_style1 w990 clearfix"]')

        category, = dl_style1.xpath('//dd[@class="current"]/h1/a/text()').extract()
        print category
        category = category.encode('utf8')

        # 菜谱列表
        div_listtyle1 = response.xpath('//div[@class="listtyle1"]')
        for l in div_listtyle1:
            # 类别
            item = RecipeEntryItem(category=category)

            # 名字
            name, = l.xpath('./a[@class="big"]/@title').extract()
            item['name'] = name.encode('utf8')

            # url
            url, = l.xpath('./a[@class="big"]/@href').extract()
            item['url'] = url.encode('utf8')
            yield item

        # 下一页解析,和食材页面的下一页的href有所不同
        page_w = response.xpath('//div[@class="listtyle1_page_w"]')
        result, = page_w.xpath('a[@class="next"]/@href').extract()
        result.strip()
        if result:
            next_url = result
            print next_url
            yield PageItem(url=str(next_url), type=RecipeCategoryEntryItem,
                    kwargs=dict(category=category))
        return


class FunctionalRecipeListParser(object):

    def parse(self, response):
        # 解析推荐的菜谱
        listnav = response.xpath("//dl[@class='listnav_dl_style1 w990 clearfix']")
        category, = listnav.xpath('./dd[@class="current"]/h1/a/text()').extract()
        category = category.strip().encode('utf8')

        main_w = response.xpath('//div[@class="main_w clearfix"]')
        listtyle1_list = main_w.xpath('//div[@id="listtyle1_list"] [@class="listtyle1_list clearfix"]')
        divs = listtyle1_list.xpath('./div')
        for div in divs:
            temp = div.xpath('./a/@title').extract()
            if len(temp):
                name = temp[0].encode('utf8')
            temp = div.xpath('./a/@href').extract()
            if len(temp):
                url = temp[0].encode('utf8')
            item = RecipeEntryItem()
            item['name'] = name
            item['url'] = url
            yield item

        # 下一页的解析
        next_url, = response.xpath('//a[@class="next"]/@href').extract()
        yield PageItem(url=str(next_url), type=RecipeEntryItem,
                kwargs=dict(category=category))


# 解析人群、疾病、功能、脏腑膳食页面的具体信息，得到各种适/忌的食材
class RecipeCategoryDetailParser(object):

    def parse(self, response):
        listnav = response.xpath("//dl[@class='listnav_dl_style1 w990 clearfix']")
        category, = listnav.xpath('./dd[@class="current"]/h1/a/text()').extract()
        category = category.strip().encode('utf8')

        main_w = response.xpath('//div[@class="main_w clearfix"]')
        slys_con = main_w.xpath('//div[@class="slys_con"]')
        brief, = slys_con.xpath('./p[@class="p1"]/text()').extract()
        brief = brief.strip().encode('utf8')

        # 解析推荐的tips 以及 不推荐的tips
        suit_tips = []
        avoid_tips = []

        p2s = slys_con.xpath('./p[@class="p2"]')

        for x in xrange(2):
            p2 = p2s[x]
            spans = p2.xpath('./span')
            for span in spans:
                tip, = span.xpath('./text()').extract()
                tip = tip.strip().encode('utf8')
                if x % 2:
                    suit_tips.append(tip)
                else:
                    avoid_tips.append(tip)

        avoid_tips = '\n'.join(avoid_tips)
        suit_tips = '\n'.join(suit_tips)

        # 解析适宜食用的食材
        suit_material_list = []
        avoid_material_list = []

        uls = slys_con.xpath('//ul[@class="clearfix"]')
        lis = uls[0].xpath('./li')

        for li in lis:
            temp = li.xpath('./a/strong/text()').extract()
            if len(temp):
                name = temp[0].encode('utf8')

            temp = li.xpath('./a/@href').extract()
            if len(temp):
                url = temp[0].encode('utf8')

            item = MaterialEntryItem()
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

            item = MaterialEntryItem()
            item['name'] = name
            item['url'] = url

            avoid_material_list.append(item)

        yield RecipeCategoryDetailItem(category=category, brief=brief,
                suit_tips=suit_tips, avoid_tips=avoid_tips,
                suit_material_list=suit_material_list,
                avoid_material_list=avoid_material_list)

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
        items = MaterialCategoryListParser().parse(fetch(url))
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

    def show_recipe_category_list(url):
        items = RecipeCategoryListParser().parse(fetch(url))
        for item in items:
            for attr, value in item.iteritems():
                print '%s = %s' % (attr, value)
            print


    def show_commonrecipe_category_list(url):
        items = CommonRecipeCategoryListParser().parse(fetch(url))
        for item in items:
            for attr, value in item.iteritems():
                print '%s = %s' % (attr, value)
            print

    def show_chineserecipe_category_list(url):
        items = ChineseRecipeCategoryListParser().parse(fetch(url))
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

    def show_foreignrecipe_category_list(url):
        items = ForeignRecipeCategoryListParser().parse(fetch(url))
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

    def show_recipe_category_detail(url):
        items = RecipeCategoryDetailParser().parse(fetch(url))
        for item in items:
            for attr, value in item.iteritems():
                if attr in ('suit_material_list', 'avoid_material_list'):
                    print '%s = ' % (attr,)
                    for material in value:
                        for mattr, mvalue in material.iteritems():
                            print '%s=%s' % (mattr, mvalue)
                    continue
                print '%s = %s' % (attr, value)
                print
            print

    def show_functional_recipe_list(url):
        items = FunctionalRecipeListParser().parse(fetch(url))
        for item in items:
            for attr, value in item.iteritems():
                print '%s = %s' % (attr, value)
            print

    for m in ('胡萝卜', '葡萄', '香菇', '猪肉'):
        show_food_material(m)
        print

if False:

    # 食谱总纲
    url = 'http://www.meishij.net/chufang/diy/'
    show_recipe_category_list(url)

    url = 'http://www.meishij.net/china-food/caixi/'
    show_recipe_category_list(url)

    url = 'http://www.meishij.net/china-food/xiaochi/'
    show_recipe_category_list(url)

    url = 'http://www.meishij.net/chufang/diy/guowaicaipu1/'
    show_recipe_category_list(url)

    url = 'http://www.meishij.net/hongpei/'
    show_recipe_category_list(url)

    url = "http://www.meishij.net/yaoshanshiliao/renqunshanshi/"
    show_recipe_category_list(url)

    url = 'http://www.meishij.net/yaoshanshiliao/jibingtiaoli/'
    show_recipe_category_list(url)

    url = 'http://www.meishij.net/yaoshanshiliao/gongnengxing/'
    show_recipe_category_list(url)

    url = 'http://www.meishij.net/yaoshanshiliao/zangfu/'
    show_recipe_category_list(url)

    # 功能性分类简介
    url = "http://www.meishij.net/yaoshanshiliao/renqunshanshi/yunfu/"
    show_recipe_category_detail(url)

    url = "http://www.meishij.net/yaoshanshiliao/jibingtiaoli/qianliexian/"
    show_recipe_category_detail(url)

    url = "http://www.meishij.net/yaoshanshiliao/gongnengxing/meirong/"
    show_recipe_category_detail(url)

    url = "http://www.meishij.net/yaoshanshiliao/zangfu/xintiaoli/"
    show_recipe_category_detail(url)

    # 食谱列表
    url = 'http://www.meishij.net/china-food/caixi/gangtai/'
    show_recipe_list(url)

    url = 'http://www.meishij.net/china-food/caixi/other/'
    show_recipe_list(url)

    url = 'http://www.meishij.net/china-food/caixi/gangtai/'
    show_recipe_list(url)

    # 功能食谱列表
    url = "http://www.meishij.net/yaoshanshiliao/renqunshanshi/yunfu/"
    show_functional_recipe_list_detail(url)

    url = "http://www.meishij.net/yaoshanshiliao/jibingtiaoli/qianliexian/"
    show_functional_recipe_list_detail(url)

    url = "http://www.meishij.net/yaoshanshiliao/gongnengxing/meirong/"
    show_functional_recipe_list_detail(url)

    url = "http://www.meishij.net/yaoshanshiliao/zangfu/xintiaoli/"
    show_functional_recipe_list_detail(url)

    # 食谱
    url = "http://meishij.net/zuofa/huotuizhengluyu_1.html"
    show_food_recipe(url)

    for m in ('胡萝卜', '葡萄', '香菇', '猪肉'):
        show_food_material(m)
        print

    # 食材列表
    url = 'http://www.meishij.net/shicai/shucai_list'
    show_material_list(url)

    url = 'http://www.meishij.net/shicai/xurou_list'
    show_material_list(url)

    url = 'http://www.meishij.net/shicai/gulei_list'
    show_material_list(url)

    url = 'http://www.meishij.net/shicai/sushishipin_list'
    show_material_list(url)

    url = 'http://www.meishij.net/shicai/list.php?y=5'
    show_material_list(url)

    url = 'http://www.meishij.net/shicai/list.php?y=15'
    show_material_list(url)

    # 食材分类列表
    url = 'http://www.meishij.net/shicai/'
    show_category_list(url)
