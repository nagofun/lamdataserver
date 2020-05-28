# -*- coding: gbk -*-

import numpy as np
import re
import time
from django.core.cache import cache
from lamdataserver.settings import APP_PATH
import sys
import os
from math import *
SettingDict = {}
CNCSystemSyntax={
	'8070':{
		'comments_match' : '\((.*)\)',                      #       (Sub program DEFAULT 缺省子程序段)
		'SubfunctionStart_match' : '%L (.*)',               #       %L 1120
		'SubfunctionEnd_match' : '#RET',                    #       #RET
		'MainfunctionStart_match' : '%(.*)',                #       %025002
		'MainfunctionEnd_match' : 'M30|#RET',               #       M30 #RET
		'CALLorder_match' : '#CALL (.*)',                   #       #CALL 1120
		'PCALLorder_match' : '\(PCALL ([A-Za-z0-9]*), (.*)\)',            #       #PCALL 1031 A=P6 B=P12 C=P4 D=P195
		'PCALLorder_findall':'([A-Z]=?P?-?\d+\.?\d*e?-?\d*?)',
		'BlockStart_match': '\((.*) \((.*).igs\)',          #       (1-1 (0000.igs))
		'LocateByJump_match': 'G91 G01 Z-?P192 FP109',      #       G91 G01 ZP192 FP109
		'MoveOrder_match': '.*F.*',                         #       G90 G01 X204.684 Y42.687 FP109
		'assignmentOrder_match': '^(P\d+)=(.*)',            #       P6=P1*0.25
		'assignment_PCALL_match':'^([A-Z])=?([^ ]*)$',      #       A204.684  A=204.684
		'Move_findall':r'[XYZF]-?P?-?\d+\.?\d*e?-?\d*?',      #       G90 G01 X204.684 Y42.687 FP109
		'SplitParam_match':'([A-Z])=?(.*)',                 #       A204.684
		'SplitDigitParam_findall':r'[A-Z]=?P?-?\d+\.?\d*e?-?\d*?',  #      A204.684 B42.687
		'PCode_findall':'P\d+',                             #       P6, P12, P4, P195
		'PParam_match':'^P\d+$',                            #       P0
		'getPParamNum_findall':'P(\d+)',                      #       P0
		'replaceSTR' : [['[','('],[']',')'],
						['ABS','abs'],
						['SQRT','sqrt'],
						['MOD','%'],
						['ROUND','round'],
						['FIX','int'],],
		'TranslateSTR_match' : (
			('(.*)\(COS\(([^\)]*)\)\)(.*)','(cos(pi*(%s)/180.))'),
			('(.*)\(SIN\(([^\)]*)\)\)(.*)','(sin(pi*(%s)/180.))'),
			('(.*)\(TAN\(([^\)]*)\)\)(.*)','(tan(pi*(%s)/180.))'),
			('(.*)\(ATAN\(([^\)]*)\)\)(.*)','(atan(pi*(%s)/180.))'),
		),
		'CommentCode':'\n(%s)\n',
		'LaserOnCode':'#CALL 1120\n',
		'LaserOffCode':'#CALL 1121\n',
		'TurningCode':'#CALL %s\n\n',
		'SwitchBlockCode':'#CALL %s\n\n',
		'SubFunctionInfoCode_Head': '\n%%L %s\n(*********  G Code Break By Turning Point  *********)\n\n',
		'SubFunctionInfoCode_End': '\n#RET\n',
		'BlockInfoCode1': '(%s (%s.igs) -1)\n',
		'BlockInfoCode2': '(%s (%s.igs) -2)\n',

	},
	'8055':{
		'comments_match' : ';(.*)$',                        #       ;Sub program DEFAULT 缺省子程序段
		'SubfunctionStart_match' : r'\(SUB (.*)\)',          #       (SUB 1036)
		'SubfunctionEnd_match' : r'\(RET\)',                 #       (RET)
		'MainfunctionStart_match' : r'%(.*)',                #       %16k 第1截面 Z=0~16
		'MainfunctionEnd_match' : r'M30',                    #       M30
		'CALLorder_match' : r'\(CALL (.*)\)',                #       (CALL P1)
		'PCALLorder_match' : r'\(PCALL ([A-Za-z0-9]*), (.*)\) ?N?([0-9]*)',        #       (PCALL 1051, A=P1, B=P2, C=P102)
															#       (PCALL 1109, A20.000, B10.072) N3
		'PCALLorder_findall':r'([A-Z]=?P?-?\d+\.?\d*e?-?\d*?)',
		'BlockStart_match': r';(.*)\((.*).igs\)',            #       ;1-1 (0000.igs)
		'LocateByJump_match': r'G91 G01 Z-?P192 FP109',      #       G91 G01 ZP192 FP109
		'MoveOrder_match': r'.*F.*',                         #       G90 G01 X-331.000 Y97.873 FP109
		'assignmentOrder_match': r'^\((P\d+)=(.*)\)',        #       (P6=P1*0.25) ;S1/4
		'assignment_PCALL_match':r'^([A-Z])=?([^ ]*)$',      #       A204.684  A=204.684
		'Move_findall':r'[XYZF]-?P?-?\d+\.?\d*e?-?\d*?',      #       G90 G01 X204.684 Y42.687 FP109
		'SplitParam_match':r'([A-Z])=?(.*)',                   #       X204.684
		'SplitDigitParam_findall':r'[A-Z]=?P?-?\d+\.?\d*e?-?\d*?',  #      A204.684 B42.687
		'PCode_findall':r'P\d+',                             #       P6, P12, P4, P195
		'PParam_match':r'^P\d+$',                            #       P0
		'getPParamNum_findall':r'P(\d+)',                      #       P0
		'replaceSTR' :(
			['MOD','%'],
		    ['EXP','**'],
		    ['EQ','=='],
		    ['NE','!='],
		    ['GT','>'],
		    ['GE','>='],
		    ['LT','<'],
		    ['LE','<='],
		    ['AND','and'],
		    ['OR','or'],
		    ['XOR','^'],
		    ['NOT','not'],
		),

		'TranslateSTR_match' : (
			('(.*)\(COS ([^\)]*)\)(.*)','(cos(pi*(%s)/180))'),
			('(.*)\(SIN ([^\)]*)\)(.*)','(sin(pi*(%s)/180))'),
			('(.*)\(TAN ([^\)]*)\)(.*)','(tan(pi*(%s)/180))'),
			('(.*)\(ATAN ([^\)]*)\)(.*)','(atan(pi*(%s)/180))'),
			('(.*)\(ABS ([^\)]*)\)(.*)','(abs(%s))'),
			('(.*)\(SQRT ([^\)]*)\)(.*)','(sqrt(%s))'),
			('(.*)\(LOG ([^\)]*)\)(.*)','(log(%s))'),
			('(.*)\(ROUND ([^\)]*)\)(.*)','(round(%s))'),
			('(.*)\(FIX ([^\)]*)\)(.*)','(int(%s))'),
		),
		'CommentCode':'\n; %s\n',
		'LaserOnCode':'(CALL 1120)\n',
		'LaserOffCode':'(CALL 1121)\n',
		'TurningCode':'(CALL %s)\n\n',
		'SwitchBlockCode':'(CALL %s)\n\n',
		'SubFunctionInfoCode_Head': '\n(SUB %s)\n;*********  G Code Break By Turning Point  *********\n\n',
		'SubFunctionInfoCode_End': '\n(RET)\n',
		'BlockInfoCode1': ';%s (%s.igs) -1\n',
		'BlockInfoCode2': ';%s (%s.igs) -2\n',

	},
}

