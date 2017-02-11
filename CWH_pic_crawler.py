# -*- coding: utf-8 -*-
__author__ = 'songjian'

import requests
import lxml.html
import re
import time
import sys
import urllib

from datetime import datetime, timedelta

reload(sys)
sys.setdefaultencoding('utf-8')

session = requests.session()
USER_AGENT = ('Mozilla/5.0 (Windows NT 5.1) '
              'AppleWebKit/536.11 (KHTML, like Gecko) '
              'Chrome/20.0.1132.57 Safari/536.11')
session.headers['User-Agent'] = USER_AGENT

DOWNLOAD_SLEEP = 1
ENCODING = 'utf-8'

re_get_page_number = re.compile(r'page=(\d+)')

f = file("ERR_PAGES.txt", "w")

URL_BASE = "http://www.chemistwarehouse.com.au"

URL_BASE_SWISSE = 'http://www.chemistwarehouse.com.au/Shop-Online/587/Swisse'
URL_BASE_BLACKMORES = 'http://www.chemistwarehouse.com.au/Shop-Online/513/Blackmores'
URL_BASE_HEALTHY_CARE = 'http://www.chemistwarehouse.com.au/search?searchtext=healthy%20care&searchmode=allwords'

swisse_file_path = "./log/swisse/"
blackmores_file_path = "./log/blackmores/"
healthy_care_file_path = "./log/healthy care/"


def download(url, outfile):
    """
    download 'url' to 'outfile'.
    :param url:
    :param outfile:
    :return:
    """
    print url + ' is being downloading...'
    try:
        if url:
            urllib.urlretrieve(url, outfile)
            time.sleep(1)
    except:
        print url, "Failed!"


def parse_single_product(url, name, path):
    time.sleep(DOWNLOAD_SLEEP)
    try:
        content_base = session.get(url).content
        page_lxml = lxml.html.fromstring(content_base.decode(ENCODING, 'ignore'))
        price = page_lxml.xpath(r'//div[@class="Price"]')[0].text_content().strip()
        file_name = path + name + '-' + price + '.jpg'
        print '[product_name]: ' + name
        img_judge = page_lxml.xpath(r'//td[@style=" width:40%"]/a[@class="product_img_enlarge"]/@href')
        if len(img_judge) == 0:
            img_url = page_lxml.xpath(r'//td[@style=" width:40%"]/img/@src')[0]
        else:
            img_url = page_lxml.xpath(r'//td[@style=" width:40%"]/a[@class="product_img_enlarge"]/@href')[0]
        download(img_url, outfile=file_name)
    except Exception:
        f.write('large_img_err: ' + url + '\n')


def parse_product_page(url, path):
    time.sleep(DOWNLOAD_SLEEP)
    try:
        content_base = session.get(url).content
        page_lxml = lxml.html.fromstring(content_base.decode(ENCODING, 'ignore'))
        for i in page_lxml.xpath(r'//table[@id="p_lt_ctl05_pageplaceholder_p_lt_ctl00_wPListC_lstElem"]//tr'):
            for j in i.xpath(r'./td/a'):
                product_name = j.xpath(r'@title')[0]
                print product_name
                url_tail = j.xpath(r'@href')[0]
                print '[product page url is]: ' + URL_BASE + url_tail
                parse_single_product(URL_BASE + url_tail, product_name, path)
        for i in page_lxml.xpath(r'//div[@style="vertical-align: top;"][4]//div[@class="Product"]'):
            product_name = i.xpath(r'./a/@title')[0]
            print product_name
            url_tail = i.xpath(r'./a/@href')[0]
            print '[product page url is]: ' + URL_BASE + url_tail
            parse_single_product(URL_BASE + url_tail, product_name, path)
    except Exception:
        f.write('product_page_err: ' + URL_BASE + url_tail + '\n')


def start_job(brand):
    if brand == 'B':
        content_base = session.get(URL_BASE_BLACKMORES).content
        file_path = blackmores_file_path
        page_lxml = lxml.html.fromstring(content_base.decode(ENCODING, 'ignore'))
        raw_total_page_number = page_lxml.xpath(r'//div[@style="float:right"]/a[last()]/@href')[0]
        total_page_number = int(re_get_page_number.search(raw_total_page_number).group(1))
        for i in range(1, total_page_number + 1):
            single_page_url = URL_BASE_BLACKMORES + "?page=" + str(i)
            print '[PAGE OF PRODUCT LIST]: ' + single_page_url
            parse_product_page(single_page_url, file_path)
    elif brand == 'H':
        content_base = session.get(URL_BASE_HEALTHY_CARE).content
        file_path = healthy_care_file_path
        page_lxml = lxml.html.fromstring(content_base.decode(ENCODING, 'ignore'))
        raw_total_page_number = page_lxml.xpath(r'//div[@style="float:right"]/a[last()]/@href')[0]
        total_page_number = int(re_get_page_number.search(raw_total_page_number).group(1))
        for i in range(1, total_page_number + 1):
            single_page_url = URL_BASE_HEALTHY_CARE + "&page=" + str(i)
            print '[PAGE OF PRODUCT LIST]: ' + single_page_url
            parse_product_page(single_page_url, file_path)
    elif brand == 'S':
        content_base = session.get(URL_BASE_SWISSE).content
        file_path = swisse_file_path
        page_lxml = lxml.html.fromstring(content_base.decode(ENCODING, 'ignore'))
        raw_total_page_number = page_lxml.xpath(r'//div[@style="float:right"]/a[last()]/@href')[0]
        total_page_number = int(re_get_page_number.search(raw_total_page_number).group(1))
        for i in range(1, total_page_number + 1):
            single_page_url = URL_BASE_SWISSE + "?page=" + str(i)
            print '[PAGE OF PRODUCT LIST]: ' + single_page_url
            parse_product_page(single_page_url, file_path)


# url1 = "http://www.chemistwarehouse.com.au/search?searchtext=healthy%20care&searchmode=allwords&page=2"
# parse_product_page(url1)

start_job('H')
