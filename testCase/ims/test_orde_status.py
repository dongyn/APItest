# -*- coding:utf-8 -*-
#@Time  : 2019/7/31 17:39
#@Author: dongyani
#@interfacetest: https://apiv1.starschina.com/ims/v1.0/user/order/status

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
md5 = timeStamp_md5()
headers = RunMain().headers_get()

class test_Orderstatus(unittest.TestCase):
    """测试订单状态"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = baseurl + '/ims/v1.0/user/order/status'

    def get_url_params(self):
        timeStamp = int(time.mktime(datetime.now().timetuple()))
        # order_id 必填, 订单id
        data = '{"app_version":"%(version)s",' \
               '"os_type":1,' \
               '"timestamp":%(timeStamp)d,' \
               '"order_id":116592,' \
               '"app_key":"%(app_key)s"' \
               '}' % {
                   'version': version,
                   'app_key': app_key,
                   'timeStamp': timeStamp}
        data = get_Sign().encrypt(data)
        return RunMain().get_url_params(data, self.url)

    def test_orderstatus_01(self):
        """正确的参数"""
        url = self.get_url_params()
        response = requests.get(url, headers=headers)
        print(response.status_code)
        print(response.json()['data'])
        assert response.json()['data']['source_id'] == 1

'''
    def test_orderstatus_02(self):
        """headers没有token"""
        response = requests.get(self.get_url_params(), headers=RunMain().headers())
        assert response.json()['err_code'] == 500

    def test_orderstatus_03(self):
        """参数为空"""
        response = requests.get(self.url, headers=RunMain().headers())
        assert response.json()['err_code'] == 500
'''
# if __name__ == "__main__":
#     test_Orderstatus().test_orderstatus_01()
