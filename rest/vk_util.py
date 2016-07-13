import vk

vkapi = vk.API(vk.Session(), v='5.20', lang='ru', timeout=100)


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

group_fields = """city, country, place, description, wiki_page, members_count,
"counters, start_date, finish_date, can_post, can_see_all_posts, activity,
"status, contacts, links, fixed_post, verified, site,ban_info"""

def get_profile(profile_id):
    try:
        if profile_id > 0:
            return vkapi.users.get(user_ids=profile_id, fields=user_fields)[0]
        else:
            return vkapi.groups.getById(group_ids=-int(profile_id), fields=group_fields)[0]
    except:
        return {}
