# -*- coding: utf-8 -*-

import re

filehandle = open('./ImageRecognition/setting.ini', 'r')
RecordsList = filehandle.readlines()
filehandle.close()

SettingDict = {}
for line in RecordsList:
    matchObj = re.match(r'(\[.+\])(.+)',line,re.M|re.I)
    if matchObj:
        SettingDict[matchObj.group(1)] = matchObj.group(2)
