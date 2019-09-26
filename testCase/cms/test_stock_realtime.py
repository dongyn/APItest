# -*- coding:utf-8 -*-
# @Time  : 2019/8/13
# @Author: yanghuiyu
# @interfacetest: https://apiv1.starschina.com/cms/v1.2/stock/realtime

from readConfig import ReadConfig
from common.configHttp import RunMain
from common.AES_CBC import AES_CBC
from datetime import datetime
from common.md5_sms import timeStamp_md5
from common.getSign import get_Sign
import common.url as url
import unittest, json, requests, time

baseurl = url.baseurl()
version = ReadConfig().get_app('version')
app_key = ReadConfig().get_app('app_key')
headers = RunMain().headers()
aes = AES_CBC()
md5 = timeStamp_md5()


class test_Stock_realtime(unittest.TestCase):
    """获取股指最新交易数据"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = baseurl + '/cms/v1.2/stock/realtime'

    def test_realtime_01(self):
        """正确的参数"""
        timeStamp = int(time.mktime(datetime.now().timetuple()))
        access_token = md5.encrypt_md5(timeStamp)
        data = '{"app_version":"%(version)s",' \
               '"os_type":1,' \
               '"app_key":"xdThhy2239daax",' \
               '"access_token":"%(access_token)s",' \
               '"timestamp":%(timeStamp)d,' \
               '"installation_id":1904301718321742,' \
               '"stock_code":"sh000001"' \
               '}' % {
                   'version': version,
                   'access_token': access_token,
                   'timeStamp': timeStamp}
        sign = get_Sign().encrypt(data, True)["sign"]
        data = data.replace('}', ',"sign": "%s"}' % sign)
        crypt_data = aes.encrypt(data, 'c_q')
        form = {"data": crypt_data, "encode": "v1"}
        response = requests.post(self.url, data=json.dumps(form), headers=headers)
        response_stock= RunMain().decrypt_to_dict(response, 'r')[0]
        msg = "股票应该{0}是{1}".format("sh000001", response_stock["stock_name"])
        self.assertEqual("sh000001", response_stock["stock_code"], msg=msg)

    def test_realtime_02(self):
        """股票代码参数值为错误的"""
        timeStamp = int(time.mktime(datetime.now().timetuple()))
        access_token = md5.encrypt_md5(timeStamp)
        data = '{"app_version":"%(version)s",' \
               '"os_type":1,' \
               '"app_key":"xdThhy2239daax",' \
               '"timestamp":%(timeStamp)d,' \
               '"installation_id":1904301718321742,' \
               '"stock_code":"sh"' \
               '}' % {
                   'version': version,
                   'timeStamp': timeStamp}
        sign = get_Sign().encrypt(data, True)["sign"]
        data = data.replace('}', ',"sign": "%s"}' % sign)
        crypt_data = aes.encrypt(data, 'c_q')
        form = {"data": crypt_data, "encode": "v1"}
        response = requests.post(self.url, data=json.dumps(form), headers=headers)
        assert response.status_code == 200

    def test_realtime_03(self):
        """股票代码参数为空"""
        timeStamp = int(time.mktime(datetime.now().timetuple()))
        access_token = md5.encrypt_md5(timeStamp)
        data = '{"app_version":"%(version)s",' \
               '"os_type":1,' \
               '"app_key":"xdThhy2239daax",' \
               '"timestamp":%(timeStamp)d,' \
               '"installation_id":1904301718321742,' \
               '}' % {
                   'version': version,
                   'timeStamp': timeStamp}
        sign = get_Sign().encrypt(data, True)["sign"]
        data = data.replace('}', ',"sign": "%s"}' % sign)
        crypt_data = aes.encrypt(data, 'c_q')
        form = {"data": crypt_data, "encode": "v1"}
        response = requests.post(self.url, data=json.dumps(form), headers=headers)
        assert response.status_code == 403

if __name__ == "main":
    test_Stock_realtime().test_realtime_01()
    test_Stock_realtime().test_realtime_02()
    test_Stock_realtime().test_realtime_03()