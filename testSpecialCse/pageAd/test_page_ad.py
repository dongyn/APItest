# -*- coding:utf-8 -*-
# @Time  : 2019/7/10 10:23
# @Author: pengjuan
# @interfacetest: http://apiv1.starschina.com/cms/v1.2/page

from common.configHttp import RunMain
from readConfig import ReadConfig
from common.getSign import get_Sign
from common.AES_CBC import AES_CBC
import common.url as url
import requests, unittest, json, time, datetime

baseurl = url.baseurl()
version = ReadConfig().get_app('version')
app_key = ReadConfig().get_app('app_key')
aes = AES_CBC()
headers = RunMain().headers()

class test_Page_ad(unittest.TestCase):
    """测试页面加载接口"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = baseurl + "/cms/v1.2/page"
        self.none_ad_page = ["70年", "财经", "知宿"]

    def get_pages_info(self):
        # id需要在config接口中返回
        timeStamp = int(time.mktime(datetime.datetime.now().timetuple()))
        data = '{"os_type": 1,' \
               '"app_key":"%(app_key)s",' \
               '"os_version":"9",' \
               '"carrier":3,' \
               '"mac_address":"02:00:00:00:00:00",' \
               '"device_id":"802ca0fba119ab0a",' \
               '"imei":"869384032108431",' \
               '"latitude":34.223866,' \
               '"gcid":"dba9f3c2e8926564d3c930790c232bcf",' \
               '"bssid":"4c:e9:e4:7d:41:c1",' \
               '"longitude":108.909907,' \
               '"installation_id":1904301718321742,' \
               '"force_reload_user":true,' \
               '"app_version":"%(version)s",' \
               '"timeStamp":%(timeStamp)d}' % {
                   'app_key': app_key,
                   'timeStamp': timeStamp,
                   'version': version}
        sign = get_Sign().encrypt(data, True)["sign"]
        data = data.replace('}', ',"sign":"%s"}' % sign)
        crypt_data = aes.encrypt(data, 'c_q')
        form = {"data": crypt_data, "encode": "v1"}
        response = requests.post(url=baseurl + "/cms/v1.2/config", data=json.dumps(form), headers=headers)
        return RunMain().decrypt_to_dict(response, 'c_p')['pages']

    def page_sections(self, page_id, pagename):
        """测试page接口是否刷新出广告"""
        timeStamp = int(time.mktime(datetime.datetime.now().timetuple()))
        data = '{"id": [%(page_id)d], "os_type":1,' \
               '"app_version":"%(version)s",' \
               '"timestamp":%(timeStamp)d,' \
               '"page_alias":"",'\
               '"installation_id":1901231425555756,'\
               '"device_id":"40439d078e887033",'\
               '"os_version":"8.1.0",'\
               '"channel":"dopool",'\
               '"app_key": "%(app_key)s"}' % {
                   'version': version,
                   'timeStamp': timeStamp,
                   'app_key': app_key,
                   'page_id' : page_id}
        sign = get_Sign().encrypt(data, True)["sign"]
        data = data.replace('}', ',"sign":"%s"}' % sign)
        crypt_data = aes.encrypt(data, 'c_q')
        form = {'data': crypt_data, 'encode': 'v1'}
        response = requests.post(self.url, data=json.dumps(form), headers=headers)
        page_sections = RunMain().decrypt_to_dict(response, 'r')[0]["sections"]
        print(pagename)
        for i, section in enumerate(page_sections):
            if 'ad_feeds' in section.keys():
                ad_feeds = section['ad_feeds'] if type(section['ad_feeds']) == type([]) else [section['ad_feeds']]
                self.assertTrue(ad_feeds[0]['id'] != 0, f'{pagename}页面{section["name"]}分组没有刷新出广告')
                return
            if i == len(page_sections) - 1:
                if 'ad_feeds' not in section.keys():
                    self.assertTrue(False, f'{pagename}页面没有刷新出广告')


    @staticmethod
    def getTestFunc(page_id, pagename):
        def func(self):
            self.page_sections(page_id, pagename)
        return func

def __generateTestCases():
    pages_info = test_Page_ad().get_pages_info()
    for pages in pages_info:
        if pages["name"] in ["首页", "直播"]:
            for page in pages["pages"]:
                if page["name"] not in test_Page_ad().none_ad_page:
                    setattr(test_Page_ad, 'test_page_ad_%s' % (page["name"]),
                            test_Page_ad.getTestFunc(page["id"], page["name"]))

__generateTestCases()


