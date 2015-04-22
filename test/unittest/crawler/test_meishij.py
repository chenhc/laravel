#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   test_meishij.py
Author:     Chen Yanfei
@contact:   fasionchan@gmail.com
@version:   $Id$

Description:

Changelog:

'''

import pytest

import common

from crawler.utils import fetch
from crawler.items import FoodMaterialItem
from crawler.parsers.meishij import FoodMaterialParser

@pytest.fixture(scope='session')
def food_material_parser():
    return FoodMaterialParser()

class TestMeishij(object):

    @pytest.mark.parametrize(('url', 'expected'), (
        ('http://www.meishij.net/胡萝卜', FoodMaterialItem(
            name='胡萝卜',
            image_url='http://images.meishij.net/p/20111130/629aedacc88d9607d1d1caba2ec0af59_180x180.jpg',
            suit_ctcms='气虚质,气郁质,阳虚质',
            avoid_ctcms='湿热质'
            )),
        ('http://www.meishij.net/菠萝', FoodMaterialItem(
            name='菠萝',
            image_url='http://images.meishij.net/p/20120228/9b62ba3ffb7b6db3aabe3542219ad169_180x180.jpg',
            suit_ctcms='气虚质,气郁质,湿热质,痰湿质,平和质',
            avoid_ctcms='',
            )),
        ('http://www.meishij.net/香菇', FoodMaterialItem(
            name='香菇',
            image_url='http://images.meishij.net/p/20110722/3004a21d33be2257ee71323bdae37d62_180x180.jpg',
            suit_ctcms='平和质',
            avoid_ctcms='气虚质,气郁质,阳虚质,阴虚质',
            )),
        ))
    def test_food_material(self, food_material_parser, url, expected):
        response = fetch(url)
        for item in food_material_parser.parse(response):
            for attr, value in expected.iteritems():
                assert item[attr] == value
