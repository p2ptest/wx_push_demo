#! /usr/bin/env python3
# -*- coding: UTF-8 -*-
import sys
from importlib import reload
from urllib import request
import time
import json

__author__ = 'guanr'

reload(sys)

CORPID = "wx97b460a9aa734483"
CORPSECRET = "kb5ELEIVrd81tMiiIgQEEtsrGoH2IsHqhdK4piQRsvOvBmnsRikED0-KMhLs3wEa"
BASEURL = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={0}&corpsecret={1}'.format(CORPID, CORPSECRET)
URL = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s"


class Token(object):
    # get token
    def __init__(self):
        self.expire_time = sys.maxsize

    def get_token(self):
        if self.expire_time > time.time():
            res = request.urlopen(BASEURL)
            result_string = res.read().decode("utf-8")
            result_json = json.loads(result_string)
            if 'errcode' in result_json.keys():
                print(result_json['errmsg'], sys.stderr)
                sys.exit(1)
            self.expire_time = time.time() + result_json['expires_in']
            self.access_token = result_json['access_token']
        return self.access_token


def send_message(title, content):
    team_token = Token().get_token()
    print(team_token)
    url = URL % team_token
    wechat_json = {
        "toparty": "1",
        "msgtype": "text",
        "agentid": "1",
        "text": {
            "content": "title:{0}\n content:{1}".format(title, content)
        },
        "safe": "0"
    }
    data = json.dumps(wechat_json, ensure_ascii=False)
    data = data.encode("utf-8")
    response = request.urlopen(url, data)
    print(json.loads(response.read().decode("utf-8")))


if __name__ == '__main__':
    send_message("BF_P2P_TEST", "欢迎大家加入")
