import json
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client
import news_topic_modeling_service_client

NEWS_CATEGORIES = json.loads(open('../news_pipeline/news_categories.json').read())

if __name__ == '__main__':
    db = mongodb_client.get_db()
    news_cursor = db['news'].find({})
    count = 0
    for news in news_cursor:
        count += 1
        print count
        if news['source'] in NEWS_CATEGORIES:
            news['class'] = NEWS_CATEGORIES[news['source']]
        if 'class' not in news or news['class'] == 'general':
            print 'Populating classes'
            description = news['title']
        top = news_topic_modeling_service_client.classify(description)
        news['class'] = top
        db['news'].replace_one({'digest': news['digest']}, news, upsert=True)
