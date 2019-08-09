# -*- coding:utf-8 -*-
# @Time  : 2019/7/10 10:23
# @Author: dongyani
# @interfacetest: http://apiv1.starschina.com/cms/v1.0/funtv/accesskey

import requests, unittest
from common.AES_CBC import AES_CBC
from readConfig import ReadConfig
from common.configHttp import RunMain

baseurl = ReadConfig().get_http("baseurl")
version = ReadConfig().get_app("version")
app_key = ReadConfig().get_app("app_key")
funtv_version = ["8.0.1", "8.0.2", "8.0.3", "8.0.4", "8.0.5", "8.0.6"]
headers = RunMain().headers_get()
aes = AES_CBC()


class funtv_accesskey(unittest.TestCase):
    """测试风行缓存接口"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = baseurl + "/cms/v1.0/funtv/accesskey"

    def get_url_param(self):
        # cp: fiag64t; secret_key: !N6nYXm9i@V 这两个参数是必传的
        data = '{"cp":"fiag64t",' \
               '"secret_key":"!N6nYXm9i@V",' \
               '"app_version":"%(version)s",' \
               '"app_key":"%(app_key)s", ' \
               '"os_type":1}' % {
                   'version': version,
                   'app_key': app_key}
        return RunMain().get_url_params(data, self.url)

    @unittest.skipIf(version not in funtv_version, '8.0.7以后的版本不运行风行缓存接口')
    def test_01_funtv_accesskey(self):
        '''正确的请求参数'''
        response = requests.get(url=self.get_url_param(), headers=headers)
        assert len(response.json()['data']['access_key']) > 20 & response.json()['err_code'] == 0

    @unittest.skipIf(version not in funtv_version, '8.0.7以后的版本不运行风行缓存接口')
    def test_02_funtv_accesskey_cp_error(self):
        '''请求参数cp的值错误'''
        url = self.get_url_param().replace('cp=fiag64t', 'cp=fiag32taaa')
        response = requests.get(url=url, headers=headers)
        assert response.json()['err_code'] == 500

    @unittest.skipIf(version not in funtv_version, '8.0.7以后的版本不运行风行缓存接口')
    def test_03_funtv_accesskey_secret_key_error(self):
        '''请求参数secret_key的值错误'''
        url = self.get_url_param().replace('secret_key=!N6nYXm9i@V', 'secret_key=!N6nYXm9iaaa')
        response = requests.get(url=url, headers=headers)
        assert response.json()['err_code'] == 500

    @unittest.skipIf(version not in funtv_version, '8.0.7以后的版本不运行风行缓存接口')
    def test_04_funtv_accesskey_null(self):
        '''请求参数cp与secret_key值为空'''
        url = self.get_url_param().replace('cp=fiag64t', 'cp=')
        url = url.replace('secret_key=!N6nYXm9i@V', 'secret_key=')
        response = requests.post(url=url, headers=headers)
        assert response.status_code == 404

# if __name__ == "__main__":
#     print(version)
#     config_app_scret_key().test_01_config_correct()
