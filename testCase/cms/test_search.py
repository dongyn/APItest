# -*- coding:utf-8 -*-
# @Time  : 2019/7/10 10:23
# @Author: pengjuan
# @interfacetest: http://apiv1.starschina.com/cms/v1.2/content/search

from common.configHttp import RunMain
from readConfig import ReadConfig
from common.configMysql import OperationDbInterface
from common.getSign import get_Sign
from common.AES_CBC import AES_CBC
from datetime import datetime
import common.url as url
import requests, unittest, json, time

baseurl = url.baseurl()
version = ReadConfig().get_app('version')
app_key = ReadConfig().get_app('app_key')
aes = AES_CBC()
headers = RunMain().headers()
mysql = OperationDbInterface()


class test_Search(unittest.TestCase):
    """测试搜索接口"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = baseurl + '/cms/v1.2/content/search'
        self.title = mysql.select_one('select video.title FROM video LEFT JOIN resource_param on video.id = '
                                      'resource_param.content_id where resource_param.online = 1 and '
                                      'resource_param.app_id = 1 and resource_param.content_type = 1 '
                                      'ORDER BY RAND() LIMIT 1;')['title']

    def test_search_01(self):
        """正确的请求参数"""
        timeStamp = int(time.mktime(datetime.now().timetuple()))
        data = '{"title": "%(title)s", ' \
               '"os_type":1, ' \
               '"app_version": "%(version)s", ' \
               '"timestamp":%(timeStamp)d,' \
               '"app_key":"%(app_key)s"}' % {
                   'title': self.title,
                   'version': version,
                   'timeStamp': timeStamp,
                   'app_key': app_key}
        sign = get_Sign().encrypt(data, True)["sign"]  # 无效的签名
        data = data.replace('}', ',"sign":"%s"}' % sign)
        crypt_data = aes.encrypt(data, 'c_q')
        form = {"data": crypt_data, 'encode': "v1"}
        response = requests.post(self.url, data=json.dumps(form), headers=headers)
        response_data = RunMain().decrypt_to_dict(response, 'r')['result'][0]['title']
        assert response_data == self.title

    def test_search_02(self):
        """错误的请求参数"""
        timeStamp = int(time.mktime(datetime.now().timetuple()))
        data = '{"title": "集体么去impose", ' \
               '"os_type":1, ' \
               '"app_version": "%(version)s", ' \
               '"timestamp":%(timeStamp)d,' \
               '"app_key":"%(app_key)s"}' % {
                   'version': version,
                   'timeStamp': timeStamp,
                   'app_key': app_key}
        sign = get_Sign().encrypt(data, True)["sign"]  # 无效的签名
        data = data.replace('}', ',"sign":"%s"}' % sign)
        crypt_data = aes.encrypt(data, 'c_q')
        form = {"data": crypt_data, 'encode': "v1"}
        response = requests.post(self.url, data=json.dumps(form), headers=headers)
        response_data = RunMain().decrypt_to_dict(response, 'r')['result'][0]['title']
        assert response_data != '集体么去impose'

    def test_search_03(self):
        """错误的请求参数"""
        data = '{"title": "%(title)s", ' \
               '"os_type":3, ' \
               '"app_version": "%(version)s", ' \
               '"app_key":"%(app_key)s"}' % {
                   'title': self.title,
                   'version': version,
                   'app_key': app_key}
        crypt_data = aes.encrypt(data, 'c_q')
        form = {"data": crypt_data, 'encode': "v1"}
        response = requests.post(self.url, data=json.dumps(form), headers=headers)
        assert response.status_code == 403

    def test_search_04(self):
        """os_type参数值为空"""
        data = '{"title": "%(title)s", ' \
               '"os_type":, ' \
               '"app_version": "%(version)s", ' \
               '"app_key":"%(app_key)s"}' % {
                   'title': self.title,
                   'version': version,
                   'app_key': app_key}
        crypt_data = aes.encrypt(data, 'c_q')
        form = {"data": crypt_data, 'encode': "v1"}
        response = requests.post(self.url, data=json.dumps(form), headers=headers)
        assert response.status_code == 403
