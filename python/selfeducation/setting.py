# This file local settings
import redis

USER = {
    'login': 'e.titov',
    'domain': 'SHAHTA12',
    'password': '47tit_evg'
}
CONN_REDIS = redis.Redis(host='localhost', port=6379)
