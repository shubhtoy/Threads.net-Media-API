import requests
from flask import Flask, request, jsonify, render_template
import re
import json

app = Flask(__name__)

def shorten_url(long_url):
    response = requests.get(f'http://tinyurl.com/api-create.php?url={long_url}')
    if response.status_code == 200:
        return response.text
    return None

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/media', methods=['POST'])
def get_all_media():
    url = request.form.get('url')
    if not url:
        return jsonify({'error': 'URL parameter is missing'}), 400

    post_id = get_post_id(url)
    if post_id is None:
        return jsonify({'error': 'Invalid URL or post ID not found'}), 400

    post_data = get_post_data(post_id)
    thread_items = post_data.get("data", {}).get("data", {}).get("containing_thread", {}).get("thread_items", [])
    all_media = get_media(thread_items[-1])

    shortened_url = shorten_url(all_media.get('media'))
    if shortened_url:
        all_media['shortened_url'] = shortened_url

    return jsonify(all_media)

def get_post_data(id):
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "x-asbd-id": "129477",
        "x-fb-friendly-name": "BarcelonaPostPageQuery",
        "x-fb-lsd": "N1RcROyvW2TeIOAP1NF1Rw",
        "x-ig-app-id": "238260118697367",
    }
    data = {
        "lsd": "N1RcROyvW2TeIOAP1NF1Rw",
        "variables": json.dumps({"postID": id}),
        "doc_id": "5587632691339264"
    }
    response = requests.post("https://www.threads.net/api/graphql", headers=headers, data=data)
    response_data = response.json()
    # print(response_data)
    with open("data.json", "w") as f:
        json.dump(response_data, f)
    return response_data

def get_post_id(url):
    response = requests.get(url)
    response_text = response.text
    post_id_match = re.search(r'{"post_id":"(.*?)"}', response_text)
    # print(post_id_match)
    if post_id_match:
        return post_id_match.group(1)
    return None

def get_media(thread):
    media_true = thread["post"]
    media = media_true.get("text_post_app_info", {}).get("share_info", {}).get("quoted_post", None)  # quoted post
    if not media:
        media=media_true
    else:
        is_quoted=True
    media = media.get("text_post_app_info", {}).get("share_info", {}).get("reposted_post", None)  # reposted post
    if not media:
        media=media_true
    else:
        is_reposted=True
    # print(media)

    if media.get("carousel_media"):
        if media["carousel_media"][0].get("video_versions"):
            return {
                "username": media["user"]["username"],
                "is_verified": media["user"]["is_verified"],
                "caption": media["caption"]["text"] if media["caption"] else None,
                "user_profile_pic_url": media["user"]["profile_pic_url"],
                "type": "videos",
                "is_reposted": is_reposted,
                "media": [m["video_versions"][0] for m in media["carousel_media"]],
                "width": media["original_width"],
                "height": media["original_height"]
            }
        return {
            "username": media["user"]["username"],
            "is_verified": media["user"]["is_verified"],
            "user_profile_pic_url": media["user"]["profile_pic_url"],
            "caption": media["caption"]["text"] if media["caption"] else None,
            "type": "photos",
            "media": [m["image_versions2"]["candidates"][0] for m in media["carousel_media"]],
            "width": media["original_width"],
            "height": media["original_height"]
        }

    if media.get("video_versions") and len(media["video_versions"]) > 0:
        return {
            "user_profile_pic_url": media["user"]["profile_pic_url"],
            "caption": media["caption"]["text"] if media["caption"] else None,
            "username": media["user"]["username"],
            "is_verified": media["user"]["is_verified"],
            "type": "video",
            "media": media["video_versions"][0],
            "width": media["original_width"],
            "height": media["original_height"]
        }

    return {
        "user_profile_pic_url": media["user"]["profile_pic_url"],
        "caption": media["caption"]["text"] if media["caption"] else None,
        "username": media["user"]["username"],
        "is_verified": media["user"]["is_verified"],
        "type": "photo",
        "media": media["image_versions2"]["candidates"][0]["url"],
        "width": media["original_width"],
        "height": media["original_height"]
    }

if __name__ == '__main__':
    app.run()
