# -*- coding:utf-8 -*-
#@Time  : 2019/7/10 10:23
#@Author: dongyani
#@interfacetest: http://apiv1.starschina.com/cms/v1.2/epg/list

import unittest
import requests,json
import datetime
from common.configMysql import OperationDbInterface
from common.AES_CBC import AES_CBC
from common.configHttp import RunMain
from readConfig import ReadConfig


global false, null, true

headers = RunMain().headers()
baseurl = ReadConfig().get_http("baseurl")
version = ReadConfig().get_app("version")
app_key = ReadConfig().get_app("app_key")
mysql = OperationDbInterface()
aes = AES_CBC()

class test_epglist(unittest.TestCase):
    """测试节目单列表接口"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = baseurl + "/cms/v1.2/epg/list"
        self.sql_id = mysql.select_one(
            'select id FROM stream where title = "CCTV1";')
        self.stream_id = self.sql_id['id']

    def get_date_list(self):
        now_date = datetime.datetime.now()
        date_0 = str(now_date.strftime("%Y-%m-%d"))
        # datetime.datetime.now()+datetime.timedelta(days=1)
        date_1 = str((now_date - datetime.timedelta(days = 1)).strftime("%Y-%m-%d"))
        date_2 = str((now_date - datetime.timedelta(days = 2)).strftime("%Y-%m-%d"))
        date_3 = str((now_date - datetime.timedelta(days = 3)).strftime("%Y-%m-%d"))
        date_4 = str((now_date + datetime.timedelta(days = 1)).strftime("%Y-%m-%d"))
        date_list = [date_3, date_2, date_1, date_0, date_4]
        return date_list

    def test_01_epg_list(self):
        date_list = self.get_date_list()
        data = '{"stream_id":%(stream_id)d,"date":["%(date_3)s","%(date_2)s","%(date_1)s","%(date_0)s","%(date_4)s"],"os_type":1,"app_version":"%(version)s","app_key":"%(app_key)s"}'% {
            'app_key': app_key,
            'date_3': date_list[0],
            'date_2': date_list[1],
            'date_1': date_list[2],
            'date_0': date_list[3],
            'date_4': date_list[4],
            'stream_id': self.stream_id,
            'version': version}
        crypt_data = aes.encrypt(data, 'c_q')
        form = {"data": crypt_data, "encode": "v1"}
        response = requests.post(url=self.url, data=json.dumps(form), headers=headers)
        if response.status_code == 200:
            r_data = response.json()['data']
            data = aes.decrypt(r_data, 'r')
            global false, null, true
            false = null = true = ""
            a = list(eval(data))
            assert self.stream_id == list(eval(data))[0]["epg"][0]["stream_id"]
        else:
            print("获取%s接口返回的stream_id错误" %self.url)

    def test_02_epg_list_error(self):
        data = '{"os_type":1, "app_version":"%(version)s", "id":1, "app_key":"abdcdsaoswuiewka"}' % {'version':version}
        crypt_data = aes.encrypt(data, 'c_q')
        form = {"data": crypt_data, "encode": "v1"}
        response = requests.post(url=self.url, data=json.dumps(form), headers=headers)
        print(response.status_code)
        if (response.status_code == 403):
            err_code = response.json()['err_code']
            assert err_code == 500
        else:
            print("接口%s请求id和app_key参数值错误，返回的err_code应为500" %self.url)

    def test_03_epg_list_null(self):
        data = ''
        crypt_data = aes.encrypt(data, 'c_q')
        form = {"data": crypt_data, "encode": "v1"}
        response = requests.post(url=self.url, data=json.dumps(form), headers=headers)
        if (response.status_code == 403):
            err_code = response.json()['err_code']
            assert err_code == 500
        else:
            print("接口%s缺失app_version和app_key参数，返回的状态码应为403" %self.url)



# if __name__ == "__main__":
#     test_epglist().test_01_epg_list()
    # date = datetime.datetime.now().strftime("%Y-%m-%d")
    # print(date)