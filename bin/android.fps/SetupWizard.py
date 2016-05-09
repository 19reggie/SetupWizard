#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os, time

def click():
    print '开始测试...'
    time.sleep(3)
    for i in range(0,100,1):
        if i==10:
            print u'测试完成.'
            break
        else:
            print i
            #语言页 > 按钮坐标 240 680
            #设置WLAN页 NEXT> 按钮坐标 400 815
            #位置服务页 不允许 按钮坐标 110 820 允许 按钮坐标 365 820
            #用户协议页 更多 按钮坐标 65 546
            #时区和时间页 > 按钮坐标 242 792
            os.popen('adb shell input tap 242 792')
            time.sleep(5)
            os.popen('adb shell input keyevent KEYCODE_BACK')
            time.sleep(3)

if __name__ == '__main__':
    click()

        
