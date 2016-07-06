# coding=utf-8
import time
import geopy
import geopy.distance
import vk
from datetime import datetime

# vkapi = vk.API(vk.Session(), v='5.20', lang='ru', timeout=100)
#



def get_news_by_time():
    day = 86400
    to_unixtime = lambda datetime_: int(time.mktime(datetime_.timetuple()))
    from_unixtime = lambda utime: datetime.fromtimestamp(utime)
    start = to_unixtime(datetime.now()) - day
    end = to_unixtime(datetime.now())
    data = set()
    while (True):
        posts = vkapi.newsfeed.search(q='spb', latitude='59.939145', longitude='30.315699', count='200',
                                      end_time=end, start_time=start)
        for post in posts['items']:
            data.add("{}_{} \n".format(post['owner_id'], post['id']))
        # print 'https://vk.com/feed?w=wall{}_{} \n'.format(post['owner_id'],post['id']), datetime.fromtimestamp(post['date'])

        end = end - day
        start = start - day
        print len(data)


# get_news_by_time()


def grid_analysing():
    build_id = lambda post: 'https://vk.com/feed?w=wall{}_{}'.format(post['owner_id'], post['id'])

    def extract_posts(latitude, longitude):
        return {build_id(post) for post in vkapi.newsfeed.search(q='#spb',
                                                                 latitude=latitude,
                                                                 longitude=longitude,
                                                                 count='200')['items']}

    def extract_all_posts(latitude, longitude):
        day = 86400
        start_time = to_unixtime(datetime.now()) - day
        end_time = to_unixtime(datetime.now())
        result_posts = set()
        enough = False
        while not enough:
            posts = vkapi.newsfeed.search(q='#spb',
                                          latitude=latitude,
                                          longitude=longitude,
                                          count='200',
                                          end_time=end_time,
                                          start_time=start_time)

            for post in posts['items']: result_posts.add(build_id(post))

            end_time -= day
            start_time -= day
            if len(result_posts) > 1000: enough = True

        return result_posts

    distance = geopy.distance.VincentyDistance(kilometers=1)
    current_point = geopy.Point(59.9823704964, 30.32410114)  # park 300 spb
    first_posts = extract_posts(current_point.latitude, current_point.longitude)
    while True:
        destination = distance.destination(point=current_point, bearing=180)
        current_point = geopy.Point(destination.latitude, destination.longitude)
        current_posts = extract_posts(current_point.latitude, current_point.longitude)
        print "{0}, {1}".format(str(destination.latitude), str(destination.longitude)), len(first_posts),\
            len(current_posts), len(first_posts.intersection(current_posts))
        first_posts = current_posts


# grid_analysing()





def sorted_containers_test():
    from sortedcontainers import SortedSet
    import random
    import time
    ss = SortedSet()
    start = time.time()
    for i in range(1000000):
        ss.add(random.randint(0, i))
    print "adding elapsed ", time.time() - start
    start = time.time()
    print ss[10]
    print "getting elapsed", time.time() - start


# sorted_containers_test()


import json

listok = {u'привет': u'медвед'}
data = json.dumps(listok)
print('Json: %s' % data)

new_obj = json.loads(data)
print('Python obj: %s' % new_obj)