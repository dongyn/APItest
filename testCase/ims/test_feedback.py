# -*- coding:utf-8 -*-
#@Time  : 2019/8/2
#@Author: yanghuiyu
#@interfacetest: https://apiv1.starschina.com/ims/v1.0/user/feedback/create

from readConfig import ReadConfig
from common.md5_sms import timeStamp_md5
from datetime import datetime
from common.getSign import get_Sign
from common.configHttp import RunMain
import unittest,json,requests,time

global false, true, null
baseurl = ReadConfig().get_http('baseurl')
version = ReadConfig().get_app('version')
app_key = ReadConfig().get_app('app_key')
headers = RunMain().headers()
md5 = timeStamp_md5()

class test_Feedback(unittest.TestCase):
    """意见反馈"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = baseurl + '/ims/v1.0/user/feedback/create'
        self.timeStamp = int(time.mktime(datetime.now().timetuple()))

    def test_feedback_01(self):
        """正确的参数"""
        timeStamp = int(time.mktime(datetime.now().timetuple()))
        access_token = md5.encrypt_md5(timeStamp)
        data = '{"app_version":"%(version)s",' \
               '"access_token":"%(access_token)s",' \
               '"os_type":1,' \
               '"timestamp":%(timeStamp)d,' \
               '"provider":1,' \
               '"app_key":"%(app_key)s",' \
               '"device_id":"f04cad98633f6da1",' \
               '"installation_id":1904301718321742,' \
               '"longitude":108.871538,' \
               '"latitude":34.22999,' \
               '"bssid": "4c:e9:e4:7d:41:c0",' \
               '"content": "\\u54c8\\u54c8",' \
               '"user_id": 7561494,' \
               '}' % {
                   'version': version,
                   'app_key': app_key,
                   'access_token': access_token,
                   'timeStamp': self.timeStamp}
        data = get_Sign().encrypt(data)
        response = requests.post(self.url, data=json.dumps(data), headers=headers)
        assert response.json()['err_code'] == 0

    def test_feedback_02(self):
        """错误的参数"""
        timeStamp = int(time.mktime(datetime.now().timetuple()))
        access_token = md5.encrypt_md5(timeStamp)
        data = '{"app_version":"%(version)s",' \
               '"access_token":"%(access_token)s",' \
               '"os_type":3,' \
               '"timestamp":%(timeStamp)d,' \
               '"provider":1,' \
               '"app_key":"%(app_key)s",' \
               '"device_id":"f04cad98633f6da1",' \
               '"installation_id":1904301718321742,' \
               '"longitude":108.871538,' \
               '"latitude":34.22999,' \
               '"bssid": "4c:e9:e4:7d:41:c0",' \
               '"content": "\\u54c8\\u54c8",' \
               '"user_id": 7561494,' \
               '}' % {
                   'version': version,
                   'app_key': app_key,
                   'access_token': access_token,
                   'timeStamp': self.timeStamp}
        data = get_Sign().encrypt(data)
        response = requests.post(self.url, data=json.dumps(data), headers=headers)
        assert response.json()['err_code'] == 500

   # def test_feedback_03(self):
   #      """空的参数"""
   #      timeStamp = int(time.mktime(datetime.now().timetuple()))
   #      access_token = md5.encrypt_md5(timeStamp)
   #      data = '{"app_version":"%(version)s",' \
   #             '"access_token":"%(access_token)s",' \
   #             '"os_type":,' \
   #             '"timestamp":%(timeStamp)d,' \
   #             '"provider":1,' \
   #             '"app_key":"%(app_key)s",' \
   #             '"device_id":"f04cad98633f6da1",' \
   #             '"installation_id":1904301718321742,' \
   #             '"longitude":108.871538,' \
   #             '"latitude":34.22999,' \
   #             '"bssid": "4c:e9:e4:7d:41:c0",' \
   #             '"content": "\\u54c8\\u54c8",' \
   #             '"user_id": 7561494,' \
   #             '}' % {
   #                 'version': version,
   #                 'app_key': app_key,
   #                 'access_token': access_token,
   #                 'timeStamp': self.timeStamp}
   #      data = get_Sign().encrypt(data)
   #      response = requests.post(self.url, data=json.dumps(data), headers=headers)
   #      assert response.json()['err_code'] == 500
# if __name__ == "__main__":
#     test_Feedbakc().test_feedback_01()
#     test_Feedback().test_feedback_02()
#     test_Feedback();test_feedback_03()
#
