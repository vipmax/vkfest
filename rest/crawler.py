# coding=utf-8
import concurrent.futures
import time
import vk
import pymongo



tags = [u'#spb', u'#saint', u'#питер', u'#спб', u'#санктпетербург', u'#санкт-петербург']
timeout = 100


def task(tag, request_timeout):
    vkapi = vk.API(vk.Session(), v='5.20', lang='ru', timeout=request_timeout)
    vk_posts_collection = pymongo.MongoClient(host="192.168.13.110")['Test']['vk_posts']

    added_count = 0
    posts = vkapi.newsfeed.search(q=tag, count='200')['items']
    for post in posts:
        key = {'_id': "{}_{}".format(post['owner_id'], post['id'])}
        fields = {'$set': post}
        try:
            updated_result = vk_posts_collection.update(key, fields, True, False)
            added_count += not updated_result['updatedExisting']
            if not updated_result['updatedExisting']:
                print("added =", key)
        except:
            pass
    return added_count


def start():
    while True:
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:

            futures = {executor.submit(task, tag, timeout): tag for tag in tags}
            for future in concurrent.futures.as_completed(futures):
                url = futures[future]
                try:
                    data = future.result()
                    print(u'{} added {} post'.format(url, data))
                except Exception as e:
                    print(u"{} generated an exception {}".format(url, e))

        time.sleep(1)


if __name__ == '__main__':
    try:
        pymongo.MongoClient(host="192.168.13.110")['Test'].create_collection('vk_posts', capped=True, size=99999999999)
        print("Table created")
    except:
        print("Table already created")

    start()
