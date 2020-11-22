import requests

def import_video(url : str) -> {}:
    r = requests.get(url, params={'__a': 1})
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