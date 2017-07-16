import operator
import os
import sys
import pyjsonrpc


sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client

PREFERENCE_MODEL_TABLE_NAME = 'user_preference_model'

MONGO_DB_HOST = 'mongodb://ds025782.mlab.com:25782/news'
MONGO_DB_PORT = '25782'
MONGO_DB_NAME = 'news'
MONGO_DB_USERNAME = 'admin'
MONGO_DB_PASSWORD = '123456'

SERVER_HOST = 'localhost'
SERVER_PORT = 5050


def isClose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

class RequestHandler(pyjsonrpc.HttpRequestHandler):
    @pyjsonrpc.rpcmethod
    def getPreferenceForUser(self, user_id):
        db = mongodb_client.get_db()
        
        model = db[PREFERENCE_MODEL_TABLE_NAME].find_one({'userId': user_id})
        if model is None:
            return

        print model
        sorted_tuples = sorted(model['preference'].items(), key=operator.itemgetter(1), reverse=True)
        sorted_list = [x[0] for x in sorted_tuples]
        sorted_value_list = [x[1] for x in sorted_tuples]

        if isClose(float(sorted_value_list[0]), float(sorted_value_list[-1])):
            return []
        
        return list(model['preference'].items())

http_server = pyjsonrpc.ThreadingHttpServer(
   server_address =  (SERVER_HOST, SERVER_PORT),
   RequestHandlerClass = RequestHandler
)
print 'Starting HTTP server on %s:%d' % (SERVER_HOST, SERVER_PORT)
http_server.serve_forever()
