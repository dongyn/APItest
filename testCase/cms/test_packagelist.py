# -*- coding:utf-8 -*-
#@Time  : 2019/7/23 17:05
#@Author: dongyani
#@interfacetest: http://apiv1.starschina.com

import unittest
import requests,json
from common.AES_CBC import AES_CBC
from common.configHttp import RunMain
from readConfig import ReadConfig

global false, null, true

headers = RunMain().headers()
baseurl = ReadConfig().get_http("baseurl")
version = ReadConfig().get_app("version")
app_key = ReadConfig().get_app("app_key")
aes = AES_CBC()


class config_app_scret_key(unittest.TestCase):
    """测试视频包接口"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = baseurl + "/cms/v1.0/funtv/accesskey"

    # 将解密后的字符串转为字典
    def decrypt_to_dict(self, text):
        r_data = text.json()['data']
        str_decrypt = str(aes.decrypt(r_data, 'c_p'))
        global false, null, true
        false = null = true = ""
        response_data = eval(str_decrypt)
        return response_data

    def test_01_packagelist(self):
        data = '{,"app_key":"xdThhy2239daax"}'
        crypt_data = aes.encrypt(data, 'c_q')
        form = {"data":crypt_data,"encode":"v1"}
        response = requests.post(url = self.url, data = json.dumps(form), headers = headers)
        if response.status_code == 200:
            response_data = self.decrypt_to_dict(response)
            response_data['api']['base'] == "http://apiv1.starschina.com"
        else:
            print("接口%s请求失败" %self.url)

    def test_02_packagelist_error(self):
        data = '{"mac_address":"02:00:00:00:00:00","device_id":"802ca0fba119ab0a","os_type": 4,"app_key":"xdThhy2239aaaa","app_version":"%(version)s","os_version":"9"}'%{
            'version': version}
        crypt_data = aes.encrypt(data, 'c_q')
        form = {"data": crypt_data, "encode": "v1"}
        response = requests.post(url=self.url, data=json.dumps(form), headers=headers)
        print(response.status_code)
        if (response.status_code == 403):
            err_code = response.json()['err_code']
            assert err_code == 500
        else:
            print("接口%s请求app_key参数值错误，返回的err_code应为500" %self.url)

    def test_03_packagelist_null(self):
        data = ''
        crypt_data = aes.encrypt(data, 'c_q')
        form = {"data": crypt_data, "encode": "v1"}
        response = requests.post(url=self.url, data=json.dumps(form), headers=headers)
        if (response.status_code == 403):
            err_code = response.json()['err_code']
            assert err_code == 500
        else:
            print("接口%s缺失app_version和app_key参数，返回的状态码应为403" %self.url)

# if __name__ == "__main__":
#     config_app_scret_key().test_01_config_correct()

