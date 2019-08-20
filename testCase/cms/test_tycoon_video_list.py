# -*- coding:utf-8 -*-
# @Time  : 2019/8/12 10:04
# @Author: dongyani
# @interfacetest: http://apiv1.starschina.com/cms/v1.2/tycoon/video/list

from common.configHttp import RunMain
from readConfig import ReadConfig
from common.configMysql import OperationDbInterface
from common.getSign import get_Sign
from common.AES_CBC import AES_CBC
from datetime import datetime
import requests, unittest, json, time

baseurl = ReadConfig().get_http('baseurl')
version = ReadConfig().get_app('version')
app_key = ReadConfig().get_app('app_key')
mysql = OperationDbInterface("cms")
aes = AES_CBC()
headers = RunMain().headers()


class test_tycoon_video_list(unittest.TestCase):
    """测试大咖列表"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = baseurl + '/cms/v1.2/tycoon/video/list'
        self.tycoon_id =  mysql.select_one('select tycoon_id from tycoon_video ORDER BY RAND() limit 1;')["tycoon_id"]
        self.tycoon_video_all = mysql.select_all('select video_id FROM tycoon_video where tycoon_id = %d;' %self.tycoon_id)
        self.tycoon_name = mysql.select_one('select tycoon.name FROM tycoon where id = %d;' %self.tycoon_id)["name"]

    def get_database_tycoon_video(self):
        database_tycoon_video = []
        for video in self.tycoon_video_all:
            database_tycoon_video.append(video['video_id'])
        return database_tycoon_video

    def get_response_tycoon_video(self, response):
        video_id_list = []
        video_all = RunMain().decrypt_to_dict(response, 'r')
        for key in video_all.keys():
            for video in video_all[key]:
                video_id_list.append(video["id"])
        return video_id_list

    def test_tycoon_list_01(self):
        """参数有tycoon_id，返回单个大咖信息"""
        timeStamp = int(time.mktime(datetime.now().timetuple()))
        data = '{"app_version":"%(version)s",' \
               '"os_type":1,' \
               '"tycoon_id":%(tycoon_id)d,' \
               '"os_version":"9",' \
               '"mac_address":"02:00:00:00:00:00",'\
               '"device_id":"802ca0fba119ab0a",' \
               '"limit":1,' \
               '"query_type":"all",' \
               '"timestamp":%(timeStamp)d,' \
               '"app_key":"%(app_key)s"' \
               '}' % {
                   'version': version,
                   'tycoon_id': self.tycoon_id,
                   'timeStamp': timeStamp,
                   'app_key': app_key}
        sign = get_Sign().encrypt(data, True)["sign"]
        data = data.replace('}', ',"sign":"%s"}' % sign)
        crypt_data = aes.encrypt(data, 'c_q')
        form = {'data': crypt_data, 'encode': 'v1'}
        response = requests.post(self.url, data=json.dumps(form), headers=headers)
        # 返回的是curriculum课程和realtime实时分析两个列表,合在一起验证
        video_dict = self.get_response_tycoon_video(response)
        for video_id in self.get_database_tycoon_video():
            self.assertIn(video_id, video_dict, "大咖{0}的视频列表中应包含的视频id为{1}".format(self.tycoon_name, video_id))

    def test_tycoon_list_02(self):
        """参数tycoon_id值错误"""
        timeStamp = int(time.mktime(datetime.now().timetuple()))
        data = '{"app_version":"%(version)s",' \
               '"os_type":1,' \
               '"tycoon_id":10000000,' \
               '"os_version":"9",' \
               '"mac_address":"02:00:00:00:00:00",'\
               '"device_id":"802ca0fba119ab0a",' \
               '"limit":1,' \
               '"query_type":"all",' \
               '"timestamp":%(timeStamp)d,' \
               '"app_key":"%(app_key)s"' \
               '}' % {
                   'version': version,
                   'timeStamp': timeStamp,
                   'app_key': app_key}
        sign = get_Sign().encrypt(data, True)["sign"]
        data = data.replace('}', ',"sign":"%s"}' % sign)
        crypt_data = aes.encrypt(data, 'c_q')
        form = {'data': crypt_data, 'encode': 'v1'}
        response = requests.post(self.url, data=json.dumps(form), headers=headers)
        video_all = RunMain().decrypt_to_dict(response, 'r')
        self.assertEqual({}, video_all, "返回的大咖视频应该为空")