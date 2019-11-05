#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2019/5/27 16:52
# @Author: dongyani
# @File  : configHttp.py
"""
这个文件主要来通过get、post、put、delete等方法来进行http请求，并拿到请求响应。
"""

from readConfig import ReadConfig
from common.AES_CBC import AES_CBC
from common.Log import logger
from common.md5_sms import timeStamp_md5
from datetime import datetime
from common.getSign import get_Sign
import common.url as url
import json, requests, time

logger = logger
version = ReadConfig().get_app('version')
app_key = ReadConfig().get_app('app_key')
telephone = ReadConfig().get_app('telephone')
baseurl = url.baseurl()
host = url.host()
md5 = timeStamp_md5()
global false, null, true
aes = AES_CBC()


class RunMain():

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timeStamp = int(time.mktime(datetime.now().timetuple()))
        self.access_token = md5.encrypt_md5(self.timeStamp)

    def get_url_params(self, params, url):
        """
        :param params: type: dict, 要拼接到url后面的所有参数
        :param url: type: str, http问号之前的那部分url地址
        :return: type:str, 拼接后的完整的url
        """
        results = ""
        if type(params) == type('a'): params = eval(params)
        keys = list(params.keys())
        for key in keys:
            format_param = results + key + "=" + str(params[key])
            results = format_param if key == keys[-1] else format_param + "&"
        url = url + '?' + results
        return url

    def headers(self):
        headers = {'Content-Type': 'application/json;charset=UTF-8',
                   'Content-Length': '732',
                   'Host': host,
                   'Accept-Encoding': 'gzip'
                   }
        return headers

    def headers_get(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 9; COL-AL10 Build/HUAWEICOL-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/72.0.3626.121 Mobile Safari/537.36",
            "Host": host,
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip"
            }
        return headers

    def shield_headers(self,city_ip):
        headers = {"Content-Type": "application/json;charset=UTF-8",
                       "User-Agent": "Mozilla/5.0 (Linux; Android 9; COL-AL10 Build/HUAWEICOL-AL10; wv) "
                                     "AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/72.0.3626.121 Mobile Safari/537.36",
                       "Host": host,
                       "Connection": "Keep-Alive",
                       "Accept-Encoding": "gzip",
                       'X-Forwarded-For': city_ip
                        }
        return headers

    # 将解密后的字符串转为字典
    def decrypt_to_dict(self, text, key_type):
        r_data = text.json()['data']
        str_decrypt = aes.decrypt(r_data, key_type)
        global false, null, true
        null = ""
        false = False
        true = True
        response_data = eval(str_decrypt)
        return response_data

    def send_post(self, url, data):  # 定义一个方法，传入需要的参数url和data
        # 参数必须按照url、data顺序传入
        result = requests.post(url=url, data=data).json()  # 因为这里要封装post方法，所以这里的url和data值不能写死
        res = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2)
        return res

    def send_get(self, url, data):
        result = requests.get(url=url, data=data)
        res = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2)
        return res

    def login(self, timeStamp):
        '''获取登录接口的token'''
        url = baseurl + '/ims/v1.0/user/login'
        data = '{"app_version":"%(version)s",' \
               '"access_token":"%(access_token)s",' \
               '"os_type":1,' \
               '"timestamp":%(timeStamp)d,' \
               '"open_id":"%(telephone)s",' \
               '"provider":1,' \
               '"app_key":"%(app_key)s",' \
               '"device_id":"802ca0fba119ab0a",' \
               '"country_code":"+86",' \
               '"installation_id":1904301718321742,' \
               '"longitude":108.90823353286173,' \
               '"latitude":34.21936825217505,' \
               '}' % {
                   'version': version,
                   'app_key': app_key,
                   'access_token': self.access_token,
                   'timeStamp': timeStamp,
                   'telephone': telephone}
        data = get_Sign().encrypt(data)
        response = requests.post(url, data=json.dumps(data), headers=self.headers())
        return response

    def get_login_token(self, timeStamp):
        response = self.login(timeStamp)
        while response.status_code != 200: response = self.login(timeStamp)
        return response.json()['data']['token']

    def headers_token(self, timeStamp):
        headers = {'Content-Type': 'application/json;charset=UTF-8',
                   'Content-Length': '732',
                   'Host': host,
                   'Accept-Encoding': 'gzip',
                   'Authorization': self.get_login_token(timeStamp=timeStamp)
                   }
        return headers

    def headers_get_token(self, timeStamp):
        headers = {"Host": host,
                   "Connection": "Keep-Alive",
                   "Accept-Encoding": "gzip",
                   "Authorization": self.get_login_token(timeStamp=timeStamp)
                   }
        return headers

    def run_main(self, method, url=None, data=None):  # 定义一个run_main函数，通过传过来的method来进行不同的get或post请求
        result = None
        if method == 'post':
            result = self.send_post(url, data)
            assert isinstance(logger, object)
            logger.info(str(result))
        elif method == 'get':
            result = self.send_get(url, data)
            logger.info(str(result))
        else:
            print("method值错误！！！")
            logger.info("method值错误！！！")
        return result

# if __name__ == '__main__':#通过写死参数，来验证我们写的请求是否正确
#     result = RunMain().run_main('post', '', 'name=xiaoming&pwd=')
#     print(result)
