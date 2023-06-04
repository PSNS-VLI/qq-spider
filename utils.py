"""
    爬虫工具函数
"""
# import requests
import json
import re
import jieba
from textrank4zh import TextRank4Keyword,TextRank4Sentence
# from cnocr import CnOcr
import datetime
import time
import os

pattern_clean = re.compile("html:'(.*)?',opuin")
pattern_parse_li = re.compile('<li\sclass="f-single.*?">(.*?)</li>')
pattern_parse_content = re.compile('<div\sclass="info-detail.*?state.*?>(.*?)</span>.*?<div.*?f-single-content.*?f-info.*?>(.*?)</div>.*?<a.*?data-clicklog="visitor".*?>(.*?)</a>', re.S)
pattern_parse_chinese = re.compile(u'[^\u4e00-\u9fa5]')
#仅仅爬取评论
pattern_parse_attach = re.compile('<div\sclass="info-detail.*?state.*?>(.*?)</span>.*?<a.*?data-clicklog="visitor".*?>(.*?)</a>', re.S)
pattern_sub = re.compile('<a.*?</a>.*?<img.*?>', re.S)
pattern_parse_image = re.compile('<a.*?class="img-item.*?pickey="(.*?)".*?</a>', re.S)

pattern_parse_visitor = re.compile('<a.*?data-clicklog="visitor".*?>(.*?)</a>', re.S)
pattern_parse_tid = re.compile('<div.*?class="f-item f-s-i".*?data-key="(.*?)".*?>', re.S)

pattern_parse_visitor_and_tid = re.compile('<a.*?class="state.*?data-config=.*?\|(.*?)\|.*?data-clicklog="visitor".*?>(.*?)</a>', re.S)

pattern_parse_image_2 = re.compile('<a.*?class="img-item.*?pickey="(.*?)".*?>.*?<img.*?src="(.*?)&.*?".*?style.*?</a>')

pattern_sub_em = re.compile('\[em\](.*?)\[/em\]')

# 头像地址 no-cookie
# http://qlogo1.store.qq.com/qzone/2653774964/2653774964/50
# 请求blog
#https://user.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6?uin=715137236&ftype=0&sort=0&pos=0&num=20&replynum=100&g_tk=1194205462&callback=_preloadCallback&code_version=1&format=jsonp&need_private_comment=1
# 请求更多blog POST
# https://user.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msgdetail_v6?&g_tk=2066534495
# 请求参数
# qzreferrer=https://user.qzone.qq.com/715137236/311?
# tid=d420a02a5299a062fa110400
# uin=715137236
# t1_source=1
# not_trunc_con=1
# hostuin=1772750193
# code_version=1
# format=fs
# 请求更多图片 GET
#https://h5.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_get_pics_v6?r=0.05045644813598016&tid=d420a02adc42a362b9720100&uin=715137236&t1_source=1&random=0.05045644813598016&g_tk=200978595
# 请求参数
# r=0.05045644813598016
# tid=d420a02adc42a362b9720100
# uin=715137236
# t1_source=1
# random=0.05045644813598016
# g_tk=200978595
# 请求参数
# uin=715137236
# ftype=0
# sort=0
# pos=0
# num=20
# replynum=100
# g_tk=1551393071
# callback=_preloadCallback
# code_version=1
# format=jsonp
# need_private_comment=1

# 获取评论 GET
#https://user.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msgdetail_v6?uin=715137236&tid=d420a02a360ca262cbb50100&t1_source=undefined&ftype=0&sort=0&pos=0&num=20&g_tk=1194205462&callback=_preloadCallback&code_version=1&format=jsonp&need_private_comment=1

# 评论参数
# uin=715137236
# tid=d420a02a360ca262cbb50100
# t1_source=undefined
# ftype=0
# sort=0
# pos=0
# num=20
# g_tk=1194205462
# callback=_preloadCallback
# code_version=1
# format=jsonp
# need_private_comment=1

# 获取表情包 GET
# https://qzonestyle.gtimg.cn/qzone/em/e111.gif

def download_image(url):
    
    print("正在下载 %s" % url)
    r = requests.get(url)
    _path = 'data/temp_image/%s-%s.png' % time.strftime("%Y-%m-%d@%H-%M")
    with open(_path, 'wb') as f:
        f.write(r.content)
    
    return _path
    
def ocr_image(_path):
    print("正在识别 %s" % _path)
    res = ocr.ocr_for_single_line(_path)
    return res
    
def remove_image(_path):
    print("正在删除 %s" % _path)
    if os.path.exists(_path):
        os.remove(_path)
        
def image_ocr(url):
    _path = download_image(url)
    res = ocr_image(_path)
    remove_image(_path)
    
    return res

def generateImg(match):
    # em_sub 替换函数
    sub = f'<img src="https://qzonestyle.gtimg.cn/qzone/em/{match.group(1)}.gif" style="max-width: 24px;max-height: 24px" />'
    return sub

def em_sub(content):
    # 替换说说中的[em]e175[/em]
    return re.sub(pattern_sub_em, generateImg, content)

def data_clean(data):
    #将爬取的QQ空间内容中的unicode字符转换为utf-8
    data = pattern_clean.search(data).group(1)
    #替换\x3C \x22 \
    data = re.sub('\\\\x3C', '<', data)
    data = re.sub('\\\\x22', '"', data)
    data = re.sub('\\\\', '', data)
    
    return data

