# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import time
from scrapy import signals
import random
import os
from myfendo.settings import USER_AGENTS
from myfendo.settings import PROXIES
import requests
class RandomUserAgent(object):
    def process_request(self, request, spider):
        useragent = random.choice(USER_AGENTS)
        #print useragent
        request.headers.setdefault("User-Agent", useragent)


class RandomProxy(object):
    def process_request(self, request, spider):
        # proxy = random.choice(PROXIES)
        # print(proxy)
        # request.meta['proxy'] = "http://" + proxy['ip_port']

        path = os.getcwd()
        parent_path = os.path.dirname(path)
        while 1:
            with open(parent_path+'\\proxies.txt', 'r') as f:
                proxies = f.readlines()
            if proxies:
                break
            else:
                time.sleep(1)
        proxy = random.choice(proxies).strip()
        try:
            requests.get('http://wenshu.court.gov.cn/', proxies={"http": proxy})
        except:
          self.process_request
        else:
            proxy(proxy)
            request.meta['proxy'] = proxy