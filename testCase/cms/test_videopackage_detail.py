# -*- coding:utf-8 -*-
# @Time  : 2019/7/23 17:05
# @Author: dongyani
# @interfacetest: http://apiv1.starschina.com/cms/v1.2/videopackage/detail

from common.configHttp import RunMain
from readConfig import ReadConfig
from common.AES_CBC import AES_CBC
from common.getSign import get_Sign
from datetime import datetime
import unittest, json, requests, time

baseurl = ReadConfig().get_http('baseurl')
version = ReadConfig().get_app('version')
app_key = ReadConfig().get_app('app_key')
headers = RunMain().headers()
aes = AES_CBC()


class videopackage_detail(unittest.TestCase):
    """测试会员套餐下的视频包详情接口"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = baseurl + '/cms/v1.2/videopackage/detail'

    def decrypt_to_dict(self, text, split_star_num, split_end_num):
        data = text.json()["data"]
        decrypt = aes.decrypt(str(data), 'r')[split_star_num:][:split_end_num]
        global false, null, true
        false = null = true = ""
        dict_decrypt = eval(decrypt)
        return dict_decrypt

    def test_01_videopackage_detail(self):
        """正确的会员套餐视频包详情参数"""
        time.sleep(1)
        timeStamp = int(time.mktime(datetime.now().timetuple()))
        data = '{"os_version":"9",' \
               '"imei":"869384032108431",' \
               '"latitude":34.223866,' \
               '"longitude":108.909907,' \
               '"gcid":"dba9f3c2e8926564d3c930790c232bcf",' \
               '"bssid":"70:57:bf:90:52:f1",' \
               '"device_id":"802ca0fba119ab0a",' \
               '"installation_id":1904301718321742,' \
               '"mac_address":"02:00:00:00:00:00",'\
               '"channel":"dopool",' \
               '"id":[1],' \
               '"os_type":1,' \
               '"app_version":"%(version)s",' \
               '"timestamp":%(timeStamp)d,' \
               '"app_key":"%(app_key)s"}' % {
                   'id': self.id,
                   'version': version,
                   'timeStamp': timeStamp,
                   'app_key': app_key}
        sign = get_Sign().encrypt(data, True)["sign"]
        data = data.replace('}', ',"sign":"%s"}' % sign)
        crypt_data = aes.encrypt(data, 'c_q')
        form = {"data": crypt_data, "encode": "v1"}
        response = requests.post(url=self.url, data=json.dumps(form), headers=headers)
        response_data = self.decrypt_to_dict(response, 1, -1)
        assert response_data["description"] == "会员专享,老的VIP用户升级专用"

    def test_02_videopackage_detail(self):
        """错误的会员套餐视频包详情参数"""
        data = '{"app_version":"%(version)s",' \
               '"app_key":"%(app_key)s", ' \
               '"os_type":3,' \
               '"id":[1],' \
               '"installation_id": 1904301718321742,' \
               '"os_version": "9",' \
               '"latitude": 34.230261,' \
               '"mac_address": "02:00:00:00:00:00",' \
               '"longitude": 108.872503,' \
               '"device_id": "802ca0fba119ab0a"}' % {
                   'version': version,
                   'app_key': app_key}
        crypt_data = aes.encrypt(data, 'c_q')
        form = {"data": crypt_data, "encode": "v1"}
        response = requests.post(url=self.url, data=json.dumps(form), headers=headers)
        assert response.json()['err_code'] == 500

    def test_03_videopackage_detail(self):
        data = 'aaaa'
        crypt_data = aes.encrypt(data, 'c_q')
        form = {"data": crypt_data, "encode": "v1"}
        response = requests.post(url=self.url, data=json.dumps(form), headers=headers)
        assert response.json()['err_code'] == 500
