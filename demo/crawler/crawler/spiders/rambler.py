#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   rambler.py
Author:     Chen Yanfei
@contact:   fasionchan@gmail.com
@version:   $Id$

Description:

Changelog:

'''

from urlparse import urlparse

import scrapy
from scrapy.contrib.linkextractors import LinkExtractor
from crawler.items import PostItem

def url_to_site(url):
    url_info = urlparse(url)
    site = url_info.hostname
    port = url_info.port
    if port and port != 80:
        site = '%s:%s' % (site, port)
    return site

class RamblerSpider(scrapy.Spider):
    name = 'rambler'
    start_urls = [
        'http://www.baidu.com'
    ]

    def __init__(self, *args, **kwargs):
        super(RamblerSpider, self).__init__(*args, **kwargs)
        self.seen_sites = set()

    def parse(self, response):
        site = url_to_site(response.url)
        #self.seen_sites.add(site)

        titles = response.xpath('//title/text()').extract()
        title = titles[0].strip() if titles else ''

        post = PostItem(url=response.url, site=site, title=title)
        yield post

        for link in LinkExtractor().extract_links(response):
            site = url_to_site(response.url)
            if site not in self.seen_sites:
                yield scrapy.Request(link.url, callback=self.parse)
