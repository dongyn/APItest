# -*- coding:utf-8 -*-
#@Time  : 2019/7/29 10:12
#@Author: pengjuan
#@interfacetest: http://apiv1.starschina.com/ims/v1.0/user/logout

from common.configHttp import RunMain
from readConfig import ReadConfig
from common.md5_sms import timeStamp_md5
from datetime import datetime
from common.getSign import get_Sign
import unittest, json, requests, time

global false, true, null
baseurl = ReadConfig().get_http('baseurl')
version = ReadConfig().get_app('version')
app_key = ReadConfig().get_app('app_key')
headers = RunMain().headers_token()
md5 = timeStamp_md5()

class test_Logout(unittest.TestCase):
    """测试用户退出登录"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = baseurl + '/ims/v1.0/user/logout'
        self.timeStamp = int(time.mktime(datetime.now().timetuple()))
        self.access_token = md5.encrypt_md5(self.timeStamp)

    def test_logout_01(self):
        """正确的退出登录参数"""
        data = '{"app_version":"%(version)s",' \
               '"access_token":"%(access_token)s",' \
               '"os_type":1,' \
               '"timestamp":%(timeStamp)d,' \
               '"provider":1,' \
               '"app_key":"%(app_key)s",' \
               '"device_id":"802ca0fba119ab0a",' \
               '"country_code":"+86",' \
               '"installation_id":1904301718321742,' \
               '"longitude":108.90823353286173,' \
               '"latitude":34.21936825217505,' \
               '}' % {
                   'version': version,
                   'app_key': app_key,
                   'access_token': self.access_token,
                   'timeStamp': self.timeStamp}
        data = get_Sign().encrypt(data)
        response = requests.post(self.url, data=json.dumps(data), headers=headers)
        if response.status_code == 200:
            response_data = response.json()
            assert response_data['err_code'] == 0
        else:
            print("获取%s接口返回的参数错误" % self.url)


    def test_logout_02(self):
        """错误的退出登录参数"""

        data = '{"app_version":"%(version)s",' \
               '"access_token":"%(access_token)s",' \
               '"os_type":1,' \
               '"timestamp":%(timeStamp)d,' \
               '"provider":1,' \
               '"app_key":"ddfsweer",' \
               '"device_id":"802ca0fba119ab0a",' \
               '"country_code":"+86",' \
               '"installation_id":1904301718321742,' \
               '"longitude":108.90823353286173,' \
               '"latitude":34.21936825217505,' \
               '}' % {
                   'version': version,
                   'access_token': self.access_token,
                   'timeStamp': self.timeStamp}
        data = get_Sign().encrypt(data)
        response = requests.post(self.url, data=json.dumps(data), headers=headers)
        if response.status_code == 403:
            err_code = response.json()['err_code']
            assert err_code == 500
        else:
            print("接口%s请求os_type参数值错误，返回的err_code应为500" % self.url)

    def test_logout_03(self):
        """空的退出登录参数"""

        data = '{"app_version":"%(version)s",' \
               '"access_token":"%(access_token)s",' \
               '"timestamp":%(timeStamp)d,' \
               '"provider":1,' \
               '"app_key":"%(app_key)s",' \
               '"device_id":"802ca0fba119ab0a",' \
               '"country_code":"+86",' \
               '"installation_id":1904301718321742,' \
               '"longitude":108.90823353286173,' \
               '"latitude":34.21936825217505,' \
               '}' % {
                   'version': version,
                   'app_key': app_key,
                   'access_token': self.access_token,
                   'timeStamp': self.timeStamp}
        data = get_Sign().encrypt(data)
        response = requests.post(self.url, data=json.dumps(data), headers=headers)
        if response.status_code == 403:
            err_code = response.json()['err_code']
            assert err_code == 500
        else:
            print("接口%s请求os_type参数值错误，返回的err_code应为500" % self.url)

if __name__ == "__main__":

    test_Logout().test_logout_01()
    test_Logout().test_logout_02()
    test_Logout().test_logout_03()