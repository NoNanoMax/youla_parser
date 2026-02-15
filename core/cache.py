from cachetools import TTLCache

links_cache = TTLCache(maxsize=256, ttl=120)
avto_cache = TTLCache(maxsize=2048, ttl=300)