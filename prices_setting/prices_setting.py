# -*- coding: utf-8 -*-
__author__ = 'songjian'

import requests
import lxml.html
import re
import time
import sys
import urllib
from urllib import quote

from datetime import datetime, timedelta

reload(sys)
sys.setdefaultencoding('utf-8')

session = requests.session()
USER_AGENT = ('Mozilla/5.0 (Windows NT 5.1) '
              'AppleWebKit/536.11 (KHTML, like Gecko) '
              'Chrome/20.0.1132.57 Safari/536.11')
session.headers['User-Agent'] = USER_AGENT

DOWNLOAD_SLEEP = 3
ENCODING = 'GBK'

URL_PREFIX = "https:"

URL_SEARCH = 'http://s.taobao.com/search?q=%s&bcoffset=1&s=%d&tab=all'
'''
keyword = "护肝"
u = keyword.decode('utf-8')
keyword = u.encode(ENCODING)
url_done = quote(keyword)
print url_done
'''


def get_first_page_by_keyword(key, num_of_product):
    url_done = URL_SEARCH % (quote(key), 0)
    print url_done

    time.sleep(DOWNLOAD_SLEEP)
    html_body = session.get(url_done).content
    page_lxml = lxml.html.fromstring(html_body.decode(ENCODING, 'ignore'))
    '''
    count = 0
    for i in page_lxml.xpath(r'//div[@class="view grid-nosku "]/div[@class="product  "]'):
        url_subfix = i.xpath(r'.//div[@class="productImg-wrap"]/a/@href')[0]
        count = count + 1
        if count >= num_of_product:
            break
        print URL_PREFIX + url_subfix
    '''

def get_store_url():
    file_object = open('url_list.txt')
    count = 0
    while 1:
        lines = file_object.readlines(100000)
        if not lines:
            file_object.close()
            break
        for line in lines:
            print line


get_first_page_by_keyword("swisse护肝", 5)
