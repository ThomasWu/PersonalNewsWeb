import os
import pickle
import pyjsonrpc
import sys
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
# import 

SERVER_HOST = ''
SERVER_PORT = -1

class RequestHandler(pyjsonrpc.HttpRequestHandler):
    @pyjsonrpc.rpcmethod
    def log(self, text):
        pass

http_server = pyjsonrpc.ThreadingHttpServer(
    server_address=(SERVER_HOST, SERVER_PORT),
    RequestHandlerClass=RequestHandler
)

print 'Start log server on URL: %s:%d' % (SERVER_HOST, SERVER_PORT)

http_server.serve_forever()
