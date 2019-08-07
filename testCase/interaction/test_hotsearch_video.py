# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2019/8/5 16:32
# @Author: dongyani
# @interfacetest:
# 1.热搜列表 :/cms/v1.0/hotsearch/list
# 2.遍历热搜列表所有页签所有点播视频是否可以点播
# 3.播放此视频: /cms/v1.2/video

from common.configHttp import RunMain
from readConfig import ReadConfig
from common.md5_sms import timeStamp_md5
from common.AES_CBC import AES_CBC
from common.getSign import get_Sign
import unittest, json, requests

global false, true, null
baseurl = ReadConfig().get_http('baseurl')
version = ReadConfig().get_app('version')
app_key = ReadConfig().get_app('app_key')
md5 = timeStamp_md5()
aes = AES_CBC()


class test_hotsearch_video(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bookmark_dict = {"猜你想搜": "%E7%8C%9C%E4%BD%A0%E6%83%B3%E6%90%9C",
                              "电影": "CRI",
                              "新闻": "%E7%9F%AD%E8%A7%86%E9%A2%91",
                              "电视剧": "%E7%BB%BC%E8%89%BA",
                              "体育": "%E8%B4%A2%E7%BB%8F",
                              "短视频": "%E7%94%B5%E5%BD%B1",
                              "综艺": "%E6%96%B0%E9%97%BB",
                              "财经": "%E7%94%B5%E8%A7%86%E5%89%A7",
                              "动漫": "%E4%BD%93%E8%82%B2"
                              }

    def get_url_params(self, url, bookmark):
        # order_id 必填, 订单id
        data = '{"app_version":"%(version)s",' \
               '"category":"%(bookmark)s",' \
               '"os_type":1,' \
               '"order_id":116592,' \
               '"app_key":"%(app_key)s"' \
               '}' % {
                   'version': version,
                   'bookmark': bookmark,
                   'app_key': app_key}
        data = get_Sign().encrypt(data)
        return RunMain().get_url_params(data, url)

    def hotsearch_list(self, bookmark):
        """正确的请求参数"""
        url = baseurl + '/cms/v1.0/hotsearch/list'
        url = self.get_url_params(url, bookmark)
        headers = RunMain().headers_get()
        response = requests.get(url, headers=headers)
        hotsearch_list = list(response.json()['data'])
        return hotsearch_list

    def get_hotsearch_list_content(self, bookmark):
        hotsearch_list = self.hotsearch_list(bookmark)
        hotsearch_content = []
        for hotsearch in hotsearch_list:
            hotsearch_content.append({"content_id": hotsearch["content_id"],
                                      "content_type": hotsearch["content_type"],
                                      "title": hotsearch["title"]})
        return hotsearch_content

    def hotsearch_list_video(self, content, bookmark):
            data = '{"content_id": %(content_id)d, ' \
                   '"content_type": %(content_type)d, ' \
                   '"os_type": 1, ' \
                   '"app_version": "%(version)s", ' \
                   '"app_key":"%(app_key)s"}' % {
                       'content_id': content["content_id"],
                       'content_type': content["content_type"],
                       'version': version,
                       'app_key': app_key}
            crypt_data = aes.encrypt(data, 'c_q')
            form = {"data": crypt_data, "encode": "v1"}
            headers = RunMain().headers()
            url = baseurl + "/cms/v1.2/video"
            response = requests.post(url=url, data=json.dumps(form), headers=headers)
            msg = "搜索页面{0}页签的{1}视频无法点播".format(bookmark, content["title"])
            self.assertEqual(200, response.status_code, msg=msg)
            response_data = RunMain().decrypt_to_dict(response, 'r')
            self.assertEqual(content["content_id"], response_data['id'], msg=msg)

    @staticmethod
    def getTestFunc(content, bookmark):
        def func(self):
            self.hotsearch_list_video(content, bookmark)
        return func

def __generateTestCases():
    bookmark_dict = {"猜你想搜": "%E7%8C%9C%E4%BD%A0%E6%83%B3%E6%90%9C",
                     "电影": "%E7%94%B5%E5%BD%B1",
                     "新闻": "%E6%96%B0%E9%97%BB",
                     "电视剧": "%E7%94%B5%E8%A7%86%E5%89%A7",
                     "体育": "%E4%BD%93%E8%82%B2",
                     "CRI": "CRI",
                     "短视频": "%E7%9F%AD%E8%A7%86%E9%A2%91",
                     "综艺": "%E7%BB%BC%E8%89%BA",
                     "财经": "%E8%B4%A2%E7%BB%8F",
                     "动漫": "%E5%8A%A8%E6%BC%AB"
                     }
    for bookmark in list(bookmark_dict.keys()):
        hotsearch_content = test_hotsearch_video().get_hotsearch_list_content(bookmark_dict[bookmark])
        for content in hotsearch_content:
            setattr(test_hotsearch_video, 'test_func_%s_%s' % (bookmark, content["title"]),
                    test_hotsearch_video.getTestFunc(content, bookmark))

__generateTestCases()

if __name__ == '__main__':
    unittest.main()