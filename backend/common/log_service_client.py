import pyjsonrpc

class LogSystemClient(object):
    def __init__(self, url):
        self.url = url
        self.client = pyjsonrpc.HttpClient(url=self.url)

    def log(self, )