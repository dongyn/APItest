# -*- coding:utf-8 -*-
#@Time  : 2019/7/10 10:23
#@Author: pengjuan
#@interfacetest: http://apiv1.starschina.com/cms/v1.0/stream/randlist

from common.AES_CBC import AES_CBC
from common.configHttp import RunMain
from readConfig import ReadConfig
from common.getSign import get_Sign
import common.url as url
import unittest, requests, json, datetime, time

global false, null, true

headers = RunMain().headers()
baseurl = url.baseurl()
version = ReadConfig().get_app("version")
app_key = ReadConfig().get_app("app_key")
aes = AES_CBC()

# 获取随机排序的直播列表
class test_randlist(unittest.TestCase):
    """测试获取随机排序的直播列表接口"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = baseurl + "/cms/v1.2/stream/randlist"

    # 将解密后的字符串转为字典
    def decrypt_to_dict(self, text, split_num, str_split):
        decrypt = str(aes.decrypt(text, 'r'))[split_num:].split(str_split)[0] + str_split
        global false, null, true
        false = null = true = ""
        dict_decrypt = eval(decrypt)
        return dict_decrypt

    def test_01_getlivelist(self):
        """正确的请求参数"""
        timeStamp = int(time.mktime(datetime.datetime.now().timetuple()))
        data = '{"os_type":1, ' \
               '"app_version":"%(version)s", ' \
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
        r_data = response.json()['data']
        #"stream_tabs":null}: 接口返回数组的第一个电视台信息的最后一个键值对
        response_data = self.decrypt_to_dict(r_data, 1, '"stream_tabs":null}')
        assert response_data['id'] != "" and response_data['title'] != ""

    def test_02_getlivelist_error(self):
        """错误的请求参数"""
        data = '{"os_type":1, ' \
               '"app_version":"%(version)s", ' \
               '"id":160, ' \
               '"app_key":"abdcdsaoswuiewka"}' % {'version':version}
        crypt_data = aes.encrypt(data, 'c_q')
        form = {"data": crypt_data, "encode": "v1"}
        response = requests.post(url=self.url, data=json.dumps(form), headers=headers)
        assert response.json()['err_code'] == 500

    def test_03_getlivelist_null(self):
        """请求参数为空"""
        data = ''
        crypt_data = aes.encrypt(data, 'c_q')
        form = {"data": crypt_data, "encode": "v1"}
        response = requests.post(url=self.url, data=json.dumps(form), headers=headers)
        assert response.json()['err_code'] == 500
