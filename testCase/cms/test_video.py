# -*- coding:utf-8 -*-
#@Time  : 2019/7/10 10:23
#@Author: pengjuan
#@interfacetest: http://apiv1.starschina.com/cms/v1.2/video

from common.AES_CBC import AES_CBC
from common.configMysql import OperationDbInterface
from common.configHttp import RunMain
from readConfig import ReadConfig
import requests
import unittest
import json

global true, false, null

headers = RunMain().headers()
baseurl = ReadConfig().get_http('baseurl')
version = ReadConfig().get_app('version')
app_key = ReadConfig().get_app('app_key')
aes = AES_CBC()
mysql = OperationDbInterface()

class test_Video(unittest.TestCase):
    """测试点播接口"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = baseurl + "/cms/v1.2/video"
        self.sql_id = mysql.select_one('select video.id FROM video LEFT JOIN resource_param on video.id = resource_param.content_id where resource_param.online = 1 and resource_param.app_id = 1 and resource_param.content_type = 1 ORDER BY RAND() LIMIT 1;')
        self.content_id = self.sql_id['id']

    def test_video_01(self):
        """正确的请求参数"""
        data = '{"content_id": %(content_id)d, "content_type": 1, "os_type": 1, "app_version": "%(version)s", "app_key":"%(app_key)s"}' % {
            'content_id': self.content_id, 'version': version, 'app_key': app_key}
        crypt_data = aes.encrypt(data, 'c_q')
        form = {"data": crypt_data, "encode" : "v1"}
        response = requests.post(self.url, data=json.dumps(form), headers=self.headers)

        if response.status_code == 200:
            r_data = response.json()['data']
            response_data = RunMain().decrypt_to_json(r_data, 'r')
            assert response_data['id'] == self.content_id
        else:
            print("获取%s接口返回的content_id错误" %self.url)

    def test_video_02(self):
        """错误的请求参数"""
        data = '{"content_id": %(content_id)d, "content_type": 1, "os_type": 4, "app_version": "%(version)s", "app_key":"%(app_key)s"}' % {
            'content_id': self.content_id, 'version': version, 'app_key': app_key}
        crypt_data = aes.encrypt(data, 'c_q')
        form = {"data": crypt_data, "encode" : "v1"}
        response = requests.post(self.url, data=json.dumps(form), headers=self.headers)
        if response.status_code == 403:
            err_code = response.json()['err_code']
            assert err_code == 500
        else:
            print("接口%s请求os_type参数值错误，返回的err_code应为500" % self.url)


    def test_video_03(self):
        """参数为空"""
        data = '{"content_id": %(content_id)d, "content_type": , "os_type": , "app_version": "%(version)s", "app_key":"%(app_key)s"}' % {
            'content_id': self.content_id, 'version': version, 'app_key': app_key}
        crypt_data = aes.encrypt(data, 'c_q')
        form = {"data": crypt_data, "encode" : "v1"}
        response = requests.post(self.url, data=json.dumps(form), headers=self.headers)
        if response.status_code == 403:
            err_code = response.json()['err_code']
            assert err_code == 500
        else:
            print("接口%s请求os_type参数值错误，返回的err_code应为500" % self.url)

# if __name__ == 'main':

    # test_Video().test_video_01()
    # test_Video().test_video_02()
    # test_Video().test_video_03()







