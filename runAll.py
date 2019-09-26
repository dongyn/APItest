#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2019/5/27 16:57
# @Author: dongyani
# @File  : runAll.py

import unittest, time, os, readConfig, common.Log
import common.HTMLTestRunner_cn as HTMLTestRunner
from common.configEmail import send_email
from common.configHttp import RunMain

ip = RunMain().get_host_ip()
send_mail = send_email()
on_off = readConfig.ReadConfig().get_email('on_off')
retry = int(readConfig.ReadConfig().get_test('retry'))
log = common.Log.logger

# 这个是优化版执行所有用例并发送报告，分四个步骤
# 第一步加载用例
# 第二步执行用例
# 第三步获取最新测试报告
# 第四步发送邮箱 （这一步不想执行的话，可以注释掉最后面那个函数就行）

# 当前脚本所在文件真实路径
file_path = "//testCase" if ip == "39.105.54.219" else "\\testCase"
cur_path = os.path.dirname(os.path.realpath(__file__)) + file_path

def all_case():
    testcase = unittest.TestSuite()
    discover = unittest.defaultTestLoader.discover(cur_path, pattern="test*.py", top_level_dir=None)
    # discover方法筛选出来的用例，循环添加到测试套件中
    for test_suite in discover:
        for test_case in test_suite:
            # 添加用例到testcase
            # print(test_case)
            testcase.addTests(test_case)
    return testcase


def run_case(all_case, reportName="report"):
    '''第二步：执行所有的用例, 并把结果写入HTML测试报告'''
    now = time.strftime("%Y_%m_%d_%H_%M_%S")
    report_path = os.path.join(cur_path, reportName)  # 用例文件夹
    # 如果不存在这个report文件夹，就自动创建一个
    if not os.path.exists(report_path): os.mkdir(report_path)
    report_abspath = os.path.join(report_path, now + "result.html")
    print("report path:%s" % report_abspath)
    fp = open(report_abspath, "wb")
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp,
                                           title=u'自动化测试报告,测试结果如下：',
                                           description=u'用例执行情况：',
                                           verbosity=2,
                                           retry=retry)
    # 调用add_case函数返回值
    runner.run(all_case)
    fp.close()


def get_report_file(report_path):
    '''第三步：获取最新的测试报告'''
    lists = os.listdir(report_path)
    lists.sort(key=lambda fn: os.path.getmtime(os.path.join(report_path, fn)))
    print(u'最新测试生成的报告： ' + lists[-1])
    # 找到最新生成的报告文件
    report_file = os.path.join(report_path, lists[-1])
    return report_file


if __name__ == "__main__":
    all_case = all_case()  # 1加载用例
    # 生成测试报告的路径
    run_case(all_case)  # 2执行用例
    # 获取最新的测试报告文件
    report_path = os.path.join(cur_path, "report")  # 用例文件夹
    report_file = get_report_file(report_path)  # 3获取最新的测试报告
    # 判断邮件发送的开关
    if on_off == 'on':
        send_mail.tx_mial(report_file)  # 4发送邮件
    else:
        print("邮件发送开关配置关闭，请打开开关后可正常自动发送测试报告")
