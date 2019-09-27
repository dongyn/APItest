# -*- coding:utf-8 -*-
#@Time  : 2019/9/26 13:32
#@Author: dongyani
#@Function: 获取本机ip、url和host

import socket

def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

def baseurl():
    ip = get_host_ip()
    url = "http://test.ams.starschina.com" if ip[0:7]== "192.168" else "https://apiv1.starschina.com"
    return url

def host():
    ip = get_host_ip()
    host = 'test.ams.starschina.com' if ip[0:7]== "192.168" else 'apiv1.starschina.com'
    return host

# print(get_host_ip())