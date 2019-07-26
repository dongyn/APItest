# -*- coding:utf-8 -*-
#@Time  : 2019/7/10 10:23
#@Author: pengjuan
#@interfacetest: http://apiv1.starschina.com/cms/v1.2/page

import unittest
import requests
import json
from readConfig import ReadConfig
from common.AES_CBC import AES_CBC
from common.configHttp import RunMain
global true, false, null

headers = RunMain().headers()
baseurl = ReadConfig().get_http('baseurl')
version = ReadConfig().get_app('version')
app_key = ReadConfig().get_app('app_key')
aes = AES_CBC()

class test_Page(unittest.TestCase):
    """测试页面加载接口"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = baseurl + "/cms/v1.2/page"

    # 正确的请求参数，id为综艺page
    def test_page_01(self):
        """正确的请求参数"""
        data = '{"id" : [119639], "os_type" : 1, "app_version":"%(version)s", "app_key": "%(app_key)s"}' % {'version': version, 'app_key': app_key}
        crypt_data = aes.encrypt(data, 'c_q')
        form = {'data': crypt_data, 'encode': 'v1'}
        response = requests.post(self.url, data=json.dumps(form), headers=headers)
        if response.status_code == 200:
            r_data = response.json()['data']
            response_data = RunMain().decrypt_to_json(r_data, 'r')[0]
            assert response_data['id'] == 119639
        else:
            print('请求失败')

    def test_page_02(self):
        """错误的请求参数"""
        data = '{"id" : [119639], "os_type" : 3, "app_version": "%(verison)s", "app_key":"%(app_key)s"}'%{'verison': version, 'app_key': app_key}
        crypt_data = aes.encrypt(data, 'c_q')
        form = {'data': crypt_data, 'encode': 'v1'}
        response = requests.post(self.url, data=json.dumps(form), headers=headers)
        assert response.status_code == 403

    def test_page_03(self):
        """请求参数为空"""
        data = '{"id" : [119639], "os_type" : , "app_version": "%(verison)s", "app_key":"%(app_key)s"}'%{'verison': version, 'app_key': app_key}
        crypt_data = aes.encrypt(data, 'c_q')
        form = {'data': crypt_data, 'encode': 'v1'}
        response = requests.post(self.url, data=json.dumps(form), headers=headers)
        assert response.status_code == 403


if __name__ == '__main__':

    test_Page().test_page_01()
#     test_Page().test_page_02()
#     test_Page().test_page_03()







