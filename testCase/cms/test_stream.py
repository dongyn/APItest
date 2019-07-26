# -*- coding:utf-8 -*-
#@Time  : 2019/7/10 10:23
#@Author: dongyani
#@interfacetest: http://apiv1.starschina.com/cms/v1.2/stream

import unittest,requests,json
from common.AES_CBC import AES_CBC
from common.configHttp import RunMain
from readConfig import ReadConfig

global false, null, true

headers = RunMain().headers()
baseurl = ReadConfig().get_http("baseurl")
version = ReadConfig().get_app("version")
app_key = ReadConfig().get_app("app_key")
aes = AES_CBC()

class test_stream(unittest.TestCase):
    """测试查看直播详情接口"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = baseurl + "/cms/v1.2/stream"

    def test_01_Viewlivestreamdetails_correct(self):
        """正确的请求参数"""
        data = '{"os_type":1, "app_version":"%(version)s", "id":160, "app_key":"%(app_key)s"}' % {'version':version,
                                                                                                  'app_key':app_key}
        crypt_data = aes.encrypt(data, 'c_q')
        form = {"data":crypt_data,"encode":"v1"}
        response = requests.post(url = self.url, data = json.dumps(form), headers = headers)
        if (response.status_code == 200):
            response_data = RunMain().decrypt_to_dict(response, 'r')
            assert  response_data['title'] == "CCTV1"
        else:
            print("接口%s返回的节目名称title错误" %self.url)

    def test_02_Viewlivestreamdetails_error(self):
        """错误的请求参数"""
        data = '{"os_type":1, "app_version":"%(version)s", "id":160, "app_key":"abdcdsaoswuiewka"}' % {'version':version}
        crypt_data = aes.encrypt(data, 'c_q')
        form = {"data": crypt_data, "encode": "v1"}
        response = requests.post(url=self.url, data=json.dumps(form), headers=headers)
        if (response.status_code == 403):
            err_code = response.json()['err_code']
            assert err_code == 500
        else:
            print("接口%s请求app_key参数值错误，返回的err_code应为500" %self.url)

    def test_03_Viewlivestreamdetails_null(self):
        """请求参数为空"""
        crypt_data = aes.encrypt('', 'c_q')
        form = {"data": crypt_data, "encode": "v1"}
        response = requests.post(url=self.url, data=json.dumps(form), headers=headers)
        if (response.status_code == 403):
            err_code = response.json()['err_code']
            assert err_code == 500
        else:
            print("接口%s缺失app_version和app_key参数，返回的状态码应为403" %self.url)

if __name__ == "__main__":
#     suite = unittest.TestLoader().loadTestsFromTestCase(test_stream)
#     suite.TextTestsRunner().run(suite)
    test_stream().test_01_Viewlivestreamdetails_correct()