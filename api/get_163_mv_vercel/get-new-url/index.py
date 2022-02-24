# coding:utf-8

import requests
import execjs
from http.server import BaseHTTPRequestHandler
import json
import redis
import os

"""
运行本份代码需要搭建node.js环境
node需要安装crypto-js模块
"""

env_dist = os.environ
PASSWORD = env_dist.get('PASSWORD')

r = redis.Redis(
    host='apn1-destined-giraffe-32369.upstash.io',
    port=32369,
    password=PASSWORD, ssl=True)


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
}


def get_params(video_id):
    """
    获取加密参数
    """
    with open('163.js', 'r', encoding='utf-8') as f:
        ctx = execjs.compile(f.read())
        params = {
            "id": video_id,
            "r": "1080",
            "csrf_token": ""
        }
        second = "010001"
        three = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        four = '0CoJUm6Qyw8W8jud'
        dit = ctx.call('jia_mi', json.dumps(params), second, three, four)
        return dit


def get_data(encText, encSecKey):
    url = 'https://music.163.com/weapi/song/enhance/play/mv/url?csrf_token='
    data = {
        'params': encText,
        'encSecKey': encSecKey
    }
    response = requests.post(url, headers=headers, data=data)
    return response.json()


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        video_id = self.path.split('?')[1]
        _dict = get_params(video_id)
        print(_dict)
        encText = _dict['encText']
        encSecKey = _dict['encSecKey']
        data = get_data(encText, encSecKey)
        print(data)
        url_ = data['data']['url']
        r.set(video_id, url_, ex=7200)
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(url_.encode('utf-8'))
        return None