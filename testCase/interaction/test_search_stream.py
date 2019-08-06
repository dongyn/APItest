# -*- coding:utf-8 -*-
#@Time  : 2019/8/5 16:25
#@Author: pengjuan
#interfacetest:
#1. 打开应用
#2. 搜索直播视频名称
#3. 进行播放


import unittest
import requests, json
from common.AES_CBC import AES_CBC
from common.configMysql import OperationDbInterface
from readConfig import ReadConfig
from common.configHttp import RunMain


global true, null, false

class test_search_stream(unittest.TestCase):
    """
    1. 打开应用
    2. 搜索直播视频名称
    3. 进行播放
    """
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.headers = RunMain().headers()
        self.baseurl = ReadConfig().get_http("baseurl")
        self.version = ReadConfig().get_app("version")
        self.app_key = ReadConfig().get_app("app_key")
        self.mysql = OperationDbInterface()
        self.aes = AES_CBC()

    def get_sql_list(self):
        """查询数据库，循环取值"""
        return self.mysql.select_all(
            'select stream.id, stream.title from stream LEFT JOIN resource_param on stream.id = resource_param.content_id '
            'where resource_param.online = 1 and resource_param.app_id = 1 and resource_param.content_type = 4;')

    def test_Viewlivestreamdetails(self):
        stream_list = self.get_sql_list()
        for stream in stream_list:
            # for id in list(stream_list.)
            url = self.baseurl + "/cms/v1.2/stream"
            data = '{"os_type":1, ' \
                   '"app_version":"%(version)s", ' \
                   '"id":%(stream_id)d, ' \
                   '"app_key":"%(app_key)s"}' % {
                'version': self.version,
                'app_key': self.app_key,
                'stream_id': stream["id"]}
            crypt_data = self.aes.encrypt(data, 'c_q')
            form = {"data": crypt_data, "encode": "v1"}
            response = requests.post(url=url, data=json.dumps(form), headers=self.headers)
            response_data = RunMain().decrypt_to_dict(response, 'r')
            msg = "直播接口返回的电视台名称应该是{0}实际是{1}".format(stream["title"], response_data["title"])
            self.assertEqual(stream["title"], response_data["title"], msg=msg)


# if __name__ == "__main__":
#     test_search_stream().get_sql_list()



