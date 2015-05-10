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

from crawler.items import HackItem, FoodMaterialItem, FoodRecipeItem,MaterialListItem


class HackParser(object):
    def parse(self, response):
        form = response.xpath('//form[@id="hack_form"]')
        print form.extract()
        verifycode_key, = form.xpath('./input[@name="verifycode_key"]/@value').extract()
        verifycode, = form.xpath('./input[@name="verifycode"]/@value').extract()
        verifycode_shicai, = form.xpath('./input[@name="verifycode_shicai"]/@value').extract()
        verify_shicai, = form.xpath('./input[@name="verify_shicai"]/@value').extract()
        img_src, = form.xpath('.//img/@src').extract()
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
                if attr is not None and value is not None:
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
            if attr is not None and value is not None:
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

#parse 分析食材百科页面 分析页面里面的每一个食材的名字，类型，对应的链接，以及得到食材页面下一页的链接，继续分析
class MaterialListParser(object):
    def parse(self,response):
        other_c = response.xpath('//div[@class="other_c listnav_con clearfix"]')
        #得到类型
        typename, = other_c.xpath('//dd[@class="current"]/h1/a/text()').extract()
        listtyle1 = response.xpath('//div[@class="listtyle1"]')
        for l in listtyle1:
            listitem = MaterialListItem()
            listitem['typename'] = typename.encode('utf8')
            name, = l.xpath('./div[@class="info1"]/h3/a/text()').extract()
            listitem['name'] = name.encode('utf8')
            url, = l.xpath('./div[@class="img"]/a/@href').extract()
            print url
            listitem['url'] = url
            rootpage = response.url.split(u'?',1)[0]
            page_w = response.xpath('//div[@class="listtyle1_page_w"]')
            nxt, = page_w.xpath('a[@class="next"]/@href').extract()
            url = response.url + nxt
            yield listitem
        #分割去除'?page=x'字段
        rootpage = response.url.split(u'?',1)[0]
        #print 'root',rootpage
        page_w = response.xpath('//div[@class="listtyle1_page_w"]')
        #得到下一页'?page=x+1' 字段
        nxt, = page_w.xpath('a[@class="next"]/@href').extract()
        #两个拼接
        url = rootpage + nxt
        #print 'url', url
        show_material_list(fetch(url))

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
            
    def show_food_recipe():
        url = "http://meishij.net/zuofa/huotuizhengluyu_1.html"
        item, = FoodRecipeParser().parse(fetch(url))
        for attr, value in item.iteritems():
            print '%s=%s' % (attr, value)
            print
   
    def show_material_list(response):
        items = MaterialListParser().parse(response)
        for item in items:
                print item['name']
                print item['typename']
                print item['url']
                print 


    #for m in ('香菇',):
    for m in ('胡萝卜', '葡萄', '香菇', '猪肉'):
        show_food_material(m)
        print

    url = "http://www.meishij.net/shicai/shucai_list"
    response = fetch(url)
    show_material_list(response)
    show_food_recipe()
