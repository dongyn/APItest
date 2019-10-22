# -*- coding:utf-8 -*-
#@Time  : 2019/8/29 11:15
#@Author: dongyani
#@interfacetest: http://apiv1.starschina.com
#@Features:

import datetime, time, runPageAd

start_date = datetime.datetime.now()
deadtime = str((start_date + datetime.timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M:%S"))
while str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) < deadtime:
    all_case = runPageAd.all_case()  # 1加载用例
    runPageAd.run_case(all_case)  # 2执行用例
    time.sleep(5)
runPageAd.send_mail_report()
