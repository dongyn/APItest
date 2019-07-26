# -*- coding:utf-8 -*-
#@Time  : 2019/7/13 15:11
#@Author: pengjuan
#@interfacetest: http://apiv1.starschina.com/ims/v1.0/user/login

from readConfig import ReadConfig
from common.md5_sms import timeStamp_md5
from common.getSign import get_Sign
from common.configHttp import RunMain
from datetime import datetime
import time,unittest,json,requests

global false, true, null
headers = RunMain().headers()
baseurl = ReadConfig().get_http('baseurl')
version = ReadConfig().get_app('version')
app_key = ReadConfig().get_app('app_key')
md5 = timeStamp_md5()
getSign = get_Sign()

class test_Login(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url =  baseurl + '/ims/v1.0/user/login'
        self.timeStamp = int(time.mktime(datetime.now().timetuple()))

    # 正确的登录参数
    def test_login_01(self):
        """正确的请求参数"""
        access_token = md5.encrypt_md5(self.timeStamp)
        data = '{"app_version":"%(version)s",' \
               '"access_token":"%(access_token)s",' \
               '"os_type":1,' \
               '"timestamp":%(timeStamp)d,' \
               '"open_id":"19991828757",' \
               '"provider":1,' \
               '"app_key":"xdThhy2239daax",' \
               '"device_id":"802ca0fba119ab0a",' \
               '"country_code":"+86",' \
               '"installation_id":1904301718321742,' \
               '"longitude":108.90823353286173,' \
               '"latitude":34.21936825217505}' % {
            'version':version,
            'access_token':access_token,
            'timeStamp':self.timeStamp}
        data = getSign.encrypt(data)
        response = requests.post(self.url, data=json.dumps(data), headers=headers)
        if response.status_code == 200:
            response_errcode = response.json()['err_code']
            assert response_errcode == 0
        else:
            print("获取%s接口返回的参数错误" % self.url)

    # 错误的登录参数
    # def test_login_02(self):
    #     data = '{"gcid": "a6046afa66261aed7d3aef819eb9f0cb","app_key": "%(app_key)s","app_version": "%(version)s","sign": "A8FDEBE6CF94B9F78CC52172AFFAEAD435A25302","installation_id": 1904151004093101,"latitude": 34.263161,"os_type": 3, "longitude": 108.948024,"country_code": "+86","timestamp": 1563001102,"access_token": "%(access_token)s","provider": 1,"open_id": "18192873108","device_id": "CDDFDD2C-77E5-4768-A1A2-209D699A9DDB","BSSID": "ec:41:18:4f:74:24"}'% {
    #         'access_token': self.access_token, 'version': version, 'app_key': app_key}
    #     response = requests.post(self.url, data=json.dumps(data), headers=headers)
    #     if response.status_code == 403:
    #         err_code = response.json()['err_code']
    #         assert err_code == 500
    #     else:
    #         print("接口%s请求os_type参数值错误，返回的err_code应为500" % self.url)
    #
    #  # 为空的登录参数
    # def test_login_03(self):
    #     data = '{"gcid": "a6046afa66261aed7d3aef819eb9f0cb","app_key": "%(app_key)s","app_version": "%(version)s","sign": "A8FDEBE6CF94B9F78CC52172AFFAEAD435A25302","installation_id": 1904151004093101,"latitude": 34.263161,"os_type": , "longitude": 108.948024,"country_code": "+86","timestamp": 1563001102,"access_token": "%(access_token)s","provider": 1,"open_id": "18192873108","device_id": "CDDFDD2C-77E5-4768-A1A2-209D699A9DDB","BSSID": "ec:41:18:4f:74:24"}'% {
    #         'access_token': self.access_token, 'version': version, 'app_key': app_key}
    #     response = requests.post(self.url, data=json.dumps(data), headers=headers)
    #     if response.status_code == 403:
    #         err_code = response.json()['err_code']
    #         assert err_code == 500
    #     else:
    #         print("接口%s请求os_type参数值错误，返回的err_code应为500" % self.url)

if __name__ == "__main__":
    test_Login().test_login_01()
    # test_Login().test_login_02()
    # test_Login().test_login_03()
