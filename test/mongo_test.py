import pymongo
import time

db = pymongo.MongoClient("192.168.13.110").Test
coll = db.captest
cursor = coll.find({}, {}, cursor_type=pymongo.CursorType.TAILABLE_AWAIT)
while True:
    for doc in cursor:
        print(doc)
    time.sleep(1)
