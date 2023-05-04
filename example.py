import requests
import cache_json as cache

url = 'https://dummyjson.com/product/1'

cache = cache.CacheJSON()
if cache.is_expired():
    print('Cache is expired')
    r = requests.get(url)
    data = r.json()
    cache.set(data)
else:
    print('Cache is valid')
    data = cache.get()

print(data)
