import json
import pymongo
from mitmproxy import ctx

client = pymongo.MongoClient('localhost')
db = client['igetget']
collection = db['books']
url = 'https://entree-ali.igetget.com/label/v2/algo/product/list'

def response(flow):
    if flow.request.url.startswith(url):
        print(type(flow.request))
        print(type(flow.request.url))
        print(type(flow.response))
        text = flow.response.text
        data = json.loads(text)
        print(data)
        books = data.get('c').get('product_list')
        for book in books:
            data = {
                'title': book.get('name'),
                'cover': book.get('index_img'),
                'summary': book.get('intro'),
                'price': book.get('price')
            }
            ctx.log.info(str(data))
            collection.insert_one(data)
