# -*- coding:utf-8 -*-
# @Time  : 2019/8/12 10:04
# @Author: dongyani
# @interfacetest: http://apiv1.starschina.com/cms/v1.2/researchreport/list

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

class test_Researchreport_list(unittest.TestCase):
    """测试研报列表"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = baseurl + '/cms/v1.2/researchreport/list'
        self.researchreport_detail = mysql.select_one('select * FROM cms.researchreport ORDER BY RAND() limit 1;')
        self.researchreport_title = mysql.select_all('select researchreport.title FROM cms.researchreport;')

    def test_researchreport_list_01(self):
        """参数有tycoon_id，返回大咖主页研报"""
        timeStamp = int(time.mktime(datetime.now().timetuple()))
        data = '{"app_version":"%(version)s",' \
               '"os_type":1,' \
               '"os_version":"9",' \
               '"mac_address":"02:00:00:00:00:00",' \
               '"device_id":"802ca0fba119ab0a",' \
               '"tycoon_id":%(tycoon_id)d,' \
               '"query_type":"all",' \
               '"timestamp":%(timeStamp)d,' \
               '"app_key":"%(app_key)s"' \
               '}' % {
                   'version': version,
                   'tycoon_id': self.researchreport_detail["tycoon_id"],
                   'timeStamp': timeStamp,
                   'app_key': app_key}
        sign = get_Sign().encrypt(data, True)["sign"]
        data = data.replace('}', ',"sign":"%s"}' % sign)
        crypt_data = aes.encrypt(data, 'c_q')
        form = {'data': crypt_data, 'encode': 'v1'}
        response = requests.post(self.url, data=json.dumps(form), headers=headers)
        researchreport_all = RunMain().decrypt_to_dict(response, 'r')
        # - charge 列表为收费研报
        # - free  列表为免费研报
        title_list = []
        for free_page in ["free", "charge"]:
            if free_page in researchreport_all.keys():
                for researchreport in researchreport_all[free_page]:
                    title_list.append(researchreport["title"])
        msg = f'大咖id为{self.researchreport_detail["tycoon_id"]}，大咖的研报应该包含{self.researchreport_detail["title"]}'
        self.assertIn(self.researchreport_detail["title"], title_list, msg)

    def test_researchreport_list_02(self):
        """researchreport_id参数为错误"""
        timeStamp = int(time.mktime(datetime.now().timetuple()))
        data = '{"app_version":"%(version)s",' \
               '"os_type":1,' \
               '"os_version":"9",' \
               '"mac_address":"02:00:00:00:00:00",' \
               '"device_id":"802ca0fba119ab0a",' \
               '"tycoon_id":%(tycoon_id)d,' \
               '"timestamp":%(timeStamp)d,' \
               '"app_key":"%(app_key)s"' \
               '}' % {
                   'version': version,
                   'tycoon_id': 10000000000,
                   'timeStamp': timeStamp,
                   'app_key': app_key}
        sign = get_Sign().encrypt(data, True)["sign"]
        data = data.replace('}', ',"sign":"%s"}' % sign)
        crypt_data = aes.encrypt(data, 'c_q')
        form = {'data': crypt_data, 'encode': 'v1'}
        response = requests.post(self.url, data=json.dumps(form), headers=headers)
        self.assertEqual(500, response.json()["err_code"], "大咖的id参数错误，接口应返回err_code为500")

    @staticmethod
    def getTestFunc(researchreport):
        def func(self):
            self.researchreport_list(researchreport)
        return func


def __generateTestCases():
    researchreport_list = test_Researchreport_list().get_researchreport_list()
    for researchreport in researchreport_list:
        setattr(test_Researchreport_list, 'test_func_%s' % (researchreport["title"]),
                test_Researchreport_list.getTestFunc(researchreport))


__generateTestCases()
