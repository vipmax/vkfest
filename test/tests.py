# coding=utf-8
import time
import geopy
import geopy.distance
import re
import requests
import vk
from datetime import datetime
import concurrent.futures


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
        print("{0}, {1}".format(str(destination.latitude), str(destination.longitude)), len(first_posts), \
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






import vk
import re
import requests
import time
from datetime import datetime

vkapi = vk.API(vk.Session(), v='5.20', lang='ru', timeout=100)


def get_photo_ids(geohash='8NTZtoXr'):
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

    content = requests.Session().post('https://vk.com/al_places.php', data=data, headers=headers)
    html = content.content.decode('utf-8')
    prog = re.compile('href="\/photo(\w+)"')
    photo_ids = set(prog.findall(html))

    return photo_ids


def get_photos(photo_ids):
    return vkapi.photos.getById(photos=photo_ids)


def get_photos_with_posts(photo_ids):
    return list(filter(lambda p: 'post_id' in p, vkapi.photos.getById(photos=photo_ids)))


def get_photos_with_posts(photos):
    return list(filter(lambda p: 'post_id' in p, photos))


alphabet = set(map(chr, range(ord('a'), ord('z') + 1)))
alphabet.update(set(map(chr, range(ord('A'), ord('Z') + 1))))
alphabet.update(set(map(chr, range(ord('0'), ord('9') + 1))))
alphabet.update({'-', '_'})

all_tags = set()
for c1 in alphabet:
    for c2 in alphabet:
        for c3 in alphabet:
            all_tags.add("8NTZE" + c1 + c2 + c3)

print(len(all_tags))

all_photo_ids = set()
all_photos_with_post = set()
photos_count = 0
timeout = 100


def start_geohash_crawler(geohash, timeout):
    try:
        global photos_count
        photo_ids = get_photo_ids(geohash)
        photos_count += len(photo_ids)
        all_photo_ids.update(photo_ids)
        photos = get_photos(photo_ids=','.join(photo_ids))
        posts = ['{}_{}'.format(p['owner_id'], p['post_id']) for p in photos if 'post_id' in p.keys()]

        all_photos_with_post.update(posts)

        print("{} геохеш = {} максимум {}, {} добавлено, {} всего фото, всего с постами {}".format(
            datetime.now(),
            geohash,
            photos_count,
            len(photo_ids),
            len(all_photo_ids),
            len(all_photos_with_post)))
        return len(posts)
    except Exception as e:
        print(e)
    return 0

# while True:
with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
    i = 0
    futures = {executor.submit(start_geohash_crawler, tag, timeout): tag for tag in list(all_tags)[:300]}
    for future in concurrent.futures.as_completed(futures):
        url = futures[future]
        try:
            data = future.result()
            i += 1
            print(u'{} {} added {} post'.format(i, url, data))
        except Exception as e:
            print(u"{} generated an exception {}".format(url, e))

    # time.sleep(1)
