import redis

r = redis.Redis(host='localhost', port=6379)

r.set('key1', 'value1')

r.hset('name', 'key', 'value')
r.hget('name','key')
#output b'value'

a={'key1':'value1','key2':'value2','keyN':'valueN'}
r.hmset('a',a)

r.hgetall('a')
#output 
{ b'key1': b'value1',
 b'key2': b'value2',
 b'keyN': b'valueN'}

