# -*- coding:utf-8 -*-
# @Time  : 2019/8/12
# @Author: yanghuiyu
# @interfacetest: https://apiv1.starschina.com/cms/v1.2/stock/dot/list

from readConfig import ReadConfig
from common.configHttp import RunMain
from common.AES_CBC import AES_CBC
from common.getSign import get_Sign
from common.md5_sms import timeStamp_md5
from datetime import datetime
from common.configMysql import OperationDbInterface
import unittest,datetime, requests, json

baseurl = ReadConfig().get_http('baseurl')
version = ReadConfig().get_app('version')
app_key = ReadConfig().get_app('app_key')
headers = RunMain().headers()
aes = AES_CBC()
md5 = timeStamp_md5()
mysql = OperationDbInterface()
global stock_code

def __get_stock_code():
    today = datetime.date.today().strftime("%Y-%m-%d")
    code_time_all = mysql.select_all('select stock_code, dot_time from stock_dot')
    global stock_code
    stock_code = ""
    for code_time in code_time_all:
        if code_time["dot_time"].strftime("%Y-%m-%d") == today:
            stock_code = code_time["stock_code"]
            if stock_code != "": return stock_code

stock_code = __get_stock_code()

class test_Dot_list(unittest.TestCase):
    """股指分时打点数据"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = baseurl + '/cms/v1.2/stock/dot/list'

    @unittest.skipIf(stock_code != "", '股票上没有打点数据')
    def test_dotlist_01(self):
        """正确的参数"""
        stock_code = self.get_stock_code()
        data = '{"app_version":"%(version)s",' \
               '"os_type":1,' \
               '"app_key":"xdThhy2239daax",' \
               '"installation_id":1904301718321742,' \
               '"stock_code":"%(stock_code)s"' \
               '}' % {
                   'version': version,
                   'stock_code': stock_code}
        sign = get_Sign().encrypt(data, True)["sign"]
        data = data.replace('}', ',"sign": "%s"}' % sign)
        crypt_data = aes.encrypt(data, 'c_q')
        form = {"data": crypt_data, "encode": "v1"}
        response = requests.post(self.url, data=json.dumps(form), headers=headers)
        response_stock = RunMain().decrypt_to_dict(response, 'r')[0]
        msg = "股票应该{0}是{1}".format("sh000001", response_stock["name"])
        self.assertEqual("sh000001", response_stock["stock_code"], msg=msg)

    def test_dotlist_02(self):
        """股票代码参数值为错误的"""
        data = '{"app_version":"%(version)s",' \
                '"os_type":1,' \
               '"app_key":"xdThhy2239daax",' \
                '"installation_id":1904301718321742,' \
               '"stock_code":"sh"' \
               '}' % {
                    'version': version}
        sign = get_Sign().encrypt(data, True)["sign"]
        data = data.replace('}', ',"sign": "%s"}' % sign)
        crypt_data = aes.encrypt(data, 'c_q')
        form = {"data": crypt_data, "encode": "v1"}
        response = requests.post(self.url, data=json.dumps(form), headers=headers)
        assert response.status_code == 200

    def test_dotlist_03(self):
        """股票代码参数值为空"""
        data = '{"app_version":"%(version)s",' \
               '"os_type":1,' \
                '"app_key":"xdThhy2239daax",' \
               '"installation_id":1904301718321742' \
                '}' % {
                    'version': version}
        sign = get_Sign().encrypt(data, True)["sign"]
        data = data.replace('}', ',"sign": "%s"}' % sign)
        crypt_data = aes.encrypt(data, 'c_q')
        form = {"data": crypt_data, "encode": "v1"}
        response = requests.post(self.url, data=json.dumps(form), headers=headers)
        assert response.status_code == 400