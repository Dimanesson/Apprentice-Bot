import requests
import json
import uuid
import os

class auto_deleting_file(object):
    def __init__(self, path : str, title : str):
        self.title = title
        self.path = path

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        os.remove(self.path)

    path : str
    title : str


def download(url, local_filename):
    r = requests.get(url, stream=True)
    with open(os.getcwd()+"/"+local_filename, 'wb') as f:
        for chunk in r.iter_content(1024):
            if chunk:
                f.write(chunk)
                f.flush()
    return local_filename

def import_video(url : str) -> auto_deleting_file:
    r = requests.get(url, params={'__a': 1})
    headers = r.headers['Content-type']
    rjson = r.json()
    if (
        (not 'application/json' in headers) or
        (not 'graphql' in rjson)
    ):
        raise Exception('Wrong link')
    
    with open("media.json", "w") as file:
        file.write(json.dumps(rjson, indent=4, sort_keys=True))

    media = rjson['graphql']['shortcode_media']
    if media['is_video']:
        return auto_deleting_file(download(media["video_url"], str(uuid.uuid4()) + ".mp4"), media["title"])
    else:
        raise Exception("The post is not a video")

    # application/json; charset=utf-8