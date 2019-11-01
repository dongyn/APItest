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
import unittest, requests, json, datetime, time, xlrd, os


baseurl = url.baseurl()
host = url.host()
version = ReadConfig().get_app("version")
app_key = ReadConfig().get_app("app_key")
keyword = ReadConfig().get_app("keyword")
starttime = ReadConfig().get_app("starttime")
endtime = ReadConfig().get_app("endtime")
aes = AES_CBC()
mysql = OperationDbInterface()
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+ os.path.sep+"files"
xlsfile = os.path.join(parent_dir, 'IPList.xlsx')

class test_epg_shield(unittest.TestCase):
    """测试屏蔽节目单接口"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = baseurl + "/cms/v1.2/epg/list"

    def get_ip(self, n):
        book = xlrd.open_workbook(xlsfile)  # 调用xlrd，打开Excel文件
        sheet = book.sheet_by_index(0)  # 通过索引，获取相应的列表，这里表示获取Excel第一个sheet
        return  sheet.col_values(n)

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

    def epg_shield(self, city_ip, shield_type):
        """屏蔽"""
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
        headers = RunMain().shield_headers(city_ip)
        response = requests.post(url=self.url, data=json.dumps(form), headers=headers)
        if shield_type == "keyword":
            self.assert_epg_keyword_blocked(response, keyword)
        else:
            self.assert_epg_timeslot_blocked(response, starttime, endtime)

    @staticmethod
    def getTestFunc(city_ip, shield_type):
        def func(self):
            self.epg_shield(city_ip, shield_type)
        return func


def __generateTestCases():
    ip_list = test_epg_shield().get_ip(2)
    for city_ip in ip_list:
        for shield_type in ["keyword", "timeslot"]:
            setattr(test_epg_shield, 'epg_shield_%s_%s' % (shield_type, city_ip),
                    test_epg_shield.getTestFunc(city_ip, shield_type))

__generateTestCases()