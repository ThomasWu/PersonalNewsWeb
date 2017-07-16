import pyjsonrpc
import configuration_service_client as conf_client

URL = 'http://localhost:6060'

client = pyjsonrpc.HttpClient(url=URL)

def classify(text):
    topic = client.call('classify', text)
    return topic