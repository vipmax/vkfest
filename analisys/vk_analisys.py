# coding=utf-8
import pymongo
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import time

import logging
logger = logging.getLogger('tipper')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())
# logging.basicConfig(filename='log.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# vk_posts_collection = pymongo.MongoClient(host="192.168.13.110")['VKFest']['VkFest2016_posts']
# start = datetime.datetime(2015, 7, 16)
# end = datetime.datetime(2015, 7, 22)
# q = {
#     '$and': [
#         {'geo_coordinates': {'$exists': True}}
#         ,{'geo_coordinates': {'$ne': 'Unk'}}
#         ,{'date': {'$lt': end, '$gte': start}}
#     ]
# }
#
# posts = list()
# i = 0
# for p in vk_posts_collection.find(q):
#     geo = p['geo_coordinates'].split(" ")
#     lan = float(geo[0])
#     lon = float(geo[1])
#     i += 1
#     print(p)
#
#     # if 59.990438 > lan > 59.977705 and 30.183583 < lon < 30.212783:  # 300park
#     if 60.173958 > lan > 59.714529 and 29.837154 < lon < 30.675976:    # sbp
#         posts.append(p)
#         print(u'в квадрате {} из {}'.format(len(posts), i))
#
#

def activity():
    global time
    vk_posts_collection = pymongo.MongoClient(host="192.168.13.110")['Test']['vk_photos_collection']
    to_unixtime = lambda datetime_: int(datetime_.strftime("%s"))
    from_date = datetime.datetime(2016, 7, 9)
    q = {
        '$and': [
            {'date': {'$exists': True}}
            , {'date': {'$gte': to_unixtime(from_date)}}
        ]
    }
    data = []
    for entry in vk_posts_collection.find(q):
        logging.info(entry)
        time = datetime.datetime.fromtimestamp(entry['date'])
        data.append([time, 1])
    data = sorted(data, key=lambda x: x[0])
    i = 1
    for e in data:
        i += 1
        e[1] = i

    logging.info(data)
    logging.info(len(data))
    logging.info(to_unixtime(from_date))
    x = [e[0] for e in data]
    y = [e[1] for e in data]
    from matplotlib import rc
    #
    # font = {
    #     'family': 'Verdana',
    #     'weight': 'normal',
    #     'size': 10
    # }
    # rc('font', **font)
    plt.figure(figsize=(20, 10))
    plt.title(u'Posts activity')
    plt.xlabel(u'Time of post')
    plt.ylabel(u'Posts')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
    plt.gca().xaxis.set_major_locator(mdates.HourLocator())
    plt.plot(x, y, marker='o', label=u"Posts")
    plt.xticks(rotation=90)
    plt.legend()
    plt.grid()
    # plt.savefig(str(id) + "_posts", bbox_inches='tight', dpi=500)
    plt.show()

activity()
