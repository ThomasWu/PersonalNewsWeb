import datetime
import os
import sys

from dateutil import parser
from sklearn.feature_extraction.text import TfidfVectorizer

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client
from cloudAMQP_client import CloudAMQPClient
from logger import Logger

SYSTEM_NAME = 'news-deduper'

DEDUPE_NEWS__AMQP_TASK = 'dedupe_news_task'

SLEEP_TIME_IN_SECONDS = 1

SAME_NEWS_SIMILARITY_THRESHOLD = 0.9

NEWS_TABLE_NAME = 'news'

cloudAMQP_client = CloudAMQPClient(task=DEDUPE_NEWS__AMQP_TASK)
logger = Logger(SYSTEM_NAME)

def handle_msg(msg):
    if msg is None or not isinstance(msg, dict):
        return 
    task = msg
    task['text'] = task['text'].encode('utf-8', errors='replace')
    text = str(task['text'])
    if text is None:
        logger.log('Skipped empty news %s' % task['digest'])
        return

    published_at = parser.parse(task['publishedAt'])
    published_at_day_begin = datetime.datetime(published_at.year, published_at.month, published_at.day, 0, 0, 0, 0)
    published_at_day_end = published_at_day_begin + datetime.timedelta(days=1)

    db = mongodb_client.get_db()

    same_day_news_list = list(db[NEWS_TABLE_NAME].find(
        {'publishedAt': 
            {
                '$gte': published_at_day_begin,
                '$lt': published_at_day_end
            }
        }
    ))

    if same_day_news_list is not None and len(same_day_news_list) > 0:
        documents = [str(news['text']) for news in same_day_news_list]
        documents.insert(0, text)

        tfidf = TfidfVectorizer().fit_transform(documents)
        pairwise_sim = tfidf * tfidf.T

        print pairwise_sim
        rows, _ = pairwise_sim.shape

        for row in range(1, rows):
            if pairwise_sim[row, 0] > SAME_NEWS_SIMILARITY_THRESHOLD:
                logger.log('Ignored duplicated news %s' % task['digest'])
                print 'ignoring duplicated news'
                return

    print datetime.datetime.utcnow().strftime('%Y-%m-%d %H-%M-%SZ'),
    print 'inserting news with digest %s' % task['digest']
    logger.log('Inserted new news %s into database' % task['digest'])
    task['publishedAt'] = parser.parse(task['publishedAt'])
    db[NEWS_TABLE_NAME].replace_one({'digest': task['digest']}, task, upsert=True)

while True:
    if cloudAMQP_client is not None:
        msg = cloudAMQP_client.getMessage()
        if msg is not None:
            try:
                handle_msg(msg)
            except Exception as e:
                print e

        cloudAMQP_client.sleep(SLEEP_TIME_IN_SECONDS)


