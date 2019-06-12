import copy

import redis

import bgm_tv_spider.spiders.redis_bgm_tv
from bgm_tv_spider import settings


def chunk_iter_list(raw_list, chunk_size):
    ds = copy.copy(raw_list)
    while ds:
        yield ds[:chunk_size]
        ds = ds[chunk_size:]


if __name__ == '__main__':
    r = redis.Redis(host=settings.REDIS_HOST, **settings.REDIS_PARAMS)
    for chunk in chunk_iter_list([
        bgm_tv_spider.spiders.redis_bgm_tv.url_from_id(x)
        for x in range(1, 290000)
    ], 500):
        print(chunk[0])
        r.lpush(settings.REDIS_START_URL_KEY, *chunk)