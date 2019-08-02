# -*- coding:utf-8 -*-
#@Time  : 2019/7/10 10:23
#@Author: dongyani
#@interfacetest: http://apiv1.starschina.com/cms/v1.0/funtv/accesskey

import unittest
import requests,json
from common.AES_CBC import AES_CBC
from readConfig import ReadConfig
from common.configHttp import RunMain

global false, null, true

baseurl = ReadConfig().get_http("baseurl")
version = ReadConfig().get_app("version")
app_key = ReadConfig().get_app("app_key")
headers = RunMain().headers()
aes = AES_CBC()

class funtv_accesskey(unittest.TestCase):
    """测试风行缓存接口"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = baseurl + "/cms/v1.0/funtv/accesskey"

    def test_01_funtv_accesskey(self):
        '''正确的请求参数'''
        data = '{"cp":,"app_key":"%(app_key)s"}' % {'app_key':app_key}
        crypt_data = aes.encrypt(data, 'c_q')
        form = {"data":crypt_data,"encode":"v1"}
        response = requests.post(url = self.url, data = json.dumps(form), headers = headers)
        response_data = RunMain().decrypt_to_dict(response)
        assert response_data['access_key'] == "Zno2djRmbiwxNTU5MTgzMjA3LDhhOTYyNWJlZTBmNWM1NzZiZjU4M2RkOTQ5NTNmNWQ5"

    def test_02_funtv_accesskey_error(self):
        '''错误的请求参数'''
        data = '{"cp":,"app_key":"%(app_key)s"}' % {'app_key':app_key}
        crypt_data = aes.encrypt(data, 'c_q')
        form = {"data": crypt_data, "encode": "v1"}
        response = requests.post(url=self.url, data=json.dumps(form), headers=headers)
        assert response.json()['err_code'] == 500

    def test_03_funtv_accesskey_null(self):
        '''请求参数为空'''
        data = ''
        crypt_data = aes.encrypt(data, 'c_q')
        form = {"data": crypt_data, "encode": "v1"}
        response = requests.post(url=self.url, data=json.dumps(form), headers=headers)
        assert response.json()['err_code'] == 500

# if __name__ == "__main__":
#     config_app_scret_key().test_01_config_correct()

