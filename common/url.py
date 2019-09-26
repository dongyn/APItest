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
    url = "https://apiv1.starschina.com" if ip == "39.105.54.219" else "http://test.ams.starschina.com"
    return url

def host():
    ip = get_host_ip()
    host = 'apiv1.starschina.com' if ip == "39.105.54.219" else 'test.ams.starschina.com'
    return host