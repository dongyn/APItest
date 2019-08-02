# -*- coding:utf-8 -*-
# @Time  : 2019/7/23 17:05
# @Author: dongyani
# @interfacetest: http://apiv1.starschina.com/cms/v1.2/videopackage/detail

import unittest, json, requests, time
from datetime import datetime
from common.AES_CBC import AES_CBC
from common.configHttp import RunMain
from readConfig import ReadConfig

global false, null, true

baseurl = ReadConfig().get_http("baseurl")
version = ReadConfig().get_app("version")
app_key = ReadConfig().get_app("app_key")
headers = RunMain().headers()
aes = AES_CBC()


class videopackage_detail(unittest.TestCase):
    """测试会员套餐下的视频包详情接口"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = baseurl + '/cms/v1.2/videopackage/detail'
        self.timeStamp = int(time.mktime(datetime.now().timetuple()))

    def decrypt_to_dict(self, text, split_star_num, split_end_num):
        data = text.json()["data"]
        decrypt = aes.decrypt(str(data), 'r')[split_star_num:][:split_end_num]
        global false, null, true
        false = null = true = ""
        dict_decrypt = eval(decrypt)
        return dict_decrypt

    def test_01_videopackage_detail(self):
        """正确的会员套餐视频包详情参数"""
        data = '{"bssid":"4c:e9:e4:7d:41:d0",' \
               '"app_version":"%(version)s",' \
               '"app_key":"%(app_key)s",' \
               '"os_type":1,' \
               '"id":[1],' \
               '"gcid":"cb777ec42e05089bc189cd255def16d5",' \
               '"imei":"869384032108431",' \
               '"channel":"huawei",' \
               '"installation_id": 1904301718321742,' \
               '"os_version": "9",' \
               '"latitude": 34.230261,' \
               '"mac_address": "02:00:00:00:00:00",' \
               '"longitude": 108.872503,' \
               '"device_id": "802ca0fba119ab0a"}' % {
                   'version': version,
                   'app_key': app_key}
        crypt_data = aes.encrypt(str(data), 'c_q')
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

if __name__ == "__main__":
    videopackage_detail().test_01_videopackage_detail()
# a = '[{"aa":a, "bb":[{"cc":c}]}]'
# print(a[1:][-1:])
