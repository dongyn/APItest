# -*- coding:utf-8 -*-
# @Time  : 2019/8/12 10:04
# @Author: dongyani
# @interfacetest: http://apiv1.starschina.com/cms/v1.2/researchreport/list

from common.configHttp import RunMain
from readConfig import ReadConfig
from common.configMysql import OperationDbInterface
from common.AES_CBC import AES_CBC
import requests, unittest, json

baseurl = ReadConfig().get_http('baseurl')
version = ReadConfig().get_app('version')
app_key = ReadConfig().get_app('app_key')
mysql = OperationDbInterface()
aes = AES_CBC()
headers = RunMain().headers()


class test_Researchreport_list(unittest.TestCase):
    """测试研报列表"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = baseurl + '/cms/v1.2/researchreport/list'
        self.researchreport_detail = mysql.select_one('select * FROM researchreport ORDER BY RAND() limit 1;')
        self.researchreport_title = mysql.select_all('select researchreport.title FROM researchreport;')

    def test_researchreport_list_01(self):
        """参数有tycoon_id，返回大咖主页研报"""
        data = '{"app_version":"%(version)s",' \
               '"os_type":1,' \
               '"tycoon_id":%(tycoon_id)d,' \
               '"query_type":"all",' \
               '"app_key":"%(app_key)s"' \
               '}' % {
                   'version': version,
                   'tycoon_id': self.researchreport_detail["tycoon_id"],
                   'app_key': app_key}
        crypt_data = aes.encrypt(data, 'c_q')
        form = {'data': crypt_data, 'encode': 'v1'}
        response = requests.post(self.url, data=json.dumps(form), headers=headers)
        researchreport_title = RunMain().decrypt_to_dict(response, 'r')["free"][0]["title"]
        msg = "大咖{0}研报应是应该是{1}".format(self.researchreport_detail["tycoon_name"],
                                       self.researchreport_detail["title"])
        self.assertEqual(self.researchreport_detail["title"], researchreport_title, msg)

    def test_researchreport_list_02(self):
        """researchreport_id参数为错误"""
        data = '{"app_version":"%(version)s",' \
               '"os_type":1,' \
               '"tycoon_id":%(tycoon_id)d,' \
               '"app_key":"%(app_key)s"' \
               '}' % {
                   'version': version,
                   'tycoon_id': -1,
                   'app_key': app_key}
        crypt_data = aes.encrypt(data, 'c_q')
        form = {'data': crypt_data, 'encode': 'v1'}
        response = requests.post(self.url, data=json.dumps(form), headers=headers)
        self.assertEqual(400, response.status_code, "大咖的id参数错误，研报接口状态码应为400")
        self.assertEqual(500, response.json()["err_code"], "大咖的id参数错误，研报接口应返回err_code为500")

    def get_researchreport_title(self):
        titles = []
        for researchreport in self.researchreport_title:
            titles.append(researchreport["title"])
        return titles

    def get_researchreport_list(self):
        data = '{"app_version":"%(version)s",' \
               '"os_type":1,' \
               '"query_type":"all",' \
               '"app_key":"%(app_key)s"' \
               '}' % {
                   'version': version,
                   'app_key': app_key}
        crypt_data = aes.encrypt(data, 'c_q')
        form = {'data': crypt_data, 'encode': 'v1'}
        response = requests.post(self.url, data=json.dumps(form), headers=headers)
        return RunMain().decrypt_to_dict(response, 'r')["free"]

    def researchreport_list(self, researchreport):
        """参数没有researchreport_id，返回多个大咖信息"""
        self.assertIn(researchreport["title"], self.get_researchreport_title(),
                      "研报表中未包含研报{0}".format(researchreport["title"]))

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
