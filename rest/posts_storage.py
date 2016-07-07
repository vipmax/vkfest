# coding=utf-8
import threading
import vk
from sortedcontainers import SortedSet
import sentiment_analisys
from post import Post
import pymongo
import time

buffer = SortedSet()
lock = threading.Lock()


def add_toBuffer(post):
    if post not in buffer:
        sentiment_result = sentiment_analisys.process(post['text'])
        post['sentiment_result'] = sentiment_result
        # lock.acquire()
        # critical section start
        if len(buffer) > 10000:
            print('deleting ' + str(buffer[0]))
            del buffer[0]

        buffer.add(post)
        print('buffer len = {}'.format(len(buffer)))
        # critical section end
        # lock.release()


def get(from_timestamp, count):
    if from_timestamp == -1:
        data = buffer[-count:]
        for d in data:
            print(d['date'])
        return data

    index = buffer.bisect_left(Post({'date': from_timestamp}))
    data = buffer[index: index + count]
    for d in data:
        print(d['date'])
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
        print(post['date'])


# for testing
# add_posts()




def stream_new_posts():
    db = pymongo.MongoClient("192.168.13.110").Test
    coll = db.vk_posts
    cursor = coll.find(cursor_type=pymongo.CursorType.TAILABLE_AWAIT)
    while True:
        for doc in cursor:
            print(doc)
            add_toBuffer(Post(doc))
        time.sleep(1)
        print()


thread = threading.Thread(target=stream_new_posts)
thread.start()
