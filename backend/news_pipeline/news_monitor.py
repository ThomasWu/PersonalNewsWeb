import datetime
import hashlib
import os
import sys

import redis

# import modules from common folder
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import news_api_client
import configuration_service_client as conf_client
from cloudAMQP_client import CloudAMQPClient

# NEWS_SOURCES ues default setting

REDIS_HOST = 'localhost'
REDIS_PORT = 6379

NEWS_TIME_OUT_IN_SECONDS = 3600 * 24 * 1 # One day
SLEEP_TIME_IN_SECONDS = 10

redis_client = redis.StrictRedis(REDIS_HOST, REDIS_PORT)

SCRAPE_NEWS_AMQP_TASK = 'scrape_news_task'

cloudAMQP_client = CloudAMQPClient(task=SCRAPE_NEWS_AMQP_TASK)

while True:
    news_list = news_api_client.getNewsFromSources()
    num_of_new_news = 0

    for news in news_list:
        news_digest = hashlib.md5(news['title'].encode('utf-8')).digest().encode('base64')

        if redis_client.get(news_digest) is None:
            num_of_new_news += 1
            news['digest'] = news_digest

			# fill a date if no publish date
            if news['publishedAt'] is None:
                news['publishedAt'] = datetime.datetime.utcnow().strftime('%Y-%m-%d%H:%M:%SZ')

            redis_client.set(news_digest, '1')
            redis_client.expire(news_digest, NEWS_TIME_OUT_IN_SECONDS)

            cloudAMQP_client.sendMessage(news)

	#if num_of_new_news > 0:
    print datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%SZ'),
    print 'fetched %d news.' % num_of_new_news
    cloudAMQP_client.sleep(SLEEP_TIME_IN_SECONDS)
