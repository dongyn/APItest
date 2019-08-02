# -*- coding:utf-8 -*-
# @Time  : 2019/8/1 14:44
# @Author: dongyani
# @interfacetest: http://apiv1.starschina.com/cms/v1.2/filter/result

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


class test_Filterresult(unittest.TestCase):
    """测试页面加载接口"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = baseurl + "/cms/v1.2/filter/result"

    def decrypt_to_dict(self, text, split_num, split_str):
        data = text.json()["data"]
        decrypt = aes.decrypt(str(data), 'r')[split_num:][split_str][0] + split_str
        global false, null, true
        false = null = true = ""
        dict_decrypt = eval(decrypt)
        return dict_decrypt


    # 正确的请求参数，id为综艺page
    def test_filter_result_01(self):
        """正确的请求参数"""
        data = '{"category_id" : 1, ' \
               '"os_type" : 1, ' \
               '"app_version":"%(version)s", ' \
               '"app_key": "%(app_key)s", ' \
               '"content_type": 1,' \
               '"limit":5,' \
               '"offset":0}' % {'version': version, 'app_key': app_key}
        crypt_data = aes.encrypt(data, 'c_q')
        form = {'data': crypt_data, 'encode': 'v1'}
        response = requests.post(self.url, data=json.dumps(form), headers=headers)
        response_data = self.decrypt_to_dict(response.json()['data'], 'r', 1, '"expired_at":null}')[0]
        assert response_data['title'] == '剧场'


    def test_filter_result_02(self):
        """错误的请求参数"""
        data = '{"category_id" : 1, ' \
               '"os_type" : 4, ' \
               '"app_version":"%(version)s", ' \
               '"app_key": "%(app_key)s", ' \
               '"content_type": 1,' \
               '"limit":5,' \
               '"offset":0}' % {'version': version, 'app_key': app_key}
        crypt_data = aes.encrypt(data, 'c_q')
        form = {'data': crypt_data, 'encode': 'v1'}
        response = requests.post(self.url, data=json.dumps(form), headers=headers)
        assert response.json()['err_code']==500

    def test_filter_result_03(self):
        """请求参数为空"""
        data = ''
        crypt_data = aes.encrypt(data, 'c_q')
        form = {'data': crypt_data, 'encode': 'v1'}
        response = requests.post(self.url, data=json.dumps(form), headers=headers)
        assert response.json()['err_code']==500


# if __name__ == '__main__':
#     test_Filterresult().test_filter_result_01()
#     test_Page().test_filter_result_02()
#     test_Page().test_filter_result_03()
