import requests
from bs4 import BeautifulSoup

x = 0
url = 'https://s.weibo.com/top/summary'
headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
'Cookie': 'SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5NB5-D_jJs2GyvC-WL_Yjf5JpX5KMhUgL.FoM01K.ESoq7e0q2dJLoI7UeK8._9JSo; UOR=login.sina.com.cn,s.weibo.com,login.sina.com.cn; SINAGLOBAL=7182470150063.305.1653524844761; ALF=1686015600; SSOLoginState=1654479603; SCF=As5GC1xZvJEooHoC1B1j-NW2kNELndj0qWajnd1Ilo9vuW-TzueegO4e2y9vZrhfOvrvz-GzEe58tw6ig6pVBKI.; SUB=_2A25PmSqhDeRhGeFN4lsT9ijMyDqIHXVs7xtprDV8PUNbmtAKLWfRkW9NQ75pipKUQGzPiPVToRseQviqt44Ik5Ua; _s_tentry=login.sina.com.cn; Apache=2152279172614.1443.1654479603536; ULV=1654479603550:3:1:2:2152279172614.1443.1654479603536:1653892645825; PC_TOKEN=38e100ff79; WBStorage=4d96c54e|undefined'
}

res = requests.get(url,headers=headers)
bs_hots = BeautifulSoup(res.text,'html.parser')
hots = bs_hots.find_all('td',class_='td-02')
for hot in hots:
    hotline = hot.find('a')
    if x == 0:
        print('置顶热搜:{}'.format(hotline.text))
        x += 1
    else:
        print('第{}热搜:{}'.format(x,hotline.text))
        x += 1
