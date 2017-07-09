import os
import sys
import datetime

from newspaper import Article

sys.path.append(os.path.join(os.path.dirname(__file__), '..','common'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'scrapers'))

#import cnn_news_scrapper
from cloudAMQP_client import CloudAMQPClient

SLEEP_TIME_IN_SECONDS = 5

DEDUPE_NEWS_TASK_QUEUE_URL = 'amqp://qyvxxytd:q2jeUmNZFfO5ExqupNzrdc3u93fxS6J4@fish.rmq.cloudamqp.com/qyvxxytd'
DEDUPE_NEWS_TASK_QUEUE_NAME = 'complete_news'
SCRAPE_NEWS_TASK_QUEUE_URL = 'amqp://qyvxxytd:q2jeUmNZFfO5ExqupNzrdc3u93fxS6J4@fish.rmq.cloudamqp.com/qyvxxytd'
SCRAPE_NEWS_TASK_QUEUE_NAME = 'raw_news'

dedupe_news_queue_client = CloudAMQPClient(DEDUPE_NEWS_TASK_QUEUE_URL, DEDUPE_NEWS_TASK_QUEUE_NAME)
scrape_news_queue_client = CloudAMQPClient(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)

def handle_message(msg):
	if msg is None or not isinstance(msg, dict):
		print 'message is broken'
		return

	task = msg
	text = None

	article = Article(task['url'])
	article.download()
	article.parse()

	task['text'] = article.text
	
	print datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%SZ'),
	print 'Downloaded url: %s' % task['url']
	dedupe_news_queue_client.sendMessage(task)

while True:
	if scrape_news_queue_client is not None and dedupe_news_queue_client is not None:
		msg = scrape_news_queue_client.getMessage()
		if msg is not None:
			try:
				handle_message(msg)
			except Exception as e:
				print e
				pass
	else:
		print 'client not opened'
	scrape_news_queue_client.sleep(SLEEP_TIME_IN_SECONDS)
