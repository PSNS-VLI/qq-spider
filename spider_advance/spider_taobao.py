from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pyquery import PyQuery as pq
from urllib.parse import quote
import time
import pymongo
MONGO_URL='localhost'
MONGO_DB='taobao'
MONGO_COLLECTION='products2'

browser = webdriver.Firefox()
wait = WebDriverWait(browser, 10)

def get_url(word, page):
    word = quote(word)
    return 'https://uland.taobao.com/sem/tbsearch?'+\
    f'refpid=mm_26632258_3504122_32538762&keyword={word}'+\
    '&clk1=1d3536927506a0014ac11fc68b8172b0'+\
    f'&upsId=1d3536927506a0014ac11fc68b8172b0&pnum={page}'

def index_page(page):
    print("正在爬取第%d页" % page)
    try:
        browser.get(get_url('ipad', page-1))
        html = browser.page_source
        get_products(html)
    except TimeoutException:
        index_page(page)

def get_products(html):
    doc = pq(html)
    items = doc('#mx_5 .pc-search-items-list .pc-items-item').items()
    for item in items:
        item.find('.seller-info .seller-icon').remove()
        product = {
            'image': item.find('.pc-items-item-img').attr('src'),
            'price': item.find('.price-con .coupon-price-afterCoupon').text(),
            'deal': item.find('.item-footer .sell-info').text(),
            'title': item.find('.pc-items-item-title .title-text').text(),
            'shop': item.find('.seller-info').text()
        }
        print(product)
        save_to_mongo(product)
    
def save_to_mongo(result):
    client = pymongo.MongoClient(MONGO_URL)
    db = client[MONGO_DB]
    collection = db[MONGO_COLLECTION]
    try:
        insert = collection.insert_one(result)
        if insert:
            print('存储成功-->%s' % str(insert.inserted_id))
    except Exception:
        print('存储失败')
        
def main():
    for i in range(1, 100):
        index_page(i)
        time.sleep(10)
        
main()
