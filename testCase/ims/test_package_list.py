# -*- coding:utf-8 -*-
#@Time  : 2019/7/30 10:22
#@Author: dongyn
#@interfacetest: http://apiv1.starschina.com/ims/v1.0/package/list


from requests_toolbelt import MultipartEncoder
from common.configHttp import RunMain
from common.getSign import get_Sign
from common.md5_sms import timeStamp_md5
from readConfig import ReadConfig
from datetime import datetime
from requests.cookies import RequestsCookieJar
import requests, unittest, json, time, os, uuid

global false, true, null
baseurl = ReadConfig().get_http('baseurl')
version = ReadConfig().get_app('version')
app_key = ReadConfig().get_app('app_key')
md5 = timeStamp_md5()
headers = RunMain().headers_get()
class test_Packagelist(unittest.TestCase):
    '''获取套餐列表接口'''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = baseurl + '/ims/v1.0/package/list'

    def get_url_params(self):
        timeStamp = int(time.mktime(datetime.now().timetuple()))
        url_params = '{"app_version":"%(version)s",' \
                     '"app_key":"%(app_key)s", ' \
                     '"os_type":1,' \
                     '"timestamp":%(timeStamp)d,' \
                     '"installation_id": 1904301718321742,' \
                     '"os_version": "9",' \
                     '"latitude": 34.230261,' \
                     '"mac_address": "02:00:00:00:00:00",' \
                     '"longitude": 108.872503,' \
                     '"device_id": "802ca0fba119ab0a"}' % {
                         'version': version,
                         'app_key': app_key,
                         'timeStamp': timeStamp}
        params = get_Sign().encrypt(url_params)
        return RunMain().get_url_params(params, self.url)

    def test_packagelist_01(self):
        '''正确的参数'''
        timeStamp_login = int(time.mktime(datetime.now().timetuple()))
        token = RunMain().get_login_token(timeStamp_login)
        headers['Cookie'] = 'sessionid=%s' %token
        url = self.get_url_params()
        response = requests.get(url=url, headers=headers)
        assert int(response.json()['count']) >= 1

    def test_packagelist_02(self):
        '''参数为空'''
        response = requests.get(self.url,headers=headers)
        assert response.status_code == 403



# if __name__ == '__main__':
#     test_Upload().test_upload_01()