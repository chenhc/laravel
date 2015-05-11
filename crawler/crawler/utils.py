#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   utils.py
Author:     Chen Yanfei
@contact:   fasionchan@gmail.com
@version:   $Id$

Description:

Changelog:

'''

from scrapy.crawler import CrawlerProcess
from scrapy.shell import Shell
from scrapy.settings import Settings
from threading import Thread


def get_fetch(log=False):
    settings = Settings()
    settings.set('LOG_ENABLED', log)

    crawler_process = CrawlerProcess(settings)
    crawler = crawler_process.create_crawler()
    crawler_process.start_crawling()

    t = Thread(target=crawler_process.start_reactor)
    t.daemon = True
    t.start()

    shell = Shell(crawler)
    shell.code = 'adsf'

    import threading
    lock = threading.Lock()

    def fetch(url_or_request):
        lock.acquire()
        try:
            shell.fetch(url_or_request)
            response = shell.vars.get('response')
            return response
        finally:
            lock.release()

    return fetch

fetch = get_fetch()
