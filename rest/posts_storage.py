# coding=utf-8
import threading
from datetime import datetime

import vk
from sortedcontainers import SortedSet
from post import Post
import pymongo
import time

import sentiment_analisys
import db
import vk_util
import poligons

import logging
logger = logging.getLogger('rest')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())
# logging.basicConfig(filename='log.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

buffer = SortedSet()
lock = threading.Lock()

vkapi = vk.API(vk.Session(), v='5.20', lang='ru', timeout=100)


def add_toBuffer(post):
    if post not in buffer:
        post['sentiment_result'] = sentiment_analisys.process(post['text'])
        post['owner_info'] = vk_util.get_profile(post['owner_id'])

        if len(buffer) >= 10000:
            logging.info('deleting ' + str(buffer[0]))
            del buffer[0]

        post["added_time"] = int(datetime.now().strftime("%s"))
        try:
            post['zone'] = poligons.get_zone(post['lat'], post['long'])
        except:
            post['zone'] = "nozone"

        buffer.add(post)
        db.save(post.data)
        logging.info('buffer len = {}'.format(len(buffer)))


def get(from_timestamp, count):
    if from_timestamp == -1:
        data = buffer[-count:]
        for d in data:
            logging.info(d['date'])
        return data

    index = buffer.bisect_left(Post({'added_time': from_timestamp}))
    data = buffer[index: index + count]
    for d in data:
        logging.info(d['added_time'])
    return data


# just while testing
def add_posts():
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
    q = {'date': {'$gte': int(datetime.now().strftime("%s"))}}

    db = pymongo.MongoClient("192.168.13.133").VkFest
    coll = db.data
    cursor = coll.find({}, cursor_type=pymongo.CursorType.TAILABLE_AWAIT)
    while True:
        for doc in cursor:
            logging.info(doc)
            add_toBuffer(Post(doc))
        time.sleep(0.5)
        logging.info("")

thread = threading.Thread(target=stream_new_posts)
thread.start()
