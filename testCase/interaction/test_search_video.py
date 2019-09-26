# -*- coding:utf-8 -*-
# @Time: 2019/08/06
# @Author: yanghuiyu
# @interfacetest:
# 1.在数据库中随机查找1000个安卓剧集类型上线的点播视频的id和title
# 2.播放搜到的点播视频: /cms/v1.2/video


from common.configHttp import RunMain
from readConfig import ReadConfig
from common.AES_CBC import AES_CBC
from common.configMysql import OperationDbInterface
from common.getSign import get_Sign
from datetime import datetime
import common.url as url
import unittest, json, requests, time

mysql = OperationDbInterface()

class test_Search_video(unittest.TestCase):
    # 搜索点播视频，播放视频

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.headers = RunMain().headers()
        self.baseurl = url.baseurl()
        self.version = ReadConfig().get_app("version")
        self.app_key = ReadConfig().get_app("app_key")
        self.aes = AES_CBC()

    def get_sql_list(self):
        return mysql.select_all(
            'select video.id, video.title FROM cms.video LEFT JOIN cms.resource_param on '
            'cms.video.id = cms.resource_param.content_id '
            'where resource_param.online = 1 and resource_param.app_id = 1 and resource_param.content_type = 1;'
        )

    def videolist(self,video):
            time.sleep(1) #点播资源连跑有5000多条，服务器请求会有延时，加3秒等待下就好了
            url = self.baseurl + "/cms/v1.2/video"
            timeStamp = int(time.mktime(datetime.now().timetuple()))
            data = '{"os_type":1, ' \
                   '"app_version":"%(version)s", ' \
                   '"content_id":%(video_id)d, ' \
                   '"content_type":1,' \
                   '"timestamp":%(timeStamp)d,' \
                   '"app_key":"%(app_key)s"}' % {
                       'version': self.version,
                       'app_key': self.app_key,
                       'timeStamp': timeStamp,
                       'video_id': video["id"]}
            sign = get_Sign().encrypt(data, True)["sign"]
            data = data.replace('}', ',"sign":"%s"}' % sign)
            crypt_data = self.aes.encrypt(data, 'c_q')
            form = {"data": crypt_data, "encode": "v1"}
            response = requests.post(url=url, data=json.dumps(form), headers=self.headers)
            response_data = RunMain().decrypt_to_dict(response, 'r')
            msg = '上线剧集{0}的期望id是{1},实际id是{2}'.format(video["title"], video["id"], response_data["id"])
            self.assertEqual(video["id"], response_data["id"], msg=msg)

    @staticmethod
    def getTestFunc(video):
        def func(self):
            self.videolist(video)
        return func


def __generateTestCases():
    video_list = test_Search_video().get_sql_list()
    for video in video_list:
        setattr(test_Search_video, 'test_video_%s' % (video["title"]),
                test_Search_video.getTestFunc(video))


__generateTestCases()
