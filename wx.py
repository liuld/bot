#!/usr/bin/env python3
# _*_ coding: utf-8 _*_


import requests
import json
import logging


class WeChat(object):
    s = requests.session()
    token = None

    def __init__(self, corp_id, secret):
        self.token = self.get_token(corp_id, secret)

    def get_token(self, corp_id, secret):
        url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={0}&corpsecret={1}".format(corp_id, secret)
        rep = self.s.get(url)
        if rep.status_code == 200:
            return json.loads(rep.content)['access_token']
        else:
            logging.error("get_token: request failed.")
            return None

    def send_msg(self, content):

        url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + self.token
        header = {
            "Content-Type": "application/json"
        }
        form_data = {
            "touser": '@all',
            "toparty": "1",
            "msgtype": "text",
            "agentid": 1000002,
            "text": {
                "content": content
            },
            "safe": 0
        }
        rep = self.s.post(url, data=json.dumps(form_data).encode('utf-8'), headers=header)

        if rep.status_code == 200:
            return json.loads(rep.content)
        else:
            logging.error("send_msg: request failed.")
            return None
