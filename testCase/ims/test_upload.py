# -*- coding:utf-8 -*-
#@Time  : 2019/7/30 10:22
#@Author: pengjuan
#@interfacetest: http://apiv1.starschina.com/ims/v1.0/upload


from requests_toolbelt import MultipartEncoder
from common.configHttp import RunMain
from common.getSign import get_Sign
from common.md5_sms import timeStamp_md5
from readConfig import ReadConfig
from datetime import datetime
import requests, unittest, json, time, os, uuid

global false, true, null
baseurl = ReadConfig().get_http('baseurl')
version = ReadConfig().get_app('version')
app_key = ReadConfig().get_app('app_key')
md5 = timeStamp_md5()

class test_Upload(unittest.TestCase):
    '''用户上传头像接口'''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = baseurl + '/ims/v1.0/upload'
        self.timeStamp = int(time.mktime(datetime.now().timetuple()))
        self.access_token = md5.encrypt_md5(self.timeStamp)
        self.boundary = '--'+ str(uuid.uuid1())
        self.file = os.path.abspath(os.path.join(os.getcwd(), "../..")) + '\\files\\Avatar.png'

    def get_url_params(self):
        timeStamp = int(time.mktime(datetime.now().timetuple()))
        url_params = '{"app_version":"%(version)s",' \
                     '"app_key":"%(app_key)s", ' \
                     '"os_type":1,' \
                     '"id":[111],' \
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

    def test_upload_01(self):
        '''正确的参数'''
        timeStamp_login = int(time.mktime(datetime.now().timetuple()))
        headers = RunMain().headers_token(timeStamp_login)
        params = '{"Content-Disposition": "form-data",' \
                 '"name":"file",' \
                 '"filename":"blob.png",' \
                 '"Content-Type":"image/png",' \
                 '"Content-Length": 6569}'
        m = MultipartEncoder(fields={params : json.dumps(params),'file': ('file', open(self.file, 'rb'), 'application/octet-stream')}, boundary=self.boundary)
        headers['Content-Type'] = m.content_type
        response = requests.post(self.get_url_params(),
                                 data=m,
                                 headers=headers)
        if response.status_code == 200:
            assert response.json()["err_code"] == 0
        else:
            print("接口%s请求失败" % self.url)

    def test_upload_02(self):
        '''参数为空'''
        timeStamp_login = int(time.mktime(datetime.now().timetuple()))
        headers = RunMain().headers_token(timeStamp_login)
        params = '{"Content-Disposition": "form-data",' \
                 '"name":"file",' \
                 '"filename":"blob.png",' \ 
                 '"Content-Type":"image/png",' \
                 '"Content-Length": 6569}'
        m = MultipartEncoder(fields={params : json.dumps(params),'file': ('file', open(self.file, 'rb'), 'application/octet-stream')}, boundary=self.boundary)
        headers['Content-Type'] = m.content_type
        response = requests.post(self.url,
                                 data=m,
                                 headers=headers)
        assert response.status_code == 403



if __name__ == '__main__':
    test_Upload().test_upload_01()