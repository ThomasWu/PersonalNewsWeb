import pyjsonrpc

class NewsRecommendationServiceClient(object):
    def __init__(self, url):
        self.url = url
        self.client = pyjsonrpc.HttpClient(url=self.url)

    def getPreferenceForUser(self, user_id):
        preference = self.client.call('getPreferenceForUser', user_id)
        # TODO: logs fetching operation to log system
        return preference