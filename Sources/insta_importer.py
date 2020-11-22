import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager

__session__ : requests.Session

def import_video(url : str) -> {}:
    r = __session__.get(url, params={'__a': 1})
    headers = r.headers['Content-type']
    rjson = r.json()
    if (
        (not 'application/json' in headers) or
        (not 'graphql' in rjson)
    ):
        raise Exception('Wrong link')

    media = rjson['graphql']['shortcode_media']
    if media['is_video']:
        return {
            "url" : media["video_url"],
            "title" : f"{media['title']} {media['edge_media_to_caption']['edges'][0]['node']['text']}",
            "preview" : media["display_resources"][0]["src"],
            "description" : media["owner"]["full_name"],
            "username" : media["owner"]["username"],
            "usericon" : media["owner"]["profile_pic_url"]
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


def init(port):
    __session__ = requests.Session()
    __session__.mount('http://', SourcePortAdapter(port))
    __session__.mount('https://', SourcePortAdapter(port))