AlphabetList ='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
SubParamNameList = ['P%d'%i for i in range(26)]
# Alphabet_ZIP_TO_SubParamZip = zip(AlphabetList, SubParamNameList)
Alphabet_To_SubParam_Dict = {i[0]:i[1] for i in zip(AlphabetList, SubParamNameList)}
Global_CNC_ParamDict = {}


def CacheOperator(operateType, ifget, ParamSet,data=None):
	'''
	:param operateType:
		'recordLastTime'
		'CleanUpTime'
		'ProgressBarValue_CompleteInspect_MissionId'    由process_realtime_finedata中的CacheOperator进行赋值
		'ProgressBarValue_PracticalTools_SShapeBreak_By_GUID'    由SShapeBreak中的CacheOperator进行赋值
	:param ifget:
	:param ParamSet:    (worksectionid,datatype)
		datatype:laser, oxygen, cncstatus
	:param data:
	:return:
	'''
	revalue = None
	if operateType == 'ProgressBarValue_PracticalTools_SShapeBreak_By_GUID':
		GUID = ParamSet
		key = 'PBR_Tools_SSBK_GUID%s' % (GUID)
		if not ifget:
			cache.set(key, data)
			# print(key,data)
		else:
			revalue = cache.get(key)
	return revalue

def readInitFile():
	global SettingDict
	with open(os.path.join(APP_PATH, './PracticalTools/setting1.ini').replace('\\', '/'), 'r', encoding='utf-8') as filehandle:
		# filehandle = open('./PracticalTools/setting1.ini', 'r', encoding='utf-8')
		RecordsList = filehandle.readlines()
		# filehandle.close()

	for line in RecordsList:
		matchObj = re.match(r'(\[.+\])(.+)', str(line), re.M | re.I)
		if matchObj:
			SettingDict[matchObj.group(1)] = matchObj.group(2)

