# coding=utf-8
import concurrent.futures
import time
import pymongo as pymongo
import vk
import re
import requests
from datetime import datetime

import logging
logger = logging.getLogger('rest')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())
# logging.basicConfig(filename='log.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

vkapi = vk.API(vk.Session(), v='5.20', lang='ru', timeout=100)
vk_photos_collection = pymongo.MongoClient(host="192.168.13.110")['Test']['data']


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


#
# alphabet = set(map(chr, range(ord('a'), ord('z') + 1)))
# alphabet.update(set(map(chr, range(ord('A'), ord('Z') + 1))))
# alphabet.update(set(map(chr, range(ord('0'), ord('9') + 1))))
# alphabet.update({'-', '_'})
#
# all_tags = set()
# for c1 in alphabet:
#     for c2 in alphabet:
#         for c3 in alphabet:
#             all_tags.add("8NTZE" + c1 + c2 + c3)


all_tags = ['8NTZEo1h', '8NTZEpiU', '8NTZEpmw', '8NTZEpn_', '8NTZEp8m', '8NTZEsqZ', '8NTZEsu_', '8NTZEuRh', '8NTZEuXa',
            '8NTZEtio', '8NTZEnqx', '8NTZEniW', '8NTZElvn', '8NTZEnXG', '8NTZElNu', '8NTZEP7L', '8NTZEPpi', '8NTZEOzr',
            '8NTZEOmt', '8NTZEL2N', '8NTZEL7W', '8NTZEkAU', '8NTZEkQu', '8NTZEkXn', '8NTZEk0v', '8NTZEknE', '8NTZEhfL',
            '8NTZEhn8', '8NTZEh8W', '8NTZEksz', '8NTZEk8d', '8NTZEmbF', '8NTZEmD-', '8NTZEjVI', '8NTZEhvs', '8NTZEjG8',
            '8NTZEjZD', '8NTZEj1z', '8NTZEmmo', '8NTZEm-B', '8NTZEsbn', '8NTZEsnO', '8NTZEshp', '8NTZEpV9', '8NTZEj4x',
            '8NTZEpN4', '8NTZEvNm', '8NTZEtYM', '8NTZEnzR', '8NTZEl0b', '8NTZEO_g', '8NTZEOb2', '8NTZEOWN', '8NTZEM_C',
            '8NTZEMxp', '8NTZEMNK', '8NTZEMBO', '8NTZEJWn', '8NTZEMKP', '8NTZEMj3', '8NTZEMiw', '8NTZEJaM', '8NTZEJkl',
            '8NTZEJxs', '8NTZEJ_s', '8NTZELQb', '8NTZEkLa', '8NTZEkww', '8NTZEk-7', '8NTZEmxH', '8NTZEmGI', '8NTZEpV9',
            '8NTZEu3T', '8NTZGFIB', '8NTZGFoH', '8NTZGGUm', '8NTZGGaU', '8NTZGGsQ', '8NTZGD9s', '8NTZGDf0', '8NTZGDUv',
            '8NTZGDBT', '8NTZGAsQ', '8NTZGANv', '8NTZEq4c', '8NTZEqWH', '8NTZErI7', '8NTZEq9n', '8NTZGAe0', '8NTZGBMY',
            '8NTZErt_', '8NTZErwa', '8NTZErNT', '8NTZErWw', '8NTZErfr', '8NTZEuoB', '8NTZGBUf', '8NTZGEJO', '8NTZGEHO',
            '8NTZEutP', '8NTZGEzi', '8NTZGGBw', '8NTZGB3s', '8NTZEvls', '8NTZGFYW', '8NTZGHLN', '8NTZGMH4']

logging.info(len(all_tags))

all_photo_ids = 0
photos_count = 0
timeout = 100


def start_geohash_crawler(geohash, timeout):
    try:
        global photos_count, all_photo_ids, all_photos_with_post

        photo_ids = get_photo_ids(geohash)
        photos_count += len(photo_ids)
        all_photo_ids += len(photo_ids)
        photos = get_photos(photo_ids=','.join(photo_ids))

        added_count = 0
        for p in photos:
            ur = vk_photos_collection.update({'_id': p['id']}, {'$set': p}, True, False)
            added_count += not ur['updatedExisting']

        logging.info("{} геохеш = {} {} добавлено, всего {} новых фото".format(
                    datetime.now(),
                    geohash,
                    len(photo_ids),
                    added_count))
        return added_count
    except Exception as e:
        logging.info(e)
    return 0


if __name__ == '__main__':
    try:
        pymongo.MongoClient(host="192.168.13.110")['Test'].create_collection('data', capped=True, size=99999999999)
        logging.info("Table created")
    except:
        logging.info("Table already created")

    while True:
        try:
            all_photo_ids = 0
            all_photos_with_post = 0
            photos_count = 0
            with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
                i = 0
                futures = {executor.submit(start_geohash_crawler, tag, timeout): tag for tag in list(all_tags)}
                for future in concurrent.futures.as_completed(futures):
                    url = futures[future]
                    try:
                        data = future.result()
                        i += 1
                        logging.info(u'{} {} added {} post'.format(i, url, data))
                    except Exception as e:
                        logging.info(u"{} generated an exception {}".format(url, e))

            time.sleep(10)
        except:
            pass
