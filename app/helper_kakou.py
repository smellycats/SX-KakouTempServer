# -*- coding: utf-8 -*-
import json

import requests
from requests.auth import HTTPBasicAuth


class Kakou(object):
    def __init__(self, **kwargs):
        self.host = kwargs['host']
        self.port = kwargs['port']
	self.username = kwargs['username']
	self.password = kwargs['password']
        self.headers = {'content-type': 'application/json'}

    def get_kakou_maxid(self):
        """根据时间,地点,方向获取车流量"""
        url = 'http://{0}:{1}/maxid'.format(self.host, self.port)
        #print url
        try:
            r = requests.get(url, headers=self.headers,
			     auth=HTTPBasicAuth(self.username, self.password))
            if r.status_code == 200:
                return json.loads(r.text)
        except Exception as e:
            raise

    def get_kakou_info(self, start_id, end_id):
        """根据id范围获取车辆信息"""
        url = 'http://{0}:{1}/kakou/{2}/{3}'.format(
            self.host, self.port, start_id, end_id)
        try:
            r = requests.get(url, headers=self.headers,
			     auth=HTTPBasicAuth(self.username, self.password))
            if r.status_code == 200:
                return json.loads(r.text)
        except Exception as e:
            raise

    def get_kkdd_all(self):
        """获取所有卡口地点名称"""
        url = 'http://{0}:{1}/kkdd'.format(self.host, self.port)
        try:
            r = requests.get(url, headers=self.headers,
			     auth=HTTPBasicAuth(self.username, self.password))
            if r.status_code == 200:
                return json.loads(r.text)
        except Exception as e:
            raise
