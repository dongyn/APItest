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
import requests,json
from readConfig import ReadConfig
global false, null, true

baseurl = ReadConfig().get_http("baseurl")
version = ReadConfig().get_app("version")
app_key = ReadConfig().get_app("app_key")

class AES_CBC():
    def __init__(self):
        self.key_config_request = 'CiZa4fDec10jzgHC'.encode("utf-8")
        self.key_config_response = "xdThhy2239daaxc0".encode("utf-8")
        # key_response就是app_scret_key，变更新版本时，运行一下get_app_scret_key就可以了
        self.key_response = '39F03D73105EC77D'.encode("utf-8")
        self.mode = AES.MODE_CBC
        self.iv = 'q@7m*d3e4pk5c3wd'.encode("utf-8")
        self.url = baseurl + "/cms/v1.2/config"
        self.headers = {'Content-Type': 'application/json;charset=UTF-8',
                        'Content-Length': '732',
                        'Host': 'apiv1.starschina.com',
                        'Accept-Encoding': 'gzip'
                        }

    def get_app_scret_key(self):
        data = '{"mac_address":"02:00:00:00:00:00","device_id":"802ca0fba119ab0a","os_type": 1,"app_key":"xdThhy2239daax","app_version":"%(version)s","os_version":"9"}'% {'version':version}
        crypt_data = self.encrypt(data, 'c_q')
        form = {"data":crypt_data,"encode":"v1"}
        response = requests.post(url = self.url, data = json.dumps(form), headers = self.headers)
        r_data = response.json()['data']
        str_decrypt = str(aes.decrypt(r_data, 'c_p'))
        global false, null, true
        false = null = true = ""
        response_data = eval(str_decrypt)
        app_scret_key = response_data["setting"]["app_scret_key"][0:16]
        return app_scret_key

    def get_key(self, type):
        """
        获取密钥 n 密钥长度
        :return:
        """
        key = ""
        if type == 'c_q':
            key = self.key_config_request
        elif type == 'c_p':
            key = self.key_config_response
        else:
            key = self.key_response
        return key


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
        return result

if __name__ == '__main__':
    aes = AES_CBC()
    # # 刚好16字节的情况
    # en_16 = 'abcdefgj10124567'
    # encrypt_en = aes.encrypt(en_16, 'r')
    # print(encrypt_en)
    # 解密
    encrypt_en = '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'
    decrypt_en = aes.decrypt(encrypt_en, 'r')
    print(decrypt_en)
    # print(en_16 == decrypt_en)
    # mix_16 = 'abx张三丰12sa'
    # encrypt_mixed = aes.encrypt(mix_16, 'r')
    # print(encrypt_mixed)
    # decrypt_mixed = aes.decrypt(encrypt_mixed, 'r')
    # print(decrypt_mixed)
    # print(decrypt_mixed == mix_16)
    '''
    # Test
    # 非16字节的情况
    # aes_key = get_key(16)
    # print('aes_key:' + aes_key)
    # 对英文加密
    source_en = 'Hello!'
    encrypt_en = aes.encrypt('r', source_en)
    print(encrypt_en)
    # 解密
    decrypt_en = aes.decrypt('r', encrypt_en)
    print(decrypt_en)
    print(source_en == decrypt_en)
    # 中英文混合加密
    source_mixed = 'Hello, 韩- 梅 -梅'
    encrypt_mixed = aes.encrypt('r', source_mixed)
    print(encrypt_mixed)
    decrypt_mixed = aes.decrypt('r', encrypt_mixed)
    print(decrypt_mixed)
    print(decrypt_mixed == source_mixed)
'''

