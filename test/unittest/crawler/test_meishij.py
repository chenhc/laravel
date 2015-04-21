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
            name='胡萝卜', suit_types='气虚质,气郁质,阳虚质',
            avoid_types='湿热质'
            )),
        ))
    def test_food_material(self, food_material_parser, url, expected):
        response = fetch(url)
        for item in food_material_parser.parse(response):
            for attr, value in expected.iteritems():
                assert item[attr] == value
