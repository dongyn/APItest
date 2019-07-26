# -*- coding:utf-8 -*-
#@Time  : 2019/7/10 10:23
#@Author: pengjuan
#@interfacetest: http://apiv1.starschina.com/cms/v1.2/content/search

from common.AES_CBC import AES_CBC
from common.configMysql import OperationDbInterface
from common.configHttp import RunMain
from readConfig import ReadConfig
import unittest
import json
import requests

global false, true, null
headers = RunMain().headers()
baseurl = ReadConfig().get_http('baseurl')
version = ReadConfig().get_app('version')
app_key = ReadConfig().get_app('app_key')
aes = AES_CBC()
mysql = OperationDbInterface()


class test_Search(unittest.TestCase):
    """测试搜索接口"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = baseurl + '/cms/v1.2/content/search'
        self.sql_title = mysql.select_one('select video.title FROM video LEFT JOIN resource_param on video.id = resource_param.content_id where resource_param.online = 1 and resource_param.app_id = 1 and resource_param.content_type = 1 ORDER BY RAND() LIMIT 1;')
        self.title = self.sql_title['title']

    # 将响应转为字典
    def decrypt_to_json(self, text):
        global false, true, null
        false = true = null = ''
        str_decrypt = str(aes.decrypt(text, 'r'))
        dic_decrypt = eval(str_decrypt)
        return dic_decrypt

    # 正确的请求参数，搜索title存在
    def test_search_01(self):
        data = '{"title": "%(title)s", "os_type":1, "app_version": "%(version)s", "app_key":"%(app_key)s"}' % {'title': self.title, 'version':version, 'app_key':app_key}
        crypt_data = aes.encrypt(data, 'c_q')
        form = {"data":crypt_data, 'encode':"v1"}
        response = requests.post(self.url, data=json.dumps(form), headers=headers)
        if response.status_code == 200:
            r_data = response.json()['data']
            response_data1 = self.decrypt_to_json(r_data)
            response_data = self.decrypt_to_json(r_data)['result'][0]['title']
            assert response_data == self.title
        else:
            print("请求失败")

    # 正确的请求参数，搜索title不存在
    def test_search_02(self):
        data = '{"title": "集体么去impose", "os_type":1, "app_version": "%(version)s", "app_key":"%(app_key)s"}' % {'version': version, 'app_key': app_key}
        print(data)
        crypt_data = aes.encrypt(data, 'c_q')
        form = {"data": crypt_data, 'encode': "v1"}
        response = requests.post(self.url, data=json.dumps(form), headers=headers)
        if response.status_code == 200:
            r_data = response.json()['data']
            response_data1 = self.decrypt_to_json(r_data)
            response_data = self.decrypt_to_json(r_data)['result'][0]['title']
            print(response_data)
            assert response_data == ''
        else:
            print("请求失败")

    # 错误的请求参数
    def test_search_03(self):
        data = '{"title": "%(title)s", "os_type":3, "app_version": "%(version)s", "app_key":"%(app_key)s"}' % {'title': self.title, 'version': version, 'app_key': app_key}
        crypt_data = aes.encrypt(data, 'c_q')
        form = {"data": crypt_data, 'encode': "v1"}
        response = requests.post(self.url, data=json.dumps(form), headers=headers)
        assert response.status_code == 403

    # 请求参数为空
    def test_search_04(self):
        data = '{"title": "%(title)s", "os_type":, "app_version": "%(version)s", "app_key":"%(app_key)s"}' % {'title': self.title, 'version': version, 'app_key': app_key}
        crypt_data = aes.encrypt(data, 'c_q')
        form = {"data": crypt_data, 'encode': "v1"}
        response = requests.post(self.url, data=json.dumps(form), headers=headers)
        assert response.status_code == 403

# if __name__ == '__main__':
#     test_Search().test_search_01()
#     test_Search().test_search_02()
#     test_Search().test_search_03()
#     test_Search().test_search_04()
