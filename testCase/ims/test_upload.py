# -*- coding:utf-8 -*-
#@Time  : 2019/7/30 10:22
#@Author: pengjuan
#@interfacetest: http://apiv1.starschina.com/ims/v1.0/upload


from requests_toolbelt import MultipartEncoder
from common.configHttp import RunMain
from common.getSign import get_Sign
from readConfig import ReadConfig
from datetime import datetime
import common.url as url
import requests, unittest, json, time, os, uuid

baseurl = url.baseurl()
version = ReadConfig().get_app('version')
app_key = ReadConfig().get_app('app_key')

class test_Upload(unittest.TestCase):
    '''用户上传头像接口'''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = baseurl + '/ims/v1.0/upload'
        self.boundary = '--'+ str(uuid.uuid1())
        self.file = os.path.join(os.path.abspath(os.path.join(os.getcwd(), "../../..")),'API-Test', 'files', 'Avatar.png')

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
        params = '{"Content-Disposition": "form-data","name":"file","filename":"blob.png","Content-Type":"image/png","Content-Length": 6569}'
        m = MultipartEncoder(fields={params : json.dumps(params),
                                     'file': ('file', open(self.file, 'rb'),
                                              'application/octet-stream')},
                             boundary=self.boundary)
        headers['Content-Type'] = m.content_type
        response = requests.post(self.get_url_params(),
                                 data=m,
                                 headers=headers)
        assert response.json()["err_code"] == 0

    def test_upload_02(self):
        """参数为空"""
        timeStamp_login = int(time.mktime(datetime.now().timetuple()))
        headers = RunMain().headers_token(timeStamp_login)
        params = '{"Content-Disposition": "form-data","name":"file","filename":"blob.png","Content-Type":"image/png","Content-Length": 6569}'
        m = MultipartEncoder(fields={params : json.dumps(params),
                                     'file': ('file', open(self.file, 'rb'),
                                              'application/octet-stream')},
                             boundary=self.boundary)
        headers['Content-Type'] = m.content_type
        response = requests.post(self.url,
                                 data=m,
                                 headers=headers)
        assert response.status_code == 403


# if __name__ == '__main__':
    # test_Upload().test_upload_01()
    # a = os.path.abspath(os.path.join(os.getcwd(), "../..")).join('files','Avatar.png')
    # print(a)
