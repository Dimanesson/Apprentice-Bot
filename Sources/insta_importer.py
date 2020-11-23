# -*- coding: utf-8 -*-

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager

__port__ = 5000


def import_video(url: str) -> {}:
    u_a = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"

    r: requests.Response
    with requests.Session() as session:
        global __port__
        session.mount('http://', SourcePortAdapter(__port__))
        session.mount('https://', SourcePortAdapter(__port__))
        print("Performing request")
        r = session.get(
            url, params={'__a': 1}, headers={"x-requested-with": "XMLHttpRequest", "user-agent": u_a, "accept": "application/json"})
        print("Got request")

    headers = r.headers['Content-type']

    print("Got headers")

    if (
        (not 'application/json' in headers) or
        (not 'graphql' in r.json())
    ):
        print(headers)
        raise Exception('Wrong link')

    print("Link confirmed")

    print(r.json())
    print("Dumped JSON")

    media = r.json()['graphql']['shortcode_media']

    print("Got media")

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


class SourcePortAdapter(HTTPAdapter):
    """"Transport adapter" that allows us to set the source port."""

    def __init__(self, port, *args, **kwargs):
        self._source_port = port
        super(SourcePortAdapter, self).__init__(*args, **kwargs)

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(
            num_pools=connections, maxsize=maxsize,
            block=block, source_address=('', self._source_port))


def init(port: int):
    global __port__
    __port__ = port