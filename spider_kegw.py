from lxml import etree
from utils import date_clean
import requests
import random
import time
import json
import re
import os
from settings import *

def request_data():
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0',
    'Upgrade-Insecure-Requests': '1'
    }
    url = 'https://www.tyust.edu.cn/xyxw/xyyw.htm'
    r = requests.get(url, headers=headers, verify=False)
    r.encoding = 'utf-8'

    dom = etree.HTML(r.text)
    content_list = dom.xpath('//li[@id]')

    data_list = []
    base_url = 'https://www.tyust.edu.cn'
    for content in content_list:
        data = {}
        data['origin'] = 'tyust.edu.cn(科大官网)'
        data['cover'] = base_url + content.xpath('./div/a/img/@src')[0]
        data['title'] = content.xpath('./div[@class="lbtxt fl"]/a/text()')[0]
        url = content.xpath('./div[@class="lbtxt fl"]/a/@href')[0].replace('..', base_url)
        data['url'] = url

        data['visitor'] = random.randint(3000, 5000)
    
        r = requests.get(url, headers=headers, verify=False)
        r.encoding = 'utf-8'
        dom = etree.HTML(r.text)
        date = dom.xpath('//span[@class="date"]/text()')[0] + '00:00'
        data['date'] = date_clean(date)[0]
        # 获取id
        pattern = re.compile('(\d*).htm')
        result = pattern.search(url)
        data['id'] = date_clean(date)[1] + int(result.group(1))
        
        content = dom.xpath('//div[@class="v_news_content"]')[0]
        imgs = content.xpath('.//img[@class="img_vsb_content"]')
        for img in imgs:
            img_url = base_url + img.get('src')
            img.set('width','100%')
            img.set('src', img_url)
        data['content'] = etree.tostring(content, encoding='utf-8', method='html').decode('utf-8')
        data_list.append(data)

    return data_list

def collect_data(data):
    result = {"data": data}
    #将解析的json保存到本地
    prefix = 'data/news/%s-%s' % (time.strftime("%Y-%m-%d@%H-%M"), '科大新闻')
    with open(prefix+'.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(result,ensure_ascii=False))
        
    #发送数据
    with open(prefix+'.json', 'r', encoding='utf-8') as f:
        data = str(f.read()).encode('utf-8')
        send_result = send_data({"data": data, "password": password})
        print(send_result)
        
    return result

def send_data(data):
    #将数据发送到服务器
    send_headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 HBPC/12.0.0.301'
    }
    # send_url = 'http://127.0.0.1:8001/feed/news/post'
    # send_url = 'https://xinxiyouxuan.xyz/feed/news/post'
    # send_url = 'http://10.10.10.15:8001/feed/news/post'
    send_url = 'https://yuliangliang.top/feed/news/post'
    #不依赖外部存储文件时
    # data = str(json.dumps(data)).encode('utf-8')
    r = requests.post(send_url, headers=send_headers, data=data, verify=False)
    return (r.status_code, r.text)
    
def send_data_from_local():
    target_path = 'data/tyust_news'
    json_lst = [f for f in os.listdir(target_path) if f.endswith('.json')]
    for item in json_lst:
        print('正在处理', item, sep='-')
        with open(f'data\\tyust_news\\{item}', 'r', encoding='utf-8') as f:
            data = str(f.read()).encode('utf-8')
            send_result = send_data({"data": data, "password": "yhl@521"})
            print(send_result)
        time.sleep(2)

def main():
    collect_data(request_data())

if __name__ == '__main__':
    # main()
    send_data_from_local()
