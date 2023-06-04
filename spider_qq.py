import requests
import time
import json
from settings import *
from utils import data_parse

cookie = "__Q_w_s__QZN_TodoMsgCnt=1; pgv_pvid=1285134080; ptui_loginuin=1772750193@qq.com; RK=xrOotVMwbU; ptcz=2438c80d18e46d131a515b9e6e71a4afd6ef0ff66091d521289a20d23801d4c8; QZ_FE_WEBP_SUPPORT=1; cpu_performance_v8=17; pt_sms_phone=156******76; __Q_w_s_hat_seed=1; _qpsvr_localtk=0.5585212456102961; pgv_info=ssid=s2442643798; uin=o1772750193; skey=@LTpaQXJPl; p_uin=o1772750193; pt4_token=DKKa*K-Gar621s12-lCV8PcnrXd6tOXC9zUBgPEHTjo_; p_skey=VWUpdhqqOVzom73MSczAQL0upfWzmgcl18FMntv5oLY_; Loading=Yes; rv2=80DA5B4E5B7463A7B59E07EBAC4D0114576126D6F621926A74; property20=68111E5CD44626330CB304B8DB7446910E1E04C7666CFB6AA76D610BA67279EC8329B3CABB9B58FF"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 HBPC/12.0.0.301',
    'Cookie': cookie
}

baseUrl = f'https://user.qzone.qq.com/proxy/domain/ic2.qzone.qq.com/cgi-bin/feeds/feeds_html_act_all?scope=0&filter=all&flag=1&refresh=0&firstGetGroup=0&mixnocache=0&scene=0&begintime=undefined&icServerTime=&sidomain=qzonestyle.gtimg.cn&useutf8=1&outputhtmlfeed=1&refer=2&r=0.8235246405772889'

def get_g_tk(cookie):
    #获取token
    pskey_start = cookie.find('p_skey=')
    pskey_end = cookie.find(';', pskey_start)
    p_skey = cookie[pskey_start+7: pskey_end]
    h = 5381
    for s in p_skey:
        h += (h << 5) + ord(s)
        
    return h & 2147483647
    
def request_data(host):
    #请求数据
    print("正在爬取%s" % host["name"])
    #生成token
    token = str(get_g_tk(cookie))
    param = f'&g_tk={token}&hostuin={host["number"]}&start=0&count=10'
    targetUrl = baseUrl + param
    r = requests.get(targetUrl, headers = headers)
    return r.text

def collect_data(html, host):
    #从爬取的js收集数据
    prefix = 'data/qqzone_js/%s-%s' % (time.strftime("%Y-%m-%d@%H-%M"), host["name"])
    #将js备份到本地
    with open(prefix+'.js', 'w', encoding='utf-8') as f:
        f.write(html)
    # try:
    #调用解析函数
    data = data_parse(html)
    result = {"name": host["name"], "number": host["number"], "data": data}
    #将解析的json保存到本地
    prefix = 'data/qqzone_json/%s-%s' % (time.strftime("%Y-%m-%d@%H-%M"), host["name"])
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
    #'https://xinxiyouxuan.xyz/hotspot/post'
    # 'http://127.0.0.1:8001/hotspot/post'
    send_url = 'https://xinxiyouxuan.xyz/hotspot/post'
    #不依赖外部存储文件时
    # data = str(json.dumps(data)).encode('utf-8')
    r = requests.post(send_url, headers=send_headers, data=data)
    return (r.status_code, r.text)


def simulate_send():
    #模拟发送到数据库
    with open('data/json/2022-05-11@15-22-太原科技大学表白墙.json', 'r', encoding='utf-8') as f:
        data = str(f.read()).encode('utf-8')
        send_result = send_data({"data": data, "password": "yhl@521"})
        print(send_result)

def main():
    for host in host_list:
        collect_data(request_data(host), host)
        time.sleep(10)
        
main()
# simulate_send()

