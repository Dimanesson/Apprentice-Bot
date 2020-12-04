# -*- coding: utf-8 -*-

import requests
import re
import json
from bs4 import BeautifulSoup


def import_video(url: str, session=requests.Session()) -> {}:
    url = re.sub(r"/\?.+", "", url)

    u_a = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
    r = session.get(
        url, params={'__a': 1}, headers={"x-requested-with": "XMLHttpRequest", "user-agent": u_a, "accept": "application/json"})

    headers = r.headers['Content-type']

    media = {}

    if (
        ('application/json' in headers) and
        ('graphql' in r.json())
    ):
        print("Got JSON response")

        media = r.json()['graphql']['shortcode_media']

    elif ('text/html' in headers):
        print("Got HTML response")
        
        bs = BeautifulSoup(r.text, features="html.parser")
        for script in bs.find_all("script"):
            if script.string and "window._sharedData = " in script.string:
                json_str = re.sub("window._sharedData = ", "", script.string)
                json_str = json_str[:-1]
                print(json.dumps(json_str, indent="\t"))
                media = json.loads(
                    json_str)['entry_data']['PostPage'][0]['graphql']['shortcode_media']

    if media['is_video']:
        return {
            "url": media["video_url"],
            "title": f"{media['title']} {media['edge_media_to_caption']['edges'][0]['node']['text']}",
            "preview": media["display_resources"][0]["src"],
            "description": media["owner"]["full_name"],
            "username": media["owner"]["username"],
            "usericon": media["owner"]["profile_pic_url"]
        }
    else:
        raise Exception("The post is not a video")