def CheckVectorsReverse(V1, V2):
	isReverse = False
	if (V1[0] == 0 and V2[0] == 0 and V1[1] * V2[1] < 0) or \
		(V1[1] == 0 and V2[1] == 0 and V1[0] * V2[0] < 0):
		isReverse = True
	elif V1[0] * V1[1] * V2[0] * V2[1] != 0:
		# 两向量坐标中无0值
		_normV1 = V1/np.linalg.norm(V1)
		_normV2 = V2/np.linalg.norm(V2)

		if abs(_normV1[0] * _normV2[1] - _normV1[1] * _normV2[0]) < 0.001 and V1[0]* V2[0] < 0:
			isReverse = True
	return isReverse


class Function:
	def __init__(self,name, CNCSystemType, comment):
		self.name = name
		self.startlineid=None
		self.endlineid=None
		self.paramdict = {}
		# 填充路径列表
		self.TrackList = []
		self.CNCSystemType = CNCSystemType
		self.ifJump = False
		# 如果为注释，则跳过继续
		matchObj = re.match(CNCSystemSyntax[self.CNCSystemType]['comments_match'], comment, re.M | re.I)
		if matchObj:
			self.comment = matchObj[0]
		else:
			self.comment = '\n'
		pass

	def setJump(self, _b):
		self.ifJump = _b

	def setstartlineid(self,id):
		self.startlineid = id
	def setendlineid(self, id):
		self.endlineid = id
	def setcodelist(self, CodeList):
		self.codelist = CodeList[self.startlineid+1: self.endlineid]  # 不包含头尾


	def setParam(self, strP, Param):
		'''
		对于赋值语句有效
		:param strP:
		:param Param:
		:return:
		'''
		if type(Param) == str and not Param.isdigit():
			Param = AnalyseField(Param, self)
		if type(Param) == str and Param.isdigit():
			Param = float(Param)
		if len(strP) == 1 and strP >= 'A' and strP <= 'Z':
			self.paramdict[Alphabet_To_SubParam_Dict[strP]] = Param
			return
		elif strP != '' and strP.startswith('P'):
			num = strP[1:]
			if num.isdigit():
				num = int(num)
				if num <= 99:
					self.paramdict[strP] = Param
				elif num <= 9999:
					Global_CNC_ParamDict[strP] = Param

	def runGCode(self, startPoint,Track, ParamList=[]):
		return AnalyseCodeList(ParamList + self.codelist, self, startPoint, Track)

	def OutputGcode(self, TurningFunction, SwitchBlockFunction, IfPrintTurningFunction, IfPrintSwitchBlockFunction):
		def appendSwitchBlock(outputcode):
			if IfPrintSwitchBlockFunction:
				outputcode += [CNCSystemSyntax[self.CNCSystemType]['CommentCode'] % 'SwitchBlock']
				outputcode += [SwitchBlockCode]
			else:
				outputcode += ['\n\n']
		def appendTurningPoint(outputcode):
			if IfPrintTurningFunction:
				outputcode += [CNCSystemSyntax[self.CNCSystemType]['CommentCode'] % 'TurningPoint']
				outputcode += [TurningCode]
			else:
				outputcode += ['\n\n']

		outputcode = []
		TurningCode = CNCSystemSyntax[self.CNCSystemType]['TurningCode']%TurningFunction
		SwitchBlockCode = CNCSystemSyntax[self.CNCSystemType]['SwitchBlockCode']%SwitchBlockFunction
		Comment = self.comment
		SubFunction_Head = CNCSystemSyntax[self.CNCSystemType]['SubFunctionInfoCode_Head']%(self.name)
		SubFunction_End = CNCSystemSyntax[self.CNCSystemType]['SubFunctionInfoCode_End']

		outputcode += ['\n', Comment]
		outputcode += [SubFunction_Head]
		for _tk in self.TrackList:
			# outputcode += ['\n']
			outputcode += [CNCSystemSyntax[self.CNCSystemType]['BlockInfoCode1']%(_tk.label, _tk.igsname)]
			outputcode += _tk.GCodeTrack1
			# 增加分块间的函数调用
			appendSwitchBlock(outputcode)

		# 增加转折点处函数调用
		appendTurningPoint(outputcode)

		for _tk in self.TrackList:
			# outputcode += ['\n']
			outputcode += [CNCSystemSyntax[self.CNCSystemType]['BlockInfoCode2']%(_tk.label, _tk.igsname)]
			outputcode += _tk.GCodeTrack2
			# 增加分块间的函数调用
			appendSwitchBlock(outputcode)



		outputcode += [SubFunction_End]
		return outputcode

		# ...20200118
		'''
		'LaserOnCode':'(CALL 1120)\n',
		'LaserOffCode':'(CALL 1121)\n',
		'TurningCode':'(CALL %s)\n',
		'SubFunctionInfoCode_Head': ';%s.igs\n(SUB %s)\n;*********  G Code Break By Turning Point  *********\n\n',
		'SubFunctionInfoCode_End': '\n(RET)\n',
		'BlockInfoCode1': ';%s (%s.igs) -1\n',
		'BlockInfoCode2': ';%s (%s.igs) -2\n',
		'''


