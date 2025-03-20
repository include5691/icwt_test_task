import time
from flask import request

cache = {}

def cached(func):
    "Result caching decorator for api endpoints. TTL = 5 min."
    def wrapper(*args, **kwargs):
        key = (func.__name__, args, frozenset(kwargs.items()), request.args)
        if key in cache:
            if cache[key]['timestamp'] + 600 > time.time():
                return cache[key]['value']
        value = func(*args, **kwargs)
        cache[key] = {'value': value, 'timestamp': time.time()}
        return value
    return wrapper