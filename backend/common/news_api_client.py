import requests
from json import loads
import configuration_service_client as conf_client

class NewsApiClient(object):
    SYSTEM_NAME = 'news-api'

    def __init__(self, sortBy='top'):
        self.settings = conf_client.getSystemSettings(self.SYSTEM_NAME)
        self.sources = self.settings['sources']
        self.url = self.settings['api-endpoint']
        self.apiKey = self.settings['api-key']
        self.sortBy = sortBy
        
    def changeSources(self, newSources):
        self.sources = newSources

    def getNews(self):
        articles = []
        for source in self.sources:
            payload = {
                'apiKey': self.apiKey,
                'source': source,
                'sortBy': self.sortBy
            }
            response = requests.get(self.url, params=payload)
            if response.status_code != 200:
                continue
            res_json = loads(response.content)
            if ( res_json is not None and 
                res_json['status'] == 'ok' and
                res_json['source'] is not None):
                for news in res_json['articles']:
                    news['source'] = res_json['source']
            articles.extend(res_json['articles'])
        # TODO: logs retrieved articles and time
        return articles

