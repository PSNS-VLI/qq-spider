import json


def response(flow):
    url = 'client.action?functionId=wareBusiness'
    if url in flow.request.url:
        text = flow.response.text
        data = json.loads(text)
        info = data.get('floors')[len(data.get('floors'))-1].get('data')
        name = info.get('wareInfo').get('name')
        price = info.get('priceInfo').get('jprice')
        images = [item.get('small') for item in info.get('wareImage')]
        print(name, price, images, sep="  ")

    #评论数据
    url =  'client.action?functionId=getCommentListWithCard'
    if url in flow.request.url:
        text = flow.response.text
        data = json.loads(text)
        comments = data.get('commentInfoList')
        for comment in comments:
            comment = comment.get('commentInfo')
            if comment:
                nick = comment.get('userNickName')
                text = comment.get('commentData')
                date = comment.get('commentDate')
                pictures = [item['picURL'] \
                for item in comment.get('pictureInfoList') \
                if comment.get('pictureInfoList') and \
                len(comment.get('pictureInfoList')) != 0]
                print(nick, text, date, sep='  ')

