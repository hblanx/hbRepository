# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 15:24:26 2021
@author: hblanx
"""

msg = input("输入总共多少GB和已经下载多少GB（以空格分开）")
GBmsg = msg.split(" ")
speed = eval(input("输入下载速度，单位MB（仅数字）"))
leftMB = (float(GBmsg[0])-float(GBmsg[1])) * 1024
time=leftMB/speed
print("还要下载{0:.0f}秒，约{1:.0f}分钟，{2:.0f}小时".format(time,time/60,time/3600))