class Track:
	# TrackList = []
	NextID = 0
	def __init__(self, parentFunction):
		self.id = Track.NextID
		Track.NextID+=1
		self.parentFunction = parentFunction
		self.PointList = []
		self.SpeedList = []
		self.startPoint = None
		self.turningPoint = None
		self.lastPoint = None           # 遍历操作的上一个P
		self.maxDistance = None
		# self.minDistance = 0
		# self.distancelist = []
		self.vectorlist = []
		self.ScanningVector = None      # 直道扫描方向
		self.StepVector = None          # 步进方向
		self.label = ''
		self.igsname = ''
		self.startlineid=None
		self.endlineid=None
		self.truninglineid = None
		self.ifJump = False

		self.GCodeTrack1 = []
		self.GCodeTrack2 = []
		# Track.TrackList.append(self)

	def addlabel(self,label):
		self.label = label
	def addigsname(self, name):
		self.igsname = name
	def setstartlineid(self,id):
		self.startlineid = id
	def setendlineid(self, id):
		self.endlineid = id
	def setturninglineid(self, id):
		self.truninglineid = id
	def setcodelist(self, CodeList):
		self.codelist = CodeList[self.startlineid+1: self.endlineid]  # 不包含头尾
	def setJump(self, _b):
		self.ifJump = _b
	def getJump(self):
		return self.ifJump
	def addPoint(self, P, SPD):
		'''
		Add one NUMPY-Type Point and STRING-Type Speed
		:param P: numpy
		:param SPD: string
		:return: None
		'''
		isturning = False
		if self.startPoint is None:
			# 第一个点
			self.startPoint = P
			# self.maxDistance = 0
			# self.turningPoint = P
			# self.distancelist.append(self.maxDistance)
			# self.minDistance = min(self.distancelist)
		else:
			# 其余点
			# 当前点与上一个点所形成的的向量
			_thisVector = P - self.lastPoint
			if np.linalg.norm(_thisVector) == 0: return False
			_thisVector = _thisVector / np.linalg.norm(_thisVector)
			# ifverseList = [CheckVectorsReverse(_v, _thisVector) for _v in self.vectorlist]
			'''当没有获得步进向量时'''
			if self.ScanningVector is None:
				'''首先获得直道方向'''
				isScanningVector = False
				for _v in self.vectorlist:
					if CheckVectorsReverse(_v, _thisVector):
						isScanningVector = True
						break
				'''然后获得步进向量'''
				if isScanningVector:
					self.ScanningVector = _thisVector
					_StepVector = np.array([-_thisVector[1], _thisVector[0], 0.0])
					# 将_StepVector调整至与前半段步进方向同向
					for _v in self.vectorlist:
						_dot = np.dot(_v,_StepVector)
						if abs(_dot) <0.001:
							continue
						else:
							if _dot<0:
								_StepVector = -1*_StepVector
							break
					self.StepVector = _StepVector/np.linalg.norm(_StepVector)
			'''再对后续向量进行判断'''
			if not self.StepVector is None and self.turningPoint is None:
				_thisVnorm = _thisVector / np.linalg.norm(_thisVector)
				if np.dot(self.StepVector, _thisVnorm) <0 and abs(np.dot(self.StepVector, _thisVnorm))>0.001:
					self.turningPoint = self.lastPoint
					isturning = True

			self.vectorlist.append(_thisVector)

			# 当最小值开始降低时，取转折点
			# 20200318
			# _distance = np.linalg.norm(self.startPoint - P)
			# if _distance < self.minDistance and self.turningPoint is None:
			# 	self.turningPoint = P
			# 	isturning = True
			# else:
			# 	self.distancelist.append(_distance)
			# 	self.minDistance = min(self.distancelist)

			# if _distance>self.maxDistance:
			# 	self.turningPoint = P
			# 	self.maxDistance=_distance
			# 	isturning = True
		self.lastPoint = P
		self.PointList.append(P)
		self.SpeedList.append(SPD)
		return isturning
	def addPVList(self,Plist,SPDlist):
		isturning = False
		_ist = []
		for _p, _spd in zip(Plist, SPDlist):
			_ist.append(self.addPoint(_p, _spd))
		isturning = any(_ist)
		return isturning
	def analyse(self, start_position):
		Plist, SPDlist, end_position = AnalyseCodeList(self.codelist, self.parentFunction, start_position, self)
		# self.addPVList(Plist, SPDlist)
		return end_position
	def divide(self):
		'''
		自转折点中分代码
		:return:
		'''
		# print(self.codelist[self.truninglineid])
		self.GCodeTrack1 = self.codelist[:self.truninglineid+1] + [CNCSystemSyntax[self.parentFunction.CNCSystemType]['LaserOffCode']]

		_gcode = []
		if self.getJump():
			_gcode.extend(['G91 G01 ZP192 FP109\n'])
		_gcode.extend(['G90 G01 X%.3f Y%.3f FP109\n'%(self.turningPoint[0],self.turningPoint[1])])
		if self.getJump():
			_gcode.extend(['G91 G01 Z-P192 FP109\n'])
		_gcode.extend([CNCSystemSyntax[self.parentFunction.CNCSystemType]['LaserOnCode']])
		_gcode.extend(self.codelist[self.truninglineid+1:])

		self.GCodeTrack2 = _gcode


		# print(self.codelist[:self.truninglineid+1])
		# if self.getJump():
		# 	print('G91 G01 ZP192 FP109')
		# print('G90 G01 X%.3f Y%.3f FP109'%(self.turningPoint[0],self.turningPoint[1]))
		# if self.getJump():
		# 	print('G91 G01 Z-P192 FP109')
		# print(self.codelist[self.truninglineid+1:])
		pass


