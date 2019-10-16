# -*- coding:utf-8 -*-
# @Time  : 2019/8/16 10:43
# @Author: dongyani
# @interfacetest: http://apiv1.starschina.com/cms/v1.2/tycoon/detail

from readConfig import ReadConfig
from common.md5_sms import timeStamp_md5
from common.configMysql import OperationDbInterface
from datetime import datetime
from common.AES_CBC import AES_CBC
from common.getSign import get_Sign
from common.configHttp import RunMain
import common.url as url
import unittest, json, requests, time

global false, null, true
baseurl = url.baseurl()
version = ReadConfig().get_app('version')
app_key = ReadConfig().get_app('app_key')
headers = RunMain().headers()
aes = AES_CBC()
mysql = OperationDbInterface()
md5 = timeStamp_md5()

global tycoon_id, video_id, tycoon_video, tycoon_name
tycoon_id = video_id = tycoon_video = tycoon_name = {}
tycoon_id = mysql.select_one(
            'select id from tycoon WHERE id in (SELECT tycoon_id from tycoon_video left join resource_param on '
            'tycoon_video.video_id = resource_param.content_id where resource_param.online = 1 '
            'and resource_param.app_id = 1 and resource_param.content_type = 1)ORDER BY RAND() limit 1;')
video_id = mysql.select_one(
            'select video_id from tycoon_video left join resource_param on '
            'tycoon_video.video_id = resource_param.content_id where resource_param.online = 1 '
            'and resource_param.app_id = 1 and resource_param.content_type = 1 and '
            'tycoon_id = %d ORDER BY RAND() limit 1;' % tycoon_id["id"])
tycoon_id.update(video_id)
tycoon_video = tycoon_id
video_title = mysql.select_one('SELECT title from video where id = %d;' % video_id["video_id"])
tycoon_name = mysql.select_one('SELECT tycoon.name from tycoon where id = %d;'% tycoon_id["id"])

class test_tycoon_detail(unittest.TestCase):
    """测试用户信息"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = baseurl + "/cms/v1.2/tycoon/detail"
        self.timeStamp = int(time.mktime(datetime.now().timetuple()))
        self.content_video_error = {"id": 1000000000, "video_id": 1000000000}

    def tycoon_detail(self, params, param):
        timeStamp = int(time.mktime(datetime.now().timetuple()))
        data = '{"app_version":"%(version)s",' \
               '"installation_id":1904301718321742,' \
               '"timestamp":%(timeStamp)d,' \
               '"app_key":"%(app_key)s", ' \
               '"os_version":"9",' \
               '"mac_address":"02:00:00:00:00:00",' \
               '"device_id":"802ca0fba119ab0a",' \
               '"os_type":1,' \
               '"%(key)s":%(id)d}' % {
                   'version': version,
                   'key': param,
                   'id': params[param],
                   'timeStamp': timeStamp,
                   'app_key': app_key}
        sign = get_Sign().encrypt(data, True)["sign"]
        data = data.replace('}', ',"sign":"%s"}' % sign)
        crypt_data = aes.encrypt(data, 'c_q')
        form = {"data": crypt_data, "encode": "v1"}
        response = requests.post(url=self.url, data=json.dumps(form), headers=headers)
        if type(params.values()) != type("a"):
            if list(params.values())[0] < 1000000000:
                acturl_tycoon_name = RunMain().decrypt_to_dict(response, 'r')["name"]
                msg = "大咖详情接口返回的大咖-{0}信息错误".format(tycoon_name["name"])
                self.assertEqual(tycoon_name["name"], acturl_tycoon_name, msg)
        else:
            self.assertEqual(400, response.status_code, "参数错误，接口应返回400")
            self.assertEqual(500, response.json()["err_code"], "参数错误，接口应返回err_code500")


    def get_test_func(self, params, id):
        if params[id] == 1000000000:
            return id + "错误"
        elif id == "video_id":
            return video_title["title"]
        else:
            return tycoon_name["name"]


    @staticmethod
    def getTestFunc(params, id):
        def func(self):
            self.tycoon_detail(params, id)
        return func


def __generateTestCases():
    for params in [tycoon_video, test_tycoon_detail().content_video_error]:
        for id in params.keys():
            setattr(test_tycoon_detail, 'test_tycoon_detail_%s' % (test_tycoon_detail().get_test_func(params, id)),
                    test_tycoon_detail.getTestFunc(params, id))


__generateTestCases()
