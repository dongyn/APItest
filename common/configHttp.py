#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Time  : 2019/5/27 16:52
#@Author: dongyani 
#@File  : configHttp.py
"""
这个文件主要来通过get、post、put、delete等方法来进行http请求，并拿到请求响应。
"""

import requests
import json
from common.AES_CBC import AES_CBC
from common.Log import logger

logger = logger
global false, null, true
aes = AES_CBC()
class RunMain():

    def headers(self):
        self.headers = {'Content-Type': 'application/json;charset=UTF-8',
                        'Content-Length': '732',
                        # 'Host': 'test.ams.starschina.com',
                        'Host': 'apiv1.starschina.com',
                        'Accept-Encoding': 'gzip'
                        }
        return self.headers

    # 将解密后的字符串转为字典
    def decrypt_to_dict(self, text, key_type):
        r_data = text.json()['data']
        str_decrypt = aes.decrypt(r_data, key_type)
        global false, null, true
        false = null = true = ""
        response_data = eval(str_decrypt)
        return response_data

    def send_post(self, url, data):# 定义一个方法，传入需要的参数url和data
        # 参数必须按照url、data顺序传入
        result = requests.post(url=url, data=data).json()# 因为这里要封装post方法，所以这里的url和data值不能写死
        res = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2)
        return res

    def send_get(self, url, data):
        result = requests.get(url=url, data=data)
        res = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2)
        return res

    def run_main(self, method, url=None, data=None):#定义一个run_main函数，通过传过来的method来进行不同的get或post请求
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

if __name__ == '__main__':#通过写死参数，来验证我们写的请求是否正确
    result = RunMain().run_main('post', 'http://127.0.0.1:8888/login', 'name=xiaoming&pwd=')
    print(result)