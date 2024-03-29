# -*- coding:utf-8 -*-
#@Time  : 2019/7/10 10:23
#@Author: pengjuan
#@interfacetest: http://apiv1.starschina.com/cms/v1.2/stream/list

from common.AES_CBC import AES_CBC
from common.configHttp import RunMain
from readConfig import ReadConfig
from common.getSign import get_Sign
import common.url as url
import unittest, requests, json, datetime, time

headers = RunMain().headers()
baseurl = url.baseurl()
version = ReadConfig().get_app("version")
app_key = ReadConfig().get_app("app_key")
aes = AES_CBC()


class test_streamlist(unittest.TestCase):
    """测试获取直播列表接口"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = baseurl + "/cms/v1.2/stream/list"

    # 将解密后的字符串转为字典
    def decrypt_to_dict(self, text, split_num, str_split):
        data = text.json()["data"]
        decrypt = aes.decrypt(data, 'r')
        split_decrypt = decrypt[split_num:].split(str_split)
        str_decrypt = split_decrypt[0] + str_split
        global false, null, true
        false = null = true = ""
        dict_decrypt = eval(str_decrypt)
        return dict_decrypt

    def test_01_getlivelist(self):
        """正确的请求参数"""
        timeStamp = int(time.mktime(datetime.datetime.now().timetuple()))
        data = '{"os_type":1, ' \
               '"app_version":"%(version)s", ' \
               '"id":160, ' \
               '"timestamp":%(timeStamp)d,' \
               '"app_key":"%(app_key)s"}' % {
            'version': version,
            'timeStamp': timeStamp,
            'app_key': app_key}
        sign = get_Sign().encrypt(data, True)["sign"]
        data = data.replace('}', ',"sign":"%s"}' % sign)
        crypt_data = aes.encrypt(data, 'c_q')
        form = {"data": crypt_data, "encode": "v1"}
        response = requests.post(url=self.url, data=json.dumps(form), headers=headers)
        response_data = self.decrypt_to_dict(response, 1, '"stream_tabs":null}')
        assert response_data['id'] != "" and response_data['title'] != ""

    def test_02_getlivelist_error(self):
        """错误的请求参数"""
        data = '{"os_type":1, "app_version":"%(version)s", "id":160, "app_key":"abdcdsaoswuiewka"}' % {'version':version}
        crypt_data = aes.encrypt(data, 'c_q')
        form = {"data": crypt_data, "encode": "v1"}
        response = requests.post(url=self.url, data=json.dumps(form), headers=headers)
        assert response.json()['err_code'] == 500

    def test_03_getlivelist_null(self):
        """请求参数为空"""
        crypt_data = aes.encrypt('', 'c_q')
        form = {"data": crypt_data, "encode": "v1"}
        response = requests.post(url=self.url, data=json.dumps(form), headers=headers)
        assert response.json()['err_code'] == 500
