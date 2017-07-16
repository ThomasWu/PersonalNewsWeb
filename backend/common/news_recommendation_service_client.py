import pyjsonrpc
import configuration_service_client as conf_client

URL = 'http://localhost:5050'

client = pyjsonrpc.HttpClient(url=URL)

def getPreferenceForUser(user_id):
    preference = client.call('getPreferenceForUser', user_id)
    # TODO: logs fetching operation to log system
    return preference