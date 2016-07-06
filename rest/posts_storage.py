# coding=utf-8
import sys
import threading
import vk
from sortedcontainers import SortedSet
import sentiment_analisys
from post import Post
from multiprocessing.pool import ThreadPool
import time, random
# reload(sys)
# sys.setdefaultencoding('UTF8')

buffer = SortedSet()
lock = threading.Lock()

def add_toBuffer(post):
    if post not in buffer:
        sentiment_result = sentiment_analisys.process(post['text'])
        post['sentiment_result'] = sentiment_result
        # lock.acquire()
        # critical section start
        buffer.add(post)
        print('buffer len = {}'.format(len(buffer)))
        # critical section end
        # lock.release()

def get(from_timestamp, count):
    index = buffer.bisect_left(Post({'date': from_timestamp}))
    data = buffer[index: index + count]
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


add_posts()
#
#
# def job(tag):
#     print tag
#     while True:
#         print "da"
#         vkapi = vk.API(vk.Session(), v='5.20', lang='ru', timeout=100)
#         posts = vkapi.newsfeed.search(q=tag, latitude='59.939145', longitude='30.315699', count='200')['items']
#         for p in posts: add_toBuffer(Post(p))
#         # time.sleep(random.randint(0, 10))
#
#
# pool = ThreadPool(12)
#
# # pool.map(job, [u'spb', u'saint', u'питер', u'спб', u'санктпетербург'])
# pool.map(job, [u'#spb', u'#saint', u'#питер', u'#спб', u'#санктпетербург'])
#
# # pool.close()
# pool.join()


#
# import crawler
#
# thread = threading.Thread(target=crawler.start)
# thread.start()
