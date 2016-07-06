# coding=utf-8

import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import socket
import json

import posts_storage
import sentiment_analisys


class WSHandler(tornado.websocket.WebSocketHandler):
    def data_received(self, chunk):
        pass

    def open(self):
        print('New connection {0}'.format(str(self.request.remote_ip)))

    def on_message(self, message):
        print('Message received:  {0}'.format(message))
        sentiment_result = sentiment_analisys.process(message)
        self.write_message(sentiment_result)

    def on_close(self):
        print('Connection closed {0}'.format(str(self.request.remote_ip)))

    def check_origin(self, origin):
        return True


class MainHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        print(chunk)

    def get(self):
        from_timestamp = int(self.get_argument('from_timestamp'))
        count = int(self.get_argument('count'))
        print('getdata request. from_timestamp = {0} count = {1}'.format(from_timestamp, count))

        posts = [post.data for post in posts_storage.get(from_timestamp, count)]
        print("response with {0} posts".format(len(posts)))
        self.write({'posts': posts})

application = tornado.web.Application([
    (r'/ws', WSHandler),
    (r'/getdata', MainHandler),
    (r"/(.*)", tornado.web.StaticFileHandler, {"path": "data/index.html"})
])

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    myIP = socket.gethostbyname(socket.gethostname())
    print(u'*** Server Started at {0:s}:8888'.format(myIP))
    tornado.ioloop.IOLoop.instance().start()


