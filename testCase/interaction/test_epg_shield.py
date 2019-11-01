# -*- coding:utf-8 -*-
# @Time  : 2019/10/15
# @Author: yanghuiyu
# @interfacetest: http://apiv1.starschina.com/cms/v1.2/epg/list


from common.AES_CBC import AES_CBC
from common.configHttp import RunMain
from readConfig import ReadConfig
from common.configMysql import OperationDbInterface
from common.getSign import get_Sign
import common.url as url
import unittest, requests, json, datetime, time

headers = RunMain().shield_headers()
baseurl = url.baseurl()
host = url.host()
version = ReadConfig().get_app("version")
app_key = ReadConfig().get_app("app_key")
shield_ip = ReadConfig().get_app("xi'an_ip")
keyword = ReadConfig().get_app("keyword")
starttime = ReadConfig().get_app("starttime")
endtime = ReadConfig().get_app("endtime")
aes = AES_CBC()
mysql = OperationDbInterface()


class test_epg_shield(unittest.TestCase):
    """测试屏蔽节目单接口"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = baseurl + "/cms/v1.2/epg/list"

    def get_date_list(self):
        now_date = datetime.datetime.now()
        date_0 = str(now_date.strftime("%Y-%m-%d"))
        date_1 = str((now_date - datetime.timedelta(days=1)).strftime("%Y-%m-%d"))
        date_2 = str((now_date - datetime.timedelta(days=2)).strftime("%Y-%m-%d"))
        date_3 = str((now_date - datetime.timedelta(days=3)).strftime("%Y-%m-%d"))
        date_4 = str((now_date + datetime.timedelta(days=1)).strftime("%Y-%m-%d"))
        date_list = [date_3, date_2, date_1, date_0, date_4]
        return date_list

    def assert_epg_keyword_blocked(self, response, keyword):
        all_days_epg_dict = RunMain().decrypt_to_dict(response, 'r')
        for epg_dict_oneday in all_days_epg_dict:
            for epg in epg_dict_oneday["epg"]:
                if keyword in epg["title"]:
                    self.assertTrue(epg["blocked"], f"{epg['title']}节目中包含关键字{keyword}，""应该被屏蔽")

    def assert_epg_timeslot_blocked(self, response, starttime, endtime):
        all_days_epg_dict = RunMain().decrypt_to_dict(response, 'r')
        for oneday_epg_dict in all_days_epg_dict:
            for epg in oneday_epg_dict["epg"]:
                if epg["start"]<= endtime or epg["end"]>= starttime :
                    self.assertTrue(epg["blocked"], f"{epg['title']}"
                    f"节目在屏蔽时段{starttime}至{endtime}，""应该被屏蔽")

    def test_01_epg_shield_keyword(self):
        """按关键字屏蔽"""
        stream_id = mysql.select_one('select id FROM stream where title = "CCTV1";')["id"]
        date_list = self.get_date_list()
        timeStamp = int(time.mktime(datetime.datetime.now().timetuple()))
        data = '{"stream_id":%(stream_id)d,' \
               '"date":["%(date_3)s","%(date_2)s","%(date_1)s","%(date_0)s","%(date_4)s"],' \
               '"os_type":1,' \
               '"app_version":"%(version)s",' \
               '"timestamp":%(timeStamp)d,' \
               '"app_key":"%(app_key)s"}' % {
                   'date_3': date_list[0],
                   'date_2': date_list[1],
                   'date_1': date_list[2],
                   'date_0': date_list[3],
                   'date_4': date_list[4],
                   'stream_id': stream_id,
                   'version': version,
                   'timeStamp': timeStamp,
                   'app_key': app_key}
        sign = get_Sign().encrypt(data, True)["sign"]
        data = data.replace('}', ',"sign":"%s"}' % sign)
        crypt_data = aes.encrypt(data, 'c_q')
        form = {"data": crypt_data, "encode": "v1"}
        response = requests.post(url=self.url, data=json.dumps(form), headers=headers)
        print(response.status_code, response.json())
        self.assert_epg_keyword_blocked(response, keyword)

    def test_02_epg_shield_timeslot(self):
        """按时段屏蔽"""
        stream_id = mysql.select_one('select id FROM stream where title = "CCTV3";')["id"]
        date_list = self.get_date_list()
        timeStamp = int(time.mktime(datetime.datetime.now().timetuple()))
        data = '{"stream_id":%(stream_id)d,' \
               '"date":["%(date_3)s","%(date_2)s","%(date_1)s","%(date_0)s","%(date_4)s"],' \
               '"os_type":1,' \
               '"app_version":"%(version)s",' \
               '"timestamp":%(timeStamp)d,' \
               '"app_key":"%(app_key)s"}' % {
                   'date_3': date_list[0],
                   'date_2': date_list[1],
                   'date_1': date_list[2],
                   'date_0': date_list[3],
                   'date_4': date_list[4],
                   'stream_id': stream_id,
                   'version': version,
                   'timeStamp': timeStamp,
                   'app_key': app_key}
        sign = get_Sign().encrypt(data, True)["sign"]
        data = data.replace('}', ',"sign":"%s"}' % sign)
        crypt_data = aes.encrypt(data, 'c_q')
        form = {"data": crypt_data, "encode": "v1"}
        response = requests.post(url=self.url, data=json.dumps(form), headers=headers)
        self.assert_epg_timeslot_blocked(response, starttime, endtime)