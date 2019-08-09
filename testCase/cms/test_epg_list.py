# -*- coding:utf-8 -*-
# @Time  : 2019/7/10 10:23
# @Author: dongyani
# @interfacetest: http://apiv1.starschina.com/cms/v1.2/epg/list


from common.configMysql import OperationDbInterface
from common.AES_CBC import AES_CBC
from common.configHttp import RunMain
from readConfig import ReadConfig
import unittest, requests, json, datetime


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
        date_1 = str((now_date - datetime.timedelta(days=1)).strftime("%Y-%m-%d"))
        date_2 = str((now_date - datetime.timedelta(days=2)).strftime("%Y-%m-%d"))
        date_3 = str((now_date - datetime.timedelta(days=3)).strftime("%Y-%m-%d"))
        date_4 = str((now_date + datetime.timedelta(days=1)).strftime("%Y-%m-%d"))
        date_list = [date_3, date_2, date_1, date_0, date_4]
        return date_list

    def test_01_epg_list(self):
        """正确的请求参数"""
        date_list = self.get_date_list()
        data = '{"stream_id":%(stream_id)d,' \
               '"date":["%(date_3)s","%(date_2)s","%(date_1)s","%(date_0)s","%(date_4)s"],' \
               '"os_type":1,' \
               '"app_version":"%(version)s",' \
               '"app_key":"%(app_key)s"}' % {
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
        data = aes.decrypt(response.json()['data'], 'r')
        global false, null, true
        false = null = true = ""
        assert self.stream_id == list(eval(data))[0]["epg"][0]["stream_id"]

    def test_02_epg_list_error(self):
        """错误的请求参数"""
        data = '{"os_type":1, "app_version":"%(version)s", "id":1, "app_key":"abdcdsaoswuiewka"}' % {'version': version}
        crypt_data = aes.encrypt(data, 'c_q')
        form = {"data": crypt_data, "encode": "v1"}
        response = requests.post(url=self.url, data=json.dumps(form), headers=headers)
        assert response.json()['err_code'] == 500

    def test_03_epg_list_null(self):
        """请求参数为空"""
        crypt_data = aes.encrypt('', 'c_q')
        form = {"data": crypt_data, "encode": "v1"}
        response = requests.post(url=self.url, data=json.dumps(form), headers=headers)
        assert response.json()['err_code'] == 500

# if __name__ == "__main__":
#     test_epglist().test_01_epg_list()
# date = datetime.datetime.now().strftime("%Y-%m-%d")
# print(date)
