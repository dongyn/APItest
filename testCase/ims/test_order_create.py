# -*- coding:utf-8 -*-
#@Time  : 2019/7/31 17:15
#@Author: dongyani
#@interfacetest: https://apiv1.starschina.com/ims/v1.0/user/order/create

from common.configHttp import RunMain
from readConfig import ReadConfig
from common.md5_sms import timeStamp_md5
from datetime import datetime
from common.getSign import get_Sign
import common.url as url
import unittest, json, requests, time

baseurl = url.baseurl()
version = ReadConfig().get_app('version')
app_key = ReadConfig().get_app('app_key')
md5 = timeStamp_md5()

class test_Ordercreate(unittest.TestCase):
    """测试创建订单"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = baseurl + '/ims/v1.0/user/order/create'

    def test_ordercreate_01(self):
        """正确的参数"""
        timeStamp_login = int(time.mktime(datetime.now().timetuple()))
        headers = RunMain().headers_token(timeStamp_login)
        timeStamp = int(time.mktime(datetime.now().timetuple()))
        access_token = md5.encrypt_md5(timeStamp)
        # source_type 必填, 1是商品, 2是套餐;source_id 必填, 商品或者套餐id;pay_method 必填, 支付方式
        data = '{"app_version":"%(version)s",' \
               '"access_token":"%(access_token)s",' \
               '"os_type":1,' \
               '"timestamp":%(timeStamp)d,' \
               '"source_id":1,'\
               '"source_type":2,'\
               '"pay_method":3,'\
               '"app_key":"%(app_key)s"' \
               '}' % {
                   'version': version,
                   'app_key': app_key,
                   'access_token': access_token,
                   'timeStamp': timeStamp}
        data = get_Sign().encrypt(data)
        response = requests.post(self.url, data=json.dumps(data), headers=headers)
        self.assertEqual(1, response.json()['data']['source_id'], "订单创建接口返回的source_id应为1")

    def test_ordercreate_02(self):
        """headers没有token"""
        timeStamp = int(time.mktime(datetime.now().timetuple()))
        access_token = md5.encrypt_md5(timeStamp)
        data = '{"app_version":"%(version)s",' \
               '"access_token":"%(access_token)s",' \
               '"os_type":1,' \
               '"timestamp":%(timeStamp)d,' \
               '"source_id":1,' \
               '"source_type":2,' \
               '"pay_method":3,' \
               '"app_key":"%(app_key)s",' \
               '}' % {
                   'version': version,
                   'app_key': app_key,
                   'access_token': access_token,
                   'timeStamp': timeStamp}
        data = get_Sign().encrypt(data)
        response = requests.post(self.url, data=json.dumps(data), headers=RunMain().headers())
        self.assertEqual(500, response.json()['err_code'], "订单创建接口入参错误返回的err_code应为1")

    def test_ordercreate_03(self):
        """source_id参数值错误"""
        timeStamp_login = int(time.mktime(datetime.now().timetuple()))
        headers = RunMain().headers_token(timeStamp_login)
        timeStamp = int(time.mktime(datetime.now().timetuple()))
        access_token = md5.encrypt_md5(timeStamp)
        data = '{"app_version":"%(version)s",' \
               '"access_token":"%(access_token)s",' \
               '"os_type":1,' \
               '"timestamp":%(timeStamp)d,' \
               '"source_id":"a",' \
               '"source_type":2,' \
               '"pay_method":3,' \
               '"app_key":"%(app_key)s",' \
               '}' % {
                   'version': version,
                   'app_key': app_key,
                   'access_token': access_token,
                   'timeStamp': timeStamp}
        data = get_Sign().encrypt(data)
        response = requests.post(self.url, data=json.dumps(data), headers=headers)
        self.assertEqual(400, response.status_code, "source_id参数值错误接口状态码应返回400")
