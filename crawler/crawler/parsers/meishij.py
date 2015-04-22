#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   meishij.py
Author:     Chen Yanfei
@contact:   fasionchan@gmail.com
@version:   $Id$

Description:

Changelog:

'''

if __name__ == '__main__':
    import mainenv

from crawler.items import FoodMaterialItem

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
            attr, value = record.split(u'：', 1)
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

        yield FoodMaterialItem(name=name.encode('utf8'),
                image_url=image_url,
                suit_mix=suit_mix.encode('utf8'),
                avoid_mix=avoid_mix.encode('utf8'),
                suit_ctcms=suit_types.encode('utf8'),
                avoid_ctcms=avoid_types.encode('utf8'), **attrs)

if __name__ == '__main__':
    from crawler.utils import fetch

    def show_food_material(name):
        url = 'http://www.meishij.net/%s' % (name,)
        item, = FoodMaterialParser().parse(fetch(url))
        for attr, value in item.iteritems():
            print '%s=%s' % (attr, value)
            print


    #for m in ('香菇',):
    for m in ('胡萝卜', '葡萄', '香菇', '猪肉'):
        show_food_material(m)
        print
