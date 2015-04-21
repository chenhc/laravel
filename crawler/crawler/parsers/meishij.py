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

from crawler.items import FoodMaterialItem

class FoodMaterialParser(object):
    def parse(self, response):
        response
        div_main = response.xpath('//div[@class="main"]')
        div_sc_header = div_main.xpath('.//div[@class="sc_header"]')
        div_sc_header_con1 = div_sc_header.xpath('.//div[@class="sc_header_con1"]')
        div_sc_header_con2 = div_sc_header.xpath('.//div[@class="sc_header_con2"]')
        name, = div_sc_header_con1.xpath('.//h1/text()').extract()
        suit_types = ','.join(div_sc_header_con2.xpath('.//li[@class="yi"]/a/text()').extract())
        avoid_types = ','.join(div_sc_header_con2.xpath('.//li[@class="ji"]/a/text()').extract())
        yield FoodMaterialItem(name=name.encode('utf8'),
                suit_types=suit_types.encode('utf8'),
                avoid_types=avoid_types.encode('utf8'))
