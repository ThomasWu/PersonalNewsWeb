import json
import os
import pickle
import random
import redis
import sys
from threading import Timer

from bson.json_util import dumps
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client
import news_recommendation_service_client
import configuration_service_client
from cloudAMQP_client import CloudAMQPClient
from logger import Logger

"""
    Configs
"""
<<<<<<< 2750d386d3c466d2c0bcb2529df255d6bbcf9fd3
SYSTEM_NAME = 'backend_server'

REDIS_SETTINGS = configuration_service_client.getSystemSettings('redis')
REDIS_HOST = REDIS_SETTINGS['host']
REDIS_PORT = REDIS_SETTINGS['port']
=======
REDIS_HOST = 'newssystemcache.3rkefe.ng.0001.use1.cache.amazonaws.com'
REDIS_PORT = 6379
>>>>>>> Fixed redis to amazon cache

MONGODB_SETTINGS = configuration_service_client.getSystemSettings('mongodb')
NEWS_TABLE_NAME = MONGODB_SETTINGS['tables']['news_table']
CLICK_LOGS_TABLE_NAME = MONGODB_SETTINGS['tables']['click_logs_table']

NEWS_LIMIT = 200
NEWS_LIST_BATCH_SIZE = 10
USER_NEWS_TIME_OUT_IN_SECOND = 60*60*24

LOG_CLICKS_AMQP_TASK = 'log_clicks_task'

# initiate service clients
redis_client = redis.StrictRedis(REDIS_HOST, REDIS_PORT, db=0)
cloudAMQP_client = CloudAMQPClient(task=LOG_CLICKS_AMQP_TASK)
logger = Logger(SYSTEM_NAME)

def keepAlive():
    cloudAMQP_client.sleep(0.1)
    timer = Timer(10, keepAlive)
    timer.start()

keepAlive()

def getNewsSummariesForUser(user_id, page_num):
    # retrieves user history
    user_liked_news_buff = redis_client.get(user_id+'liked')
    user_liked_news = pickle.loads(user_liked_news_buff) if user_liked_news_buff is not None else set()
    user_disliked_news_buff = redis_client.get(user_id+'disliked')
    user_disliked_news = pickle.loads(user_disliked_news_buff) if user_disliked_news_buff is not None else set()
    user_hided_news_buff = redis_client.get(user_id+'hided')
    user_hided_news = pickle.loads(user_hided_news_buff) if user_hided_news_buff is not None else set()

    page_num = int(page_num)
    begin_index = (page_num - 1) * NEWS_LIST_BATCH_SIZE
    end_index = page_num * NEWS_LIST_BATCH_SIZE

    sliced_news = []

    # retrieves user preference
    preference = news_recommendation_service_client.getPreferenceForUser(user_id)
    topPreference, topProbability = '', 0
    preference_thresholds =  {}
    # gets top preference
    for item in preference:
        if item[1] > topPreference:
            topPreference = item[0]
            topProbability = float(item[1])
    # generates thresholds
    for item in preference:
        preference_thresholds[item[0]] = float(item[1])/topProbability if topProbability != 0 else 1

    db = mongodb_client.get_db()

    if redis_client.get(user_id) is not None:
        news_digests = pickle.loads(redis_client.get(user_id))
        sliced_news_digests = news_digests[begin_index: end_index]
        sliced_news = list(db[NEWS_TABLE_NAME].find({'digest': {'$in': sliced_news_digests}}))
    else:
        total_news = list(db[NEWS_TABLE_NAME].find({'digest': {'$nin': list(user_disliked_news | user_hided_news)}}).sort([('publishedAt', -1)]).limit(NEWS_LIMIT))
        total_news_digests = [news['digest'] for news in total_news if 'class' in news and news['class'] in preference_thresholds and random.random() < preference_thresholds[news['class']]]

        redis_client.set(user_id, pickle.dumps(total_news_digests))
        redis_client.expire(user_id, USER_NEWS_TIME_OUT_IN_SECOND)

        sliced_news = total_news[begin_index: end_index]


    if preference is not None and len(preference) > 0:
        topPreference = preference[0]

    for news in sliced_news:
        del news['text']
        if 'class' in news and news['class'] == topPreference:
            news['reason'] = 'Recommend'
        if news['digest'] in user_liked_news:
            news['liked'] = 1 
        if news['publishedAt'].date() == datetime.today().date():
            news['time'] = 'today'
    
    logger.log('GetNews', 'Fetched %d news for %s' % (len(sliced_news), user_id))

    return json.loads(dumps(sliced_news))

def logNewsClickForUser(user_id, news_id):
    print type(user_id), user_id
    print type(news_id), news_id
    logger.log('LogClicks', 'Logged %s clicked on %s' % (user_id, news_id))

    message = {'userId': user_id, 'newsId': news_id, 'timestamp': str(datetime.utcnow())}

    db = mongodb_client.get_db()
    db[CLICK_LOGS_TABLE_NAME].insert(message)

    message = {'userId': user_id, 'newsId': news_id, 'timestamp': message['timestamp'], 'event': 'click'}

    cloudAMQP_client.sendMessage(message)

def logNewsPreferenceForUser(user_id, news_id, prefer_status):
    logger.log('LogPreference', 'Logged %s\'s preference %s on %s' % (user_id, prefer_status, news_id))
    user_liked_news_buff = redis_client.get(user_id+'liked')
    user_liked_news = pickle.loads(user_liked_news_buff) if user_liked_news_buff is not None else set()
    user_disliked_news_buff = redis_client.get(user_id+'disliked')
    user_disliked_news = pickle.loads(user_disliked_news_buff) if user_disliked_news_buff is not None else set()
    user_hided_news_buff = redis_client.get(user_id+'hided')
    user_hided_news = pickle.loads(user_hided_news_buff) if user_hided_news_buff is not None else set()
    
    message = {'userId': user_id, 'newsId': news_id, 'timestamp': str(datetime.utcnow())}

    # handles hide action
    if prefer_status == '-2':
        message['event'] = 'hide'
        if news_id in user_liked_news:
            user_liked_news.remove(news_id)
        user_hided_news.add(news_id)
    # handles dislike action
    elif prefer_status == '-1':
        message['event'] = 'dislike'
        if news_id in user_liked_news:
            user_liked_news.remove(news_id)
        user_disliked_news.add(news_id)
    # handles no preference
    elif prefer_status == '0':
        if news_id in user_liked_news:
            user_liked_news.remove(news_id)
        if news_id in user_disliked_news:
            user_disliked_news.remove(news_id)
    # handles like action
    elif prefer_status == '1':
        message['event'] = 'like'
        if news_id in user_disliked_news:
            user_disliked_news.remove(news_id)
        user_liked_news.add(news_id)

    cloudAMQP_client.sendMessage(message)

    # stores into redis
    redis_client.set(user_id+'liked', pickle.dumps(user_liked_news))
    redis_client.expire(user_id+'liked', USER_NEWS_TIME_OUT_IN_SECOND)
    redis_client.set(user_id+'disliked', pickle.dumps(user_disliked_news))
    redis_client.expire(user_id+'disliked', USER_NEWS_TIME_OUT_IN_SECOND)
    redis_client.set(user_id+'hided', pickle.dumps(user_hided_news))
    redis_client.expire(user_id+'hided', USER_NEWS_TIME_OUT_IN_SECOND)

