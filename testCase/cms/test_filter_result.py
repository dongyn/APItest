# -*- coding:utf-8 -*-
# @Time  : 2019/8/1 14:44
# @Author: dongyani
# @interfacetest: http://apiv1.starschina.com/cms/v1.2/filter/result

from common.configHttp import RunMain
from readConfig import ReadConfig
from common.getSign import get_Sign
from common.AES_CBC import AES_CBC
from datetime import datetime
import common.url as url
import requests, unittest, json, time

baseurl = url.baseurl()
version = ReadConfig().get_app('version')
app_key = ReadConfig().get_app('app_key')
aes = AES_CBC()
headers = RunMain().headers()


class test_Filterresult(unittest.TestCase):
    """测试过滤结果"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = baseurl + "/cms/v1.2/filter/result"

    def decrypt_to_dict(self, text, split_num, split_str):
        decrypt = aes.decrypt(text, 'r')[split_num:].split(split_str)[0] + split_str
        global false, null, true
        false = null = true = ""
        dict_decrypt = eval(decrypt)
        return dict_decrypt

    def test_filter_result_01(self):
        """正确的请求参数， id为综艺page"""
        timeStamp = int(time.mktime(datetime.now().timetuple()))
        data = '{"category_id" : 1, ' \
               '"os_type" : 1, ' \
               '"os_version":"9",' \
               '"mac_address":"02:00:00:00:00:00",' \
               '"device_id":"802ca0fba119ab0a",' \
               '"timestamp":%(timeStamp)d,' \
               '"app_version":"%(version)s", ' \
               '"app_key": "%(app_key)s", ' \
               '"content_type": 1,' \
               '"limit":5,' \
               '"offset":0}' % {
                   'version': version,
                   'timeStamp': timeStamp,
                   'app_key': app_key}
        sign = get_Sign().encrypt(data, True)["sign"]
        data = data.replace('}', ',"sign":"%s"}' % sign)
        crypt_data = aes.encrypt(data, 'c_q')
        form = {'data': crypt_data, 'encode': 'v1'}
        response = requests.post(self.url, data=json.dumps(form), headers=headers)
        response_data = self.decrypt_to_dict(response.json()['data'], 1, '"expired_at":null}')
        self.assertTrue(len(response_data['title'])>0, "页面加载的内容不能为空")

    def test_filter_result_02(self):
        """错误的请求参数"""
        data = '{"category_id" : -1, ' \
               '"os_type" : 1, ' \
               '"app_version":"%(version)s", ' \
               '"app_key": "%(app_key)s", ' \
               '"content_type": 1,' \
               '"limit":5,' \
               '"offset":0}' % {'version': version, 'app_key': app_key}
        crypt_data = aes.encrypt(data, 'c_q')
        form = {'data': crypt_data, 'encode': 'v1'}
        response = requests.post(self.url, data=json.dumps(form), headers=headers)
        self.assertEqual(500, response.json()['err_code'], "category_id参数错误，接口返回err_code应为500")

    def test_filter_result_03(self):
        """请求参数为空"""
        data = ''
        crypt_data = aes.encrypt(data, 'c_q')
        form = {'data': crypt_data, 'encode': 'v1'}
        response = requests.post(self.url, data=json.dumps(form), headers=headers)
        assert response.json()['err_code'] == 500

