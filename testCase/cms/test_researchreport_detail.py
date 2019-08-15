# -*- coding:utf-8 -*-
# @Time  : 2019/8/12 10:43
# @Author: pengjuan
# @interfacetest: http://apiv1.starschina.com/cms/v1.2/researchreport/detail

from readConfig import ReadConfig
from common.md5_sms import timeStamp_md5
from common.configMysql import OperationDbInterface
from datetime import datetime
from common.AES_CBC import AES_CBC
from common.getSign import get_Sign
from common.configHttp import RunMain
import unittest, json, requests, time

global false, null, true
baseurl = ReadConfig().get_http('baseurl')
version = ReadConfig().get_app('version')
app_key = ReadConfig().get_app('app_key')
headers = RunMain().headers()
aes = AES_CBC()
mysql = OperationDbInterface()
md5 = timeStamp_md5()

class test_Researchreport_Detail(unittest.TestCase):
    """测试用户信息"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = baseurl + "/cms/v1.2/researchreport/detail"
        self.timeStamp = int(time.mktime(datetime.now().timetuple()))
        self.reseachreport_id = mysql.select_one(
            'SELECT researchreport.id from researchreport '
            'left join ims.product on ims.product.content_id = cms.researchreport.tycoon_id '
            'where ims.product.content_type=35;')

    def test_researchreport_detail_01(self):
        """正确的请求参数"""
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
                   'id': self.reseachreport_id['id'],
                   'timeStamp': self.timeStamp,
                   'app_key': app_key}
        sign = get_Sign().encrypt(data, True)["sign"]
        data = data.replace('}', ',"sign":"%s"}' % sign)
        crypt_data = aes.encrypt(data, 'c_q')
        form = {"data" : crypt_data, "encode" : "v1"}
        response = requests.post(url=self.url, data=json.dumps(form), headers=headers)
        self.assertTrue(response.json()['err_code'] == 0 and response.json()['encode'] == 'v1', "请求失败")

    def test_researchreport_detail_02(self):
        """错误的请求参数"""
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
                   'timeStamp': self.timeStamp,
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
