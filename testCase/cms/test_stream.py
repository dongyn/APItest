# -*- coding:utf-8 -*-
# @Time  : 2019/7/10 10:23
# @Author: dongyani
# @interfacetest: http://apiv1.starschina.com/cms/v1.2/stream

from common.AES_CBC import AES_CBC
from common.configHttp import RunMain
from readConfig import ReadConfig
from common.getSign import get_Sign
import unittest, requests, json, datetime, time

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
        """正确的请求参数,CCTV1"""
        timeStamp = int(time.mktime(datetime.datetime.now().timetuple()))
        data = '{"os_type":1, ' \
               '"app_version":"%(version)s", ' \
               '"timestamp":%(timeStamp)d,' \
               '"id":160, ' \
               '"app_key":"%(app_key)s"}' % {
                   'version': version,
                   'timeStamp': timeStamp,
                   'app_key': app_key}
        sign = get_Sign().encrypt(data, True)["sign"]
        data = data.replace('}', ',"sign":"%s"}' % sign)
        crypt_data = aes.encrypt(data, 'c_q')
        form = {"data": crypt_data, "encode": "v1"}
        response = requests.post(url=self.url, data=json.dumps(form), headers=headers)
        response_data = RunMain().decrypt_to_dict(response, 'r')
        assert response_data['title'] == "CCTV1"

    def test_02_Viewlivestreamdetails_error(self):
        """错误的请求参数"""
        data = '{"os_type":1, "app_version":"%(version)s", "id":160, "app_key":"abdcdsaoswuiewka"}' % {
            'version': version}
        crypt_data = aes.encrypt(data, 'c_q')
        form = {"data": crypt_data, "encode": "v1"}
        response = requests.post(url=self.url, data=json.dumps(form), headers=headers)
        assert response.json()['err_code'] == 500

    def test_03_Viewlivestreamdetails_null(self):
        """请求参数为空"""
        crypt_data = aes.encrypt('', 'c_q')
        form = {"data": crypt_data, "encode": "v1"}
        response = requests.post(url=self.url, data=json.dumps(form), headers=headers)
        assert response.json()['err_code'] == 500
