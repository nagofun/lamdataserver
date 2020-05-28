# -*- coding: utf-8 -*-

import re
import os
from lamdataserver.settings import APP_PATH
# with open('log.txt','w+') as _f:
# 	_f.write('LoadSettings.py start\n')
with open(os.path.join(APP_PATH,'ImageSectionInfo_code.json').replace('\\','/'), 'r') as filehandle:
	# filehandle = open('./ImageRecognition/setting.ini', 'r')
	RecordsList = filehandle.readlines()
	filehandle.close()

SettingDict = {}
for line in RecordsList:
    matchObj = re.match(r'(\[.+\])(.+)',line,re.M|re.I)
    if matchObj:
        SettingDict[matchObj.group(1)] = matchObj.group(2)
