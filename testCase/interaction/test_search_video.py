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
from datetime import datetime
import unittest, json, requests, time

global false, true, null
mysql = OperationDbInterface()

class test_Search_video(unittest.TestCase):
    # 搜索点播视频，播放视频

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.headers = RunMain().headers()
        self.baseurl = ReadConfig().get_http("baseurl")
        self.version = ReadConfig().get_app("version")
        self.app_key = ReadConfig().get_app("app_key")
        self.aes = AES_CBC()
        self.timeStamp = int(time.mktime(datetime.now().timetuple()))

    def get_sql_list(self):
        return mysql.select_all(
            'select video.id, video.title FROM video LEFT JOIN resource_param on video.id = resource_param.content_id '
            'where resource_param.online = 1 and resource_param.app_id = 1 and resource_param.content_type = 1 limit 1000;'
        )

    def test_Videolist(self,video):
            url = self.baseurl + "/cms/v1.2/video"
            data = '{"os_type":1, ' \
                   '"app_version":"%(version)s", ' \
                   '"content_id":%(video_id)d, ' \
                   '"content_type":1,' \
                   '"timestamp":%(timeStamp)d,' \
                   '"app_key":"%(app_key)s"}' % {
                       'version': self.version,
                       'app_key': self.app_key,
                       'timeStamp': self.timeStamp,
                       'video_id': video["id"]}
            crypt_data = self.aes.encrypt(data, 'c_q')
            form = {"data": crypt_data, "encode": "v1"}
            response = requests.post(url=url, data=json.dumps(form), headers=self.headers)
            response_data = RunMain().decrypt_to_dict(response, 'r')
            msg = '上线剧集{0}的期望id是{1},实际id是{2}'.format(video["title"], video["id"], response_data["id"])
            self.assertEqual(video["id"], response_data["id"], msg=msg)

    @staticmethod
    def getTestFunc(video):
        def func(self):
            self.test_Videolist(video)

        return func


def __generateTestCases():
    video_list = test_Search_video().get_sql_list()
    for video in video_list:
        setattr(test_Search_video, 'test_func_%s' % (video["title"]),
                test_Search_video.getTestFunc(video))


__generateTestCases()

if __name__ == '__main__':
    unittest.main()
