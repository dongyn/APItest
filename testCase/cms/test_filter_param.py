# -*- coding:utf-8 -*-
#@Time  : 2019/8/1 14:44
#@Author: dongyani
#@interfacetest: http://apiv1.starschina.com/cms/v1.0/filter/param

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
headers= RunMain().headers_get()

class test_Filterparam(unittest.TestCase):
    """测试订单状态"""

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
        assert data['category_id'] == 1
        assert data['properties'][0]['name'] == '地域'


    def test_filterparam_02(self):
        """错误的参数"""
        url = self.get_url_params().replace("category_id=1", "category_id=a")
        response = requests.get(url, headers=headers)
        assert response.json()['err_code']==500

    def test_filterparam_03(self):
        """参数为空"""
        response = requests.get(self.url, headers=headers)
        assert response.json()['err_code']==500

# if __name__ == "__main__":
#     test_filterparam().test_filterparam_01()
