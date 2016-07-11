# coding=utf-8
import threading
import vk
from sortedcontainers import SortedSet
import sentiment_analisys
from post import Post
import pymongo
import time
import db

import logging
logger = logging.getLogger('rest')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())
# logging.basicConfig(filename='log.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

buffer = SortedSet()
lock = threading.Lock()


def add_toBuffer(post):
    if post not in buffer:
        sentiment_result = sentiment_analisys.process(post['text'])
        post['sentiment_result'] = sentiment_result

        if len(buffer) >= 10000:
            logging.info('deleting ' + str(buffer[0]))
            del buffer[0]

        buffer.add(post)
        db.save(post.data)
        logging.info('buffer len = {}'.format(len(buffer)))


def get(from_timestamp, count):
    if from_timestamp == -1:
        data = buffer[-count:]
        for d in data:
            logging.info(d['date'])
        return data

    index = buffer.bisect_left(Post({'date': from_timestamp}))
    data = buffer[index: index + count]
    for d in data:
        logging.info(d['date'])
    return data


# just while testing
def add_posts():
    vkapi = vk.API(vk.Session(), v='5.20', lang='ru', timeout=100)
    posts = vkapi.newsfeed.search(q='#spb',
                                  latitude='59.939145',
                                  longitude='30.315699',
                                  count='200')['items']
    for post in posts:
        # buffer.add(Post(post))
        add_toBuffer(Post(post))
        logging.info(post['date'])


# for testing
# add_posts()


def stream_new_posts():
    db = pymongo.MongoClient("192.168.13.110").Test
    coll = db.data
    cursor = coll.find({}, cursor_type=pymongo.CursorType.TAILABLE_AWAIT)
    while True:
        for doc in cursor:
            logging.info(doc)
            add_toBuffer(Post(doc))
        time.sleep(1)


thread = threading.Thread(target=stream_new_posts)
thread.start()