def date_clean(date):
    #将时间正则化并生成唯一ID
    ID = 0
    date = date.replace(' ', '')
    if len(date.replace(' ', '')) > 5:
        if '昨天' in date:
            time_day = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y/%m/%d")
            time_time = date.replace('昨天', '')
            ID = generate_id(time_day, time_time)
            date = date.replace('昨天', time_day + ' ')
        elif '前天' in date:
            time_day = (datetime.datetime.now() - datetime.timedelta(days=2)).strftime("%Y/%m/%d")
            time_time = date.replace('前天', '')
            ID = generate_id(time_day, time_time)
            date = date.replace('前天', time_day + ' ')
        else:
            #形式为n月n日
            pattern = re.compile('(\d+)月(\d+)日(.*)')
            result = pattern.search(date)
            time_day = '2022/%s/%s' % (f_d(result.group(1)), f_d(result.group(2)))
            time_time = f_t(result.group(3))
            ID = generate_id(time_day, time_time)
            date = '%s %s' % (time_day, time_time)
    else:
        #形式为n时n分
        time_day = datetime.datetime.now().strftime("%Y/%m/%d")
        ID = generate_id(time_day, date)
        date = '%s %s' % (time_day, date)
    return (date, ID)

def timestamp_clean(timestamp):
    return time.strftime('%Y/%m/%d %H:%M', time.localtime(timestamp))

def generate_id(time_day, time_time):
    #根据时间生成ID
    time_struc = '%s %s' % (time_day, f_t(time_time))
    timestamp = time.mktime(time.strptime(time_struc, "%Y/%m/%d %H:%M"))
    return int(timestamp)
    
def f_d(date):
    #将不足两位的日期格式化为两位
    if len(str(date)) < 2:
        date = '0'+str(date)
    return date

def f_t(time):
    #将不符合%H:%M的时间正则化
    time_list = time.split(':')
    for (i, t) in enumerate(time_list):
        if len(str(t)) < 2:
            time_list[i] = '0'+str(t)
    return ':'.join(time_list)
    
def content_clean(content):
    #仅保留文章HTML
    return re.sub(pattern_sub, '', content)

def title_clean(content):
    #挑出所有中文
    return re.sub(pattern_parse_chinese, '', content)[:15]
    
def extraction_chinese(content):
    return re.sub(pattern_parse_chinese, '', content)

def data_parse(data):
    #初始化数据列表
    data_list = []
    #解析发布时间、发布内容、浏览量数据
    data_li_list = pattern_parse_li.findall(data_clean(data))
    #对于每一个说说获取详细信息
    for data_li in data_li_list:
        data_item = {}
        content = pattern_parse_content.search(data_li)
        if content:
            date_id = date_clean(content.group(1))
            data_item['date'] = date_id[0]
            data_item['id'] = date_id[1]
            data_item['content'] = content_clean(content.group(2))
            data_item['title'] = title_clean(content_clean(content.group(2)))
            data_item['visitor'] = content.group(3).replace('浏览', '').replace('次', '')
        else:
            content = pattern_parse_attach.search(data_li)
            date_id = date_clean(content.group(1))
            data_item['date'] = date_id[0]
            data_item['id'] = date_id[1]
            data_item['content'] = ''
            data_item['title'] = ''
            data_item['visitor'] = content.group(2).replace('浏览', '').replace('次', '')
        #爬取图片
        images = pattern_parse_image.findall(data_li)
        if images:
            for index, image in enumerate(images):
                try:
                    images[index] = image.split(',')[1]
                except IndexError:
                    #评论区的图片
                    print(image)
                    continue
            data_item['images'] = images
        else:
            data_item['images'] = []
        data_list.append(data_item)
    
    return data_list

def extraction_topic(text):
    # 提取主题
    try:
        text = re.sub(pattern_sub_em, '', text)
        tr4s = TextRank4Sentence()
        tr4s.analyze(text=text, lower=True, source = 'no_stop_words')

        key_sentences = tr4s.get_key_sentences(num=10, sentence_min_len=5)
        for index, item in enumerate(key_sentences):
            key_sentences[index] = (item['weight'], item['sentence'])
        
        tr4w = TextRank4Keyword()

        tr4w.analyze(text=text, lower=True, window=5)
        key_words = tr4w.get_keywords(10, word_min_len=2)
        for index, item in enumerate(key_words):
            key_words[index] = (item['weight'], item['word'])
    
        data = extraction_chinese(text)
        word_list = jieba.lcut(text)
        word_dict = {}
        total = 0
        for word in word_list:
            if len(word) == 1:
                continue
            word_dict[word] = word_dict.get(word, 0) + 1
            total += word_dict[word]
    
        # 词典排序
        word_list = sorted(word_dict.items(), key=lambda d : d[1], reverse=True)
        print(word_list)
        try:
            # res = None
            # if total == len(word_list):
                # 词语无重复
            res = [{"title":word_list[0][0],"main": False}, {"title": extraction_chinese(key_sentences[0][1]),"main":True}]
            # else:
                # 词语重复
                # if len(word_list) > 6:
                    # res = [word_list[0][0], extraction_chinese(key_sentences[0][1])]
                # else:
                    # res = [word_list[0][0], extraction_chinese(key_sentences[0][1])]
    
            # 矫正
            if res[0] == res[1]:
                res = [res[0], res[2]]
    
            for index, item in enumerate(res):
                if item["title"] == '深夜' and '深夜话题' in text:
                    res[index]["title"] = '深夜话题'
    
            return res
        except Exception as e:
            print(e)
            return [{"title":extraction_chinese(key_sentences[0][1]),"main":True}]
    except Exception:
        return [{"title":"大家怎么看","main":True}]
            
if __name__ == '__main__':
    
    res = extraction_topic("焯了，我真的栓Q")
    print(res)
    
    

