# -*- coding:utf-8 -*-
#@Time  : 2019/7/10 10:23
#@Author: dongyani

"""
AES加密解密工具类
@author jzx
@date   2018/10/24
此工具类加密解密结果与 http://tool.chacuo.net/cryptaes 结果一致
数据块128位
key 为16位
iv 为16位，且与key相等
字符集utf-8
输出为base64
AES加密模式 为cbc
填充 pkcs7padding
"""

import base64
from Crypto.Cipher import AES
import common.url as url
from readConfig import ReadConfig
from common.getSign import get_Sign
from datetime import datetime
import requests, json, time

global false, null, true

baseurl = url.baseurl()
host = url.host()
version = ReadConfig().get_app("version")
config_request_key = ReadConfig().get_app("config_request")
app_key = ReadConfig().get_app("app_key")
app_scret_key = ReadConfig().get_app("app_scret_key")

class AES_CBC():
    def __init__(self):
        # self.key_config_request = 'CiZa4fDec10jzgHC'.encode("utf-8")
        # self.key_config_response = "xdThhy2239daaxc0".encode("utf-8")
        # key_response就是app_scret_key，变更新版本时，运行一下get_app_scret_key就可以了
        #UnicodeDecodeError: 'utf-8' codec can't decode byte 0xc1 in position 1: invalid start byte
        # 上面这个报错是key_response和版本不匹配造成的！！！！
        # self.key_response = 'FD6BBB4C750E7EAB'.encode("utf-8")
        self.mode = AES.MODE_CBC
        self.iv = 'q@7m*d3e4pk5c3wd'.encode("utf-8")
        self.url = baseurl + "/cms/v1.2/config"
        self.headers = {'Content-Type': 'application/json;charset=UTF-8',
                        'Content-Length': '732',
                        'Host': host,
                        'Accept-Encoding': 'gzip'
                        }

    def get_app_scret_key(self):
        timeStamp = int(time.mktime(datetime.now().timetuple()))
        # 以下参数包括sign是必传的，总共有八个参数
        data = '{"os_type": 1,' \
               '"app_key":"xdThhy2239daax",' \
               '"os_version":"9",' \
               '"mac_address":"02:00:00:00:00:00",' \
               '"device_id":"802ca0fba119ab0a",' \
               '"app_version":"%(version)s",' \
               '"timeStamp":%(timeStamp)d}' % {
                   'timeStamp': timeStamp,
                   'version': version}
        sign = get_Sign().encrypt(data, True)["sign"]
        data = data.replace('}', ',"sign":"%s"}' % sign)
        crypt_data = self.encrypt(data, 'c_q')
        form = {"data": crypt_data, "encode": "v1"}
        response = requests.post(url = self.url, data = json.dumps(form), headers = self.headers)
        print(response.status_code)
        r_data = response.json()['data']
        str_decrypt = self.decrypt(r_data, 'c_p')
        global false, null, true
        false = null = true = ""
        response_data = eval(str_decrypt)
        app_scret_key = response_data["setting"]["app_scret_key"][0:16]
        return app_scret_key

    def get_key(self, type):
        if type == 'c_q':
            return config_request_key.encode("utf-8")
        elif type == 'c_p':
            config_response_key = app_key + "c0"
            return config_response_key.encode("utf-8")
        else:
            return app_scret_key.encode("utf-8")


    def pkcs7padding(self, text):
        """
        明文使用PKCS7填充
        最终调用AES加密方法时，传入的是一个byte数组，要求是16的整数倍，因此需要对明文进行处理
        :param text: 待加密内容(明文)
        :return:
        """
        bs = AES.block_size  # 16
        length = len(text)
        bytes_length = len(bytes(text, encoding='utf-8'))
        # tips：utf-8编码时，英文占1个byte，而中文占3个byte
        padding_size = length if(bytes_length == length) else bytes_length
        padding = bs - padding_size % bs
        # tips：chr(padding)看与其它语言的约定，有的会使用'\0'
        padding_text = chr(padding) * padding
        return text + padding_text


    def pkcs7unpadding(self, text):
        """
        处理使用PKCS7填充过的数据
        :param text: 解密后的字符串
        :return:
        """
        length = len(text)
        unpadding = ord(text[length-1])
        return text[0:length-unpadding]


    def encrypt(self, content, type):
        """
        AES加密
        key,iv使用同一个
        模式cbc
        填充pkcs7
        :param key: 密钥
        :param content: 加密内容
        :return:
        """
        key = self.get_key(type)
        cipher = AES.new(key, self.mode, self.iv)
        # 处理明文
        content_padding = self.pkcs7padding(content)
        # 加密
        encrypt_bytes = cipher.encrypt(bytes(content_padding, encoding='utf-8'))
        # 重新编码
        result = str(base64.b64encode(encrypt_bytes), encoding='utf-8')
        return result


    def decrypt(self, content, type):
        """
        AES解密
         key,iv使用同一个
        模式cbc
        去填充pkcs7
        :param key:
        :param content:
        :return:
        """
        key = self.get_key(type)
        cipher = AES.new(key, self.mode, self.iv)
        # base64解码
        encrypt_bytes = base64.b64decode(content)
        # 解密
        decrypt_bytes = cipher.decrypt(encrypt_bytes)
        # 重新编码
        result = str(decrypt_bytes, encoding='utf-8')
        # 去除填充内容
        result = self.pkcs7unpadding(result)
        return str(result)

if __name__ == '__main__':
    aes = AES_CBC()
    key = aes.get_app_scret_key()
    print(key)
    # # 刚好16字节的情况
    # en_16 = 'abcdefgj10124567'
    # encrypt_en = aes.encrypt(en_16, 'r')
    # print(encrypt_en)
    # 解密
    # key = aes.get_app_scret_key()
    # print(key)
    # encrypt_en = ''
    # decrypt_en = aes.decrypt(encrypt_en, 'c_r')
    # print(decrypt_en)
    # print(en_16 == decrypt_en)
    # mix_16 = 'abx张三丰12sa'
    # encrypt_mixed = aes.encrypt(mix_16, 'r')
    # print(encrypt_mixed)
    # decrypt_mixed = aes.decrypt(encrypt_mixed, 'r')
    # print(decrypt_mixed)
    # print(decrypt_mixed == mix_16)

