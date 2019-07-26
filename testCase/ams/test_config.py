# -*- coding:utf-8 -*-
#@Time  : 2019/7/10 10:23
#@Author: dongyani
#@interfacetest: http://apiv1.starschina.com/cms/v1.2/config

import unittest
import requests,json
from common.AES_CBC import AES_CBC
from readConfig import ReadConfig
from common.configHttp import RunMain


global false, null, true

headers = RunMain().headers()
baseurl = ReadConfig().get_http("baseurl")
version = ReadConfig().get_app("version")
app_key = ReadConfig().get_app("app_key")
aes = AES_CBC()

class config_app_scret_key(unittest.TestCase):
    """测试app配置接口"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = baseurl + "/cms/v1.2/config"

    # 将解密后的字符串转为字典
    def decrypt_to_dict(self, text):
        r_data = text.json()['data']
        str_decrypt = str(aes.decrypt(r_data, 'c_p'))
        global false, null, true
        false = null = true = ""
        response_data = eval(str_decrypt)
        return response_data

    def test_01_config(self):
        data = '{"mac_address":"02:00:00:00:00:00","device_id":"802ca0fba119ab0a","os_type": 1,"app_key":"xdThhy2239daax","app_version":"%(version)s","os_version":"9"}'% {'version':version}
        crypt_data = aes.encrypt(data, 'c_q')
        form = {"data":crypt_data,"encode":"v1"}
        response = requests.post(url = self.url, data = json.dumps(form), headers = headers)
        if response.status_code == 200:
            response_data = self.decrypt_to_dict(response)
            response_data['api']['base'] == "http://apiv1.starschina.com"
        else:
            format(self.url + "接口请求失败")

    def test_02_config_error(self):
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
            print("config，接口请求app_key参数值错误，返回的err_code应为500")

    def test_03_config_null(self):
        data = ''
        crypt_data = aes.encrypt(data, 'c_q')
        form = {"data": crypt_data, "encode": "v1"}
        response = requests.post(url=self.url, data=json.dumps(form), headers=headers)
        if (response.status_code == 403):
            err_code = response.json()['err_code']
            assert err_code == 500
        else:
            print("config，接口缺失app_version和app_key参数，返回的状态码应为403")

if __name__ == "__main__":
    config_app_scret_key().test_01_config()

