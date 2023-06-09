import requests
import json
import re
from requests.exceptions import RequestException
import time

def get_one_page(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.56'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None
    
def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(.*?)</i>.*?'+\
    'data-src="(.*?)".*?name.*?a.*?>(.*?)</a>.*?star.*?>(.*?)</p>'+\
    '.*?releasetime.*?>(.*?)</p>.*?integer.*?>(.*?)</i>.*?'+\
    'fraction.*?>(.*?)</i>.*?</dd>', re.S)
    
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'index': item[0],
            'image': item[1],
            'title': item[2].strip(),
            'actor': item[3].strip()[3:] if len(item[3])>3 else '',
            'time': item[4].strip()[5:] if len(item[4])>5 else '',
            'score': item[5].strip() + item[6].strip()
        }
    
def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False)+'\n')
        

def main(offset):
    url = 'https://www.maoyan.com/board/4?timeStamp=1645352192193&channelId=40011&index=6&signKey=ab100a611a4880fa4bfd9c5cad33cd1a&sVersion=1&webdriver=false&offset='+str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)
    

if __name__ == '__main__':
    for i in range(10):
        main(i*10)
        time.sleep(1)
