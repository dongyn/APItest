# -*- coding:utf-8 -*-
#@Time  : 2019/7/24 16:01
#@Author: dongyani

from datetime import datetime
import time
import hashlib
import hmac

class get_Sign():
    def encrypt(self, resultParams):
        resultParams = eval(resultParams) if type(resultParams) == type("a") else resultParams
        if "timestamp" in list(resultParams.keys()):
            timeStamp = resultParams["timestamp"]
        else:
            # 转为时间戳
            timeStamp = int(time.mktime(datetime.now().timetuple()))
            dict_timeStamp = {"timestamp":timeStamp}
            # 把时间戳字典加到参数列表中
            resultParams.update(dict_timeStamp)

        secrte = ((timeStamp << (timeStamp % 64)) & (0x7fffffffffffffff)) | (timeStamp >> (64 - (timeStamp % 64))) #int
        results = ""
        sort_key = sorted(list(resultParams.keys()))
        for key in sort_key:
            format_param = results + key + "=" + str(resultParams[key])
            results = format_param if key == sort_key[-1] else format_param + "&"

        #hmac加密参数列表：key: 时间戳的位移运算值，msg:参数列表keys排序后的拼接字符串，加密后转大写
        sign_hmac = hmac.new(str(secrte).encode(), results.encode(), hashlib.sha1).hexdigest().upper()
        dict_sign = {"sign": sign_hmac}
        #把sign添加到参数列表中
        resultParams.update(dict_sign)
        print(resultParams)
        return resultParams

if __name__ == "__main__":
    a = "a"
    b = "b"
    print(type(a) == type(b))
    # str_dict = {"device_id":"40439d078e887033","os_version":"8.1.0","app_version":"8.0.6","gcid":"63b9d926f335078d837240764f120aa7","country_code":"+86","channel":"vivo","open_id":"18192873108","os_type":1,"imei":"A000008D9CEF1C","bssid":"02:00:00:00:00:00","access_token":"907303","timestamp":1563950104,"installation_id":1901231425555756,"app_key":"xdThhy2239daax","mac_address":"02:00:00:00:00:00","provider":1 }
    # encrypt(str_dict)

