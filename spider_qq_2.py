import os
import re
import json
import time
import random
import requests
from settings import *
from utils import data_clean, em_sub, timestamp_clean, extraction_topic

pattern_parse_callback = re.compile('.*?back\((.*)\)', re.S)
pattern_parse_visitor_and_tid = re.compile('<a.*?class="state.*?data-config=.*?\|(.*?)\|.*?data-clicklog="visitor".*?>(.*?)</a>', re.S)

# 从 jsonp 中获取 json 数据
def jsonp2dict(jsonp):
    # 以贪婪模式去除 _preloadCallbacl() 等回调函数
    pattern = pattern_parse_callback
    # 打开本地文件获取 json 数据
    result = pattern.search(jsonp)
    
    return json.loads(result.group(1))

# json 转 dict
def json2dict(json_data):
    return json.loads(json_data)


# 从cookie中提取 g_tk
def get_g_tk(cookie):
    #获取token
    pskey_start = cookie.find('p_skey=')
    pskey_end = cookie.find(';', pskey_start)
    p_skey = cookie[pskey_start+7: pskey_end]
    h = 5381
    for s in p_skey:
        h += (h << 5) + ord(s)
        
    return h & 2147483647


# 根据粉丝数随机浏览量
def random_visitor(fans):
    
    # begin = int(fans) / 20
    # end = int(int(fans) / 15)

    # return random.randint(begin, end)
    return 2000

# 随机延迟避免爬虫被识别
def random_delay(annotation=''):
    delay = random.randint(2, 4)
    print('随机延迟：%d %s' % (delay, annotation))
    time.sleep(delay)


def filter_comment_data(c):
    data = {}
    data['convert_content'] = em_sub(c['content'])
    data['content'] = c['content']
    # data['createTime'] = c['createTime']
    data['create_time'] = c['createTime2']
    data['timestamp'] = c['create_time']
    data['uin'] = c['uin']
    data['name'] = c['name']
    data['convert_name'] = em_sub(c['name'])
    data['tid'] = c['tid']
    data['reply_num'] = 0
    data['picture_num'] = 0
    data['is_external'] = True
    
    return data

# 过滤评论数据
def filter_comment(c_l):
    
    data_list = []
    for c in c_l:
        data = filter_comment_data(c)
        if c.get('list_3', ''):
            replys = c.get('list_3', '')
            for i, r in enumerate(replys):
                replys[i] = filter_comment_data(r)
            data['reply_list'] = replys
            data['reply_num'] = len(replys)
        if c.get('pic', ''):
            images = c.get('pic', '')
            for i, r in enumerate(images):
                images[i] = {
                    'url': r['hd_url'],
                    'width': r['hd_width'],
                    'height': r['hd_width'],
                    'type': 0
                }
            data['images'] = images
            data['picture_num'] = len(images)
        data_list.append(data)
    
    return data_list
    
# 过滤图片数据
def filter_picture(p_l):
    data = []
    for p in p_l:
        if p.get('is_video', ''):
            continue
        data.append({
            'url': p['smallurl'],
            'width': p['width'],
            'height': p['height'],
            'type': p['pictype']
        })
    return data

def filter_more_picture(p_l):
    data = []
    for p in p_l:
        data.append({
            'url': p.get('big_pic', ''),
            'width': p.get('big_width', 0),
            'height': p.get('big_height', 0),
            'type': 0
        })
    return data

def request_html(headers, host, token, start=0, count=19):
    # 爬取空间主页 html
    # 第一个请求无需随机延迟
    print("正在爬取空间主页：%s" % host["name"])
    
    baseUrl = f'https://user.qzone.qq.com/proxy/domain/ic2.qzone.qq.com/cgi-bin/feeds/feeds_html_act_all?scope=0&filter=all&flag=1&refresh=0&firstGetGroup=0&mixnocache=0&scene=0&begintime=undefined&icServerTime=&sidomain=qzonestyle.gtimg.cn&useutf8=1&outputhtmlfeed=1&refer=2&r=0.8235246405772889'

    param = f'&g_tk={token}&hostuin={host["uin"]}&start={start}&count={count+1}'
    targetUrl = baseUrl + param
    r = requests.get(targetUrl, headers = headers)
    
    return r.text

