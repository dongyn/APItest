# -*- coding:utf-8 -*-
# @Time  : 2019/8/12 10:04
# @Author: dongyani
# @interfacetest: http://apiv1.starschina.com/cms/v1.2/tycoon/list

from common.configHttp import RunMain
from readConfig import ReadConfig
from common.configMysql import OperationDbInterface
from common.getSign import get_Sign
from common.AES_CBC import AES_CBC
from datetime import datetime
import requests, unittest, json, time

baseurl = ReadConfig().get_http('baseurl')
version = ReadConfig().get_app('version')
app_key = ReadConfig().get_app('app_key')
mysql = OperationDbInterface()
aes = AES_CBC()
headers = RunMain().headers()


class test_Tycoon_list(unittest.TestCase):
    """测试大咖列表"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = baseurl + '/cms/v1.2/tycoon/list'
        self.tycoon_detail = mysql.select_one('select * FROM tycoon ORDER BY RAND() limit 1;')
        self.tycoon_name = mysql.select_all('select tycoon.name FROM tycoon;')

    def test_tycoon_list_01(self):
        """参数有tycoon_id，返回单个大咖信息"""
        # 在数据库中查出来有这个id的大咖，但是不知道为何接口返回为空,数据库与服务器不匹配造成的
        timeStamp = int(time.mktime(datetime.now().timetuple()))
        data = '{"app_version":"%(version)s",' \
               '"os_type":1,' \
               '"tycoon_id":%(tycoon_id)d,' \
               '"os_version":"9",' \
               '"mac_address":"02:00:00:00:00:00",'\
               '"device_id":"802ca0fba119ab0a",' \
               '"limit":1,' \
               '"timestamp":%(timeStamp)d,' \
               '"app_key":"%(app_key)s"' \
               '}' % {
                   'version': version,
                   'tycoon_id': self.tycoon_detail["id"],
                   'timeStamp': timeStamp,
                   'app_key': app_key}
        sign = get_Sign().encrypt(data, True)["sign"]
        data = data.replace('}', ',"sign":"%s"}' % sign)
        crypt_data = aes.encrypt(data, 'c_q')
        form = {'data': crypt_data, 'encode': 'v1'}
        response = requests.post(self.url, data=json.dumps(form), headers=headers)
        tycoon_name = RunMain().decrypt_to_dict(response, 'r')[0]["name"]
        self.assertEqual(self.tycoon_detail["name"], tycoon_name, "大咖姓名应该是{0}".format(self.tycoon_detail["name"]))

    def test_tycoon_list_02(self):
        """tycoon_id参数为错误"""
        data = '{"app_version":"%(version)s",' \
               '"os_type":1,' \
               '"tycoon_id":%(tycoon_id)d,' \
               '"os_version":"9",' \
               '"mac_address":"02:00:00:00:00:00",' \
               '"device_id":"802ca0fba119ab0a",' \
               '"limit":1,' \
               '"app_key":"%(app_key)s"' \
               '}' % {
                   'version': version,
                   'tycoon_id': -1,
                   'app_key': app_key}
        sign = get_Sign().encrypt(data, True)["sign"]
        data = data.replace('}', ',"sign":"%s"}' % sign)
        crypt_data = aes.encrypt(data, 'c_q')
        form = {'data': crypt_data, 'encode': 'v1'}
        response = requests.post(self.url, data=json.dumps(form), headers=headers)
        self.assertEqual(500, response.json()["err_code"], "大咖的id参数错误，接口应返回err_code为500")

    def get_tycoon_name(self):
        names = []
        for tycoon in self.tycoon_name:
            names.append(tycoon["name"])
        return names

    def get_tycoon_list(self):
        timeStamp = int(time.mktime(datetime.now().timetuple()))
        data = '{"app_version":"%(version)s",' \
               '"os_type":1,' \
               '"limit":5,' \
               '"os_version":"9",' \
               '"mac_address":"02:00:00:00:00:00",' \
               '"device_id":"802ca0fba119ab0a",' \
               '"timestamp":%(timeStamp)d,' \
               '"app_key":"%(app_key)s"' \
               '}' % {
                   'version': version,
                   'tycoon_id': self.tycoon_detail["id"],
                   'timeStamp': timeStamp,
                   'app_key': app_key}
        sign = get_Sign().encrypt(data, True)["sign"]
        data = data.replace('}', ',"sign":"%s"}' % sign)
        crypt_data = aes.encrypt(data, 'c_q')
        form = {'data': crypt_data, 'encode': 'v1'}
        response = requests.post(self.url, data=json.dumps(form), headers=headers)
        return RunMain().decrypt_to_dict(response, 'r')

    def tycoon_list(self, tycoon):
        """参数没有tycoon_id，返回多个大咖信息"""
        self.assertIn(tycoon["name"], self.get_tycoon_name(), "大咖表中未包含大咖{0}".format(tycoon["name"]))

    @staticmethod
    def getTestFunc(tycoon):
        def func(self):
            self.tycoon_list(tycoon)
        return func


def __generateTestCases():
    tycoon_list = test_Tycoon_list().get_tycoon_list()
    for tycoon in tycoon_list:
        setattr(test_Tycoon_list, 'test_tycoon_list_%s' % (tycoon["name"]),
                test_Tycoon_list.getTestFunc(tycoon))

__generateTestCases()
