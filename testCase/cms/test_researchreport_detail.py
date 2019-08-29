# -*- coding:utf-8 -*-
# @Time  : 2019/8/12 10:43
# @Author: pengjuan
# @interfacetest: http://apiv1.starschina.com/cms/v1.2/researchreport/detail

from readConfig import ReadConfig
from common.configMysql import OperationDbInterface
from datetime import datetime
from common.AES_CBC import AES_CBC
from common.getSign import get_Sign
from common.configHttp import RunMain
import unittest, json, requests, time

baseurl = ReadConfig().get_http('baseurl')
version = ReadConfig().get_app('version')
app_key = ReadConfig().get_app('app_key')
headers = RunMain().headers()
ip = RunMain().get_host_ip()
cms_db = "cms" if ip == "39.105.54.219" else "test"
cms_mysql = OperationDbInterface(cms_db)
ims_db = "ims" if ip == "39.105.54.219" else "test"
ims_mysql = OperationDbInterface(ims_db)
aes = AES_CBC()

class test_Researchreport_Detail(unittest.TestCase):
    """测试研报详情"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = baseurl + "/cms/v1.2/researchreport/detail"
        self.tycoon_id = cms_mysql.select_all('SELECT researchreport.tycoon_id from cms.researchreport')
        self.all_content_id = ims_mysql.select_all('select content_id from ims.product where content_type = 35;')
        self.all_researchreport_tycoon_id = cms_mysql.select_all('select id, tycoon_id from cms.researchreport;')

    def get_product_content_id(self):
        content_id_list = []
        for content_id in self.all_content_id: content_id_list.append(content_id['content_id'])
        return content_id_list

    def get_reseachreport_id(self):
        reseachreport_id = 1
        content_id_list = self.get_product_content_id()
        for researchreport_tycoon in self.all_researchreport_tycoon_id:
            if researchreport_tycoon["tycoon_id"] in content_id_list:
                if reseachreport_id == 1 : reseachreport_id = researchreport_tycoon["id"]
        return reseachreport_id

    def test_researchreport_detail_01(self):
        """正确的请求参数"""
        timeStamp = int(time.mktime(datetime.now().timetuple()))
        data = '{"app_version":"%(version)s",' \
               '"timestamp":%(timeStamp)d,' \
               '"app_key":"%(app_key)s", ' \
               '"installation_id": 1904301718321742,' \
               '"os_version":"9",' \
               '"mac_address":"02:00:00:00:00:00",' \
               '"device_id":"802ca0fba119ab0a",' \
               '"os_type":1,' \
               '"id": %(id)d}' % {
                   'version': version,
                   'id': self.get_reseachreport_id(),
                   'app_key': app_key,
                   'timeStamp': timeStamp}
        sign = get_Sign().encrypt(data, True)["sign"]
        data = data.replace('}', ',"sign":"%s"}' % sign)
        crypt_data = aes.encrypt(data, 'c_q')
        form = {"data" : crypt_data, "encode" : "v1"}
        response = requests.post(url=self.url, data=json.dumps(form), headers=headers)
        self.assertTrue(response.json()['err_code'] == 0 and response.json()['encode'] == 'v1', "请求失败")

    def test_researchreport_detail_02(self):
        """错误的请求参数"""
        timeStamp = int(time.mktime(datetime.now().timetuple()))
        data = '{"app_version":"%(version)s",' \
               '"timestamp":%(timeStamp)d,' \
               '"app_key":"%(app_key)s", ' \
               '"installation_id": 1904301718321742,' \
               '"os_version":"9",' \
               '"mac_address":"02:00:00:00:00:00",' \
               '"device_id":"802ca0fba119ab0a",' \
               '"os_type":1,' \
               '"id": -1}' % {
                   'version': version,
                   'timeStamp': timeStamp,
                   'app_key': app_key}
        sign = get_Sign().encrypt(data, True)["sign"]
        data = data.replace('}', ',"sign":"%s"}' % sign)
        crypt_data = aes.encrypt(data, 'c_q')
        form = {"data" : crypt_data, "encode" : "v1"}
        response = requests.post(self.url, data=json.dumps(form), headers=headers)
        self.assertEqual(400, response.status_code, "大咖的id参数错误，研报接口状态码应为400")
        self.assertEqual(500, response.json()["err_code"], "大咖的id参数错误，研报接口应返回err_code为500")

# if __name__ == "main":
#     test_Researchreport_Detail().test_researchreport_detail_01()
#     test_Researchreport_Detail().test_researchreport_detail_02()
