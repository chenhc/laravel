#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   meishiji.py
Author:     Chen Yanfei
            Liu dongqiang
@contact:   fasionchan@gmail.com
            18819451607@163.com
@version:   $Id$

Description:

Changelog:

'''

import sys
import time
import socket
import random
import hashlib
import requests
import collections
from scrapy import log
from scrapy.spider import Spider
from scrapy.http import Request

from crawler.items import PageItem, \
        CategoryMaterialPairItem, CategoryRecipePairItem, \
        RecipeClassificationCategoryPairItem
from crawler.parsers.meishij import HackParser, MaterialCategoryListParser, \
        MaterialListParser, FoodMaterialParser, \
        RecipeCategoryListParser, RecipeListParser, FoodRecipeParser, \
        EffectDetailParser, EffectRecipeListParser
from crawler.data.jpg_set import jpg_set

def random_ip():
    ip = ''.join([chr(random.randint(0, 255)) for x in xrange(4)])
    return socket.inet_ntoa(ip)

def check_response(func):
    def handler(self, response):
        if response.url == self.page404_url:
            return

        if response.url == self.hack_url:
            print response.request.meta.redirect_urls
            raw_input('hack')
            self.parse_hack(response)
            return

        for item in func(self, response):
            yield item

    return handler


class MeishijSpider(Spider):

    name = 'meishij'

    display_url = 'http://www.meishij.net/hack/display.php'
    page404_url = 'http://www.meishij.net/404.php'
    hack_url = 'http://www.meishij.net/hack/hack.php'

    food_material_category_list_url = 'http://www.meishij.net/shicai/'

    homely_recipe_category_list_url = 'http://www.meishij.net/chufang/diy/'
    chinese_recipe_category_list_url = 'http://www.meishij.net/china-food/caixi/'
    snack_recipe_category_list_url = 'http://www.meishij.net/china-food/xiaochi/'
    foreign_recipe_category_list_url = 'http://www.meishij.net/chufang/diy/guowaicaipu1/'
    bake_recipe_category_list_url = 'http://www.meishij.net/hongpei/'

    recipe_category_list_urls = set([homely_recipe_category_list_url,
        chinese_recipe_category_list_url, foreign_recipe_category_list_url,
        snack_recipe_category_list_url, bake_recipe_category_list_url])

    crowd_recipe_list_url = 'http://www.meishij.net/yaoshanshiliao/renqunshanshi/'
    disease_recipe_list_url = 'http://www.meishij.net/yaoshanshiliao/jibingtiaoli/'
    functional_recipe_list_url = 'http://www.meishij.net/yaoshanshiliao/gongnengxing/'
    organ_recipe_list_url = 'http://www.meishij.net/yaoshanshiliao/zangfu/'

    effect_recipe_category_list_urls = set([crowd_recipe_list_url,
        disease_recipe_list_url, functional_recipe_list_url,
        organ_recipe_list_url])

    start_urls = [
        #hack_url,

        #food_material_category_list_url,

        x for x in list(recipe_category_list_urls) + list(effect_recipe_category_list_urls)
        #x for x in list(effect_recipe_category_list_urls)
        #x for x in list(recipe_category_list_urls)
    ]

    def __init__(self, *args, **kwargs):
        super(MeishijSpider, self).__init__(*args, **kwargs)

        self.seen_urls = set()
        self.request_queue = collections.deque()

        self.hack_parser = HackParser()

        self.material_category_list_parser = MaterialCategoryListParser()
        self.material_list_parser = MaterialListParser()
        self.food_material_parser = FoodMaterialParser()

        self.recipe_category_list_parser = RecipeCategoryListParser()
        self.recipe_list_parser = RecipeListParser()
        self.effect_recipe_list_parser = EffectRecipeListParser()
        self.effect_detail_parser = EffectDetailParser()
        self.food_recipe_parser = FoodRecipeParser()

    def enqueue_request(self, request):
        url = str(request.url.strip())
        if url not in self.seen_urls:
            self.request_queue.append(request)
            self.seen_urls.add(url)

    def handler_hack(self, hack):
        headers = {'Referer': self.hack_url}

        display_php = requests.get(self.display_url, headers=headers).content
        code, yes, no = display_php.strip().split(';')[:3]

        _, code = code.split('=')
        code = code.strip()

        _, yes = yes.split("'")[:2]
        yes = yes.replace('code_', '')

        _, no = no.split("'")[:2]
        no = no.replace('code_', '')

        data = {
            'verifycode_key': hack['verifycode_key'],
            'verifycode_shicai': hack['verifycode_shicai'],
            'verify_shicai': code,
        }

        jpg = requests.get(hack['img_src'], headers=headers).content
        jpg_hash = hashlib.md5(jpg).hexdigest()
        jpg_type = jpg_set.get(jpg_hash)
        if not jpg_type:
            log.msg('[HACK][new] hash=%s' % (jpg_hash,), log.CRITICAL)
            while raw_input('continue(yes/no)? ').strip() != 'yes': pass

        dst_type = hack['verifycode_shicai']
        if jpg_type == dst_type:
            data['verifycode'] = yes
            log.msg('[HACK][yes] hash=%s %s==%s' %
                    (jpg_hash, jpg_type, dst_type), log.CRITICAL)
        else:
            data['verifycode'] = no
            log.msg('[HACK][no] hash=%s %s!=%s' %
                    (jpg_hash, jpg_type, dst_type), log.CRITICAL)

        res = requests.post(self.hack_url, data=data, headers=headers)
        print res
        print res.content

    def parse_hack(self, response):
        log.msg('[PARSE][hack] url=%s' % (response.url,), log.INFO)

        for item in self.hack_parser.parse(response):
            self.handler_hack(item)

    @check_response
    def parse_material_category_list(self, response):
        log.msg('[PARSE][category_list] url=%s' % (response.url,), log.INFO)

        for item in self.material_category_list_parser.parse(response):
            url = item['url']
            category = item['category']

            headers = {'X-Forwarded-For': random_ip()}
            request = Request(url, callback=self.parse_material_list,
                    headers=headers)
            request._msj_category = category
            yield request

            #self.enqueue_request(request)

            log.msg('[ENQUEUE][material_list] category=%s url=%s' %
                    (category, url), log.INFO)

    @check_response
    def parse_material_list(self, response):
        log.msg('[PARSE][material list] url=%s' % (response.url,), log.INFO)

        if response.url == self.food_material_category_list_url:
            log.msg('[PARSE][ignore] url=%s' % (response.url,), log.WARNING)
            return

        for item in self.material_list_parser.parse(response):
            if isinstance(item, PageItem):
                url = item['url']
                category = response.request._msj_category

                headers = {'X-Forwarded-For': random_ip()}
                request = Request(url, callback=self.parse_material_list,
                        headers=headers)
                request._msj_category = category
                yield request

                #self.enqueue_request(request)

                log.msg('[ENQUEUE][material_list] category=%s url=%s' %
                        (category, url), log.INFO)

                continue

            if isinstance(item, MaterialCategoryEntryItem):
                url = item['url']
                category = item['category']

                headers = {'X-Forwarded-For': random_ip()}
                request = Request(url, callback=self.parse_material_list,
                        headers=headers)
                request._msj_category = category
                yield request

                log.msg('[ENQUEUE][material_list] category=%s url=%s' %
                        (category, url), log.INFO)

                continue

            url = item['url']
            name = item['name']
            category = response.request._msj_category

            yield CategoryMaterialPairItem(category=category, material=name)

            log.msg('[PIPE][category_material_pair] category=%s material=%s' %
                    (category, name), log.INFO)


            headers = {'X-Forwarded-For': random_ip()}
            request = Request(url, callback=self.parse_food_material,
                    headers=headers)
            request._msj_category = category
            yield request

            #self.enqueue_request(request)

            log.msg('[ENQUEUE][food_material] category=%s url=%s' %
                    (category, url), log.INFO)

    @check_response
    def parse_food_material(self, response):
        log.msg('[PARSE][food_material] url=%s' % (response.url,), log.INFO)

        category = response.request._msj_category
        for item in self.food_material_parser.parse(response):
            item['category'] = category

            name = item['name']
            log.msg('[PIPE][food_material] name=%s category=%s' %
                    (name, category), log.INFO)

            yield item

    @check_response
    def parse_recipe_category_list(self, response):
        log.msg('[PARSE][recipe_category_list url=%s' % (response.url,),log.INFO)

        for item in self.recipe_category_list_parser.parse(response):
            url = item['url']
            classification = item['classification']
            category = item['category']

            yield RecipeClassificationCategoryPairItem(
                    classification=classification, category=category)

            callback = self.parse_recipe_list
            if getattr(response, '_msj_is_effect', False):
                callback = self.parse_effect_recipe_detail_and_list

            headers = {'X-Farwarded-For': random_ip()}
            request = Request(url, callback=callback, headers=headers)
            request._msj_category = category
            yield request

            log.msg('[ENQUEUE][material_list] category=%s url=%s' %
                (category, url,), log.INFO)

    @check_response
    def parse_recipe_list(self, response):
        log.msg('[PARSE][recipe_list] url=%s' %(response.url), log.INFO)

        category = response.request._msj_category
        for item in self.recipe_list_parser.parse(response):
            if isinstance(item, PageItem):
                url = item['url']
                headers = {'X-Forwarded-For': random_ip()}
                request = Request(url, callback=self.parse_recipe_list,
                        headers=headers)
                request._msj_category = category
                yield request

                log.msg('[ENQUEUE][recipes_list] category=%s url=%s' %
                        (category, url), log.INFO)

                continue

            yield CategoryRecipePairItem(category=category, recipe=item['name'])

            url = item['url']
            name = item['name']
            headers = {'X-Forwarded-For': random_ip()}
            request = Request(url, callback=self.parse_food_recipe,
                    headers=headers)
            request._msj_category  = category

            yield request

            log.msg('[PARSE][food_recipe] category=%s url=%s' %
                    (category, url ), log.INFO)

    @check_response
    def parse_effect_recipe_detail_and_list(self, response):
        for item in self.effect_detail_parser.parse(response):
            if not item.get('category'):
                item['category'] = response.request._msj_category
            yield item

        for item in self.parse_effect_recipe_list(response):
            yield item

    @check_response
    def parse_effect_recipe_list(self, response):
        log.msg('[PARSE][recipe_list] url=%s' %(response.url), log.INFO)

        category = response.request._msj_category
        for item in self.recipe_list_parser.parse(response):
            if isinstance(item, PageItem):
                url = item['url']
                headers = {'X-Forwarded-For': random_ip()}
                request = Request(url, callback=self.parse_effect_recipe_list,
                        headers=headers)
                request._msj_category = category
                yield request

                log.msg('[ENQUEUE][recipes_list] category=%s url=%s' %
                        (category, url), log.INFO)

                continue

            yield CategoryRecipePairItem(category=category, recipe=item['name'])

            url = item['url']
            name = item['name']
            headers = {'X-Forwarded-For': random_ip()}
            request = Request(url, callback=self.parse_food_recipe,
                    headers=headers)
            request._msj_category  = category

            yield request

            log.msg('[PARSE][food_recipe] category=%s url=%s' %
                    (category, url ), log.INFO)

    @check_response
    def parse_food_recipe(self, response):
        log.msg('[PARSE][food_recipe] url=%s' % (response.url,), log.INFO)

        category = response.request._msj_category
        for item in self.food_recipe_parser.parse(response):
            name = item['name']
            yield item

            log.msg('[PIPE][food_recipe] name=%s category=%s' %
                    (name, category), log.INFO)

    @check_response
    def parse(self, response):
        if response.url == self.food_material_category_list_url:
            return self.parse_material_category_list(response)

        if response.url in self.recipe_category_list_urls:
            return self.parse_recipe_category_list(response)

        if response.url in self.effect_recipe_category_list_urls:
            response._msj_is_effect = True
            return self.parse_recipe_category_list(response)

        log.msg('[URL][new] url=%s' % (response.url,), log.CRITICAL)
