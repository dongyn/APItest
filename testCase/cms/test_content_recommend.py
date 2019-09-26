# -*- coding:utf-8 -*-
#@Time  : 2019/8/7 10:45
#@Author: pengjuan
#@interfacetest: http://apiv1.starschina.com/cms/v1.0/content/recommend

from readConfig import ReadConfig
from common.md5_sms import timeStamp_md5
from common.configMysql import OperationDbInterface
from datetime import datetime
from common.getSign import get_Sign
from common.configHttp import RunMain
import common.url as url
import unittest,requests,time

global false, true, null
baseurl = url.baseurl()
version = ReadConfig().get_app('version')
app_key = ReadConfig().get_app('app_key')
headers = RunMain().headers_get()
md5 = timeStamp_md5()
mysql = OperationDbInterface()

class test_Content_Recomment(unittest.TestCase):
    """测试用户信息"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = baseurl + '/cms/v1.0/content/recommend'
        self.timeStamp = int(time.mktime(datetime.now().timetuple()))
        self.access_token = md5.encrypt_md5(self.timeStamp)
        self.content_id = mysql.select_one(
            'select video.id FROM video LEFT JOIN resource_param on video.id = resource_param.content_id '
            'where resource_param.online = 1 and resource_param.app_id = 1 '
            'and resource_param.content_type = 1 ORDER BY RAND() LIMIT 1;')['id']

    def get_url_params(self):
        timeStamp = int(time.mktime(datetime.now().timetuple()))
        url_params = '{"app_version":"%(version)s",' \
                     '"app_key":"%(app_key)s", ' \
                     '"os_type":1,' \
                     '"content_id": %(content_id)d,'\
                     '"content_type": 1,'\
                     '"timestamp":%(timeStamp)d,' \
                     '"installation_id": 1904301718321742,' \
                     '"os_version": "8.0.1",' \
                     '"latitude": 34.230261,' \
                     '"mac_address": "02:00:00:00:00:00",' \
                     '"longitude": 108.872503,' \
                     '"device_id": "802ca0fba119ab0a"}' % {
                         'version': version,
                         'app_key': app_key,
                         'timeStamp': timeStamp,
                          'content_id': self.content_id}
        params = get_Sign().encrypt(url_params)
        return RunMain().get_url_params(params, self.url)

    def test_content_recomment_01(self):
        """正确的参数"""
        timeStamp = int(time.mktime(datetime.now().timetuple()))
        headers = RunMain().headers_get_token(timeStamp)
        response = requests.get(self.get_url_params(), headers=headers)
        response_data = str(response.json()['err_code'])
        msg = "猜你喜欢的接口返回的err_code应该是{0}实际是{1}".format('0', response_data)
        self.assertEqual('0', response_data, msg=msg)

    def test_content_recomment_02(self):
        """参数为空"""
        timeStamp = int(time.mktime(datetime.now().timetuple()))
        headers = RunMain().headers_get_token(timeStamp)
        response = requests.get(self.url, headers=headers)
        response_data = str(response.json()['err_code'])
        msg = "猜你喜欢的接口返回的err_code应该是{0}实际是{1}".format('500', response_data)
        self.assertEqual('500', response_data, msg=msg)
