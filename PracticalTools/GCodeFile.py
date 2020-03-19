#!/usr/bin/env python
#coding:utf-8

#2014-02-15 GCodeFile
from math import *
from time import *
import os
from msvcrt import getch
import GCode_ExportIGES
import GCode_PreviewLayer

def removeCOMMENTs(string):
	'''È¥³ý×Ö·û´®ÖÐµÄ×¢ÊÍ'''
	if type(string)==str:
		p1=string.find('(')
		p2=string.rfind(')')
		if p1!=-1 and p2!=-1 and p1<p2:
			return string[:p1]+string[p2+1:]
	return string
'''============================================================'''

class NC_Function:
	def __init__(self,CodeList,name):
		self.codelist = CodeList
		self.name = name
		pass
class Move_Order:
	Angle_to_Radian = pi/180
	def __init__(self,positionPoint,feedSpeed,laser=True,powder=True,Arc_Center=None):
		'''
		
		'''
		self.pos_Point = positionPoint		# ÊýÄ£×ø±ê
		self.feed_Speed = feedSpeed
		self.laser = laser
		self.powder = powder
		self.Arc_Center = Arc_Center
		self.G02_03 = NCFile.GCode_STATE_Parameters['Interpolation'] 
		# print positionPoint,Arc_Center
		self.sys_Point = [0,0,0]					# ÏµÍ³×ø±ê	
		
		mirror = [1,1,1]

		if NCFile.GCode_STATE_Parameters['Mirror_Mode'] == 11:
			mirror = [-1,1,1]
		elif NCFile.GCode_STATE_Parameters['Mirror_Mode'] == 12:
			mirror = [1,-1,1]
		elif NCFile.GCode_STATE_Parameters['Mirror_Mode'] == 13:
			mirror = [1,1,-1]

		'''2014-05-28 start'''
		self.sys_Point = [ NCFile.GCode_Coordinate_Origin_to_CNCSystem['current'][i]+self.pos_Point[i]*mirror[i] for i in range(3)]
		if NCFile.GCode_STATE_Parameters['Rotate_Mode'][0]!=0.0:
			angle = -1 * NCFile.GCode_STATE_Parameters['Rotate_Mode'][0]*Move_Order.Angle_to_Radian
			# rotate = [cos(angle),sin(angle)]
			# print Move_Order.Angle_to_Radian
			rotate = [	[cos(angle),	sin(angle),	0],\
						[-sin(angle),	cos(angle),	0],\
						[0,				0,			1]]

			_dp = [0.0,0.0,0.0]
			# _rorate_centerÎªÐý×ªÖÐÐÄÔÚÊÀ½çÖÐµÄ×ø±ê
			_rorate_center = [NCFile.GCode_Coordinate_Origin_to_CNCSystem['current'][i] + NCFile.GCode_STATE_Parameters['Rotate_Mode'][1][i] for i in range(3)]
			for i in range(3):
				_dp[i] = self.sys_Point[i]-_rorate_center[i]
			# 
			self.sys_Point = [ _dp[0]*rotate[i][0]+_dp[1]*rotate[i][1]+_dp[2]*rotate[i][2]+_rorate_center[i] for i in range(3)]
		'''2014-05-28 end'''
	def PrintParm(self):
		print self.pos_Point
	def getPOS(self):
		return self.sys_Point
	def getLASER(self):
		return self.laser
	def getPOWDER(self):
		return self.powder
		
		# return self.pos_Point