def AnalyseField(field, parentFun):
	reFieldValue = field
	# 是否能直接转化
	try:
		return float(reFieldValue)
	except:
		pass

	# 替换P参数
	matchObj = re.findall(CNCSystemSyntax[parentFun.CNCSystemType]['getPParamNum_findall'], field, re.M | re.I)
	for _pnum in matchObj:
		_pnum = int(_pnum)
		strP = 'P%d'%_pnum
		if _pnum >100:
			reFieldValue = reFieldValue.replace(strP, str(Global_CNC_ParamDict[strP]))
		elif _pnum<=25:
			reFieldValue = reFieldValue.replace(strP, str(parentFun.paramdict[strP]))

	# 替换内置函数及逻辑关系
	for i in CNCSystemSyntax[parentFun.CNCSystemType]['replaceSTR']:
		reFieldValue = reFieldValue.replace(i[0], i[1])
	for i in CNCSystemSyntax[parentFun.CNCSystemType]['TranslateSTR_match']:
		matchObj = re.match(i[0], reFieldValue, re.M | re.I)
		if matchObj:
			str1 = matchObj[1]
			str2 = matchObj[3]
			param = matchObj[2]
			reFieldValue = str1 + i[1]%param + str2

	return eval(reFieldValue)


def AnalyseCodeList(codelist, parentFun, start_position, Track = False):
	def checkTrack(Plist, SPDlist, crtlineid):
		if Track:
			isturning = Track.addPVList(Plist,SPDlist)
			if isturning:
				Track.setturninglineid(crtlineid-1)

	'''

	:param codelist:    所运行的G代码列表
	:param parentFun:   父函数
	:param start_position:  起始位置
	:return:    Plist, SPDlist, end_position
	'''
	Plist = []
	SPDlist = []
	end_position = start_position
	for lineid, line in enumerate(codelist):
		# 如果为注释，则跳过继续
		matchObj = re.match(CNCSystemSyntax[parentFun.CNCSystemType]['comments_match'], line, re.M | re.I)
		if matchObj:
			continue

		# 替换局部注释
		line = re.sub(CNCSystemSyntax[parentFun.CNCSystemType]['comments_match'], "", line)
		if len(line) == 0:
			continue

		# 判断是否CALL子函数
		matchObj = re.match(CNCSystemSyntax[parentFun.CNCSystemType]['CALLorder_match'], line, re.M | re.I)
		if matchObj:
			_subfunctionname = matchObj[1]
			if parentFun.CNCSystemType == '8055':
				if _subfunctionname in BasicSubFunctionFile_8055.subfunctionDict:
					_subfunction = BasicSubFunctionFile_8055.subfunctionDict[_subfunctionname]
				else:
					print('ERROR')
			elif parentFun.CNCSystemType == '8070':
				if _subfunctionname in BasicSubFunctionFile_8070.subfunctionDict:
					_subfunction = BasicSubFunctionFile_8070.subfunctionDict[_subfunctionname]
				else:
					print('ERROR')
			try:
				_plist, _spdlist, end_position = _subfunction.runGCode(end_position, Track)
			except:
				pass
			# checkTrack(_plist, _spdlist, lineid)
			Plist.extend(_plist)
			SPDlist.extend(_spdlist)
			continue

		# 判断是否为PCALL子函数
		matchObj = re.match(CNCSystemSyntax[parentFun.CNCSystemType]['PCALLorder_match'], line, re.M | re.I)
		if matchObj:
			_subfunctionname = matchObj[1]
			_paramstr = matchObj[2]
			_paramlist = re.findall(CNCSystemSyntax[parentFun.CNCSystemType]['SplitDigitParam_findall'], _paramstr)

			try:
				_repeattimes = int(matchObj[3])
			except:
				_repeattimes = 1

			# 将A-39.000 替换为A=-39.000
			_assignment_paramlist = []
			for _param in _paramlist:
				matchObj = re.match(CNCSystemSyntax[parentFun.CNCSystemType]['SplitParam_match'], _param, re.M | re.I)
				if matchObj:
					_assignment_paramlist.append('%s=%s'%(matchObj[1], matchObj[2]))


			if parentFun.CNCSystemType == '8055':
				if _subfunctionname in BasicSubFunctionFile_8055.subfunctionDict:
					_subfunction = BasicSubFunctionFile_8055.subfunctionDict[_subfunctionname]
				else:
					print('ERROR')
			elif parentFun.CNCSystemType == '8070':
				if _subfunctionname in BasicSubFunctionFile_8070.subfunctionDict:
					_subfunction = BasicSubFunctionFile_8070.subfunctionDict[_subfunctionname]
				else:
					print('ERROR')

			while (_repeattimes):
				# 循环进行指定次数
				_repeattimes -= 1
				_plist, _spdlist, end_position = _subfunction.runGCode(end_position, Track, _assignment_paramlist)
				# checkTrack(_plist, _spdlist, lineid)
				Plist.extend(_plist)
				SPDlist.extend(_spdlist)
			continue

		# 判断是否为赋值指令
		matchObj = re.match(CNCSystemSyntax[parentFun.CNCSystemType]['assignmentOrder_match'], line, re.M | re.I)
		if matchObj:
			# 如果为赋值指令
			parentFun.setParam(matchObj[1], AnalyseField(matchObj[2], parentFun))
			continue

		# 判断是否为PCALL参数传值
		matchObj = re.match(CNCSystemSyntax[parentFun.CNCSystemType]['assignment_PCALL_match'], line, re.M | re.I)
		if matchObj:
			# 如果为赋值指令
			parentFun.setParam(matchObj[1], AnalyseField(matchObj[2], parentFun))
			continue


		# 判断是否为运动指令
		matchObj = re.match(CNCSystemSyntax[parentFun.CNCSystemType]['MoveOrder_match'], line, re.M | re.I)
		if matchObj:
			# 如果为提Z定位指令，则去掉
			matchObj = re.match(CNCSystemSyntax[parentFun.CNCSystemType]['LocateByJump_match'], line, re.M | re.I)
			if matchObj:
				parentFun.setJump(True)
				if Track:
					Track.setJump(True)
				continue
			# 如果为运动指令，则记录Track
			if 'G90' in line:
				# 绝对定位
				AbsolutePosition = True
				pass
			else:
				# 相对定位
				AbsolutePosition = False
				pass
			_order_xyzinfo = re.findall(CNCSystemSyntax[parentFun.CNCSystemType]['Move_findall'], line)
			try:
				_x, _y, _z, _f = (0, 0, 0, 0)
				for i in _order_xyzinfo:
					if '-P1' in i:
						pass
					if 'X' in i:
						_x = float(AnalyseField(i.strip('X'), parentFun))
					if 'Y' in i:
						_y = float(AnalyseField(i.strip('Y'), parentFun))
					if 'Z' in i:
						_z = float(AnalyseField(i.strip('Z'), parentFun))
					if 'F' in i:
						_f = i.replace('F', '')
			except:
				print('ERROR in checkBlockTrack()!')
			finally:
				if AbsolutePosition:
					end_position = np.array([_x, _y, _z])
				else:
					end_position = end_position + np.array([_x, _y, _z])

				checkTrack([end_position], [_f], lineid)
				Plist.append(end_position)
				SPDlist.append(_f)
			continue
	return Plist, SPDlist, end_position

