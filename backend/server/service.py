import pyjsonrpc
import operations

SERVER_HOST = 'localhost'
SERVER_PORT = 4040

class RequestHandler(pyjsonrpc.HttpRequestHandler):
    @pyjsonrpc.rpcmethod
    def add(self, a, b):
        print('add is called with %s and %s' % (str(a), str(b)))
        return a+b

    @pyjsonrpc.rpcmethod
    def getNewsSummariesForUser(self, user_id, page_num):
        return operations.getNewsSummariesForUser(user_id, page_num)

    @pyjsonrpc.rpcmethod
    def logNewsClickForUser(self, user_id, news_id):
        return operations.logNewsClickForUser(user_id, news_id)

    @pyjsonrpc.rpcmethod
    def logNewsPreferenceForUser(self, user_id, news_id, prefer_status):
        return operations.logNewsPreferenceForUser(user_id, news_id, prefer_status)

# threading HTTP server
http_server = pyjsonrpc.ThreadingHttpServer(
    server_address = (SERVER_HOST, SERVER_PORT),
    RequestHandlerClass = RequestHandler
)

print('Starting HTTP server on %s:%d' % (SERVER_HOST, SERVER_PORT))
http_server.serve_forever()
