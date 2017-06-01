#!/usr/bin/python
#-*- coding:utf-8 -*-
import xlrd
import datetime
import traceback
import sys
import io
from itfwtManger import *
baseurl = '/usr/HotLineManage/'
#baseurl =''
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
nowtime = datetime.datetime.now()
xlsfile = baseurl+'workplan.xlsx'
write_to_log('%s  自动上下线开始 \r\n' % nowtime.strftime('%Y-%m-%d %H:%M:%S'),baseurl )
#打开排班文件
book = xlrd.open_workbook(xlsfile,encoding_override='utf-8')
workPlanDict = load(baseurl+'hotlineConf.json')['workPlan']
sheet0 = book.sheet_by_index(0)
datecol = None
hotlinemanager = HotLineManger(baseurl)
#查询当前日期在排班表中的列
for i in range(sheet0.nrows):
    currow = sheet0.row(i)
    if currow[0].value=='日期':
        for l in range(len(currow)):
            if  currow[l].ctype==3:
                curdate = xlrd.xldate.xldate_as_datetime(currow[l].value, 0)
                if curdate.month==nowtime.month and curdate.day==nowtime.day:
                    datecol = l
#针对当天的排班查看如果当前小时是上下线时间执行上下线操作
workQueue = {'up':[],'down':[]}
for i in range(sheet0.nrows):
    if datecol and hotlinemanager.hasemp(sheet0.row(i)[0].value)  :
        curuser = sheet0.row(i)[0].value
        curWorkType = sheet0.row(i)[datecol].value
        if curWorkType in workPlanDict:
            #如果现在是下班时间将用户添加到下班队列
            if nowtime.hour == workPlanDict[curWorkType][1]:
                workQueue['down'].append(curuser)
            # 如果现在是上班时间将用户添加到上班队列
            elif nowtime.hour == workPlanDict[curWorkType][0]:
                workQueue['up'].append(curuser)
#先下班再上班
if len(workQueue['down'])>0:
    for i  in range(len(workQueue['down'])):
        if not hotlinemanager.logout(workQueue['down'][i]):
            write_to_log("%s  %s  下线失败 \r\n" % (nowtime.strftime('%Y-%m-%d %H:%M:%S'), workQueue['down'][i]),
                         baseurl)
        else:
            write_to_log("%s %s 下线成功 \r\n" % (nowtime.strftime('%Y-%m-%d %H:%M:%S'), workQueue['down'][i]), baseurl)
if len(workQueue['up'])>0:
    for i  in range(len(workQueue['up'])):
        if not hotlinemanager.login(workQueue['up'][i]):
            write_to_log("%s %s 上线失败 \r\n" % (nowtime.strftime('%Y-%m-%d %H:%M:%S'), workQueue['up'][i]), baseurl)
        else:
            write_to_log("%s %s 上线成功 \r\n" % (nowtime.strftime('%Y-%m-%d %H:%M:%S'), workQueue['up'][i]), baseurl)

write_to_log('%s  自动上下线结束 \r\n' % nowtime.strftime('%Y-%m-%d %H:%M:%S') ,baseurl)
