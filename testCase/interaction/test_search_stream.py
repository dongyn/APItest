# -*- coding:utf-8 -*-
#@Time  : 2019/8/5 16:25
#@Author: pengjuan
#interfacetest:
#1. 打开应用
#2. 搜索直播视频名称
#3. 进行播放


from common.configHttp import RunMain
from readConfig import ReadConfig
from common.AES_CBC import AES_CBC
from common.getSign import get_Sign
from common.configMysql import OperationDbInterface
from datetime import datetime
import common.url as url
import unittest, json, requests, time

version = ReadConfig().get_app('version')
app_key = ReadConfig().get_app('app_key')
mysql = OperationDbInterface()
aes = AES_CBC()

class test_search_stream(unittest.TestCase):
    """
    1. 打开应用
    2. 搜索直播视频名称
    3. 进行播放
    """
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.headers = RunMain().headers()
        self.baseurl = url.baseurl()
        self.version = ReadConfig().get_app("version")
        self.app_key = ReadConfig().get_app("app_key")
        self.aes = AES_CBC()

    def get_sql_list(self):
        """查询数据库，循环取值"""
        return mysql.select_all(
            'select stream.id, stream.title from cms.stream LEFT JOIN cms.resource_param on '
            'stream.id = resource_param.content_id '
            'where resource_param.online = 1 and resource_param.app_id = 1 and resource_param.content_type = 4;')

    def Viewlivestreamdetails(self, stream):
        url = self.baseurl + "/cms/v1.2/stream"
        timeStamp = int(time.mktime(datetime.now().timetuple()))
        data = '{"os_type":1, ' \
               '"app_version":"%(version)s", ' \
               '"id":%(stream_id)d, ' \
               '"timestamp":%(timeStamp)d,' \
               '"app_key":"%(app_key)s"}' % {
                   'version': self.version,
                   'app_key': self.app_key,
                   'timeStamp': timeStamp,
                   'stream_id': stream["id"]}
        sign = get_Sign().encrypt(data, True)["sign"]
        data = data.replace('}', ',"sign":"%s"}' % sign)
        crypt_data = self.aes.encrypt(data, 'c_q')
        form = {"data": crypt_data, "encode": "v1"}
        response = requests.post(url=url, data=json.dumps(form), headers=self.headers)
        response_data = RunMain().decrypt_to_dict(response, 'r')
        msg = "直播接口返回的电视台名称应该是{0}实际是{1}".format(stream["title"], response_data["title"])
        self.assertEqual(stream["title"], response_data["title"], msg=msg)

    @staticmethod
    def getTestFunc(stream):
        def func(self):
            self.Viewlivestreamdetails(stream)
        return func

def __generateTestCases():
    stream_list = test_search_stream().get_sql_list()
    for stream in stream_list:
        setattr(test_search_stream, 'test_stream_%s' % (stream["title"]),
                test_search_stream.getTestFunc(stream))

__generateTestCases()




