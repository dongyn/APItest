# -*- coding:utf-8 -*-
#@Time  : 2019/7/31 17:39
#@Author: dongyani
#@interfacetest: https://apiv1.starschina.com/ims/v1.0/user/order/status

from common.configHttp import RunMain
from readConfig import ReadConfig
from common.md5_sms import timeStamp_md5
from datetime import datetime
from common.getSign import get_Sign
import common.url as url
import unittest, requests, time

global false, true, null
baseurl = url.baseurl()
version = ReadConfig().get_app('version')
app_key = ReadConfig().get_app('app_key')
md5 = timeStamp_md5()

class test_Orderstatus(unittest.TestCase):
    """测试订单状态"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = baseurl + '/ims/v1.0/user/order/status'

    def get_url_params(self):
        # order_id 必填, 订单id
        data = '{"app_version":"%(version)s",' \
               '"os_type":1,' \
               '"order_id":116592,' \
               '"app_key":"%(app_key)s"' \
               '}' % {
                   'version': version,
                   'app_key': app_key}
        data = get_Sign().encrypt(data)
        return RunMain().get_url_params(data, self.url)

    def test_orderstatus_01(self):
        """正确的参数"""
        timeStamp = int(time.mktime(datetime.now().timetuple()))
        headers = RunMain().headers_get_token(timeStamp)
        url = self.get_url_params()
        response = requests.get(url, headers=headers)
        assert response.json()['data']['status'] == 1


    def test_orderstatus_02(self):
        """headers没有token"""
        response = requests.get(self.get_url_params(), headers=RunMain().headers_get())
        assert response.json()['err_code'] == 500


    def test_orderstatus_03(self):
        """order_id参数为空"""
        timeStamp = int(time.mktime(datetime.now().timetuple()))
        headers = RunMain().headers_get_token(timeStamp)
        url = self.get_url_params().replace('order_id=116592', 'order_id= ')
        response = requests.get(url, headers=headers)
        assert response.status_code == 400
