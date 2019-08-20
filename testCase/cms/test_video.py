# -*- coding:utf-8 -*-
# @Time  : 2019/7/10 10:23
# @Author: pengjuan
# @interfacetest: http://apiv1.starschina.com/cms/v1.2/video

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
headers = RunMain().headers()
aes = AES_CBC()


class test_Video(unittest.TestCase):
    """测试点播接口"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = baseurl + "/cms/v1.2/video"
        self.content_video = mysql.select_one(
            'select video.id, video.title FROM video LEFT JOIN resource_param on video.id = resource_param.content_id'
            ' where resource_param.online = 1 and resource_param.app_id = 1 and resource_param.content_type = 1'
            ' ORDER BY RAND() LIMIT 1;')
        self.content_type = mysql.select_one('select content_type from resource_param where content_id = %d' %
                                             self.content_video['id'])["content_type"]

    def test_video_01(self):
        """正确的请求参数"""
        timeStamp = int(time.mktime(datetime.now().timetuple()))
        data = '{"content_id": %(content_id)d, ' \
               '"content_type": %(content_type)d, ' \
               '"os_type": 1, ' \
               '"app_version": "%(version)s", ' \
               '"timestamp":%(timeStamp)d,' \
               '"app_key":"%(app_key)s"}' % {
                   'content_id': self.content_video['id'],
                   'content_type': self.content_type,
                   'version': version,
                   'timeStamp': timeStamp,
                   'app_key': app_key}
        sign = get_Sign().encrypt(data, True)["sign"]
        data = data.replace('}', ',"sign":"%s"}' % sign)
        crypt_data = aes.encrypt(data, 'c_q')
        form = {"data": crypt_data, "encode": "v1"}
        response = requests.post(self.url, data=json.dumps(form), headers=headers)
        response_data = RunMain().decrypt_to_dict(response, 'r')
        msg = '上线剧集{0}的期望id是{1},实际id是{2}'.format(self.content_video["title"],
                                                 self.content_video["id"],
                                                 response_data["id"])
        self.assertEqual(self.content_video["id"], response_data["id"], msg=msg)

    def test_video_02(self):
        """错误的请求参数"""
        timeStamp = int(time.mktime(datetime.now().timetuple()))
        data = '{"content_id": %(content_id)d, ' \
               '"content_type": 1, ' \
               '"os_type": 4, ' \
               '"app_version": "%(version)s", ' \
               '"timestamp":%(timeStamp)d,' \
               '"app_key":"%(app_key)s"}' % {
                   'content_id': self.content_video['id'],
                   'version': version,
                   'timeStamp': timeStamp,
                   'app_key': app_key}
        sign = get_Sign().encrypt(data, True)["sign"]
        data = data.replace('}', ',"sign":"%s"}' % sign)
        crypt_data = aes.encrypt(data, 'c_q')
        form = {"data": crypt_data, "encode": "v1"}
        response = requests.post(self.url, data=json.dumps(form), headers=headers)
        assert response.json()['err_code'] == 500


