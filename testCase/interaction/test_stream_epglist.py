# -*- coding:utf-8 -*-
# @Time  : 2019/8/6 16:16
# @Author: dongyani
# @interfacetest: http://apiv1.starschina.com
# 1.播放直播节目:/cms/v1.2/stream
# 2.回看节目:/cms/v1.2/epg/list


from common.AES_CBC import AES_CBC
from common.configHttp import RunMain
from readConfig import ReadConfig
from common.configMysql import OperationDbInterface
from common.getSign import get_Sign
import unittest, requests, json, datetime, time

headers = RunMain().headers()
baseurl = ReadConfig().get_http("baseurl")
version = ReadConfig().get_app("version")
app_key = ReadConfig().get_app("app_key")
aes = AES_CBC()
mysql = OperationDbInterface("cms")


class test_stream(unittest.TestCase):
    """测试查看直播详情接口"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_stream_title(self):
        """正确的请求参数"""
        timeStamp = int(time.mktime(datetime.datetime.now().timetuple()))
        data = '{"os_type":1, ' \
               '"app_version":"%(version)s", ' \
               '"id":160, ' \
               '"timestamp":%(timeStamp)d,' \
               '"app_key":"%(app_key)s"}' % {
                   'version': version,
                   'timeStamp': timeStamp,
                   'app_key': app_key}
        sign = get_Sign().encrypt(data, True)["sign"]
        data = data.replace('}', ',"sign":"%s"}' % sign)
        crypt_data = aes.encrypt(data, 'c_q')
        form = {"data": crypt_data, "encode": "v1"}
        url = baseurl + "/cms/v1.2/stream"
        response = requests.post(url=url, data=json.dumps(form), headers=headers)
        response_data = RunMain().decrypt_to_dict(response, 'r')
        return response_data["title"]

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

    def get_response_stream_id(self, response):
        data = aes.decrypt(response.json()['data'], 'r')
        global false, null, true
        false = null = true = ""
        return list(eval(data))[0]["epg"][0]["stream_id"]

    def test_stream_epg_list(self):
        """正确的请求参数"""
        stream_title = self.get_stream_title()
        stream_id = mysql.select_one('select id FROM stream where title = "%s"' % stream_title)["id"]
        date_list = self.get_date_list()
        timeStamp = int(time.mktime(datetime.datetime.now().timetuple()))
        data = '{"stream_id":%(stream_id)d,' \
               '"date":["%(date_3)s","%(date_2)s","%(date_1)s","%(date_0)s","%(date_4)s"],' \
               '"os_type":1,' \
               '"app_version":"%(version)s",' \
               '"timestamp":%(timeStamp)d,' \
               '"app_key":"%(app_key)s"}' % {
                   'app_key': app_key,
                   'date_3': date_list[0],
                   'date_2': date_list[1],
                   'date_1': date_list[2],
                   'date_0': date_list[3],
                   'date_4': date_list[4],
                   'stream_id': stream_id,
                   'timeStamp': timeStamp,
                   'version': version}
        sign = get_Sign().encrypt(data, True)["sign"]
        data = data.replace('}', ',"sign":"%s"}' % sign)
        crypt_data = aes.encrypt(data, 'c_q')
        form = {"data": crypt_data, "encode": "v1"}
        url = baseurl + "/cms/v1.2/epg/list"
        response = requests.post(url=url, data=json.dumps(form), headers=headers)
        actual_id = self.get_response_stream_id(response)
        msg = "{0}电视台返回的id应该是{1}，实际是{2}".format(stream_title, stream_id, actual_id)
        self.assertEqual(stream_id, actual_id, msg)
