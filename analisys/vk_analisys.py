import pymongo
import datetime



vk_posts_collection = pymongo.MongoClient(host="192.168.13.110")['VKFest']['VkFest2016_posts']

start = datetime.datetime(2015, 7, 16)
end = datetime.datetime(2015, 7, 22)
q = {
    '$and': [
        {'geo_coordinates': {'$exists': True}}
        ,{'geo_coordinates': {'$ne': 'Unk'}}
        ,{'date': {'$lt': end, '$gte': start}}
    ]
}

posts = list()
i = 0
for p in vk_posts_collection.find(q):
    geo = p['geo_coordinates'].split(" ")
    lan = float(geo[0])
    lon = float(geo[1])
    i += 1
    print(p)

    # if 59.990438 > lan > 59.977705 and 30.183583 < lon < 30.212783:  # 300park
    if 60.173958 > lan > 59.714529 and 29.837154 < lon < 30.675976:    # sbp
        posts.append(p)
        print('в квадрате {} из {}'.format(len(posts), i))