# 请求 jsonp 格式的说说数据
def request_content(headers, host, token, start=0, count=19):
    # 第二个请求 随即延迟
    random_delay('jsonp')
    print('正在爬取jsonp：%s'%host['name'])
    baseUrl = 'https://user.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6?ftype=0&sort=0&replynum=100&callback=_preloadCallback&code_version=1&format=jsonp&need_private_comment=1'
    
    param = f'&g_tk={token}&uin={host["uin"]}&pos={start}&num={count}' # 0 19
    targetUrl = baseUrl + param
    # 返回jsonp
    r = requests.get(targetUrl, headers = headers)
    
    return jsonp2dict(r.text)

# 请求更多数据
def request_more_content(headers, host, token, tid):
    # 第三个请求 随机延迟
    random_delay('more_content')
    print('正在爬取更多content：%s'%host['name'])
    
    # headers['Content-Type'] = 'application/x-www-form-urlencoded'
    data = {
        'qzreferrer': f'https://user.qzone.qq.com/{host["uin"]}/311?',
        'tid': tid,
        'uin': host["uin"],
        't1_source': '1',
        'not_trunc_con': '1',
        'hostuin': host["uin"],
        'code_version': '1',
        'format': 'fs'
    }
    # post 请求
    baseUrl = f'https://user.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msgdetail_v6?&g_tk={token}'
    
    r = requests.post(baseUrl, data=data, headers=headers)
    
    return jsonp2dict(r.text)

# 请求更多图片
def request_more_picture(headers, host, token, tid):
    # 第四个请求 随机延迟
    random_delay('more_picture')
    print('正在爬取更多content：%s'%host['name'])
    
    baseUrl = 'https://h5.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_get_pics_v6?r=0.05045644813598016&t1_source=1&random=0.05045644813598016'
    param = f'&g_tk={token}&uin={host["uin"]}&tid={tid}'
    targetUrl = baseUrl + param
    
    r = requests.get(targetUrl, headers=headers)

    return jsonp2dict(r.text)

# 请求更多评论
def request_more_comment(headers, host, token, tid, start):
    # 第五个请求 随机延迟
    random_delay('more_comment')
    print('正在爬取更多评论：%s'%host['name'])
    
    baseUrl = 'https://user.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msgdetail_v6?t1_source=undefined&ftype=0&callback=_preloadCallback&code_version=1&format=jsonp&need_private_comment=1'
    param = f'&g_tk={token}&uin={host["uin"]}&tid={tid}&sort=0&pos={start}&num=20'
    targetUrl = baseUrl + param
    
    r = requests.get(targetUrl, headers=headers)
    
    return jsonp2dict(r.text)

# 提取浏览数据 内容 jsonp 中没有 visitor 数据
def extraction_visitor(headers, host, token, start=0, count=19):
    # 请求数据
    print("正在提取浏览量信息")
    html = data_clean(request_html(headers, host, token, start=start, count=count))
    results = pattern_parse_visitor_and_tid.findall(html)
    data = {}
    for r in results:
        data[r[0]] = r[1].replace('浏览', '').replace('次', '')
    
    # data: {'uin': {'tid': 'visitor'}}
    return data