class NCFile:
	'''´°ÌåÐÅÏ¢·´À¡'''
	PARENT = None

	'''-------G´úÂëÖÐµÄÈ«¾Ö²ÎÊý------'''
	GCode_global_Parameters={'P102':1000 ,'P104':900 ,'P103':900 ,'P105':800 ,'P101':800 ,'P106':1000 ,'P107':800 ,'P108':800 ,'P109':2000 ,'P136':800 ,'P137':800 ,'P138':800 ,'P139':800 ,'P181':7000 ,'P185':6300,'P184':300 ,'P191':1.0 ,'P192':10 ,'P112':0 ,'P195':0 ,'P196':0 ,'P197':0 ,'P198':0 ,'P199':0 ,'P200':0 ,'P208':0 ,'P209':0 ,'P115':800 ,'P116':800 ,'P117':800 ,'P118':800 ,'P119':800 ,'P201':15 ,'P202':0.85 ,'P203':0.85 ,'P204':0.80 ,'P205':0.75 ,'P110':1,'P111':1,'P193':0}

	'''-------G´úÂëÖÐµÄÈ«¾Öº¯Êý------'''
	GCode_global_Functions={}
	GCode_Coordinate_Origin_to_CNCSystem = {
		'current':[0,0,0],\
		'G54':[0,0,0],\
		'G55':[0,0,0],\
		'G56':[0,0,0],\
		'G57':[0,0,0],\
		'G58':[0,0,0],\
		'G59':[0,0,0]	
	}
	GCode_STATE_Parameters={'Interpolation':0, 			\
							# '''G0/G1/G2/G3'''
							'Relative_Mode':90, 		\
							# '''G90/G91'''
							'Mirror_Mode':10,			\
							# '''G10	cancle
							#	G11		change X
							#	G12		change y
							#	G13		change z
							#	G14     '''
							'Rotate_Mode':[0.0,[0.0,0.0,0.0]],	\
							# '''G73'''
							'Laser_Position':[0,0,0],	\
							# '''¹â·ÛñîºÏµãÈý×ø±ê'''
							'Feeding_Speed':10.0,\
							# ²å²¹ËÙ¶È
							'Laser':False,
							# ÊÇ·ñ¿ª¹â
							'Powder':False,
							# ÊÇ·ñ¿ª·Û							
							'Moving_Speed':100.0\
							# ¿ìËÙÒÆ¶¯ËÙ¶È
							}
	GCode_SUB_PATH=''
	
	# @staticmethod
	# def SET_PARENT(parent):
	# 	PARENT = parent
	# 	print PARENT,'----------------------------'
	@staticmethod
	def GET_POSITION_IN_CNCSYSTEM():
		pass
	@staticmethod
	def INIT_PARAMETERS():
		GCode_global_Parameters={'P%d'%i:0.0 for i in range(1000)}
		pass
	@staticmethod
	def READ_PARAMETERS():
		_p = NCFile.GCode_Coordinate_Origin_to_CNCSystem.copy()
		_p['Laser_Position'] = NCFile.GCode_STATE_Parameters['Laser_Position']
		return _p.copy()
	@staticmethod
	def WRITE_PARAMETERS(_p):
		NCFile.GCode_Coordinate_Origin_to_CNCSystem['G54']=_p['G54']
		NCFile.GCode_Coordinate_Origin_to_CNCSystem['G55']=_p['G55']
		NCFile.GCode_Coordinate_Origin_to_CNCSystem['G56']=_p['G56']
		NCFile.GCode_Coordinate_Origin_to_CNCSystem['G57']=_p['G57']
		NCFile.GCode_Coordinate_Origin_to_CNCSystem['G58']=_p['G58']
		NCFile.GCode_Coordinate_Origin_to_CNCSystem['G59']=_p['G59']
		NCFile.GCode_STATE_Parameters['Laser_Position'] = _p['Laser_Position'] 
		# print _p
		# print NCFile.GCode_STATE_Parameters
	def Add_Global_NCFunction(self):
		if self.Main_Function !=None:
			NCFile.GCode_global_Functions[self.Main_Function.name] = self.Main_Function
	def PUSH_FunctionParm(self):
		self.FunctionParamStack.append(self.Private_Parameters)
		self.Private_Parameters = self.Private_PCALL_Parameters
		self.Private_PCALL_Parameters = {}

	def POP_FunctionParm(self):
		self.Private_Parameters = self.FunctionParamStack.pop()

	def __init__(self,filename):
		GCode_ExportIGES.ExportIGES.setPATH(os.path.dirname(filename))

		filehandle = open(filename,'r')
		self.RecordsList = filehandle.readlines()
		filehandle.close()

		self.debug=False
		
		'''-------G´úÂëÖÐµÄ¾Ö²¿²ÎÊý------'''
		self.Private_Parameters= {}
		self.Private_PCALL_Parameters = {}
		# for i in range(1,100):
		# 	_P='P%d'%i
		# 	self.Private_Parameters[_P]=0
		
		'''-------G´úÂëÖÐµÄ¾Ö²¿º¯Êý------'''
		self.Private_Functions = {}


		'''-------------G´úÂë------------'''
		self.PureRecordsList = []

		'''--------------Í³¼Æ------------'''
		self.StatisticsData={'total_time':0,'laser_ON_path':0,'laser_OFF_path':0}

		'''--------------¶¯×÷------------'''
		self.FunctionParamStack = []
		self.MoveOrder_list = []
		self.PathView_StartPoint=[None,None]
		self.PathView_EndPoint=[None,None]
		self.PathView_Size=[0.0,0.0]

		
		for l in self.RecordsList:
			l=removeCOMMENTs(l)
			while True:
				if l.find(' '*2)==-1:
					break
				l=l.replace(' '*2,' ')
			self.PureRecordsList.append(l.strip())

		# print 'INIT1'
		self.initFunctions()
		# print 'INIT2', self.out_Function.codelist
		# self.operateOrderList(self.out_Function.codelist)
		# if self.Main_Function !=None:
		# 	self.operateOrderList(self.Main_Function.codelist)
		# self.startOperate()
	def startOperate(self):
		# print self.out_Function.codelist
		self.refresh()
		self.operateOrderList(self.out_Function.codelist)
		if self.Main_Function !=None:
			self.operateOrderList(self.Main_Function.codelist)
		self.OnEndOperate()

		# print self.Main_Function.codelist

	def OnEndOperate(self):
		# NCFile.PARENT.mt_INFO_TemData['ReadingNCFilePosition']=[-1,-1]
		pass
	def refresh(self):
		self.StatisticsData={'total_time':0,'laser_ON_path':0,'laser_OFF_path':0}
		self.Private_Parameters= {}
		self.MoveOrder_list = []
		# self.Private_Functions = {}
		# self.PureRecordsList = []
	def initFunctions(self):
		self.Private_Functions={}
		self.Main_Function = None
		self.out_Function = NC_Function([],'out')
		_current_mode = 'out'	#'''out,sub,main'''
		_start_id = -1
		_end_id=-1
		_fun_name = ''
		for i, record in enumerate(self.PureRecordsList):
			_rlst = record.split(' ')
			# print 'record',_rlst,_start_id,_current_mode
			
			if _current_mode == 'out':
				if _rlst[0] == '%L':
					_start_id = i
					_fun_name = _rlst[1]
					_current_mode = 'sub'
				elif _rlst[0]!='' and _rlst[0][0] == '%':
					_start_id = i
					_fun_name = _rlst[0][1:]
					_current_mode = 'main'
					# print '+++',_rlst
			# elif _current_mode == 'out':
				if _start_id == -1:
					l=self.PureRecordsList[i]
					# print 'l1',l
					if l != '':
						self.out_Function.codelist.append(l)
						# print 'l2',l

			elif _rlst[0] in ['#RET','M30']:
				if _current_mode == 'sub':

					_end_id = i
					lst = [ l for l in self.PureRecordsList[_start_id+1:_end_id] if l !='']
					fun = NC_Function(lst,_fun_name)
					self.Private_Functions[_fun_name]=fun

					_start_id = -1
					_current_mode = 'out'
				elif _current_mode == 'main':
					# print 'main'
					_end_id = i
					lst = [ l for l in self.PureRecordsList[_start_id+1:_end_id] if l !='']
					fun = NC_Function(lst,_fun_name)
					self.Main_Function=fun

					_start_id = -1
					_current_mode = 'out'
					# print '---',self.Main_Function
	def checkOrder(self,order):
		while True:
			if order.find(' '*2)==-1:
				break
			order = order.replace(' '*2,' ')
		if order.find(' =')!=-1:
			order = order.replace(' =','=')
		if order.find('= ')!=-1:
			order = order.replace('= ','=')
		order = order.strip()
		# order=order.replace(' =','=').replace('= ','=').strip()
		return order
	def Type(self,word):
		if word == '' or type(word) != str:
			return None

		return word[0]
	def readParam(self,strP):
		if strP.startswith('='):
			strP=strP[1:]
		_replaceSTR = [['[','('],[']',')'],\
						['ABS','abs'],\
						['SQRT','sqrt'],\
						['MOD','%'],\
						['ROUND','round'],\
						['FIX','int'],\
						['V.A.PPOS.X',str(NCFile.GCode_STATE_Parameters['Laser_Position'][0])],\
						['V.A.PPOS.Y',str(NCFile.GCode_STATE_Parameters['Laser_Position'][1])],\
						['V.A.PPOS.Z',str(NCFile.GCode_STATE_Parameters['Laser_Position'][2])],\
						['ATAN','atan'],\
						['COS','cos'],\
						['SIN','sin'],\
						['ATAN','atan']]
		for i in _replaceSTR:
			strP=strP.replace(i[0],i[1])
		_param_all_replace = False
		while True:
			_x = strP.find('P')

			if _x != -1 and not _param_all_replace:
				_p = 'P'
				for i in strP[_x+1:]:
					if i.isdigit():
						_p+=i
					else:
						break
				# if strP=='0.9*P181':
				# 	self.debug=True
				# 	print 'a1'
				if _p=='P':
					strP = strP[:_x] +'p' + strP[_x+len(_p):]
					_param_all_replace=True
					continue

				# if self.debug:
				# 	print strP,_x,_p
				num = _p[1:]
				num = int(num)
				if num<=99 and _p in self.Private_Parameters:
					_tem = self.Private_Parameters[_p]
				elif num <=9999 and _p in NCFile.GCode_global_Parameters:
					_tem = NCFile.GCode_global_Parameters[_p]

				# try:
				# 	a=_tem
				# except Exception, e:
				# 	print strP,_tem

				# try:
				# 	strP = strP[:_x] +str(_tem) + strP[_x+len(_p):]
				# except Exception, e:
				# 	print '321',num,_p,_tem
				strP = strP[:_x] +str(_tem) + strP[_x+len(_p):]
			else:
				alpha='ABCDEFGHIJKLMNOpQRSTUVWXYZ'
				for i in alpha:
					if i in strP:
						num = alpha.find(i)
						_p = 'P%d'%num
						if _p in self.Private_Parameters:
							strP = strP.replace(i,str(self.Private_Parameters[_p]))
							
				break
		
		return eval(strP)	
	
	def setParam(self,strP,Param):

		if type(Param)==str and not Param.isdigit():
			
			Param=self.readParam(Param)
		if type(Param)==str and Param.isdigit():
			
			Param=float(Param)
				
			
		# print '      SetParam:',strP,Param
		if len(strP)==1 and strP>='A' and strP<='Z':
			alpha='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
			num = alpha.find(strP)
			self.Private_PCALL_Parameters['P%d'%num]=Param
			return
		elif strP!='' and strP.startswith('P'):
			num = strP[1:]
			if num.isdigit():
				num = int(num)
				if num<=99:
					self.Private_Parameters[strP]=Param
				elif num <=9999:
					NCFile.GCode_global_Parameters[strP]=Param
	def echo_One_Order(self,order):
		# print '    ECHO:',order
		# getch()
		if self.Type(order)=='P' and '=' in order:
			'''¸³Öµ'''
			while True:
				x=order.find(' ')
				if x!=-1:
					''''''
					_od=order[:x]
					order = order[x:].strip()
				else:
					_od = order
				if '+=' in _od:
					_P=_od.split('+=')
					# print self.readParam(_P[0])+self.readParam(_P[1])
					self.setParam(_P[0],self.readParam(_P[0])+self.readParam(_P[1]))
				elif '-=' in _od:
					_P=_od.split('-=')
					self.setParam(_P[0],self.readParam(_P[0])-self.readParam(_P[1]))
				elif '*=' in _od:
					_P=_od.split('*=')
					self.setParam(_P[0],self.readParam(_P[0])*self.readParam(_P[1]))
				elif '/=' in _od:
					_P=_od.split('/=')
					self.setParam(_P[0],self.readParam(_P[0])/self.readParam(_P[1]))
				elif '=' in _od:
					_P=_od.split('=')
					# try:
					# 	self.setParam(_P[0],_P[1])
					# except Exception, e:
					# 	print _P[0],_P[1],self.readParam(_P[1])
					self.setParam(_P[0],_P[1])

				if _od==order:
					break
		elif self.Type(order) in ['G','X','Y','Z','F','M']:
			_odlist=order.split(' ')
			_movePath_flag = [False] * 3
			_movePath = [None] * 3
			_G04 = False
			_G73 = False
			_G02_03_RelativeCenter = [0,0,0]
			
			#
			for _od in _odlist:
				# _mode = NCFile.GCode_STATE_Parameters['Interpolation']
				if _od.startswith('G'):
					_mode = self.readParam(_od[1:])
					if _mode in [0,1,2,3]:
						NCFile.GCode_STATE_Parameters['Interpolation']=_mode
					elif _mode in [90,91]:
						NCFile.GCode_STATE_Parameters['Relative_Mode']=_mode
					elif _mode in [54,55,56,57,58,59]:
						NCFile.GCode_Coordinate_Origin_to_CNCSystem['current'] = NCFile.GCode_Coordinate_Origin_to_CNCSystem['G%d'%_mode]
					elif _mode in [10,11,12,13,14]:
						NCFile.GCode_STATE_Parameters['Mirror_Mode']=_mode
					elif _mode in [73]:
						_G73 = True
						if len(_odlist) == 1:
							NCFile.GCode_STATE_Parameters['Rotate_Mode']=[0.0,[0.0,0.0,0.0]]
						pass
					elif _mode in [4]:
						_G04 = True
						pass

				elif _od.startswith('Q'):
					if _G73:
						NCFile.GCode_STATE_Parameters['Rotate_Mode'][0] += self.readParam(_od[1:])
					# if NCFile.GCode_STATE_Parameters['Rotate_Mode'][0] != 0.0:
					# 	NCFile.GCode_STATE_Parameters['Rotate_Mode'][0]=self.readParam(_od[1:])
						# print 'Q',NCFile.GCode_STATE_Parameters['Rotate_Mode']
				elif _od.startswith('I'):
					if _G73:
					# if NCFile.GCode_STATE_Parameters['Rotate_Mode'][0] != 0.0:
						NCFile.GCode_STATE_Parameters['Rotate_Mode'][1][0]=self.readParam(_od[1:])
					elif NCFile.GCode_STATE_Parameters['Interpolation'] in [2,3]:
						_G02_03_RelativeCenter[0] = self.readParam(_od[1:])
				elif _od.startswith('J'):
					if _G73:
					# if NCFile.GCode_STATE_Parameters['Rotate_Mode'][0] != 0.0:
						NCFile.GCode_STATE_Parameters['Rotate_Mode'][1][1]=self.readParam(_od[1:])
						# print NCFile.GCode_STATE_Parameters['Rotate_Mode']
					elif NCFile.GCode_STATE_Parameters['Interpolation'] in [2,3]:
						_G02_03_RelativeCenter[1] = self.readParam(_od[1:])
				elif _od.startswith('X'):
					_x=self.readParam(_od[1:])
					_movePath[0] = _x
					_movePath_flag[0] = True
					pass
				elif _od.startswith('Y'):
					_y=self.readParam(_od[1:])
					_movePath[1]=_y
					_movePath_flag[1] = True
					pass
				elif _od.startswith('Z'):
					_z=self.readParam(_od[1:])
					_movePath[2]=_z
					_movePath_flag[2] = True
					pass
				elif _od.startswith('F'):
					_feed = self.readParam(_od[1:])
					NCFile.GCode_STATE_Parameters['Feeding_Speed']=_feed
					pass
				elif _od.startswith('M'):

					if _od == 'M20':
						NCFile.GCode_STATE_Parameters['Laser'] = True
						# print '20-',_od
					elif _od == 'M21':
						NCFile.GCode_STATE_Parameters['Laser'] = False
						# print '21-',_od
					elif _od == 'M12':
						NCFile.GCode_STATE_Parameters['Powder'] = True
					elif _od == 'M13':
						NCFile.GCode_STATE_Parameters['Powder'] = False
					pass
				elif _od.startswith('K'):
					if _G04:
						self.StatisticsData['total_time'] += self.readParam(_od[1:])
						_G04=False
					elif NCFile.GCode_STATE_Parameters['Interpolation'] in [2,3]:
						_G02_03_RelativeCenter[2] = self.readParam(_od[1:])

			if any(_movePath_flag):
			# if float(_movePath[0]) != -1 or float(_movePath[1]) != -1 or float(_movePath[2]) != -1:

				# print order
				# print NCFile.GCode_STATE_Parameters['Laser_Position'],'----'
				if NCFile.GCode_STATE_Parameters['Interpolation'] == 0:
					# G00	¿ìËÙ¶¨Î»					
					_speed = NCFile.GCode_STATE_Parameters['Moving_Speed']
				elif NCFile.GCode_STATE_Parameters['Interpolation'] == 1:
					# G01	Ö±Ïß²å²¹
					_speed = NCFile.GCode_STATE_Parameters['Feeding_Speed']
				elif NCFile.GCode_STATE_Parameters['Interpolation'] == 2:
					# G02 顺时针
					_speed = NCFile.GCode_STATE_Parameters['Feeding_Speed']
					pass
				elif NCFile.GCode_STATE_Parameters['Interpolation'] == 3:
					# G03 逆时针
					_speed = NCFile.GCode_STATE_Parameters['Feeding_Speed']
					pass
				else:
					print NCFile.GCode_STATE_Parameters['Interpolation']


				if NCFile.GCode_STATE_Parameters['Interpolation'] in [2,3]:
					#预存圆心坐标
					_center = [NCFile.GCode_STATE_Parameters['Laser_Position'][i] +_G02_03_RelativeCenter[i] for i in range(3)]

				if NCFile.GCode_STATE_Parameters['Relative_Mode'] == 90:
					# ¾ø¶ÔÎ»ÒÆ
					_movePath = [NCFile.GCode_STATE_Parameters['Laser_Position'][i] if not _movePath_flag[i] else _movePath[i] for i in range(3)]
					# for i in range(3):
					# 	if _movePath[i] == -1:
					# 		_movePath[i] = NCFile.GCode_STATE_Parameters['Laser_Position'][i]


					p1 = NCFile.GCode_STATE_Parameters['Laser_Position']
					p2 = _movePath
					
					# print '--'
					_len = sqrt((p1[0]*1.-p2[0])**2+(p1[1]-p2[1])**2+(p1[2]-p2[2])**2)
					NCFile.GCode_STATE_Parameters['Laser_Position'] = _movePath

				elif NCFile.GCode_STATE_Parameters['Relative_Mode'] == 91:
					# Ïà¶ÔÎ»ÒÆ
					_movePath = [0 if not _movePath_flag[i] else _movePath[i] for i in range(3)]
					# for i in range(3):
					# 	if _movePath[i] == -1:
					# 		_movePath[i] = 0

					# p1 = NCFile.GCode_STATE_Parameters['Laser_Position']
					p2 = _movePath
				
					_len = sqrt((p2[0])**2+(p2[1])**2+(p2[2])**2)
					# print NCFile.GCode_STATE_Parameters['Laser_Position'],'----'
					for i in range(3):						
						NCFile.GCode_STATE_Parameters['Laser_Position'][i]+=_movePath[i]

				_positionPoint = NCFile.GCode_STATE_Parameters['Laser_Position'][:]

				if NCFile.GCode_STATE_Parameters['Interpolation'] in [2,3]:
					# _center = [_positionPoint[i] -_G02_03_RelativeCenter[i] for i in range(3)]
					'''近似计算圆弧长度'''
					_len*=1.3

					_moveorder = Move_Order(_positionPoint,_speed,NCFile.GCode_STATE_Parameters['Laser'],NCFile.GCode_STATE_Parameters['Powder'],_center)
				else:
					_moveorder = Move_Order(_positionPoint,_speed,NCFile.GCode_STATE_Parameters['Laser'],NCFile.GCode_STATE_Parameters['Powder'])
				self.MoveOrder_list.append(_moveorder)
				self.exportStructure(_moveorder)
				
				for i in range(2):
					if self.PathView_StartPoint[i] == None or self.PathView_StartPoint[i] > _positionPoint[i]:
						self.PathView_StartPoint[i] = _positionPoint[i]
					if self.PathView_EndPoint[i] == None or self.PathView_EndPoint[i] < _positionPoint[i]:
						self.PathView_EndPoint[i] = _positionPoint[i]

				# print order,':',NCFile.GCode_STATE_Parameters['Laser_Position'],'--',_moveorder.PrintParm()
				# print order
				# for i in nc.MoveOrder_list:
				# 	print i,'==='
				# 	i.PrintParm()
				'''_speed : mm/min
				   _len : mm
				'''
				# print order,_len,_speed


				_t = _len*60.0/_speed
				
				if NCFile.GCode_STATE_Parameters['Laser']:
					self.StatisticsData['laser_ON_path']+=_len
					
				else:
					self.StatisticsData['laser_OFF_path']+=_len
					
				self.StatisticsData['total_time'] += _t
			# print self.Main_Function.name, order,NCFile.GCode_STATE_Parameters['Laser']
			# getch()
			# print 'MoveOrder_list1',self.MoveOrder_list
	def exportStructure(self,moveorder):
		GCode_ExportIGES.ExportIGES.ADD_ORDER(moveorder)
		GCode_PreviewLayer.PreviewLayer.ADD_ORDER(moveorder)
		pass
	def operateOrderList(self,orderlist):
		currentI=0
		# self.StatisticsData={'total_time':0,'laser_ON_path':0,'laser_OFF_path':0}
 		
		while True:
			if currentI>=len(orderlist):
				break

			order = orderlist[currentI]
			order = self.checkOrder(order)
			
			# try:
			# 	if operateOD(order)=='break':
			# 		break
			# except Exception, e:
			# 	NCFile.PARENT.OutputINFO('ERROR: %s\n'%order)
			try:
				if order.startswith('$FOR'):
					j=currentI+1
					ForLayer = 1
					while True:
						if orderlist[j].startswith('$FOR'):
							ForLayer+=1
						if orderlist[j]=='$ENDFOR':
							ForLayer-=1
							if ForLayer==0:
								break
						j+=1

					_odlist = orderlist[currentI+1:j]
					'''¹¹ÔìÑ­»·  ²¢µ÷ÓÃ'''

					_p = order[order.find(' '):order.find('=')].strip()
					_d = order[order.find('=')+1:].replace(' ','').split(',')
					_d = [int(i) for i in _d]
					for i in range(_d[0],_d[1]+_d[2],_d[2]):
						self.setParam(_p,i)
						re = self.operateOrderList(_odlist)
						if re == '$BREAK':
							break
						if re == '$CONTINUE':
							continue
					'''Ìø¹ýÌõ¼þÑ¡Ôñ³ÌÐò¶Î'''
					currentI=j
				elif order.startswith('#CALL'):
					# print self.FunctionParamStack
					self.PUSH_FunctionParm()
					_od = order.split(' ')
					_name = _od[1]

					if _name in self.Private_Functions:
						
						
						self.operateOrderList(self.Private_Functions[_name].codelist)
						
					# elif NCFile.GCode_SUB_PATH == '' or not os.listdir(NCFile.GCode_SUB_PATH):
					# 	# print self.Private_Functions,_name,type(_name)
					# 	NCFile.PARENT.OutputINFO( u'SUB路径无效\n    CODE: %s\n'%order)
					# 	return 'break'
					elif _name.lower() in os.listdir(NCFile.GCode_SUB_PATH) or _name.upper() in os.listdir(NCFile.GCode_SUB_PATH) or _name in os.listdir(NCFile.GCode_SUB_PATH):
					# elif _name in NCFile.GCode_global_Functions:
						if NCFile.PARENT!=None:
							# NCFile.PARENT.PrintReadingNCFileName(NCFile.PARENT.mt_INFO,'Z=%.1f µ÷ÓÃ%s'%(NCFile.GCode_STATE_Parameters['Laser_Position'][2],_name))
							# NCFile.PARENT.mt_INFO('\b'*50+'OPEN FILE %s'%_name)
							NCFile.PARENT.OutputINFO('Z=%.1f : %s\n'%(NCFile.GCode_STATE_Parameters['Laser_Position'][2],_name))
							# pass
						_filename = NCFile.GCode_SUB_PATH+_name
						_ncFile = NCFile(_filename)
						_ncFile.startOperate()

						for i in self.StatisticsData:
							self.StatisticsData[i] += _ncFile.StatisticsData[i]
						self.MoveOrder_list += _ncFile.MoveOrder_list

						# print 'open File %s start'%_filename
						# print NCFile.PARENT
						# print _ncFile.MoveOrder_list
						# self.operateOrderList(_ncFile.Main_Function.codelist)


						# _filehandle = open('e:\\record.txt','w')
						# for i in _ncFile.Main_Function.codelist:

						# 	_filehandle.write(i+'\n')

						# _filehandle.close()
						# print 'open File %s end'%_filename
					else:
						NCFile.PARENT.OutputINFO(u'SUB路径下无%s\n'%_name)
					self.POP_FunctionParm()
				elif order.startswith('#PCALL'):
					# print self.FunctionParamStack
					
					# print '!!PCALL', order
					# self.echo_One_Order(order)

					_od = order.split(' ')
					_name = _od[1]
					for i in _od[2:]:
						_p = i.split('=')

						self.setParam(_p[0],_p[1])
					self.PUSH_FunctionParm()

					if _name in self.Private_Functions:
						self.operateOrderList(self.Private_Functions[_name].codelist)
					elif _name in NCFile.GCode_global_Functions:
						self.operateOrderList(NCFile.GCode_global_Functions[_name].codelist)
					self.POP_FunctionParm()	
				elif order.startswith('$BREAK'):
					return '$BREAK'
				elif order.startswith('$CONTINUE'):
					return '$CONTINUE'
				elif order.startswith('$IF'):
					# print 'IF:',order
					j=currentI+1
					IfLayer = 1
					SplitJ = [currentI]
					SplitOrder = []
					while True:
						if orderlist[j].startswith('$IF'):
							IfLayer+=1
						elif orderlist[j].startswith('$ELSEIF'):
							if IfLayer==1:
								SplitJ.append(j)
						elif orderlist[j].startswith('$ELSE'):
							if IfLayer==1:
								SplitJ.append(j)
						elif orderlist[j]=='$ENDIF':
							IfLayer-=1
							if IfLayer==0:
								SplitJ.append(j)
								break
						j+=1
					# print 'SplitJ',SplitJ
					for i in range(len(SplitJ)-1):
						_if = orderlist[SplitJ[i]]
						_odlist = orderlist[SplitJ[i]+1:SplitJ[i+1]]
						# self.debug = True
						# print '_if',_if[_if.find(' '):],self.readParam(_if[_if.find(' '):]),NCFile.GCode_STATE_Parameters['Laser_Position']
						if _if.startswith('$IF') or _if.startswith('$ELSEIF'):
							if self.readParam(_if[_if.find(' '):]):
								re = self.operateOrderList(_odlist)
								if re == '$BREAK':
									return '$BREAK'
								if re == '$CONTINUE':
									return '$CONTINUE'
								break
						elif _if.startswith('$ELSE'):
							re = self.operateOrderList(_odlist)
							if re == '$BREAK':
								return '$BREAK'
							if re == '$CONTINUE':
								return '$CONTINUE'
					'''Ìø¹ýÌõ¼þÑ¡Ôñ³ÌÐò¶Î'''
					currentI=j
				elif order.startswith('$SWITCH'):
					j=currentI+1
					SwitchLayer = 1
					SplitJ = [currentI]
					SplitOrder = []
					while True:
						if orderlist[j].startswith('$SWITCH'):
							SwitchLayer+=1
						elif orderlist[j].startswith('$CASE'):
							if SwitchLayer==1:
								SplitJ.append(j)
						elif orderlist[j]=='$ENDSWITCH':
							SwitchLayer-=1
							if SwitchLayer==0:
								SplitJ.append(j)
								break
						j+=1
					_switch_p = ''
					for i in range(len(SplitJ)-1):
						_case = orderlist[SplitJ[i]].split(' ')
						# print _case
						if _case[0]=='$SWITCH':
							_switch_p = self.readParam(_case[1]) 
						else:
							if _switch_p == self.readParam(_case[1]):
								_odlist=[]
								_odlist = orderlist[SplitJ[i]+1:SplitJ[i+1]]
								re = self.operateOrderList(_odlist)
								if re == '$BREAK':
									break
					'''Ìø¹ýÌõ¼þÑ¡Ôñ³ÌÐò¶Î'''
					currentI=j
				elif order.startswith('$WHILE'):
					j=currentI+1
					WhileLayer = 1
					while True:
						if orderlist[j].startswith('$WHILE'):
							WhileLayer+=1
						if orderlist[j]=='$ENDWHILE':
							WhileLayer-=1
							if WhileLayer==0:
								break
						j+=1
					_odlist = orderlist[currentI+1:j]
					_while = order.replace('$WHILE','')
					while True:
						if not self.readParam(_while):
							break
						re = self.operateOrderList(_odlist)
						if re == '$BREAK':
							break
						if re == '$CONTINUE':
							continue
					'''Ìø¹ýÌõ¼þÑ¡Ôñ³ÌÐò¶Î'''
					currentI=j
				elif order.startswith('$DO'):
					j=currentI+1
					DoLayer = 1
					while True:
						if orderlist[j]=='$DO':
							DoLayer+=1
						if orderlist[j].startswith('$ENDDO'):
							DoLayer-=1
							if DoLayer==0:
								order = orderlist[j]
								break
						j+=1
					_odlist = orderlist[currentI+1:j]
					_while = order.replace('$ENDDO','')
					while True:
						re = self.operateOrderList(_odlist)
						if re == '$BREAK':
							break
						if re == '$CONTINUE':
							continue
						if not self.readParam(_while):
							break
					'''Ìø¹ýÌõ¼þÑ¡Ôñ³ÌÐò¶Î'''
					currentI=j
				elif order.startswith('#ECHO'):
					_od = order.split(' ')
					
					for i in _od[1:]:
						NCFile.PARENT.OutputINFO('%s:%.3f\n'%(i,self.readParam(i)))
						# print "%s:%f\t"%(i,self.readParam(i))
				elif order.startswith('#EXPORT'):
					if not GCode_ExportIGES.ExportIGES.checkPATH():
						NCFile.PARENT.OutputINFO('Z=%.1f IGESÎÄ¼þÂ·¾¶ÎÞÐ§\n'%NCFile.GCode_STATE_Parameters['Laser_Position'][2])
						return 'break'
						
					# if NCFile.IGES_EXPORT_FILE != None:
					# 	NCFile.PARENT.OutputINFO('Z=%.1f IGESÎÄ¼þÎ´¹Ø±Õ\n'%NCFile.GCode_STATE_Parameters['Laser_Position'][2])
					# 	break

					GCode_ExportIGES.ExportIGES.NEW_IGES()

					pass
				elif order.startswith('#DISEXPORT'):
					GCode_ExportIGES.ExportIGES.SAVE_IGES()
					pass
				elif order.startswith('#PREVIEW'):
					GCode_PreviewLayer.PreviewLayer.NEW_LAYER(NCFile.GCode_STATE_Parameters['Laser_Position'][2])
					pass
				elif order.startswith('#NEXTPREVIEW'):
					GCode_PreviewLayer.PreviewLayer.CLOSE_LAYER()
					pass
				else:
					
					self.echo_One_Order(order)
					# try:
					# 	self.echo_One_Order(order)
					# except Exception, e:
					# 	NCFile.PARENT.OutputINFO('ERROR: %s\n'%order)
						# print NCFile.GCode_global_Parameters
						# print order
					# self.echo_One_Order(order)
			except Exception, e:
				NCFile.PARENT.OutputINFO("ERROR: %s\n" % order)
				# print e



			currentI += 1