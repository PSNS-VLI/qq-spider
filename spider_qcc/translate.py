import json
import requests

targetUrl = 'http://fanyi.youdao.com/translate?&doctype=json&type=AUTO&i='

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 HBPC/12.0.0.301',
}
def translater(chinese):
    r = requests.get(f'{targetUrl}{chinese}', headers = headers)
    return json.loads(r.text)['translateResult'][0][0]['tgt']
