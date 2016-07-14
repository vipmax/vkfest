from datetime import datetime

import pymongo
import time


import logging
logger = logging.getLogger('rest')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())
# logging.basicConfig(filename='log.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

db = pymongo.MongoClient("192.168.13.110").Test
coll = db.data
q = {'date': {'$gte': int(datetime.now().strftime("%s"))}}
# q = {}
cursor = coll.find(q, cursor_type=pymongo.CursorType.TAILABLE_AWAIT)
while True:
    for doc in cursor:
        logging.info(doc)
    time.sleep(1)
    logging.info("")
