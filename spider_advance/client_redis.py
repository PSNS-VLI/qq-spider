from redis import StrictRedis

redis = StrictRedis(host='localhost',port=6379)
redis.set('name', 'Bob')
print(redis.get('name'))
