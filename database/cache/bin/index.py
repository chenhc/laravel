#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   index.py
Author:     Chen Yanfei
@contact:   fasionchan@gmail.com
@version:   $Id$

Description:

Changelog:

'''

import common

from pylib.multirun.cron import run_cron
from pylib.server import uri2service
from modules.index import IndexCacher

from config.database import CACHE_MYSQL_URI, CACHE_REDIS_URI

def parse_args():
    from optparse import OptionParser
    parser = OptionParser()     
    parser.add_option('-m', '--mysql-uri', dest='mysql_uri', type='string',)
    parser.add_option('-r', '--redis-uri', dest='redis_uri', type='string',)

    options, args =  parser.parse_args()

    mysql_uri = options.mysql_uri
    if not mysql_uri:
        mysql_uri = CACHE_MYSQL_URI

    redis_uri = options.redis_uri
    if not redis_uri:
        redis_uri = CACHE_REDIS_URI

    return mysql_uri, redis_uri

def build_cache(mysql_uri, redis_uri):
    mysqldb = uri2service(mysql_uri)
    redisdb = uri2service(redis_uri)
    IndexCacher(mysqldb=mysqldb, redisdb=redisdb).build()
    
def main():
    import logging
    logging.basicConfig(level=logging.INFO)
    json_category_file, mysql_uri, redis_uri = parse_args()
    run_cron(target=build_cache, args=(mysql_uri, redis_uri), interval=3600)

if __name__ == '__main__':
    main()
