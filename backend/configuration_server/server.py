import pyjsonrpc

SERVER_HOST = 'localhost'
SERVER_PORT = 4041

class RequestHandler(pyjsonrpc.HttpRequestHandler):
    @pyjsonrpc.rpcmethod
    def getNewsSummariesForUser(self, user_id, page_num):
        return operations.getNewsSummariesForUser(user_id, page_num)

    @pyjsonrpc.rpcmethod
    def logNewsClickForUser(self, user_id, news_id):
        return operations.logNewsClickForUser(user_id, news_id)

# threading HTTP server
http_server = pyjsonrpc.ThreadingHttpServer(
    server_address = (SERVER_HOST, SERVER_PORT),
    RequestHandlerClass = RequestHandler
)

print('Starting HTTP server on %s:%d' % (SERVER_HOST, SERVER_PORT))
http_server.serve_forever()
