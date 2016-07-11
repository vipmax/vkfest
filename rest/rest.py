# coding=utf-8

import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import socket
import json

import posts_storage
import sentiment_analisys
import db


import logging
logger = logging.getLogger('rest')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())
# logging.basicConfig(filename='log.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class WSHandler(tornado.websocket.WebSocketHandler):
    def data_received(self, chunk):
        pass

    def open(self):
        logging.info('New connection {0}'.format(str(self.request.remote_ip)))

    def on_message(self, message):
        logging.info('Message received:  {0}'.format(message))
        sentiment_result = sentiment_analisys.process(message)
        self.write_message(sentiment_result)

    def on_close(self):
        logging.info('Connection closed {0}'.format(str(self.request.remote_ip)))

    def check_origin(self, origin):
        return True


class GetDataHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        logging.info(chunk)

    def get(self):
        from_timestamp = int(self.get_argument('from_timestamp'))
        count = int(self.get_argument('count'))
        logging.info('getdata request. from_timestamp = {0} count = {1}'.format(from_timestamp, count))
        posts = posts_storage.get(from_timestamp, count)
        posts = [post.data for post in posts]
        logging.info("response with {0} posts".format(len(posts)))
        self.write({'posts': posts})


class GetDataHandler2(tornado.web.RequestHandler):
    def data_received(self, chunk):
        logging.info(chunk)

    def get(self):
        start_timestamp = int(self.get_argument('start_timestamp'))
        end_timestamp = int(self.get_argument('end_timestamp'))
        logging.info('getdata request. from_timestamp = {0} count = {1}'.format(start_timestamp, end_timestamp))

        posts = db.get(start_timestamp, end_timestamp)

        logging.info("response with {0} posts".format(len(posts)))
        self.write({'posts': posts})

application = tornado.web.Application([
    (r'/ws', WSHandler),
    (r'/getdata', GetDataHandler),
    (r'/getdata2', GetDataHandler2),
    (r"/(.*)", tornado.web.StaticFileHandler, {"path": "data/index.html"})
])

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(9999)
    myIP = socket.gethostbyname(socket.gethostname())
    logging.info(u'*** Server Started at {0:s}:9999'.format(myIP))
    tornado.ioloop.IOLoop.instance().start()


