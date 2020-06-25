import ReadIGESFiles as IGES
from functools import reduce
import random
import math

# 切割图形，得到交点列表
def getGyratorCrossPointlist_By_Yvalue(iges_obj, YValue):
	crossP_list = []


	for _loop in iges_obj.LoopPointsListDict.values():
		_plist = _loop[:]
		_plist.insert(0, _plist.pop())
		_tupleP = zip(_plist, _loop)
		for P1, P2 in _tupleP:
			# print(P1,P2)
			if (P1.y - YValue) * (P2.y - YValue) < 0:
				# 有相交
				crs_X = P1.x + (P2.x - P1.x) * (YValue - P1.y) / (P2.y - P1.y)
				# 判断交点处是否外延，计算外延角度
				if P2.x == P1.x:
					theta = 0
				else:
					theta = (P2.x - P1.x) / ((P2.x - P1.x) ** 2 + (P2.y - P1.y) ** 2) ** 0.5
				# = (P2.y-P1.y)/(P2.x-P1.x)
				crossP_list.append([crs_X, theta])
				pass
			elif (P1.y - YValue) * (P2.y - YValue) == 0:
				# 以相邻截面代替
				return getGyratorCrossPointlist_By_Yvalue(iges_obj, YValue + 0.0001)



	# for line_obj in iges_obj.LinesList:
	# 	P1 = line_obj.P1
	# 	P2 = line_obj.P2
	# 	if (P1.y-YValue)*(P2.y-YValue) <0:
	# 		# 有相交
	# 		crs_X = P1.x + (P2.x-P1.x)*(YValue-P1.y)/(P2.y-P1.y)
	# 		# 判断交点处是否外延，计算外延角度
	# 		if P2.x == P1.x:
	# 			theta = 0
	# 		else:
	# 			theta = (P2.x-P1.x)/( (P2.x-P1.x)**2 + (P2.y-P1.y)**2  )**0.5
	# 			# = (P2.y-P1.y)/(P2.x-P1.x)
	# 		crossP_list.append([crs_X, theta])
	# 		pass
	# 	elif (P1.y-YValue)*(P2.y-YValue) ==0:
	# 		# 以相邻截面代替
	# 		return getGyratorCrossPointlist_By_Yvalue(iges_obj, YValue+0.0001)

			# # 仅计入1点相交
			# if (P1.y-YValue)==0:
			# 	crossP_list.append(P1.x)
			# elif (P2.y-YValue)==0:
			# 	crossP_list.append(P2.x)
	if len(crossP_list)%2 != 0:
		print('ERROR in getGyratorCrossPointlist_By_Yvalue!')
	crossP_list.sort()
	set_crossPList = [[crossP_list[2*i], crossP_list[2*i+1]] for i in range(int(len(crossP_list)/2))]
	return set_crossPList

# 等分每个线段，返回内部填充圆的半径列表
def getFillRadiuslist(crsPointList, targetoffset, outline_offset):
	RadiusList = []
	for _plist in crsPointList:
		Max_X_value = max(_plist)
		Min_X_value = min(_plist)
		_count = round((Max_X_value-Min_X_value + 2*outline_offset)/targetoffset)
		_offset = (Max_X_value-Min_X_value + 2*outline_offset)/_count
		RadiusList.extend( [Min_X_value - outline_offset + i*_offset for i in range(1, _count)] )
	return RadiusList

