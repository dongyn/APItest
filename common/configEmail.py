#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Time  : 2019/5/27 16:52
#@Author: dongyani 
#@File  : configEmail.py
"""
这个文件主要是配置发送邮件的主题、正文等，将测试报告发送并抄送到相关人邮箱的逻辑。
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import readConfig
read_conf = readConfig.ReadConfig()
sender = read_conf.get_email('sender')
psw = read_conf.get_email('psw')
receiver = read_conf.get_email('receiver')
smtpserver = read_conf.get_email('smtp_server')
port = read_conf.get_email('port')

class send_email():

    # get receiver list
    def many_receiver(self):
        receivers = []
        for n in str(receiver).split(","):
            receivers.append(n)
        return receivers

    # 发送邮件
    def tx_mial(self, report_file):
        '''发送最新的测试报告内容'''
        with open(report_file, "rb") as f:
            mail_body = f.read()
        # 定义邮件内容
        msg = MIMEMultipart()
        body = MIMEText(mail_body, _subtype='html', _charset='utf-8')
        msg['Subject'] = u"接口自动化测试报告"  #邮件主题
        msg["from"] = sender                    #
        msg["to"] = psw
        msg.attach(body)
        # 添加附件
        att = MIMEText(open(report_file, "rb").read(), "base64", "utf-8")
        att["Content-Type"] = "application/octet-stream"
        att["Content-Disposition"] = 'attachment; filename= "report.html"'
        msg.attach(att)
        try:
            smtp = smtplib.SMTP_SSL(smtpserver, port)
        except:
            smtp = smtplib.SMTP()
            smtp.connect(smtpserver, port)
        # 用户名密码
        smtp.login(sender, psw)
        receivers = send_email().many_receiver()
        smtp.sendmail(sender, receivers, msg.as_string())
        smtp.quit()
        print('test report email has send out !')



if __name__ == '__main__':# 运行此文件来验证写的send_email是否正确
    # 邮箱配置
    # print(os.path.dirname(sys.path[0])) # send_email().tx_mial()
      # 4最后一步发送报告
    # report_file =
      send_email().tx_mial(report_file)
    # os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.getcwd()))))
    # print(receiver)
    # a = "1;2;3"
    # b = receiver.split(";")
    # print(b)
