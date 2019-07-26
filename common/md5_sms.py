# -*- coding:utf-8 -*-
#@Time  : 2019/7/12 18:12
#@Author: pengjuan
"""
t=时间戳，秒
t=(t/300)*300
acccessKey = "edeac39d37f25c04020b9e6aa4802965500c26ea"
 sum=md5(t+acccessKey +t)
取sum 前6位做验证码
"""

import hashlib
class timeStamp_md5():

    def encrypt_md5(self, timeStamp):
        timestr = str(int(int(timeStamp / 300) * 300))
        key = "edeac39d37f25c04020b9e6aa4802965500c26ea"
        sum_time = timestr + key + timestr
        md5_str = hashlib.md5(sum_time.encode()).hexdigest()[0:6]
        return md5_str

# 调用
if __name__ == '__main__':
    # c0d1bc
    print(timeStamp_md5().encrypt_md5())