class GCodeFile:
	def __init__(self, filename, file=None, GUID=None):
		# 子函数字典
		self.subfunctionDict = {}
		self.paramdict = {}

		# 主函数
		self.mainfunction = None

		if filename.endswith('nc'):
			self.CNCSystemType = '8070'

		elif filename.endswith('pim'):
			self.CNCSystemType = '8055'

		if file is None:
			with open(os.path.join(APP_PATH, '%s'%filename).replace('\\', '/'), 'r', encoding='gbk') as filehandle:
				self.lines = filehandle.readlines()
			# with open(filename, 'r') as file:
			# 	self.lines = file.readlines()
		else:
			self.lines = file.readlines()
			try:
				self.lines = list(map(lambda l:str(l, encoding="utf8").replace('\r',''), self.lines))
			except:
				pass

		if_in_subfunction=False
		if_in_mainfunction=False
		# function_startlineid = None
		# function_endlineid = None
		current_subfunction = None

		# 划分结构，提取函数
		_linecount = len(self.lines)
		_writeCacheCount = int(_linecount/20)
		for lineid, line in enumerate(self.lines):
			# try:
			# 	line = str(line, encoding="utf8")
			# except:
			# 	pass
			if lineid%_writeCacheCount==0:
				CacheOperator('ProgressBarValue_PracticalTools_SShapeBreak_By_GUID', False, GUID,
				              0.25 * lineid / _linecount)

			matchObj = re.match(CNCSystemSyntax[self.CNCSystemType]['comments_match'], line, re.M | re.I)
			if matchObj:
				# 如果为注释，则跳过继续
				continue

			matchObj = re.match(CNCSystemSyntax[self.CNCSystemType]['SubfunctionStart_match'], line, re.M | re.I)
			if matchObj:
				# 子函数开始
				if_in_subfunction = True
				# function_startlineid = lineid
				try:
					_cmt = self.lines[lineid-1]
				except:
					_cmt = ''
				current_subfunction=Function(matchObj[1], self.CNCSystemType, _cmt)
				current_subfunction.setstartlineid(lineid)
				continue

			matchObj = re.match(CNCSystemSyntax[self.CNCSystemType]['MainfunctionStart_match'], line, re.M | re.I)
			if matchObj:
				# 主函数开始
				try:
					_cmt = self.lines[lineid-1]
				except:
					_cmt = ''
				if_in_mainfunction = True
				# function_startlineid = lineid
				self.mainfunction=Function(matchObj[1], self.CNCSystemType, _cmt)
				self.mainfunction.setstartlineid(lineid)
				continue

			if if_in_subfunction:
				matchObj = re.match(CNCSystemSyntax[self.CNCSystemType]['SubfunctionEnd_match'], line,
				                    re.M | re.I)
				if matchObj:
					# 子函数结束
					if_in_subfunction=False
					current_subfunction.setendlineid(lineid)
					current_subfunction.setcodelist(self.lines)
					# self.subfunctionlist.append(current_subfunction)
					self.subfunctionDict[current_subfunction.name]=current_subfunction

			elif if_in_mainfunction:
				if matchObj:
					# 主函数结束
					if_in_mainfunction=False
					self.mainfunction.setendlineid(lineid)
					self.mainfunction.setcodelist(self.lines)
			else:
				pass

	def setParam(self, strP, Param):
		'''
		对于赋值语句有效
		:param strP:
		:param Param:
		:return:
		'''
		if type(Param) == str and not Param.isdigit():
			Param = AnalyseField(Param, self)
		if type(Param) == str and Param.isdigit():
			Param = float(Param)
		if len(strP) == 1 and strP >= 'A' and strP <= 'Z':
			self.paramdict[Alphabet_To_SubParam_Dict[strP]] = Param
			return
		elif strP != '' and strP.startswith('P'):
			num = strP[1:]
			if num.isdigit():
				num = int(num)
				if num <= 99:
					self.paramdict[strP] = Param
				elif num <= 9999:
					Global_CNC_ParamDict[strP] = Param

	def checkBlockTrack(self, GUID):
		# 按block方式检查切分G代码
		_checkcount=0
		_functioncount = len(self.subfunctionDict)
		_writeCacheCount = int(_functioncount / 20) if int(_functioncount / 20)>0 else 1
		for SubFunName in self.subfunctionDict:
			_checkcount += 1
			if _checkcount % _writeCacheCount==0:
				CacheOperator('ProgressBarValue_PracticalTools_SShapeBreak_By_GUID', False, GUID,
			              0.25+0.75 * _checkcount / _functioncount)
			SubFunction = self.subfunctionDict[SubFunName]

			current_position = np.array([0,0,0])
			current_track = None
			for lineid,line in enumerate(SubFunction.codelist):
				line = line.strip()

				# 判断是否为Track开始
				matchObj = re.match(CNCSystemSyntax[self.CNCSystemType]['BlockStart_match'], line, re.M | re.I)
				if matchObj:
					# 如果为Track开始,则开始新track，关闭旧track
					if current_track:
						# 如有，则加入列表
						current_track.setendlineid(lineid)
						current_track.setcodelist(SubFunction.codelist)
						SubFunction.TrackList.append(current_track)
					# 启动新对象
					current_track = Track(SubFunction)
					current_track.addlabel(matchObj[1])
					current_track.addigsname(matchObj[2])
					current_track.setstartlineid(lineid)
					continue
			if current_track:
				# 加入列表
				current_track.setendlineid(lineid)
				current_track.setcodelist(SubFunction.codelist)
				SubFunction.TrackList.append(current_track)

			for _track in SubFunction.TrackList:
				current_position = _track.analyse(current_position)
	def divideByTurningPoint(self):
		for SubFunName in self.subfunctionDict:
			SubFunction = self.subfunctionDict[SubFunName]
			for _track in SubFunction.TrackList:
				_track.divide()
		pass

	def outputGCode(self, TurningFunction, SwitchBlockFunction, IfPrintTurningFunction, IfPrintSwitchBlockFunction):
		outputgcode = []
		for SubFunName in self.subfunctionDict:
			SubFunction = self.subfunctionDict[SubFunName]
			outputgcode += SubFunction.OutputGcode(TurningFunction, SwitchBlockFunction, IfPrintTurningFunction, IfPrintSwitchBlockFunction)
		return outputgcode


