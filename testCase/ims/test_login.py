# -*- coding:utf-8 -*-
# @Time  : 2019/7/13 15:11
# @Author: pengjuan
# @interfacetest: http://apiv1.starschina.com/ims/v1.0/user/login

from readConfig import ReadConfig
from common.md5_sms import timeStamp_md5
from datetime import datetime
from common.getSign import get_Sign
from common.configHttp import RunMain
import unittest, json, requests, time

global false, true, null
baseurl = ReadConfig().get_http('baseurl')
version = ReadConfig().get_app('version')
app_key = ReadConfig().get_app('app_key')
telephone = ReadConfig().get_app('telephone')
headers = RunMain().headers()
md5 = timeStamp_md5()


class test_Login(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = baseurl + '/ims/v1.0/user/login'


    # def test_login_01(self):
    #     '''正确的参数'''
    #     timeStamp = int(time.mktime(datetime.now().timetuple()))
    #     access_token = md5.encrypt_md5(timeStamp)
    #     data = '{"app_version":"%(version)s",' \
    #            '"access_token":"%(access_token)s",' \
    #            '"os_type":1,' \
    #            '"timestamp":%(timeStamp)d,' \
    #            '"open_id":"%(telephone)s",' \
    #            '"provider":1,' \
    #            '"app_key":"%(app_key)s",' \
    #            '"device_id":"802ca0fba119ab0a",' \
    #            '"country_code":"+86",' \
    #            '"installation_id":1904301718321742,' \
    #            '"longitude":108.90823353286173,' \
    #            '"latitude":34.21936825217505,' \
    #            '}' % {
    #                'version': version,
    #                'app_key': app_key,
    #                'access_token': access_token,
    #                'timeStamp': timeStamp,
    #                'telephone': telephone}
    #     data = get_Sign().encrypt(data)
    #     response = requests.post(self.url, data=json.dumps(data), headers=headers)
    #     assert response.json()['err_code'] == 0
    #
    # def test_login_02(self):
    #     '''错误的参数'''
    #     timeStamp = int(time.mktime(datetime.now().timetuple()))
    #     access_token = md5.encrypt_md5(timeStamp)
    #     data = '{"app_version":"%(version)s",' \
    #            '"access_token":"%(access_token)s",' \
    #            '"os_type":3,' \
    #            '"timestamp":%(timeStamp)d,' \
    #            '"open_id":"%(telephone)s",' \
    #            '"provider":1,' \
    #            '"app_key":"%(app_key)s",' \
    #            '"device_id":"802ca0fba119ab0a",' \
    #            '"country_code":"+86",' \
    #            '"installation_id":1904301718321742,' \
    #            '"longitude":108.90823353286173,' \
    #            '"latitude":34.21936825217505' \
    #            '}' % {
    #                'version': version,
    #                'access_token': access_token,
    #                'timeStamp': timeStamp,
    #                'app_key': app_key,
    #                'telephone': telephone}
    #     data = get_Sign().encrypt(data)
    #     response = requests.post(self.url, data=json.dumps(data), headers=headers)
    #     assert response.json()['err_code'] == 500


    def test_login_03(self):
        '''参数为空'''
        timeStamp = int(time.mktime(datetime.now().timetuple()))
        access_token = md5.encrypt_md5(timeStamp)
        data = '{"app_version":"%(version)s",' \
               '"access_token":"%(access_token)s",' \
               '"os_type":1,' \
               '"timestamp":%(timeStamp)d,' \
               '"open_id":"",' \
               '"provider":1,' \
               '"app_key":"%(app_key)s",' \
               '"device_id":"802ca0fba119ab0a",' \
               '"country_code":"+86",' \
               '"installation_id":1904301718321742,' \
               '"longitude":108.90823353286173,' \
               '"latitude":34.21936825217505' \
               '}' % {
                   'version': version,
                   'access_token': '',
                   'timeStamp': timeStamp,
                   'app_key': app_key,
                   'telephone': telephone}
        data = get_Sign().encrypt(data)
        response = requests.post(self.url, data='', headers=headers)
        print(response.status_code)
        assert response.json()['err_code'] == 500

# if __name__ == "__main__":
#     test_Login().test_login_01()
#     test_Login().test_login_02()
#     test_Login().test_login_03()
