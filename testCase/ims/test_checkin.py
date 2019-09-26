# -*- coding:utf-8 -*-
#@Time  : 2019/7/30 9:05
#@Author: pengjuan
#@interfacetest: http://apiv1.starschina.com/ims/v1.0/user/checkin

from common.configHttp import RunMain
from common.getSign import get_Sign
from common.md5_sms import timeStamp_md5
from readConfig import ReadConfig
from datetime import datetime
import common.url as url
import unittest, requests, json, time

global false, true, null
baseurl = url.baseurl()
version = ReadConfig().get_app('version')
app_key = ReadConfig().get_app('app_key')
md5 = timeStamp_md5()

class test_Checkin(unittest.TestCase):
    """测试用户签到"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = baseurl + '/ims/v1.0/user/checkin'
        self.timeStamp = int(time.mktime(datetime.now().timetuple()))
        self.access_token = md5.encrypt_md5(self.timeStamp)

    def test_checkin_01(self):
        # 正确的签到参数
        timeStamp_login = int(time.mktime(datetime.now().timetuple()))
        headers = RunMain().headers_token(timeStamp_login)
        timeStamp = int(time.mktime(datetime.now().timetuple()))
        access_token = md5.encrypt_md5(timeStamp)
        data = '{"app_version":"%(version)s",' \
               '"access_token":"%(access_token)s",' \
               '"os_type":1,' \
               '"timestamp":%(timeStamp)d,' \
               '"provider":1,' \
               '"app_key":"%(app_key)s",' \
               '"device_id":"802ca0fba119ab0a",' \
               '"installation_id":1904301718321742,' \
               '"longitude":108.90823353286173,' \
               '"latitude":34.21936825217505,' \
               '}' % {
                   'version': version,
                   'app_key': app_key,
                   'access_token': access_token,
                   'timeStamp': timeStamp}
        data = get_Sign().encrypt(data)
        response = requests.post(self.url, data=json.dumps(data), headers=headers)
        response_data = response.json()
        assert response_data['err_code'] == 0 and response_data['data']['already_checkin'] == True

    def test_checkin_02(self):
        timeStamp = int(time.mktime(datetime.now().timetuple()))
        access_token = md5.encrypt_md5(timeStamp)
        data = '{"app_version":"%(version)s",' \
               '"access_token":"%(access_token)s",' \
               '"os_type":1,' \
               '"timestamp":%(timeStamp)d,' \
               '"provider":1,' \
               '"app_key":"%(app_key)s",' \
               '"device_id":"802ca0fba119ab0a",' \
               '"installation_id":1904301718321742,' \
               '"longitude":108.90823353286173,' \
               '"latitude":34.21936825217505,' \
               '}' % {
                   'version': version,
                   'app_key': app_key,
                   'access_token': access_token,
                   'timeStamp': timeStamp}
        data = get_Sign().encrypt(data)
        response = requests.post(self.url, data=json.dumps(data), headers=RunMain().headers())
        assert response.json()['err_code'] == 500


if __name__ == "__main__":

    test_Checkin().test_checkin_01()
    test_Checkin().test_checkin_02()

