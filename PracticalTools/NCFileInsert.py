# -*- coding: gbk -*-
import re
import time
import sys
SettingDict = {}

def readInitFile():
	global SettingDict
	filehandle = open('setting.ini', 'r')
	RecordsList = filehandle.readlines()
	filehandle.close()

	for line in RecordsList:
		matchObj = re.match(r'(\[.+\])(.+)', line, re.M | re.I)
		if matchObj:
			SettingDict[matchObj.group(1)] = matchObj.group(2)


if __name__ == '__main__':
	# print(sys.argv)
	readInitFile()
	newText = ''
	try:
		readfilename = sys.argv[1]
	except:
		readfilename = SettingDict['[NCFileName]']
	print('start')
	with open(readfilename,'r') as file:
		lines = file.readlines()
		# True ���뺯����  False ������
		new_function_flag = False
		block_num = 1

		for oneline in lines:
			block_in_flag = False
			block_out_flag = False

			if '%L' in oneline:
				new_function_flag = True
			if '#RET' in oneline:
				new_function_flag = False
				block_num = 1

			if new_function_flag:
				if '.igs))' in oneline or '-F)' in oneline or '-B)' in oneline:
					# �˴��ոս���ֿ��ڣ�����ж���Ϣ
					block_in_flag = True
					# block_num = int(oneline.split('-')[0][1:])

				if '#CALL 1121' in oneline:
					# ��Ҫ�߳��ֿ飬��Ҫ��ӽ�����Ϣ
					block_out_flag = True
					block_num +=1
			newline = '\t' if (new_function_flag and not block_in_flag and '%L' not in oneline) else ''


			if block_in_flag:
				newline += '$IF [%s<=%d]\n\t'%(SettingDict['[ParamCounter]'],block_num)

			newline += oneline
			if block_out_flag:
				newline += '\t%s=%d\n' % (SettingDict['[ParamCounter]'], block_num)
				newline += '\t%s=V.A.PPOS.X\n' % (SettingDict['[ParamCurrentPPOSX]'])
				newline += '\t%s=V.A.PPOS.Y\n' % (SettingDict['[ParamCurrentPPOSY]'])
				newline += '\t%s=V.A.PPOS.Z\n' % (SettingDict['[ParamCurrentPPOSZ]'])
				newline += '$ENDIF\n'
			newText += newline

	with open(readfilename+' %s.NC'%time.strftime('%Y%m%d_%H%M%S',time.localtime(time.time())),'w') as file:
		file.write(newText)
	print('finish')