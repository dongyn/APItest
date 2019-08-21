# -*- coding:utf-8 -*-
# @Time  : 2019/7/10 10:23
# @Author: dongyani
# @interfacetest: http://apiv1.starschina.com/cms/v1.2/config

from common.AES_CBC import AES_CBC
from readConfig import ReadConfig
from common.configHttp import RunMain
from common.getSign import get_Sign
from datetime import datetime
import requests, unittest, json, time

global false, null, true

baseurl = ReadConfig().get_http("baseurl")
version = ReadConfig().get_app("version")
app_key = ReadConfig().get_app("app_key")
headers=RunMain().headers()
aes = AES_CBC()


class test_config(unittest.TestCase):
    """测试app配置接口"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = baseurl + "/cms/v1.2/config"

    def test_01_config(self):
        """正确的请求参数"""
        time.sleep(1)
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
        response = requests.post(url=self.url, data=json.dumps(form), headers=headers)
        response_data = RunMain().decrypt_to_dict(response, 'c_p')
        self.assertEqual("1.0", response_data['api']['version'],
                         "config接口返回的api-version应该为%s" % response_data['api']['version'])

    def test_02_config_error(self):
        """错误的os_type请求参数"""
        timeStamp = int(time.mktime(datetime.now().timetuple()))
        data = '{"os_type": 3,' \
               '"app_key":"%(app_key)s",' \
               '"os_version":"9",' \
               '"carrier":3,' \
               '"mac_address":"02:00:00:00:00:00",' \
               '"device_id":"802ca0fba119ab0a",' \
               '"app_version":"%(version)s",' \
               '"timeStamp":%(timeStamp)d}' % {
                   'app_key': app_key,
                   'timeStamp': timeStamp,
                   'version': version}
        crypt_data = aes.encrypt(data, 'c_q')
        form = {"data": crypt_data, "encode": "v1"}
        response = requests.post(url=self.url, data=json.dumps(form), headers=headers)
        assert response.json()['err_code'] == 500