def MakeSShapeBreakGCode(filename,
                         file,
                         # PowderOnOrder,
                         # PowderOffOrder,
                         TurningFunction,
                         SwitchBlockFunction,
                         IfPrintTurningFunction,
                         IfPrintSwitchBlockFunction,
                         GUID):
	t1 = time.time()
	gcodefile = GCodeFile(filename, file, GUID=GUID)
	# 更新进度条
	# CacheOperator('ProgressBarValue_PracticalTools_SShapeBreak_By_GUID', False, GUID, 0.3)
	t2=time.time()
	gcodefile.checkBlockTrack(GUID)
	t3 = time.time()
	gcodefile.divideByTurningPoint()
	t4 = time.time()
	reGCodelist = gcodefile.outputGCode(TurningFunction, SwitchBlockFunction, IfPrintTurningFunction, IfPrintSwitchBlockFunction)
	t5 = time.time()
	print(t2-t1)
	print(t3-t2)
	print(t4-t3)
	print(t5-t4)

	return list(map(lambda l:l.encode(), reGCodelist))

readInitFile()
BasicSubFunctionFile_8055 = GCodeFile('./PracticalTools/8070 default Sub program.nc')
BasicSubFunctionFile_8070 = GCodeFile('./PracticalTools/8055 default Sub program.pim')

# if __name__ == '__main__':
# 	readInitFile()
# 	newText = ''
# 	try:
# 		import os.path
# 		readfilename = sys.argv[1]
# 	except:
# 		readfilename = SettingDict['[GCodeFileName]']
# 	writefilename = os.path.splitext(readfilename)[0] + '-SShapeBreak' + os.path.splitext(readfilename)[1]
#
# 	BasicSubFunctionFile_8055 = GCodeFile(SettingDict['[8055BasicSubFunctionFile]'])
# 	BasicSubFunctionFile_8070 = GCodeFile(SettingDict['[8070BasicSubFunctionFile]'])
# 	gcodefile = GCodeFile(readfilename)
# 	gcodefile.checkBlockTrack()
#
# 	gcodefile.divideByTurningPoint()
# 	gcodefile.outputGCode(filename=writefilename)

