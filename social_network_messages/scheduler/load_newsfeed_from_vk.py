import calendar
import datetime
import re

from django.db import IntegrityError
from vk_api import vk_api

import configurations
from social_network_messages.models import Message


def _auth():
    vk_session = vk_api.VkApi(configurations.vk_api["user"], configurations.vk_api["password"])

    try:
        vk_session.auth(reauth=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)

    return vk_session


def _create_message(post):
    message = Message(url=post["url"],
                      name=post["name"],
                      content=post["text"],
                      source=post["from"],
                      createdAt=post["date_time"])
    try:
        message.save()
    except IntegrityError:
        pass


def _format_posts(raw_posts):
    def get_info_from_club(post):
        for found_group in filter(lambda group: group["id"], raw_posts["groups"]):
            name = found_group["name"]

        return {"from": "VK club", "name": name}

    def get_info_from_profile(post):
        for found_profile in filter(lambda profile: profile["id"], raw_posts["profiles"]):
            name = f"{found_profile['first_name']} {found_profile['last_name']}"

        return {"from": "VK profile", "name": name}

    def inner_format_post(post):
        source_info = get_info_from_club(post) if post['from_id'] < 0 else get_info_from_profile(post)

        url = f"vk.com/wall{post['owner_id']}_{post['id']}"
        text = re.sub(r"[\n\t]", "", post['text'])
        date_time = datetime.datetime.utcfromtimestamp(int(post['date']))

        return {"from": source_info["from"], "name": source_info["name"], "url": url, "text": text,
                "date_time": date_time}

    return [inner_format_post(post) for post in raw_posts['items'] if post['post_type'] == 'post']


def load_newsfeed():
    query = configurations.query_search
    limit_per_list = 200
    current_time = calendar.timegm((datetime.datetime.utcnow().date() - datetime.timedelta(days=1)).timetuple())

    session = _auth()
    vk = session.get_api()

    buffer = []

    raw_posts = vk.newsfeed.search(q=query, count=limit_per_list, start_time=current_time, extended=1)

    for post in _format_posts(raw_posts):
        buffer.append(post)

    while "next_from" in raw_posts:
        raw_posts = vk.newsfeed.search(q=query, count=limit_per_list, start_from=raw_posts["next_from"],
                                       start_time=current_time, extended=1)
        for post in _format_posts(raw_posts):
            buffer.append(post)

    [_create_message(post) for post in buffer]
