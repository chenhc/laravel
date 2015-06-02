#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   cron.py
Author:     Chen Yanfei
@contact:   fasionchan@gmail.com
@version:   $Id$

Description:

Changelog:

'''

import time

from threading import Thread


def run_cron(target, interval, args=()):
    interval = float(interval)
    while True:
        target(*args)
        time.sleep(interval)


class CronThread(Thread):

    def __init__(self, target, interval, args=(), **kwargs):
        super(CronThread, self).__init__(**kwargs)
        self.target = target
        self.interval = float(interval)
        self.args = args

    def run(self):
        self.running = True
        while self.running:
            self.target(*self.args)
            time.sleep(self.interval)

    def join(self):
        self.running = False
        return super(CronThread, self).join()