# 提取说说数据和评论
def extraction_content(headers, host, token, visitor, start=0, count=19):
    
    json_data = request_content(headers, host, token, start=start, count=count)
    msg_list = json_data['msglist']
    content_list = []
    for msg in msg_list:
        data = {}
        data['tid'] = msg['tid']
        data['is_external'] = True
        
        data['uin'] = host['uin']
        if msg.get('userinfo', ''):
            data['name'] = msg['userinfo']['name']
        else:
            data['name'] = host['name']
        
        if msg.get('rt_con', ''):
            # 转发文章
            content = msg['rt_con']['content']
            # topic_list
            data['topic'] = extraction_topic(content)
            data['content'] = content
            data['convert_content'] = em_sub(content)
        else:
            # 原创文章
            if int(msg['has_more_con']) == 1:
                content = request_more_content(headers, host, token, 
                                                msg['tid'])['content']
                data['topic'] = extraction_topic(content)
                data['content'] = content
                data['convert_content'] = em_sub(content)
            else:
                data['content'] = msg['content']
                data['topic'] = extraction_topic(msg['content'])
                data['convert_content'] = em_sub(msg['content'])
            
        data['create_time'] = timestamp_clean(msg['created_time'])
        data['create_timestamp'] = msg['created_time']
        
        data['modify_timestamp'] = msg['lastmodify']
        if msg['lastmodify'] == msg['created_time']:
            data['is_modified'] = False
        else:
            data['is_modified'] = True

        pics = msg.get('pic', '')
        if pics:
            # 存在图片
            if int(msg['pictotal']) > len(pics):
                data['images'] = filter_more_picture(
                                request_more_picture(headers, host,
                                token, msg['tid'])['images'])
            else:
                data['images'] = filter_picture(pics)
        else:
            data['images'] = []
        data['picture_num'] = len(data['images'])
            
        data['visitor_num'] = visitor.get(msg['tid'], random_visitor(host['fans']))
        
        cmtnum = msg.get('cmtnum')
        data['comment_num'] = cmtnum
        commentlist = msg.get('commentlist', [])
        if cmtnum == 0:
            data['comment_list'] = commentlist
        else:
            if cmtnum > len(commentlist):
                comment_list = []
                for start in range(0, cmtnum, 20):
                    json_data = request_more_comment(headers, host, token,
                                msg['tid'], start)
                    comment_list += filter_comment(json_data['commentlist'])
                data['comment_list'] = comment_list
            else:
                data['comment_list'] = filter_comment(commentlist)

        content_list.append(data)
        
    return content_list
    
# 提取数据，生成 内容表、评论表、关键词表
def extraction_data(headers, host, token, start=0, count=19):
    visitor = extraction_visitor(headers, host, token, start=start, count=count)
    data = extraction_content(headers, host, token, visitor, start=start, count=count)
    
    return data
    
# 存储数据
def storage_dict_data(data, host):
    
    _path = 'data/qqzone_json2/%s-%s.json' % (time.strftime("%Y-%m-%d@%H-%M"), host["name"])
    with open(_path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False))
        
    return _path

# 发送数据
def send_data(data):
    
    send_headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 HBPC/12.0.0.301'
    }

    r = requests.post(send_url, headers=send_headers, data=data)
    return (r.status_code, r.text)


def main():
    
    cookie = "pgv_pvid=1491417900; RK=Gi9R9RkFHQ; ptcz=8020b8c9c76410cd079ad4c8c1a482e6b67d0b4dfb146783e71cd1e5d891f7a6; QZ_FE_WEBP_SUPPORT=1; eas_sid=o1G6u773Y708s8h6M3A7812937; tvfe_boss_uuid=cee4900ebdd77ae1; cpu_performance_v8=36; __Q_w_s__QZN_TodoMsgCnt=1; _qpsvr_localtk=0.5923384104459285; pgv_info=ssid=s5328032304; uin=o1772750193; skey=@JvzeaSuNf; p_uin=o1772750193; pt4_token=E3aJhPuZS1-PcF5-5AccqzCfugZn9hqSvqcOv*awGAI_; p_skey=EhLFBrVdAEzhUrDFM*0bxkh-U6QCQjaK3nisrsSzgNk_; Loading=Yes; rv2=80268978563CBDE11238B74E8C6961EA892302AA22702FCF1E; property20=B59D1016D364F41CFE097F6617F3A59AE04FBD4BC069C248CD6887665E79963F75F5DA11C336B0B3"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 HBPC/12.0.0.301',
        'Cookie': cookie
    }
    token = get_g_tk(cookie)
    for host in host_list:
        data = extraction_data(headers, host, token, start=20, count=20)
        _path = storage_dict_data(data, host)
        try:
            with open(_path, 'r', encoding='utf-8') as f:
                data = str(f.read()).encode('utf-8')
                send_result = send_data({"data": data, "password": password, "uin": int(host['uin'])})
                print(send_result)
        except Exception as e:
            print(e)
            continue
 
if __name__ == '__main__':
    main()
