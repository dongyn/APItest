# -*- coding:utf-8 -*-
#@Time  : 2019/7/10 10:23
#@Author: dongyani
#@interfacetest: http://apiv1.starschina.com/cms/v1.2/stream

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

class test_stream(unittest.TestCase):
    """测试查看直播详情接口"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = baseurl + "/cms/v1.2/stream"
        headers = {'Content-Type': 'application/json;charset=UTF-8',
                   'Content-Length': '651',
                   'Host': 'apiv1.starschina.com',
                   'Accept-Encoding': 'gzip'
                   }

    # 将解密后的字符串转为字典
    def decrypt_to_dict(self, text, split_num, str_split):
        # print(str(aes.decrypt(text, 'r'))[2:])
        str_decrypt = str(aes.decrypt(text, 'r'))[split_num:].split(str_split)[0] + str_split
        global false, null, true
        false = null = true = ""
        dict_decrypt = eval(str_decrypt)
        return dict_decrypt

    def test_01_Viewlivestreamdetails_correct(self):
        data = '{"os_type":1, "app_version":"%(version)s", "id":160, "app_key":"%(app_key)s"}' % {'version':version,
                                                                                                  'app_key':app_key}
        crypt_data = aes.encrypt(data, 'c_q')
        form = {"data":crypt_data,"encode":"v1"}
        response = requests.post(url = self.url, data = json.dumps(form), headers = headers)
        if (response.status_code == 200):
            r_data = response.json()['data']
            response_data = self.decrypt_to_dict(r_data, 2, '}]}]}')
            assert  response_data['title'] == "CCTV1"
        else:
            print("接口%s返回的节目名称title错误" %self.url)

    def test_02_Viewlivestreamdetails_error(self):
        data = '{"os_type":1, "app_version":"%(version)s", "id":160, "app_key":"abdcdsaoswuiewka"}' % {'version':version}
        crypt_data = aes.encrypt(data, 'c_q')
        form = {"data": crypt_data, "encode": "v1"}
        response = requests.post(url=self.url, data=json.dumps(form), headers=headers)
        print(response.status_code)
        if (response.status_code == 403):
            err_code = response.json()['err_code']
            assert err_code == 500
        else:
            print("接口%s请求app_key参数值错误，返回的err_code应为500" %self.url)

    def test_03_Viewlivestreamdetails_null(self):
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
#     suite = unittest.TestLoader().loadTestsFromTestCase(test_stream)
#     suite.TextTestsRunner().run(suite)
    # test_streamlist().test_04_getlivelist