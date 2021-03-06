# -*- coding: utf-8 -*-

import news_classes
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client
from cloudAMQP_client import CloudAMQPClient

NUM_OF_CLASSES = 6
INITIAL_P = 1.0 / NUM_OF_CLASSES
CLICK_ALPHA = 0.1
LIKE_PROMOTE = 1.5
DISLIKE_PENALTY = 0.5
HIDE_PENALTY = 0.1

SLEEP_TIME_IN_SECONDS = 1

LOG_CLICKS_AMQP_TASK = 'log_clicks_task'

PREFERENCE_MODEL_TABLE_NAME = 'user_preference_model'
NEWS_TABLE_NAME = 'news'

cloudAMQP_client = CloudAMQPClient(task=LOG_CLICKS_AMQP_TASK)

def handle_message(msg):
    if msg is None or not isinstance(msg, dict):
        return

    if ('userId' not in msg or 'newsId' not in msg or 'timestamp' not in msg or 'event' not in msg):
        return

    userId = msg['userId']
    newsId = msg['newsId']
    event = msg['event']

    db = mongodb_client.get_db()
    model = db[PREFERENCE_MODEL_TABLE_NAME].find_one({'userId': userId})

    if model is None:
        print 'Creating preference model for user %s' % userId
        new_model = {'userId': userId}
        preference = {}
        for i in news_classes.classes:
            preference[i] = float(INITIAL_P)
        new_model['preference'] = preference
        model = new_model

    print 'Updating preference model for user %s' % userId

    news = db[NEWS_TABLE_NAME].find_one({'digest': newsId})
    if (news is None
        or 'class' not in news
        or news['class'] not in news_classes.classes):
        print 'Error case: skipping update process'
        return

    click_class = news['class']

    print click_class
    print model['preference']
    print list(model['preference'])

    if event == 'click':
        old_p = model['preference'][click_class]
        model['preference'][click_class] = float((1 - CLICK_ALPHA) * old_p + CLICK_ALPHA)

        for i, prob in model['preference'].iteritems():
            if not i == click_class:
                model['preference'][i] = (1 - CLICK_ALPHA) * float(model['preference'][i])
    elif event == 'like':
        old_p = model['preference'][click_class]
        model['preference'][click_class] = old_p * LIKE_PROMOTE
        for i, prob in model['preference'].iteritems():
            if not i == click_class:
                model['preference'][i] = (1 - CLICK_ALPHA) * float(model['preference'][i])
    elif event == 'dislike':
        old_p = model['preference'][click_class]
        model['preference'][click_class] = old_p * DISLIKE_PENALTY
        delta = float(model['preference'][click_class]) - old_p
        for i, prob in model['preference'].iteritems():
            if not i == click_class:
                model['preference'][i] = float(model['preference'][i]) - delta / 5   
    elif event == 'hide':
        old_p = model['preference'][click_class]
        model['preference'][click_class] = HIDE_PENALTY if old_p > HIDE_PENALTY else 0
        delta = float(model['preference'][click_class]) - old_p
        for i, prob in model['preference'].iteritems():
            if not i == click_class:
                model['preference'][i] = float(model['preference'][i]) - delta / 5    

    db[PREFERENCE_MODEL_TABLE_NAME].replace_one({'userId': userId}, model, upsert=True)

def run():
    while True:
        if cloudAMQP_client is not None:
            msg = cloudAMQP_client.getMessage()
            if msg is not None:
                try: 
                    handle_message(msg)
                except Exception as e:
                    print e
                    pass
            cloudAMQP_client.sleep(SLEEP_TIME_IN_SECONDS)

if __name__ == '__main__':
    run()
    