# -*- coding:utf-8 -*-
#@Time  : 2019/8/12
#@Author: yanghuiyu
#@interfacetest: https://apiv1.starschina.com/cms/v1.2/stock/minutely/list

from readConfig import ReadConfig
from common.configHttp import RunMain
from common.AES_CBC import AES_CBC
from datetime import datetime
from common.md5_sms import timeStamp_md5
from common.getSign import get_Sign
import unittest,json,requests,time

baseurl = ReadConfig().get_http('baseurl')
version = ReadConfig().get_app('version')
app_key = ReadConfig().get_app('app_key')
headers = RunMain().headers()
aes = AES_CBC()
md5 = timeStamp_md5()

class test_Minutely_list(unittest.TestCase):
    """获取股指分时数据， 分时曲线数据"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = baseurl + '/cms/v1.2/stock/minutely/list'
        self.timeStamp = int(time.mktime(datetime.now().timetuple()))

    def test_minutelylist_01(self):
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
               '}'% {
                   'version': version,
                   'access_token': access_token,
                   'timeStamp': self.timeStamp}
        sign = get_Sign().encrypt(data, True)["sign"]
        data = data.replace('}', ',"sign": "%s"}'%sign)
        crypt_data = aes.encrypt(data, 'c_q')
        form = {"data": crypt_data, "encode": "v1"}
        response = requests.post(self.url, data=json.dumps(form), headers=headers)
        response_stock = RunMain().decrypt_to_dict(response, 'r')["minutely"][0]
        self.assertEqual("sh000001", response_stock["stock_code"], "上证股票号码应该sh000001")

    def test_minutelylist_02(self):
        """股票代码参数为错误值"""
        timeStamp = int(time.mktime(datetime.now().timetuple()))
        access_token = md5.encrypt_md5(timeStamp)
        data = '{"app_version":"%(version)s",' \
               '"os_type":1,' \
               '"app_key":"xdThhy2239daax",' \
               '"access_token":"%(access_token)s",' \
               '"timestamp":%(timeStamp)d,' \
               '"installation_id":1904301718321742,' \
               '"stock_code":"sh"' \
               '}'% {
                   'version': version,
                   'access_token': access_token,
                   'timeStamp': self.timeStamp}
        sign = get_Sign().encrypt(data, True)["sign"]
        data = data.replace('}', ',"sign": "%s"}'%sign)
        crypt_data = aes.encrypt(data, 'c_q')
        form = {"data": crypt_data, "encode": "v1"}
        response = requests.post(self.url, data=json.dumps(form), headers=headers)
        assert response.status_code == 400

    def test_minutelylist_03(self):
        """股票代码参数为空"""
        timeStamp = int(time.mktime(datetime.now().timetuple()))
        access_token = md5.encrypt_md5(timeStamp)
        data = '{"app_version":"%(version)s",' \
               '"os_type":1,' \
               '"app_key":"xdThhy2239daax",' \
               '"access_token":"%(access_token)s",' \
               '"timestamp":%(timeStamp)d,' \
               '"installation_id":1904301718321742' \
               '}'% {
                   'version': version,
                   'access_token': access_token,
                   'timeStamp': self.timeStamp}
        sign = get_Sign().encrypt(data, True)["sign"]
        data = data.replace('}', ',"sign": "%s"}'%sign)
        crypt_data = aes.encrypt(data, 'c_q')
        form = {"data": crypt_data, "encode": "v1"}
        response = requests.post(self.url, data=json.dumps(form), headers=headers)
        assert response.status_code == 400


if __name__ == "main":
            test_Minutely_list().test_minutelylist_01()
            test_Minutely_list().test_minutelylist_02()
            test_Minutely_list().test_minutelylist_03()


