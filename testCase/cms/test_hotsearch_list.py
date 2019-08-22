# -*- coding:utf-8 -*-
#@Time  : 2019/8/21 15:58
#@Author: dongyani
#@interfacetest: http://apiv1.starschina.com


from common.configHttp import RunMain
from readConfig import ReadConfig
from common.AES_CBC import AES_CBC
from common.getSign import get_Sign
from datetime import datetime
import unittest, json, requests, time

baseurl = ReadConfig().get_http('baseurl')
version = ReadConfig().get_app('version')
app_key = ReadConfig().get_app('app_key')
headers = RunMain().headers_get()
aes = AES_CBC()


class test_hotsearch_list(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_url_params(self, url, category):
        # order_id 必填, 订单id
        data = '{"app_version":"%(version)s",' \
               '"category":"%(category)s",' \
               '"os_type":1,' \
               '"os_version":"9",' \
               '"mac_address":"02:00:00:00:00:00",' \
               '"device_id":"802ca0fba119ab0a",' \
               '"imei":"869384032108431",' \
               '"latitude":34.223866,' \
               '"gcid":"dba9f3c2e8926564d3c930790c232bcf",' \
               '"bssid":"4c:e9:e4:7d:41:c1",' \
               '"longitude":108.909907,' \
               '"installation_id":1904301718321742,' \
               '"app_key":"%(app_key)s"' \
               '}' % {
                   'version': version,
                   'category': category,
                   'app_key': app_key}
        data = get_Sign().encrypt(data)
        return RunMain().get_url_params(data, url)

    def test_hotsearch_list_01(self):
        """正确的请求参数"""
        url = baseurl + '/cms/v1.0/hotsearch/list'
        url = self.get_url_params(url, "CRI")
        response = requests.get(url=url, headers=headers)
        hotsearch_list = list(response.json()['data'])
        # 热搜列表配置的内容一般不小于4条
        self.assertTrue(len(hotsearch_list)>=4, "热搜列表配置的内容一般不小于4条")
        self.assertTrue(len(hotsearch_list[0]['title'])>=1, "任意内容的字符长度不应小于1")

    def test_hotsearch_list_02(self):
        """错误的请求参数"""
        url = baseurl + '/cms/v1.0/hotsearch/list'
        url = self.get_url_params(url, "CRI")
        url = url.replace("category=CRI","category=%123123")
        response = requests.get(url=url, headers=headers)
        self.assertEqual(str(response.json()['data']), "None", "category参数错误，返回的data应该是None")
