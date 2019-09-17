# -*- coding:utf-8 -*-
#@Time  : 2019/9/17 16:48
#@Author: dongyani
#@Function: 生成所有直播台接口返回的数据
#数据格式：电视台名称（title）+接口返回的数据

from common.configHttp import RunMain
from readConfig import ReadConfig
from common.AES_CBC import AES_CBC
from common.getSign import get_Sign
from common.configMysql import OperationDbInterface
from datetime import datetime
import unittest, json, requests, time

baseurl = ReadConfig().get_http('baseurl')
version = ReadConfig().get_app('version')
app_key = ReadConfig().get_app('app_key')
ip = RunMain().get_host_ip()
db = "cms" if ip == "39.105.54.219" else "test"
mysql = OperationDbInterface(db)
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
        self.baseurl = ReadConfig().get_http("baseurl")
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
        content = stream["title"] + ": " + str(response_data) + "\n"
        fout = open('all_stream_response', 'a+', encoding='utf8')
        fout.write(content)
        fout.close()
        self.assertTrue(True, "生成所有直播台接口返回的数据")

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

# if __name__ == '__main__':
#     unittest.main()



