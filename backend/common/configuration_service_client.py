import json
import pyjsonrpc

class ConfigurationServiceClient(object):
    def __init__(self, url):
        self.url = url
        self.client = pyjsonrpc.HttpClient(url=self.url)

    def setAMQPSettings(self, settings):
        pass

    def getAMQPSettings(self):
        pass

    def setMongoDbSettings(self, settings):
        pass

    def getMongoDbSettings(self):
        pass

    def getNewsRecommendationSettings(self):
        pass

    def getNewsTopicModelingSettings(self):
        pass