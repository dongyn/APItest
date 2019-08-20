# -*- coding:utf-8 -*-
# @Time  : 2019/7/10 10:23
# @Author: pengjuan
# @interfacetest: http://apiv1.starschina.com/cms/v1.2/page

from common.configHttp import RunMain
from readConfig import ReadConfig
from common.getSign import get_Sign
from common.AES_CBC import AES_CBC
from datetime import datetime
import requests, unittest, json, time

baseurl = ReadConfig().get_http('baseurl')
version = ReadConfig().get_app('version')
app_key = ReadConfig().get_app('app_key')
aes = AES_CBC()
headers = RunMain().headers()


class test_Page(unittest.TestCase):
    """测试页面加载接口"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = baseurl + "/cms/v1.2/page"

    # 正确的请求参数，id为综艺page
    def test_page_01(self):
        """正确的请求参数"""
        timeStamp = int(time.mktime(datetime.now().timetuple()))
        #id需要在数据库中查, 提示-无效的签名
        data = '{"id": [122632], "os_type" : 1,' \
               '"app_version":"%(version)s",' \
               '"timestamp":%(timeStamp)d,' \
               '"app_key": "%(app_key)s"}' % {
                   'version': version,
                   'timeStamp': timeStamp,
                   'app_key': app_key}
        sign = get_Sign().encrypt(data, True)["sign"]
        data = data.replace('}', ',"sign":"%s"}' % sign)
        crypt_data = aes.encrypt(data, 'c_q')
        form = {'data': crypt_data, 'encode': 'v1'}
        response = requests.post(self.url, data=json.dumps(form), headers=headers)
        response_data = RunMain().decrypt_to_dict(response, 'r')[0]
        assert response_data['id'] == 122632

    def test_page_02(self):
        """错误的请求参数"""
        timeStamp = int(time.mktime(datetime.now().timetuple()))
        data = '{"id": [0],' \
               '"os_type" : 1,' \
               '"app_version":"%(version)s",' \
               '"timestamp":%(timeStamp)d,' \
               '"app_key":"%(app_key)s"}' % {
                   'verison': version,
                   'timeStamp': timeStamp,
                   'app_key': app_key}
        sign = get_Sign().encrypt(data, True)["sign"]
        data = data.replace('}', ',"sign":"%s"}' % sign)
        crypt_data = aes.encrypt(data, 'c_q')
        form = {'data': crypt_data, 'encode': 'v1'}
        response = requests.post(self.url, data=json.dumps(form), headers=headers)
        assert response.json()['err_code'] == 500

    def test_page_03(self):
        """请求参数为空"""
        data = '{"id": , ' \
               '"os_type" : 3, ' \
               '"app_version": ' \
               '"%(verison)s", ' \
               '"app_key":"%(app_key)s"}' % {
                   'verison': version,
                   'app_key': app_key}
        crypt_data = aes.encrypt(data, 'c_q')
        form = {'data': crypt_data, 'encode': 'v1'}
        response = requests.post(self.url, data=json.dumps(form), headers=headers)
        assert response.json()['err_code'] == 500

