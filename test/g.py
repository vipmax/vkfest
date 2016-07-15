import random
import time
import vk
from sortedcontainers import SortedSet

vkapi = vk.API(vk.Session(), v='5.20', lang='ru', timeout=100)

buffer = SortedSet()

at = "1a8b5a1b5851124e7f57a3e942eb7f0a4f6e7f3860abb4ffdecf401c1906cfa13e63e05d54f8c4fdd8a64"

user_fields = """photo_id, verified, sex, bdate, city, country, home_town,
has_photo, photo_50, photo_100, photo_200_orig, photo_200,
photo_400_orig, photo_max, photo_max_orig, online, lists,
domain, has_mobile, contacts, site, education, universities,
schools, status, last_seen, followers_count,  occupation, nickname,
relatives, relation, personal, connections, exports, wall_comments,
activities, interests, music, movies, tv, books, games, about, quotes,
can_post, can_see_all_posts, can_see_audio, can_write_private_message,
can_send_friend_request, is_favorite, is_hidden_from_feed, timezone,
screen_name, maiden_name, crop_photo, is_friend, friend_status, career,
 military, blacklisted, blacklisted_by_me"""


class G:
    def __init__(self, data):
        self.data = data

    def __eq__(self, other):
        return self.data['id'] == other.data['id']

    def __hash__(self):
        return hash(self.data['id'])

    def __str__(self):
        if 'bdate' in self.data.keys():
            return ', '.join([self.data['first_name'],
                              self.data['last_name'],
                              self.data['bdate'],
                              self.data['tag'],
                              "http://vk.com/id" + str(self.data['id'])])
        else:
            return ', '.join([self.data['first_name'],
                              self.data['last_name'],
                              "http://vk.com/id" + str(self.data['id'])])

    def __lt__(self, other):
        return int(self.data['id']) < int(other.data['id'])


def add_to_buffer(g):
    if g not in buffer:
        buffer.add(g)
        print("added " + str(g))
        try:
            vkapi.messages.send(user_id="32908760", message=str(g), access_token=at)
        except Exception as e:
            print(e)
        time.sleep(random.randint(2, 5))


def age_filter(g):
    try:
        bdate = g["bdate"].split(".")
        year = int(bdate[2])
        if 1991 <= year <= 1997:
            return True
        else:
            return False
    except:
        pass
    return True


def sity_filter(g):
    try:
        if g['city']['title'] == 'Санкт-Петербург':
            return True
    except:
        pass

    return False


def relationship_filter(g):
    try:
        if g['relation'] in [1,6,0]:
            return True
    except:
        pass

    return False

def friends_count_filter(g):
    try:
        if 50 < g['followers_count'] < 200:
            return True
    except:
        pass

    return False


tags = ["#спб", "спб", "#питер", "питер", "#санктпетербург", "санктпетербург", "#vkfest", "vkfest", "#знакомства",
        "знакомства"]
while True:
    for tag in tags:
        response = vkapi.newsfeed.search(q=tag, count='200', extended="1")
        users = response['profiles']
        gs = filter(lambda u: u["sex"] == 1, users)
        gs = vkapi.users.get(user_ids=','.join(list(map(lambda u: str(u['id']), gs))), fields=user_fields)
        gs = list(filter(sity_filter, gs))
        gs = list(filter(age_filter, gs))
        gs = list(filter(relationship_filter, gs))
        gs = list(filter(friends_count_filter, gs))

        for g in gs:
            g['tag'] = tag
            add_to_buffer(G(g))

    print("sleeping 1 min")
    time.sleep(60)
