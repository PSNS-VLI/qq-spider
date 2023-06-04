import io
import re
import os
import sys
import time
import random
import urllib
import requests
from lxml import etree
from abc import abstractmethod
from settings import get_header
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')

class Spider:
    SPIDER_HEADER = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 \
        Safari/537.36 HBPC/12.0.0.301',
        'Content-Type': 'text/html; charset=utf-8'
    }
    BING = 'https://cn.bing.com/search?FORM=PERE&'
    BAIDU = 'https://www.baidu.com/s?'

    def __init__(self, browser_position):
        self.__pages = []
        self.__browser = \
        webdriver.Firefox(firefox_binary=FirefoxBinary(browser_position), 
            options = self.__get_headless())
    def __del__(self):
        self.__browser.close()
        os.system('taskkill /im geckodriver.exe /F')
        os.system('taskkill /im firefox.exe /F')

    def __str__(self):
        return ''

    def search(self, key_word: str = '', target: str = None, start: int = 0,
        search_engine: str = 'BING'):
        self.key_word = key_word
        _se = eval(f'self.{search_engine}')

        _word = urllib.parse.urlencode({'q': key_word}) \
        if search_engine == Page.BING \
        else urllib.parse.urlencode({'wd': key_word})

        _target = target or f'{_se}{_word}'
        _result = Page(self.__get(_target), search_engine)
        self.__clean()
        self.__push(_result)
        return _result

    def next_page(self):
        if len(self.__pages) > 0:
            return self.search(self.key_word, (len(self.__pages) + 1) * 10)
        else:
            return None

    def get_current_page(self):
        return self.__pages[self.__page_index] \
            if len(self.__pages) > 0 else None

    def get_page_num(self):
        return len(self.__pages)

    @staticmethod
    def random_delay(annotation='', max_time = 4):
        delay = random.randint(1, max_time)
        print('【RANDOM DELAY. PLEASE WAIT：%d s】 / 【%s】' % (delay, annotation))
        time.sleep(delay)

    def __push(self, page: 'Page'):
        self.__pages.append(page)

    def __clean(self):
        self.__pages = []

    def __get_headless(self):
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        return options

    def __get_without(self, target: str = None, header: dict = None):
        _header = header or self.SPIDER_HEADER
        return requests.get(target, _header)

    def __get(self, target: str):
        self.__browser.get(target)
        return self.__browser.page_source

class Page:
    BING = 'BING'
    BAIDU = 'BAIDU'

    def __init__(self, html_str, source: str):
        self.source = source
        self.html = etree.HTML(html_str)

    def __str__(self):
        return etree.tostring(self.html).decode('utf-8')

    def locate_element(self, xpath_selector):
        data = []
        for element in self.html.xpath(xpath_selector):
            text = self.extract_text(element)
            data.append(text)
        return data

    def extract_text(self, element):
        if type(element) == etree._Element:
            text_list = element.xpath(".//text()")
            return ''.join(text_list)
        elif type(element) == etree._ElementUnicodeResult:
            return str(element)
        else:
            return None
