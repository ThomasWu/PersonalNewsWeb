import os
import sys
import datetime

from newspaper import Article

sys.path.append(os.path.join(os.path.dirname(__file__), '..','common'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'scrapers'))

#import cnn_news_scrapper
from cloudAMQP_client import CloudAMQPClient
from logger import Logger

SYSTEM_NAME = 'news-fetcher'

SLEEP_TIME_IN_SECONDS = 5

DEDUPE_NEWS_AMQP_TASK = 'dedupe_news_task'
SCRAPE_NEWS_AMQP_TASK = 'scrape_news_task'

dedupe_news_queue_client = CloudAMQPClient(task=DEDUPE_NEWS_AMQP_TASK)
scrape_news_queue_client = CloudAMQPClient(task=SCRAPE_NEWS_AMQP_TASK)
logger = Logger(SYSTEM_NAME)

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
	logger.log('Downloaded url: %s' % task['url'])
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
