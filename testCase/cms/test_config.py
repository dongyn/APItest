# -*- coding:utf-8 -*-
# @Time  : 2019/7/10 10:23
# @Author: dongyani
# @interfacetest: http://apiv1.starschina.com/cms/v1.2/config

import unittest
import requests, json
from common.AES_CBC import AES_CBC
from readConfig import ReadConfig
from common.configHttp import RunMain

global false, null, true

headers = RunMain().headers()
baseurl = ReadConfig().get_http("baseurl")
version = ReadConfig().get_app("version")
app_key = ReadConfig().get_app("app_key")
aes = AES_CBC()


class test_config(unittest.TestCase):
    """测试app配置接口"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = baseurl + "/cms/v1.2/config"

    def test_01_config(self):
        """正确的请求参数"""
        data = '{"mac_address":"02:00:00:00:00:00",' \
               '"device_id":"802ca0fba119ab0a",' \
               '"os_type": 1,' \
               '"app_key":"xdThhy2239daax",' \
               '"app_version":"%(version)s",' \
               '"os_version":"9"}' % {
                   'version': version}
        crypt_data = aes.encrypt(data, 'c_q')
        form = {"data": crypt_data, "encode": "v1"}
        response = requests.post(url=self.url, data=json.dumps(form), headers=headers)
        response_data = RunMain().decrypt_to_dict(response, 'c_p')
        response_data['api']['base'] == "https://apiv1.starschina.com"

    def test_02_config_error(self):
        """错误的请求参数"""
        data = '{"mac_address":"02:00:00:00:00:00",' \
               '"device_id":"802ca0fba119ab0a",' \
               '"os_type": 4,' \
               '"app_key":"xdThhy2239aaaa",' \
               '"app_version":"%(version)s",' \
               '"os_version":"9"}' % {
                 'version': version}
        crypt_data = aes.encrypt(data, 'c_q')
        form = {"data": crypt_data, "encode": "v1"}
        response = requests.post(url=self.url, data=json.dumps(form), headers=headers)
        assert response.json()['err_code'] == 500

    def test_03_config_null(self):
        """请求参数为空"""
        data = ''
        crypt_data = aes.encrypt(data, 'c_q')
        form = {"data": crypt_data, "encode": "v1"}
        response = requests.post(url=self.url, data=json.dumps(form), headers=headers)
        assert response.json()['err_code'] == 500

# if __name__ == "__main__":
#     test_config().test_01_config()
