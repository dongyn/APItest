# -*- coding:utf-8 -*-
#@Time  : 2019/7/31 14:16
#@Author: pengjuan
#@interfacetest: http://apiv1.starschina.com/ims/v1.0/user/bind

from common.configHttp import RunMain
from common.getSign import get_Sign
from common.md5_sms import timeStamp_md5
from readConfig import ReadConfig
from datetime import datetime
import requests, unittest, json, time

global false, true, null
baseurl = ReadConfig().get_http('baseurl')
version = ReadConfig().get_app('version')
app_key = ReadConfig().get_app('app_key')
md5 = timeStamp_md5()

class test_Bind(unittest.TestCase):
    """换绑定手机号"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = baseurl + '/ims/v1.0/user/bind'
        self.timeStamp = int(time.mktime(datetime.now().timetuple()))

    def test_bind_01(self):
        """正确的请求参数"""
        timeStamp_login = int(time.mktime(datetime.now().timetuple()))
        headers = RunMain().headers_token(timeStamp_login)
        time.sleep(5)
        timeStamp = int(time.mktime(datetime.now().timetuple()))
        access_token = md5.encrypt_md5(timeStamp)
        data = '{"app_version":"%(version)s",' \
                 '"access_token":"%(access_token)s",' \
                 '"open_id":"13032982950",' \
                 '"country_code" : "+86",'\
                 '"os_type":1,' \
                 '"timestamp":%(timeStamp)d,' \
                 '"provider":1,' \
                 '"app_key":"%(app_key)s",' \
                 '"device_id":"802ca0fba119ab0a",' \
                 '"country_code":"+86",' \
                 '"installation_id":1904301718321742,' \
                 '"device_id" : "40439d078e887033",' \
                 '"imei" : "A000008D9CEF1C",' \
                 '"gcid" : "c9d669a8cf72d08952acdff036cd7ea1",' \
                 '"os_version" : "8.1.0",' \
                 '}' % {
                     'version': version,
                     'app_key': app_key,
                     'access_token': access_token,
                     'timeStamp': timeStamp}
        data = get_Sign().encrypt(data)
        response = requests.post(self.url, data=json.dumps(data), headers=headers)
        if response.status_code == 200:
            response_data = response.json()
            assert response_data['err_code'] == 0
        else:
            print("获取%s接口返回的参数错误" % self.url)

    def test_bind_02(self):
        """错误的请求参数"""
        timeStamp_login = int(time.mktime(datetime.now().timetuple()))
        headers = RunMain().headers_token(timeStamp_login)
        time.sleep(5)
        timeStamp = int(time.mktime(datetime.now().timetuple()))
        access_token = md5.encrypt_md5(timeStamp)
        data = '{"app_version":"%(version)s",' \
                 '"access_token":"%(access_token)s",' \
                 '"open_id":"13032982950",' \
                 '"country_code" : "+86",'\
                 '"os_type":1,' \
                 '"timestamp":%(timeStamp)d,' \
                 '"provider":1,' \
                 '"app_key":"wdsfsfeerwe",' \
                 '"device_id":"802ca0fba119ab0a",' \
                 '"country_code":"+86",' \
                 '"installation_id":1904301718321742,' \
                 '"device_id" : "40439d078e887033",' \
                 '"imei" : "A000008D9CEF1C",' \
                 '"gcid" : "c9d669a8cf72d08952acdff036cd7ea1",' \
                 '"os_version" : "8.1.0",' \
                 '}' % {
                     'version': version,
                     'access_token': access_token,
                     'timeStamp': timeStamp}
        data = get_Sign().encrypt(data)
        response = requests.post(self.url, data=json.dumps(data), headers=headers)
        if response.status_code == 403:
            err_code = response.json()['err_code']
            assert err_code == 500
        else:
            print("接口%s请求os_type参数值错误，返回的err_code应为500" % self.url)

    def test_bind_03(self):
        """空的请求参数"""
        timeStamp_login = int(time.mktime(datetime.now().timetuple()))
        headers = RunMain().headers_token(timeStamp_login)
        time.sleep(5)
        timeStamp = int(time.mktime(datetime.now().timetuple()))
        access_token = md5.encrypt_md5(timeStamp)
        data = '{"app_version":"%(version)s",' \
                 '"access_token":"%(access_token)s",' \
                 '"open_id":"13032982950",' \
                 '"country_code" : "+86",'\
                 '"os_type":1,' \
                 '"timestamp":%(timeStamp)d,' \
                 '"provider":1,' \
                 '"device_id":"802ca0fba119ab0a",' \
                 '"country_code":"+86",' \
                 '"installation_id":1904301718321742,' \
                 '"device_id" : "40439d078e887033",' \
                 '"imei" : "A000008D9CEF1C",' \
                 '"gcid" : "c9d669a8cf72d08952acdff036cd7ea1",' \
                 '"os_version" : "8.1.0",' \
                 '}' % {
                     'version': version,
                     'access_token': access_token,
                     'timeStamp': timeStamp}
        data = get_Sign().encrypt(data)
        response = requests.post(self.url, data=json.dumps(data), headers=headers)
        if response.status_code == 403:
            err_code = response.json()['err_code']
            assert err_code == 500
        else:
            print("接口%s请求os_type参数值错误，返回的err_code应为500" % self.url)

if __name__ == '__main__':
    test_Bind().test_bind_01()
    test_Bind().test_bind_02()
    test_Bind().test_bind_03()