import pyjsonrpc

class NewsTopicModelingServiceClient(object):
    def __init__(self, url):
        self.url = url
        self.client = pyjsonrpc.HttpClient(url=self.url)

    def classify(self, text):
        topic = self.client.call('classify', text)
        return topic