# coding=utf-8

class Post:
    def __init__(self, data):
        self.data = data

        if 'post_type' not in data.keys():
            data['type'] = "photo"
        else:
            data['type'] = "post"

        if 'geo' in data.keys():
            geo = data['geo']['coordinates'].split(' ')
            data['lat'] = float(geo[0])
            data['long'] = float(geo[1])

        if 'attachments' in data.keys():
            for a in data['attachments']:
                if a['type'] == 'photo':
                    sizes = list(filter(lambda p: p.startswith('photo'), a['photo'].keys()))
                    maxsize = max(list(map(lambda p: int(p.replace("photo_",'')), sizes)))
                    data['photo_url'] = a['photo']['photo_' + str(maxsize)]
                    break

        if 'photo_75' in data.keys():
            sizes = list(filter(lambda p: p.startswith('photo'), data.keys()))
            maxsize = max(list(map(lambda p: int(p.replace("photo_", '')), sizes)))
            data['photo_url'] = data['photo_' + str(maxsize)]

        if 'src_xxbig' in data.keys():
            data['photo_url'] = data['src_xxbig']
        elif 'src_xbig' in data.keys():
            data['photo_url'] = data['src_xbig']
        elif 'src_big' in data.keys():
            data['photo_url'] = data['src_big']
        elif 'src' in data.keys():
            data['photo_url'] = data['src']



    def get(self, key):
        return self.data[key]

    def __lt__(self, other):
        return int(self.data['added_time']) < int(other.data['added_time'])

    def __eq__(self, other):
        return self.data['owner_id'] == other.data['owner_id'] and \
               self.data['id'] == other.data['id']

    def __hash__(self):
        return hash(self.data['owner_id']) ^ hash(self.data['id'])

    def __str__(self):
        return u'Post(id={}_{},text={},date={} added_time={})'. \
            format(self.data['owner_id'],
                   self.data['id'],
                   self.data['text'][:20].replace('\n',' ').encode("utf-8"),
                   int(self.data['date']),
                   self.data["added_time"])


    def __getitem__(self, item):
        return self.data[item]

    def __setitem__(self, key, value):
        self.data[key] = value