def saveIgsFile(Yvalue, FillRadiusList, OutlineRadiusDict, igsfilename,targetoffset, ifchangeStartPoint = False):
	# if not self.S_shapedLoopList:return
	# x1=xcos(β)-ysin(β);
	# y1=ycos(β)+xsin(β);
	_igs = IGES.IGESFile(IGES.cur_file_dir() + r"\blank.igs")
	_angle = random.random()*math.pi*2
	for _radius in FillRadiusList:
		_x, _y = _radius, 0.0
		if ifchangeStartPoint:
			rot_x = _x*math.cos(_angle) - _y * math.sin(_angle)
			rot_y = _y*math.cos(_angle) + _x * math.sin(_angle)
			_x, _y = rot_x, rot_y
		startPos = [_x, _y, Yvalue]
		endPos = startPos
		_igs.AddSingleCircle([0.0, 0.0, Yvalue], startPos, endPos)
		_angle += 0.3
	for _radius, _sin_theta in OutlineRadiusDict:
		# 负：下表面  正：上表面
		if _sin_theta > math.sin(15*math.pi/180):
			color = 'BLUE'
		elif _sin_theta > math.sin(10*math.pi/180):
			color = 'GREEN'
		elif _sin_theta > math.sin(5*math.pi/180):
			color = 'YELLOW'
		elif abs(_radius) < targetoffset:
			color = 'DEFAULT'
		else:
			color = 'RED'
		_x, _y = _radius, 0.0
		if ifchangeStartPoint:
			rot_x = _x * math.cos(_angle) - _y * math.sin(_angle)
			rot_y = _y * math.cos(_angle) + _x * math.sin(_angle)
			_x, _y = rot_x, rot_y
		startPos = [_x, _y, Yvalue]
		endPos = startPos
		_igs.AddSingleCircle([0.0, 0.0, Yvalue], startPos, endPos, col=color)
	_igs.saveIGES(igsfilename)


# 根据纵剖面igs文件，得到一系列切片填充igs以及轮廓igs
def GyratorFilling(iges_obj, Y_step=1.0, targetoffset=5.0, outline_offset = 0.0, ifchangeStartPoint=True):
	# 得到纵剖面Y范围
	Max_Y_value = max(map(lambda line_obj:line_obj.P1.y, section_iges.LinesDic.values()))
	Min_Y_value = min(map(lambda line_obj:line_obj.P1.y, section_iges.LinesDic.values()))

	# 遍历Y范围，用Y值切割纵剖面轮廓
	# (Max_Y_value-Min_Y_value)/Y_step+1
	for i in range(int((Max_Y_value-Min_Y_value)/Y_step)+1):

		_y = Min_Y_value + i*Y_step
		if _y >382:
			a=1
			pass
		# 切割图形，得到交点列表
		# 0:X坐标 1:外延系数
		crossPointList = getGyratorCrossPointlist_By_Yvalue(iges_obj, _y)
		print(crossPointList)
		RadiusList = getFillRadiuslist(list(map( lambda line: [line[0][0], line[1][0]] , crossPointList) ), targetoffset, outline_offset)
		try:
			saveIgsFile(Yvalue = _y, FillRadiusList=RadiusList, OutlineRadiusDict=reduce(lambda a,b: a+b, crossPointList), igsfilename=r'.\GyratorFilling.\%04d.igs'%i, targetoffset=targetoffset, ifchangeStartPoint=ifchangeStartPoint)
		except:
			pass
	pass

if __name__ == '__main__':
	# section_filepath='./01-2000 half.igs'
	# section_filepath='./3-01.igs'
	# section_filepath=r'F:\2-技术文件\12 - 临时数控程序 (LCX)\MPM-LCX-2020-033 SYJ.LZ.001\STEP1\229-598\outline half.igs'
	section_filepath=r'F:\2-技术文件\12 - 临时数控程序 (LCX)\MPM-LCX-2020-033 SYJ.LZ.001\STEP2\15-124\outline half.igs'
	# section_filepath=r'F:\2-技术文件\12 - 临时数控程序 (LCX)\MPM-LCX-2020-033 SYJ.LZ.001\STEP3\outline half.igs'
	# section_filepath='./test.igs'
	section_iges = IGES.IGESFile(section_filepath, MinPointArea=0.01, NearPointDistance=0.01)
	looplayerDict = section_iges.MakeLoopOrder()
	section_iges.MakeLoopClockwise(looplayerDict)
	section_iges.MakeInnerlinePointIDList(distance=5.5)
	GyratorFilling(section_iges, Y_step=0.5, targetoffset=4, outline_offset=2, ifchangeStartPoint=True)
	pass