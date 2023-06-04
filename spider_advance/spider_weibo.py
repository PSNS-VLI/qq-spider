from urllib.parse import urlencode
import requests
import time
base_url = 'https://weibo.com/ajax/statuses/mymblog?'

headers = {
    'Host': 'weibo.com',
    'Referer': 'https://passport.weibo.com/',
    'Cookie': 'XSRF-TOKEN=LvTkzWxv4-VVpRKHlAmnEBTg; SUB=_2AkMVSLQwf8NxqwJRmP0SxW_gaoxyzA3EieKjFEXrJRMxHRl-yT8XqlQMtRB6Psia33uYYMbIl0xZOzqtvWjb84OBW4WM; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9Whjp4_RBUj2J0Ar_bZ1T3.g',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0',
    'X-Requested-With': 'XMLHttpRequest'
}

def get_page(page):
    params = {
        'uid': 2830678474,
        'page': page,
        'feature': 0
    }
    
    url = base_url + urlencode(params)
    print(url)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(response.status_code)
    except requests.ConnectionError as e:
        print('Error', e.args)
        
def parse_page(json):
    if json:
        items = json.get('data').get('list')
        for item in items:
            weibo = {}
            if item.get('retweeted_status'):
                item = item.get('retweeted_status')
                weibo['id'] = item.get('idstr')
                weibo['text'] = item.get('text_raw')
            weibo['id'] = item.get('idstr')
            weibo['text'] = weibo.get('text', '') + item.get('text_raw')
            yield weibo
            
if __name__ == '__main__':
    for page in range(1, 11):
        time.sleep(1)
        json = get_page(page)
        results = parse_page(json)
        for result in results:
            print('%s\n%s' % (result['id'], result['text']))
