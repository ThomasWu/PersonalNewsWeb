import json
import pyjsonrpc

URL = 'http://localhost:4041'

client = pyjsonrpc.HttpClient(url=URL)

def getSystemSettings(systemName):
    if type(systemName) is not str:
        return None
    return client.call('getSystemSettings', systemName)

def setSystemSettings(systemName, settings):
    client.notify('setSystemSettings', systemName, settings)

def dropSystemSettings(systemName):
    client.notify('dropSystemSettings', systemName)