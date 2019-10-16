# -*- coding:utf-8 -*-
#@Time  : 2019/8/1 14:44
#@Author: dongyani
#@interfacetest: http://apiv1.starschina.com/cms/v1.0/filter/param

from common.configHttp import RunMain
from readConfig import ReadConfig
from datetime import datetime
from common.getSign import get_Sign
import common.url as url
import unittest, requests, time

global false, true, null
baseurl = url.baseurl()
version = ReadConfig().get_app('version')
app_key = ReadConfig().get_app('app_key')
headers= RunMain().headers_get()

class test_Filterparam(unittest.TestCase):
    """测试过滤参数"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = baseurl + '/cms/v1.0/filter/param'

    def get_url_params(self):
        timeStamp = int(time.mktime(datetime.now().timetuple()))
        # category_id 必填
        data = '{"os_type":1,'\
               '"os_version":9,'\
               '"app_version":"%(version)s",' \
               '"category_id":1,' \
               '"timestamp":%(timeStamp)d,' \
               '"app_key":"%(app_key)s"' \
               '}' % {
                   'version': version,
                   'app_key': app_key,
                   'timeStamp': timeStamp}
        data = get_Sign().encrypt(data)
        return RunMain().get_url_params(data, self.url)

    def test_filterparam_01(self):
        """正确的参数"""
        url = self.get_url_params()
        response = requests.get(url, headers=headers)
        data = response.json()['data']
        self.assertEqual(1, data['category_id'], "filterparam接口返回的category_id应该是1")
        self.assertEqual('地域', data['properties'][0]['name'], "filterparam接口返回properties的name应该是地域")


    def test_filterparam_02(self):
        """错误的参数"""
        url = self.get_url_params().replace("category_id=1", "category_id=11")
        response = requests.get(url, headers=headers)
        self.assertEqual("无效的签名", response.json()["err_msg"],"category_id参数错误应返回无效的签名")


    def test_filterparam_03(self):
        """参数为空"""
        response = requests.get(self.url, headers=headers)
        self.assertEqual(500, response.json()['err_code'], "category_id参数错误应返回无效的签名")

