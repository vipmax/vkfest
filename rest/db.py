import pymongo
from datetime import datetime
vk_posts_with_polarity = pymongo.MongoClient(host="192.168.13.110")['Test']['vk_posts_with_polarity_collection']


def save(post):
    vk_posts_with_polarity.update({'_id': '{}_{}'.format(post['owner_id'], post['id'])}, {'$set': post}, True, False)

def get(start, end):
    datetime.fromtimestamp(start)
    datetime.fromtimestamp(end)
    q = {'date': {'$lt': end, '$gte': start}}
    return list(vk_posts_with_polarity.find(q).limit(10000))

# for test
if __name__ == '__main__':
    for p in get(start=1467962400, end=1467963650):
        print(p)

