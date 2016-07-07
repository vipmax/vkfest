# coding=utf-8
import time
import geopy
import geopy.distance
import re
import requests
import vk
from datetime import datetime

#



def get_news_by_time():
    day = 86400
    to_unixtime = lambda datetime_: int(time.mktime(datetime_.timetuple()))
    from_unixtime = lambda utime: datetime.fromtimestamp(utime)
    start = to_unixtime(datetime.now()) - day
    end = to_unixtime(datetime.now())
    data = set()
    while (True):
        vkapi = vk.API(vk.Session(), v='5.20', lang='ru', timeout=100)
        posts = vkapi.newsfeed.search(q='spb', latitude='59.939145', longitude='30.315699', count='200',
                                      end_time=end, start_time=start)
        for post in posts['items']:
            data.add("{}_{} \n".format(post['owner_id'], post['id']))
        # print 'https://vk.com/feed?w=wall{}_{} \n'.format(post['owner_id'],post['id']), datetime.fromtimestamp(post['date'])

        end = end - day
        start = start - day
        print(len(data))


# get_news_by_time()


def grid_analysing():
    vkapi = vk.API(vk.Session(), v='5.20', lang='ru', timeout=100)
    build_id = lambda post: 'https://vk.com/feed?w=wall{}_{}'.format(post['owner_id'], post['id'])
    to_unixtime = lambda datetime_: int(time.mktime(datetime_.timetuple()))
    from_unixtime = lambda utime: datetime.fromtimestamp(utime)

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
        print("{0}, {1}".format(str(destination.latitude), str(destination.longitude)), len(first_posts),\
            len(current_posts), len(first_posts.intersection(current_posts)))
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
    print("adding elapsed ", time.time() - start)
    start = time.time()
    print(ss[10])
    print("getting elapsed", time.time() - start)


# sorted_containers_test()


def jdon_test():
    import json
    listok = {u'привет': u'медвед'}
    data = json.dumps(listok)
    print('Json: %s' % data)
    new_obj = json.loads(data)
    print('Python obj: %s' % new_obj)


# jdon_test()





geohash = '8NTZtoXr'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest'
}

data = {
    "act": "show_photo_more",
    "al": 1,
    "geohash": geohash,
    "offset": 0,
    "photo_skip": '0_',
}

s = requests.Session()

content = s.post('https://vk.com/al_places.php', data=data, headers=headers)

html = content.content.decode('utf-8')

prog = re.compile('href="\/photo(\w+)"')


photo_ids = list(prog.findall(html))

for p in photo_ids:
    print(p)

vkapi = vk.API(vk.Session(), v='5.20', lang='ru', timeout=100)
photos = vkapi.photos.getById(photos=','.join(photo_ids))

for p in photos:
    print(p)




['8NTZtoXr',
'8NTZtoc8',
'8NTZto0w',
'8NTZtoBO',
'8NTZtoHQ',
'8NTZtoTK',
'8NTZtoWk',
'8NTZtobF',
'8NTZtowS',
'8NTZtoy6',
'8NTZtom9',
'8NTZtoOf',
'8NTZtoNc',
'8NTZtoGl',
'8NTZtoLx',
'8NTZtoid',
'8NTZtoKc',
'8NTZtoIc',
'8NTZtoCA',
'8NTZs9yp',
'8NTZs9t0',
'8NTZs9va',
'8NTZs_G1',
'8NTZs9wm',
'8NTZs9ae',
'8NTZs9TS',
'8NTZs3-g',
'8NTZs9nJ',
'8NTZs9ga',
'8NTZs8N_',
'8NTZs8nE',
'8NTZs8uT',
'8NTZs-hl',
'8NTZs-mV',
'8NTZs-2r',
'8NTZs-U_',
'8NTZs3_6',
'8NTZs9c9',
'8NTZs9ev']



['8NTZEo1h',
'8NTZEpiU',
'8NTZEpmw',
'8NTZEpn_',
'8NTZEp8m',
'8NTZEsqZ',
'8NTZEsu_',
'8NTZEuRh',
'8NTZEuXa',
'8NTZEtio',
'8NTZEnqx',
'8NTZEniW',
'8NTZElvn',
'8NTZEnXG',
'8NTZElNu',
'8NTZEP7L',
'8NTZEPpi',
'8NTZEOzr',
'8NTZEOmt',
'8NTZEL2N',
'8NTZEL7W',
'8NTZEkAU',
'8NTZEkQu',
'8NTZEkXn',
'8NTZEk0v',
'8NTZEknE',
'8NTZEhfL',
'8NTZEhn8',
'8NTZEh8W',
'8NTZEksz',
'8NTZEk8d',
'8NTZEmbF',
'8NTZEmD-',
'8NTZEjVI',
'8NTZEhvs',
'8NTZEjG8',
'8NTZEjZD',
'8NTZEj1z',
'8NTZEmmo',
'8NTZEm-B',
'8NTZEsbn',
'8NTZEsnO',
'8NTZEshp',
'8NTZEpV9',
'8NTZEj4x',
'8NTZEpN4']
