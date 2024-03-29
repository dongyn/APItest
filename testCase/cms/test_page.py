# -*- coding:utf-8 -*-
# @Time  : 2019/7/10 10:23
# @Author: pengjuan
# @interfacetest: http://apiv1.starschina.com/cms/v1.2/page

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

class test_Page(unittest.TestCase):
    """测试页面加载接口"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = baseurl + "/cms/v1.2/page"

    def get_config_page_id(self):
        # id需要在config接口中返回
        timeStamp = int(time.mktime(datetime.now().timetuple()))
        data = '{"os_type": 1,' \
               '"app_key":"%(app_key)s",' \
               '"os_version":"9",' \
               '"carrier":3,' \
               '"mac_address":"02:00:00:00:00:00",' \
               '"device_id":"802ca0fba119ab0a",' \
               '"imei":"869384032108431",' \
               '"latitude":34.223866,' \
               '"gcid":"dba9f3c2e8926564d3c930790c232bcf",' \
               '"bssid":"4c:e9:e4:7d:41:c1",' \
               '"longitude":108.909907,' \
               '"installation_id":1904301718321742,' \
               '"force_reload_user":true,' \
               '"app_version":"%(version)s",' \
               '"timeStamp":%(timeStamp)d}' % {
                   'app_key': app_key,
                   'timeStamp': timeStamp,
                   'version': version}
        sign = get_Sign().encrypt(data, True)["sign"]
        data = data.replace('}', ',"sign":"%s"}' % sign)
        crypt_data = aes.encrypt(data, 'c_q')
        form = {"data": crypt_data, "encode": "v1"}
        response = requests.post(url=baseurl + "/cms/v1.2/config", data=json.dumps(form), headers=headers)
        return RunMain().decrypt_to_dict(response, 'c_p')['pages'][0]['pages'][0]['id']

    # 正确的请求参数，id为综艺page
    def test_page_01(self):
        """正确的请求参数"""
        timeStamp = int(time.mktime(datetime.now().timetuple()))
        data = '{"id": [%(page_id)d], "os_type":1,' \
               '"app_version":"%(version)s",' \
               '"timestamp":%(timeStamp)d,' \
               '"page_alias":"",'\
               '"installation_id":1901231425555756,'\
               '"device_id":"40439d078e887033",'\
               '"os_version":"8.1.0",'\
               '"channel":"dopool",'\
               '"app_key": "%(app_key)s"}' % {
                   'version': version,
                   'timeStamp': timeStamp,
                   'app_key': app_key,
                   'page_id' : self.get_config_page_id()}
        sign = get_Sign().encrypt(data, True)["sign"]
        data = data.replace('}', ',"sign":"%s"}' % sign)
        crypt_data = aes.encrypt(data, 'c_q')
        form = {'data': crypt_data, 'encode': 'v1'}
        response = requests.post(self.url, data=json.dumps(form), headers=headers)
        response_data = RunMain().decrypt_to_dict(response, 'r')[0]
        msg = '页面{0}的期望id是{1},实际id是{2}'.format(response_data['name'],
                                                 self.get_config_page_id(),
                                                 response_data['id'])
        self.assertEqual(self.get_config_page_id(), response_data['id'], msg=msg)

    def test_page_02(self):
        """错误的请求参数"""
        timeStamp = int(time.mktime(datetime.now().timetuple()))
        data = '{"id": [0], "os_type" : 1,' \
               '"app_version":"%(version)s",' \
               '"timestamp":%(timeStamp)d,' \
               '"page_alias":"",' \
               '"installation_id":1901231425555756,' \
               '"device_id":"40439d078e887033",' \
               '"os_version":"8.1.0",' \
               '"channel":"dopool",' \
               '"app_key": "%(app_key)s"}' % {
                   'version': version,
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
