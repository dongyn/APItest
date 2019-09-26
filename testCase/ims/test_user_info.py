# -*- coding:utf-8 -*-
#@Time  : 2019/7/31 16:08
#@Author: dongyani
#@interfacetest: http://apiv1.starschina.com/ims/v1.0/user/info

from readConfig import ReadConfig
from common.md5_sms import timeStamp_md5
from datetime import datetime
from common.getSign import get_Sign
from common.configHttp import RunMain
import common.url as url
import unittest,requests,time

baseurl = url.baseurl()
version = ReadConfig().get_app('version')
app_key = ReadConfig().get_app('app_key')
telephone = ReadConfig().get_app('telephone')
headers = RunMain().headers_get()
md5 = timeStamp_md5()

class test_Userinfo(unittest.TestCase):
    """测试用户信息"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = baseurl + '/ims/v1.0/user/info'
        self.timeStamp = int(time.mktime(datetime.now().timetuple()))
        self.access_token = md5.encrypt_md5(self.timeStamp)

    def get_url_params(self):
        timeStamp = int(time.mktime(datetime.now().timetuple()))
        url_params = '{"app_version":"%(version)s",' \
                     '"app_key":"%(app_key)s", ' \
                     '"os_type":1,' \
                     '"timestamp":%(timeStamp)d,' \
                     '"installation_id": 1904301718321742,' \
                     '"os_version": "9",' \
                     '"latitude": 34.230261,' \
                     '"mac_address": "02:00:00:00:00:00",' \
                     '"longitude": 108.872503,' \
                     '"device_id": "802ca0fba119ab0a"}' % {
                         'version': version,
                         'app_key': app_key,
                         'timeStamp': timeStamp}
        params = get_Sign().encrypt(url_params)
        return RunMain().get_url_params(params, self.url)


    def test_userinfo_01(self):
        """正确的参数"""
        timeStamp = int(time.mktime(datetime.now().timetuple()))
        headers = RunMain().headers_get_token(timeStamp)
        response = requests.get(self.get_url_params(), headers=headers)
        acture_name = response.json()['data']['nickname'][0:2]
        msg = "用户信息中用户的名称前两个字默认是星星，实际是{0}".format(acture_name)
        self.assertEqual('星星', acture_name, msg)

    def test_userinfo_02(self):
        """参数为空"""
        timeStamp = int(time.mktime(datetime.now().timetuple()))
        headers = RunMain().headers_get_token(timeStamp)
        response = requests.get(self.url, headers=headers)
        assert response.json()['err_code'] == 500


# if __name__ == "__main__":
#     test_Userinfo().test_userinfo_01()
#     test_Userinfo().test_userinfo_02()
#     test_Login().test_login_03()