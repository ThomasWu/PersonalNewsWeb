#!/usr/bin/env python

import json
import pyjsonrpc

SERVER_HOST = 'localhost'
SERVER_PORT = 4041

SETTINGS_FILE = 'configurations.json'
SETTINGS = {}

def loadSettings():
    global SETTINGS
    SETTINGS = json.loads(open(SETTINGS_FILE).read())

def saveSettings():
    global SETTINGS
    with open(SETTINGS_FILE, 'w') as f:
        f.write(json.dumps(SETTINGS))

loadSettings()

class RequestHandler(pyjsonrpc.HttpRequestHandler):
    @pyjsonrpc.rpcmethod
    def getSystemSettings(self, systemName):
        global SETTINGS
        if (type(systemName) is not str and
            type(systemName) is not unicode or
            systemName not in SETTINGS):
            return None
        else:
            return SETTINGS[systemName]

    @pyjsonrpc.rpcmethod
    def setSystemSettings(self, systemName, settings):
        global SETTINGS
        if (type(systemName) is not str and 
            type(systemName) is not unicode or
            type(settings) is not dict):
            return None
        SETTINGS[systemName] = settings
        saveSettings()

    @pyjsonrpc.rpcmethod
    def dropSystemSettings(self, systemName):
        global SETTINGS
        if (type(systemName) is not str and
            type(systemName) is not unicode or
            systemName not in SETTINGS):
            return None
        del SETTINGS[systemName]
        saveSettings()


# threading HTTP server
http_server = pyjsonrpc.ThreadingHttpServer(
    server_address = (SERVER_HOST, SERVER_PORT),
    RequestHandlerClass = RequestHandler
)

print('Starting HTTP server on %s:%d' % (SERVER_HOST, SERVER_PORT))
http_server.serve_forever()
