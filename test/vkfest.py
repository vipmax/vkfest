# coding=utf-8

import bisect
import vk
import threading
from multiprocessing.pool import ThreadPool
import time
import random

posts_buffer = list()
lock = threading.Lock()

def insert_to_buffer(e):
    # lock.acquire()
    print(threading.currentThread(), ' trying to add posts')
    bisect.insort_right(posts_buffer, e)
    # lock.release()


class Post:
    def __init__(self, data):
        self.data = data

    def get(self, key):
        return self.data[key]

    def __lt__(self, other):
        return int(self.data['date']) < int(other.data['date'])

    def __eq__(self, other):
        return self.data['owner_id'] == other.data['owner_id'] and self.data['id'] == other.data['id']


def job(x):
    while True:
        vkapi = vk.API(vk.Session(), v='5.20', lang='ru', timeout=100)
        posts = vkapi.newsfeed.search(q='#spb', latitude='59.939145', longitude='30.315699', count='200')['items']
        for p in posts: insert_to_buffer(Post(p))
        time.sleep(random.randint(0, 10))


if __name__ == '__main__':
    pool = ThreadPool(10)

    results = pool.map(job, list(range(3)))

    pool.close()
    pool.join()

    for post in posts_buffer[-10:]:
        print(post.get('date'))


