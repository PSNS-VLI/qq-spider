import pymongo

client = pymongo.MongoClient(host='localhost', port=27017)
print(type(client))
db = client.admin
print(type(db))
collection = db.students
print(type(collection))
result = collection.update_one({'name': 'yhl'}, {'$inc': {'age': 1}})
print(result)
