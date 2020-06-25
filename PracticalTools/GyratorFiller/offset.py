#!/usr/bin/env python
# coding:utf-8
# from math import *
from itertools import *
from time import *
from geometry import *
import ReadIGESFiles
import pdb
from random import *


NUMIGESFILENAME = 0

class Offset():
	def __init__(self, plist = None, poslist = None, pidlist = None):
		if poslist:
			self.initplist = poslist
			self.pIDlist = map(lambda p: p.ID, map(lambda pos: Point.getPoint(pos), poslist))
		elif plist:
			self.initplist = map(lambda p: p.getPOS(), plist)
			self.pIDlist = map(lambda p:p.getID(),plist)
		elif pidlist:
			self.initplist = map(lambda p: p.getPOS(), map(lambda pid: Point.PointDict[pid], pidlist))
			self.pIDlist = pidlist

		'''消除位置相同的点'''
		PList=map(lambda pid:Point.PointDict[pid],self.pIDlist)
		Point.RemoveSAMEPOSPoint(PList)
		self.pIDlist = map(lambda p:p.getID(),PList)
		self.initplist = map(lambda p: p.getPOS(), map(lambda pid: Point.PointDict[pid], self.pIDlist))

		self.rdlineDict = {}
		self.degenerateOffset = {}
		self.degoffsetrange = [None, None]
		self.rdlineCrossPointDict = {}
		self.IfClockWise = Point.IfLoopClockwise(PIDList=self.pIDlist)

		self.makeRadialLine()
		self.makeDegenerateOffset()

		pass

	def makeRadialLine(self):
		for i in xrange(len(self.pIDlist)):
			crtPID = self.pIDlist[i]
			prePID = self.pIDlist[[len(self.pIDlist) - 1, i - 1][i != 0]]
			nextPID = self.pIDlist[[0, i + 1][i != len(self.pIDlist) - 1]]
			# try:
			self.rdlineDict[crtPID] = RadialLine([prePID, nextPID], crtPID)
			# except:
			# 	pass
		pass



	def makeDegenerateOffset(self):
		# def makeDegOffsetByLine(pIDs,Accuracy=10**(-8)):
		# 	x1, y1, z1 = Point.PointDict[pIDs[0]].getPOSbyDecimal()
		# 	x2, y2, z2 = Point.PointDict[pIDs[1]].getPOSbyDecimal()
		# 	i1, j1, k1 = map(Decimal,self.rdlineDict[pIDs[0]].IN_direction)
		# 	i2, j2, k2 = map(Decimal,self.rdlineDict[pIDs[1]].IN_direction)
		# 	if i2 * j1 - i1 * j2 < Accuracy:
		# 		self.degenerateOffset[pIDs] = [float("inf"), float("inf")]
		# 		self.rdlineCrossPointDict[pIDs] = None
		# 		return
		# 	a = ((i2) * (y2 - y1) - (j2) * (x2 - x1)) / (i2 * j1 - i1 * j2)
		# 	b = ((j1) * (x1 - x2) - (i1) * (y1 - y2)) / (i2 * j1 - i1 * j2)
		# 	x, y = x1 + (i1) * a, y1 + (j1) * a
		# 	'''|(x1-x0)(y2-y0)-(x2-x0)(y1-y0)|/sqrt((x1-x2)^2+(y1-y2)^2)'''
		# 	degoffset = float(abs((x1 - x) * (y2 - y) - (x2 - x) * (y1 - y)) / ((x1 - x2) ** Decimal(2) + (y1 - y2) ** Decimal(2)) ** Decimal(0.5))
		# 	# degoffset = int(degoffset*10**8)/(1.0*10**8)
		# 	# if degoffset==0.0:
		#
		# 	self.rdlineCrossPointDict[pIDs] = Point.getPoint([x, y, z1])
		# 	self.degenerateOffset[pIDs] = [[degoffset, float("inf")], [float("inf"), degoffset]][a < 0]
		# 	pass

		def makeDegOffsetByLine(pIDs,Accuracy=10**(-8)):
			x1, y1, z1 = Point.PointDict[pIDs[0]].getPOS()
			x2, y2, z2 = Point.PointDict[pIDs[1]].getPOS()
			# print  self.rdlineDict[pIDs[0]].IN_direction, self.rdlineDict[pIDs[1]].IN_direction
			i1, j1, k1 = self.rdlineDict[pIDs[0]].IN_direction
			i2, j2, k2 = self.rdlineDict[pIDs[1]].IN_direction
			if abs(i2 * j1 - i1 * j2) < Accuracy:
				self.degenerateOffset[pIDs] = [float("inf"), float("inf")]
				self.rdlineCrossPointDict[pIDs] = None
				return
			a = ((i2) * (y2 - y1) - (j2) * (x2 - x1)) / (i2 * j1 - i1 * j2)
			b = ((j1) * (x1 - x2) - (i1) * (y1 - y2)) / (i2 * j1 - i1 * j2)
			x, y = x1 + (i1) * a, y1 + (j1) * a
			'''|(x1-x0)(y2-y0)-(x2-x0)(y1-y0)|/sqrt((x1-x2)^2+(y1-y2)^2)'''
			degoffset = float(abs((x1 - x) * (y2 - y) - (x2 - x) * (y1 - y)) / ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5)
			# degoffset = int(degoffset*10**8)/(1.0*10**8)
			# if degoffset==0.0:

			self.rdlineCrossPointDict[pIDs] = Point.getPoint([x, y, z1])
			self.degenerateOffset[pIDs] = [[degoffset, float("inf")], [float("inf"), degoffset]][a < 0]
			pass

		_pIDlist = self.pIDlist[:]
		_pIDlist.insert(0, _pIDlist.pop())
		_tuplePID = zip(_pIDlist, self.pIDlist)
		map(makeDegOffsetByLine, _tuplePID)

		_inDegOffset = map(lambda x: x[0], self.degenerateOffset.values())
		_outDegOffset = map(lambda x: x[1], self.degenerateOffset.values())
		self.degoffsetrange[0] = [min(_inDegOffset), max(_inDegOffset)]
		self.degoffsetrange[1] = [min(_outDegOffset), max(_outDegOffset)]
		pass

	def solveCrossLine(self, poslist):
		'''1. 检测顶点夹角为0的全部顶点，并将该点以及相关的边分裂出来'''
		t0 = time()
		if not poslist:return []
		_poslist1 = poslist[:]
		_poslist1.insert(0, _poslist1.pop())
		# _poslist1.insert(0, _poslist1.pop())
		_poslist2 = poslist[:]
		_poslist2.append(_poslist2[0])
		del _poslist2[0]

		# nearPlist = map(lambda plists: (plists[0].getPOS(), plists[1].getPOS(), plists[2].getPOS()),
		# 				zip(_poslist1, poslist, _poslist2))
		# SUBTRACT = lambda A, B: A - B
		# VECT = lambda plists: (plists[1], map(SUBTRACT, plists[0], plists[1]), map(SUBTRACT, plists[1], plists[2]))
		# _rePointlist = map(lambda p: p.getPOS(), poslist)

		nearPlist = zip(_poslist1, poslist, _poslist2)
		SUBTRACT = lambda A, B: A - B
		VECT = lambda plists: (plists[1], map(SUBTRACT, plists[0].getPOS(), plists[1].getPOS()), map(SUBTRACT, plists[1].getPOS(), plists[2].getPOS()))
		_rePointlist = poslist[:]


		# _rePointlist = map(lambda p: p.getPOS(), poslist)
		for vect in map(VECT, nearPlist):
			_p = vect[0]
			i1, j1, k1 = vect[1]
			i2, j2, k2 = vect[2]
			if i1 * j2 - i2 * j1 == 0:
				_rePointlist.remove(_p)

		# _rePointlist = map(lambda p: Point.getPoint(p), _rePointlist)
		# _rePointlist = map(lambda p: Point(p), _rePointlist)
		'''2. 计算多边形的每条边的相交关系，并将全部的交点信息记录下来，其中包含交点坐标point(x, y)，
		交点在所在的两条边的id0和id1，交点在两条边的位置rate0,rate1，
		其中point = edge0.Start+(edge0.End-edge0.Start)*rate0=edge1.Start+(edge1.End-edge1.Start)*rate1'''

		_PIDs = map(lambda p: p.ID, _rePointlist)
		_PIDs1 = _PIDs[:]
		_PIDs1.insert(0, _PIDs1.pop())
		_tuplePID = zip(_PIDs1, _PIDs)


		'''得到不相邻两直线组,直线由两点ID表示
		如果线段P1P2和直线Q1Q2相交，则P1P2跨立Q1Q2，
		即：( P1 - Q1 ) × ( Q2 - Q1 ) * ( Q2 - Q1 ) × ( P2 - Q1 ) >= 0。
		'''
		_crossLines = []
		_each2Lines = [(i[1], j[1]) for i in enumerate(_tuplePID) for j in enumerate(_tuplePID) if
					   i[0] != j[0] and abs(i[0] - j[0]) not in (1, len(_tuplePID) - 1) and i < j]

		_AddedCrossPPos = []

		'''消除四点共线'''
		# clear = False
		for P, Q in _each2Lines:
			# if Point.IfPointsInLine(PIDList=P + Q):
			if Point.IfPointsInLine(PIDList = P + Q) or \
					Point.IfPointsInLine(PIDList = list(P) + [Q[0]]) or \
					Point.IfPointsInLine(PIDList = list(P) + [Q[1]]) or \
					Point.IfPointsInLine(PIDList = list(Q) + [P[0]]) or \
					Point.IfPointsInLine(PIDList = list(Q) + [P[1]]):
				map(Point.ChangePointSmallStep,P + Q)
			# if Point.IfPointsInLine(PIDList = P + Q[0])
				# _pos = Point.PointDict[P[0]].getPOS()
				# _pos = [choice([-1, 1]) * random() / 1000 + _pos[0],
				# 	   choice([-1, 1]) * random() / 1000 + _pos[1],
				# 	   _pos[2]]
				# Point.PointDict[P[0]].setPOS(_pos)
				# _pos = Point.PointDict[P[1]].getPOS()
				# _pos = [choice([-1, 1]) * random() / 1000 + _pos[0],
				# 		choice([-1, 1]) * random() / 1000 + _pos[1],
				# 		_pos[2]]
				# Point.PointDict[P[1]].setPOS(_pos)
				# _pos = Point.PointDict[Q[0]].getPOS()
				# _pos = [choice([-1, 1]) * random() / 1000 + _pos[0],
				# 		choice([-1, 1]) * random() / 1000 + _pos[1],
				# 		_pos[2]]
				# Point.PointDict[Q[0]].setPOS(_pos)
				# _pos = Point.PointDict[Q[1]].getPOS()
				# _pos = [choice([-1, 1]) * random() / 1000 + _pos[0],
				# 		choice([-1, 1]) * random() / 1000 + _pos[1],
				# 		_pos[2]]
				# Point.PointDict[Q[1]].setPOS(_pos)



		for P, Q in _each2Lines:
			# if P == (34, 35) and Q == (39, 40):
			# 	# print Point.IfCrossByPID(P[0], P[1], Q[0], Q[1])
			# 	# print Point.GetCrossPointByPID(P[0], P[1], Q[0], Q[1])
			# 	print Point.IfPointsInLine(PIDList=(34, 35, 39))
			# 	pass
			# if P==(1969, 1970) and Point.IfCrossByPID(P[0], P[1], Q[0], Q[1]):
			# 	print P, Q
			# 	print '---',  Point.GetCrossPointByPID(P[0], P[1], Q[0], Q[1])
			# 	pass

			ifcross = Point.IfCrossByPID(P[0], P[1], Q[0], Q[1])
			if ifcross:
				# print (P[0], P[1], Q[0], Q[1])
				_crosspids = Point.GetCrossPointByPID(P[0], P[1], Q[0], Q[1], IfCrossFlag = ifcross)
				for pid in _crosspids:
					if Point.PointDict[pid].getPOS() in _AddedCrossPPos: continue
					_crossLines.append([P, Q, pid])
					_AddedCrossPPos.append(Point.PointDict[pid].getPOS())
				# _crossLines.extend([[P,Q, pid] for pid in _crosspids])
				# _AddedCrossPPos.extend(map(lambda pid:Point.PointDict[pid], _crosspids))
				# _crossLines.append([P, Q, Point.GetCrossPointByPID(P[0], P[1], Q[0], Q[1])])

		'''得到带有交点的节点ID列表'''
		_WithcrossPIDs = _PIDs[:]
		_crossPIDs = []
		# for _k in range(124,143):
		# 	print _k,Point.PointDict[_k].x,Point.PointDict[_k].y

		for (P1_id, P2_id), (Q1_id, Q2_id), cross_id in _crossLines:
			Point.InsertCrossPointIntoPointlistByPID(_WithcrossPIDs, P1_id, P2_id, cross_id)
			Point.InsertCrossPointIntoPointlistByPID(_WithcrossPIDs, Q1_id, Q2_id, cross_id)
			_crossPIDs.append(cross_id)
		_newloops = Point.GetSimpleLoopsByCrossLoop(_WithcrossPIDs, _crossPIDs)
		# if _newloops == [[2091, 2067, 2068, 2104, 2092, 2103]]:
		# 	pass
		map(Point.RemoveSAMEPoint_id, _newloops)
		_newloops = filter(lambda a: len(a) > 2, _newloops)



		# try:
		# 	filter(lambda loop: Point.IfLoopClockwise(PIDList=loop) == self.IfClockWise, _newloops)
		# except:
		# 	pass

		return filter(lambda loop: Point.IfLoopClockwise(PIDList=loop) == self.IfClockWise, _newloops)

	def getNEWPlistByOffset(self, offset,Accuracy=0.05):
		'''offset>0 向外-右	；	offset<0 向内-左'''
		# print 'getNEWPlistByOffset.offset',offset
		# if offset==0.0: return False
		# if abs(offset+2.6)<0.001:
		# 	pass
		_degoffsetrange = self.degoffsetrange[offset > 0]
		if abs(offset) > _degoffsetrange[1]: return False
		if len(self.pIDlist) < 3:return False
		# if abs(offset) <= Accuracy: return map(lambda pid:Point.PointDict[pid].getPOS(),self.pIDlist[:])

		_pIDlist = self.pIDlist[:]
		_pIDlist.insert(0, _pIDlist.pop())
		_tuplePID = zip(self.pIDlist, _pIDlist)

		if abs(offset) <= _degoffsetrange[0]+Accuracy:
			'''
			1.各边偏移得到新边，由点-矢量表示
			2.新边与角分线相交得到新点
			'''
			'''
			1. 				PID[1]					PID[0]
			假设对图片上任意点(x0,y0)，绕一个坐标点(rx0,ry0)逆时针旋转a角度后的新的坐标设为(x, y)，有公式：
				x= (x0 - rx0)*cos(a) - (y0 - ry0)*sin(a) + rx0 ;
				y= (x0 - rx0)*sin(a) + (y0 - ry0)*cos(a) + ry0 ;
			则旋转90°，公式简化为：
				x= -(y0 - ry0) + rx0 = rx0+ry0-y0;
				y= (x0 - rx0) + ry0  = ry0-rx0+x0;
			则矢量为：
				x= rx0+ry0-y0 - rx0 = ry0-y0;
				y= ry0-rx0+x0 - ry0 = -rx0+x0;
			'''
			NewPointList = []
			for _pids in _tuplePID:
				rx0, ry0 = Point.PointDict[_pids[0]].getPOS()[:2]
				x0, y0 = Point.PointDict[_pids[1]].getPOS()[:2]

				dx, dy = [[ry0 - y0, -rx0 + x0], [-ry0 + y0, rx0 - x0]][offset < 0]
				length = (dx ** 2 + dy ** 2) ** float(0.5)
				'''dx,dy 标准化'''
				dx, dy = dx / length, dy / length
				'''偏移新边：点Px,Py'''
				Px, Py = rx0 + dx * abs(offset), ry0 + dy * abs(offset)
				'''偏移新边：矢量i,j
				根据两个直线点-矢量信息，得到交点信息
				'''
				i1, j1 = x0 - rx0, y0 - ry0

				x1, y1 = Px, Py
				x2, y2 = rx0, ry0

				i2, j2, k2 = self.rdlineDict[_pids[0]].OUT_direction

				try:
					a = (i2 * (y2 - y1) - j2 * (x2 - x1)) / (i2 * j1 - i1 * j2)
					# b = (j1 * (x1 - x2) - i1 * (y1 - y2)) / (i2 * j1 - i1 * j2)
					'''新点'''
					x, y = x1 + i1 * a, y1 + j1 * a
					NewPointList.append([x, y, Point.PointDict[_pids[0]].getPOS()[-1]])
				except:
					# continue
					pass
			# if NewPointList == [[196.73929858158186, -105.25000000000003, 0.0], [198.72761038158188, -109.25000000000001, 0.0], [216.99613950000003, -109.25000000000003, 0.0], [216.99613950000003, -105.25000000000003, 0.0], [307.2441406, -105.25000000000003, 0.0], [307.2441406, -126.49179711244288, 0.0], [248.64677577477894, -189.07592769999997, 0.0], [238.4071651470266, -189.07592769999997, 0.0], [219.3076473470266, -150.65219119999998, 0.0], [219.30764323935387, -150.65219119999998, 0.0], [230.68457936278784, -173.53991499154725, 0.0], [224.9775083178169, -182.74999999999997, 0.0], [156.4289321872442, -182.74999999999997, 0.0], [148.50000000000003, -174.8210678127558, 0.0], [148.50000000000003, -150.65219119999998, 0.0], [148.49999999999997, -150.65219119999998, 0.0], [148.49999999999997, -174.8210678127558, 0.0], [140.5710678127558, -182.74999999999997, 0.0], [100.80796810000002, -182.74999999999997, 0.0], [100.80796810000002, -177.35353089999998, 0.0], [83.77620696999998, -177.35353089999998, 0.0], [83.77620696999998, -182.74999999999997, 0.0], [31.26854123073971, -182.74999999999997, 0.0], [27.367140984739716, -177.35351559999998, 0.0], [23.68905213258573, -177.35351559999998, 0.0], [20.139297260934047, -188.10602847023634, 0.0], [10.949238975207452, -194.74999999999997, 0.0], [-18.571067812755825, -194.74999999999997, 0.0], [-26.49999999999997, -186.8210678127558, 0.0], [-26.499999999999975, -177.35351559999998, 0.0], [-29.032447787244177, -177.35351559999998, 0.0], [-34.42893218724418, -182.74999999999997, 0.0], [-118.25129699999998, -182.74999999999997, 0.0], [-118.25129699999998, -177.35351559999998, 0.0], [-148.3656769, -177.35351559999998, 0.0], [-148.3656769, -182.74999999999997, 0.0], [-236.0710678127558, -182.74999999999997, 0.0], [-241.4675522127558, -177.35351559999998, 0.0], [-244.00000000000003, -177.35351559999998, 0.0], [-244.00000000000003, -186.8210678127558, 0.0], [-251.9289321872442, -194.74999999999997, 0.0], [-305.0710678127558, -194.74999999999997, 0.0], [-313.0, -186.8210678127558, 0.0], [-313.0, -177.35351559999998, 0.0], [-313.0, -177.35351559999998, 0.0], [-313.0, -186.8210678127558, 0.0], [-320.9289321872442, -194.74999999999997, 0.0], [-381.0710678127558, -194.74999999999997, 0.0], [-389.0, -186.8210678127558, 0.0], [-389.0, -177.35351559999998, 0.0], [-389.0, -177.35351559999998, 0.0], [-389.0, -194.75000000000003, 0.0], [-243.99999999999997, -194.75000000000003, 0.0], [-243.99999999999997, -190.6789321872442, 0.0], [-236.0710678127558, -182.75000000000003, 0.0], [-34.42893218724418, -182.75000000000003, 0.0], [-26.50000000000003, -190.6789321872442, 0.0], [-26.500000000000025, -194.75000000000003, 0.0], [17.94590430691003, -194.75000000000003, 0.0], [19.71410396496158, -189.39397149629104, 0.0], [28.904162208065383, -182.75000000000003, 0.0], [228.58798733583237, -182.75000000000003, 0.0], [238.23372114361817, -188.7270079183633, 0.0], [241.22761268978383, -194.75000000000003, 0.0], [386.0, -194.75000000000003, 0.0], [386.0, -105.24999999999997, 0.0], [146.49999999999997, -105.24999999999997, 0.0], [146.49999999999997, -105.25000000000003, 0.0]]:
			# 	pass
			Point.RemoveSAMEPoint(NewPointList)
			Point.RemoveSAMEPoint(NewPointList)
			
			# ReadIGESFiles.IGESFile.drawPointIntoIGESFile(
			# 	r"E:\chenbo\Program\20180320\test\output\%s.igs" % str(offset), NewPointList)
			# if NewPointList==[[-113.6825494082336, 23.04961665676222, 0.0], [-113.6825494082336, 28.181252408233604, 0.0], [-36.32136940370358, 28.181252408233608, 0.0], [-31.068747591766392, 22.92863059629642, 0.0], [-31.068747591766392, 22.784771930602826, 0.0], [-21.931252408233608, 22.784773675864407, 0.0], [-21.931252408233608, 34.92863059629642, 0.0], [-16.67863059629642, 40.181252408233604, 0.0], [9.47070577580108, 40.181252408233604, 0.0], [16.264361808078263, 35.2697647937614, 0.0], [20.386066035752023, 22.78477381448475, 0.0], [30.00862306842602, 22.784775550608863, 0.0], [29.91244213376858, 23.076115979335846, 0.0], [33.60321170967969, 28.181252408233608, 0.0], [79.20745937823361, 28.181252408233608, 0.0], [79.20745937823361, 22.784775627921867, 0.0], [105.37671569176639, 22.78477378854534, 0.0], [105.37671569176639, 28.181252408233604, 0.0], [138.67863059629641, 28.181252408233608, 0.0], [143.9312524082336, 22.928630596296422, 0.0], [143.9312524082336, -3.916554502195656, 0.0], [153.0687475917664, -3.9165540663371323, 0.0], [153.0687475917664, 22.92863059629642, 0.0], [158.32136940370359, 28.181252408233615, 0.0], [222.43377256798482, 28.181252408233608, 0.0], [225.46112950888238, 23.29569236686813, 0.0], [211.93457437150875, -3.9165545227663876, 0.0], [222.13868731234112, -3.9165545227663934, 0.0], [241.23820511234112, 34.5071725082336, 0.0], [246.66571035599577, 34.5071725082336, 0.0], [302.6753930082336, -25.313211133119506, 0.0], [302.6753930082336, -40.181252408233604, 0.0], [221.5648870917664, -40.181252408233604, 0.0], [221.5648870917664, -36.181252408233604, 0.0], [195.89657535380817, -36.181252408233604, 0.0], [193.90826355380818, -40.18125240823361, 0.0], [141.9312524082336, -40.181252408233604, 0.0], [141.9312524082336, -49.318747591766396, 0.0], [390.5687475917664, -49.318747591766396, 0.0], [390.5687475917664, 49.318747591766396, 0.0], [238.3965754932661, 49.318747591766396, 0.0], [234.72153614034585, 41.925453116212125, 0.0], [227.28721140595283, 37.318747591766396, 0.0], [30.382695407250583, 37.318747591766396, 0.0], [23.589039349857053, 42.23023522215296, 0.0], [21.248890268122885, 49.31874759176639, 0.0], [-31.068747591766396, 49.318747591766396, 0.0], [-31.068747591766392, 42.57136940370358, 0.0], [-36.321369403703585, 37.318747591766396, 0.0], [-234.17863059629641, 37.318747591766396, 0.0], [-239.4312524082336, 42.57136940370358, 0.0], [-239.4312524082336, 49.318747591766396, 0.0], [-393.5687475917664, 49.318747591766396, 0.0], [-393.5687475917664, 22.784773758233605, 0.0], [-384.4312524082336, 22.78477375823361, 0.0], [-384.4312524082336, 34.928630596296415, 0.0], [-379.17863059629644, 40.18125240823361, 0.0], [-322.82136940370356, 40.181252408233604, 0.0], [-317.5687475917664, 34.92863059629642, 0.0], [-317.5687475917664, 22.784773758233605, 0.0], [-308.4312524082336, 22.78477375823361, 0.0], [-308.4312524082336, 34.928630596296415, 0.0], [-303.17863059629644, 40.18125240823361, 0.0], [-253.82136940370359, 40.181252408233604, 0.0], [-248.5687475917664, 34.92863059629642, 0.0], [-248.5687475917664, 22.784773675864404, 0.0], [-239.4312524082336, 22.784771930602826, 0.0], [-239.4312524082336, 22.92863059629642, 0.0], [-234.17863059629641, 28.181252408233615, 0.0], [-152.9344244917664, 28.181252408233608, 0.0], [-152.9344244917664, 22.784773758233612, 0.0], [-113.32223152116465, 22.78477375823361, 0.0]]:
			# 	pass
			# if NewPointList==[[-118.251297, 32.74999999999999, 0.0], [-34.428932187688844, 32.74999999999999, 0.0], [-29.032452099561304, 27.353519910872453, 0.0], [-26.499999999999993, 27.35352039497997, 0.0], [-26.499999999999993, 36.82106781217004, 0.0], [-18.571067812170046, 44.74999999999999, 0.0], [10.949238981302535, 44.74999999999999, 0.0], [20.139296959595594, 38.106028665491884, 0.0], [23.689051401482534, 27.35352200228307, 0.0], [27.367146101837005, 27.353522666182386, 0.0], [31.268541224213674, 32.74999999999999, 0.0], [83.77620696999999, 32.74999999999999, 0.0], [83.77620696999999, 27.353522898324414, 0.0], [100.80796810000001, 27.353521701675586, 0.0], [100.80796810000001, 32.74999999999999, 0.0], [140.57106781217004, 32.74999999999999, 0.0], [148.5, 24.821067812170046, 0.0], [156.42893218782993, 32.75, 0.0], [224.97750955334232, 32.74999999999999, 0.0], [230.6845789551798, 23.539909888927, 0.0], [238.40716548613344, 39.0759201, 0.0], [248.6467755865249, 39.0759201, 0.0], [307.24414060000004, -23.508202673127055, 0.0], [307.24414060000004, -44.75000000000002, 0.0], [216.9961395, -44.74999999999999, 0.0], [216.9961395, -40.74999999999999, 0.0], [198.72761038320155, -40.74999999999999, 0.0], [196.73929858320156, -44.74999999999999, 0.0], [386.00000000000006, -44.75000000000001, 0.0], [386.0, 44.74999999999998, 0.0], [241.22761200091773, 44.75000000000001, 0.0], [238.23372113942875, 38.72701231499993, 0.0], [228.58798835472004, 32.750000000000014, 0.0], [28.90416220207009, 32.75000000000001, 0.0], [19.714103964037538, 39.393971518656585, 0.0], [17.945904309482465, 44.75000000000001, 0.0], [-26.500000000000007, 44.75000000000001, 0.0], [-26.500000000000007, 40.67893218782996, 0.0], [-34.42893218782996, 32.75000000000001, 0.0], [-236.07106781217004, 32.75000000000001, 0.0], [-244.0, 40.67893218782996, 0.0], [-244.0, 44.75000000000001, 0.0], [-389.0, 44.75000000000001, 0.0], [-389.0, 36.82106781217005, 0.0], [-381.07106781217004, 44.74999999999999, 0.0], [-320.92893218782996, 44.74999999999999, 0.0], [-313.0, 36.82106781217005, 0.0], [-305.07106781217004, 44.74999999999999, 0.0], [-251.92893218782993, 44.74999999999999, 0.0], [-244.0, 36.82106781217004, 0.0], [-244.0, 27.353520394979967, 0.0], [-241.4675479004387, 27.353519910872457, 0.0], [-236.07106781231118, 32.74999999999999, 0.0], [-148.3656769, 32.74999999999999, 0.0], [-148.3656769, 27.353521349999994, 0.0], [-118.251297, 27.353521349999994, 0.0]]:
			# 	DEBUG = True
			# 	pass

			# if NewPointList==[[386.00000000000006, -44.75000000000001, 0.0], [386.0, 44.74999999999998, 0.0], [241.22761200091773, 44.75000000000001, 0.0], [238.23372113942875, 38.72701231499993, 0.0], [228.58798835472004, 32.750000000000014, 0.0], [28.90416220207009, 32.75000000000001, 0.0], [19.714103964037538, 39.393971518656585, 0.0], [17.945904309482465, 44.75000000000001, 0.0], [-26.500000000000007, 44.75000000000001, 0.0], [-26.500000000000007, 40.67893218782996, 0.0], [-34.42893218782996, 32.75000000000001, 0.0], [-236.07106781217004, 32.75000000000001, 0.0], [-244.0, 40.67893218782996, 0.0], [-244.0, 44.75000000000001, 0.0], [-389.0, 44.75000000000001, 0.0], [-389.0, 36.82106781217005, 0.0], [-381.07106781217004, 44.74999999999999, 0.0], [-320.92893218782996, 44.74999999999999, 0.0], [-313.0, 36.821067812170035, 0.0], [-313.0, 36.82106781217005, 0.0], [-305.07106781217004, 44.74999999999999, 0.0], [-251.92893218782993, 44.74999999999999, 0.0], [-244.0, 36.82106781217004, 0.0], [-244.0, 27.353520394979967, 0.0], [-241.4675479004387, 27.353519910872457, 0.0], [-236.07106781231118, 32.74999999999999, 0.0], [-148.3656769, 32.74999999999999, 0.0], [-148.3656769, 27.353521349999994, 0.0], [-118.251297, 27.353521349999994, 0.0], [-118.251297, 32.74999999999999, 0.0], [-34.428932187688844, 32.74999999999999, 0.0], [-29.032452099561304, 27.353519910872453, 0.0], [-26.499999999999993, 27.35352039497997, 0.0], [-26.499999999999993, 36.82106781217004, 0.0], [-18.571067812170046, 44.74999999999999, 0.0], [10.949238981302535, 44.74999999999999, 0.0], [20.139296959595594, 38.106028665491884, 0.0], [23.689051401482534, 27.35352200228307, 0.0], [27.367146101837005, 27.353522666182386, 0.0], [31.268541224213674, 32.74999999999999, 0.0], [83.77620696999999, 32.74999999999999, 0.0], [83.77620696999999, 27.353522898324414, 0.0], [100.80796810000001, 27.353521701675586, 0.0], [100.80796810000001, 32.74999999999999, 0.0], [140.57106781217004, 32.74999999999999, 0.0], [148.5, 24.821067812170046, 0.0], [156.42893218782993, 32.75, 0.0], [224.97750955334232, 32.74999999999999, 0.0], [230.6845789551798, 23.539909888927, 0.0], [238.40716548613344, 39.0759201, 0.0], [248.6467755865249, 39.0759201, 0.0], [307.24414060000004, -23.508202673127055, 0.0], [307.24414060000004, -44.75000000000002, 0.0], [216.9961395, -44.74999999999999, 0.0], [216.9961395, -40.74999999999999, 0.0], [198.72761038320155, -40.74999999999999, 0.0], [196.73929858320156, -44.74999999999999, 0.0]]:
			# 	pass
			if NewPointList:
				# global NUMIGESFILENAME
				# print NUMIGESFILENAME
				pidlist = self.solveCrossLine(map(lambda pos: Point.getPoint(pos), NewPointList))
				# ReadIGESFiles.IGESFile.drawPointIntoIGESFile(
				# 	r"E:\chenbo\Program\20180320\test\output\NewPointList-%d--%s.igs" % (NUMIGESFILENAME,str(offset)), NewPointList)
				
				
				re = []
				for loop in pidlist:
					_newposlist = map(lambda pid: Point.PointDict[pid].getPOS(), loop)
					re.append(_newposlist)
				# ReadIGESFiles.IGESFile.drawPointIntoIGESFile(
				# 	r"E:\chenbo\Program\20180320\test\output\pidlist-%d--%s.igs" % (NUMIGESFILENAME, str(offset)),
				# 	re)
				# NUMIGESFILENAME = NUMIGESFILENAME + 1
				if len(re) == 1:
					re = re[0]
				return re
				# dehug 若一个轮廓分裂成多个轮廓，则应返回多个pos列表
				


			else:
				return NewPointList
			# return NewPointList
		else:
			ost = Offset(poslist = self.initplist)
			_offset = float(_degoffsetrange[0])*[-1,1][offset > 0]
			# _offset = [-1 * _degoffsetrange[0], _degoffsetrange[0]][offset > 0]
			if abs(_offset + 2.6) < 0.001:
				pass
			newPList = ost.getNEWPlistByOffset(_offset)
			if not newPList:
				return []

			'''去掉重复的点：退化得到的点'''
			if type(newPList[0][0]) == float:
				Point.RemoveSAMEPoint(newPList)
			elif type(newPList[0][0]) == list:
				map(lambda loop:Point.RemoveSAMEPoint, newPList)
			_newoffset = offset - _offset
			# print '_newoffset:',_newoffset

			if abs(_newoffset) <= Accuracy: return newPList
			# if abs(_newoffset)<0.75:
			# 	pass
			# try:
			# 	print type(newPList[0][0])
			# except:
			# 	pass
			if not newPList:
				return []
			if type(newPList[0][0]) == float:
				ost = Offset(poslist = newPList)
				return ost.getNEWPlistByOffset(_newoffset)
			elif type(newPList[0][0]) == list:
				re = []
				# if abs(_newoffset + 2.2) < 0.001:
				# 	pass
				for loop in newPList:
					# ost = Offset(poslist=loop)
					try:
						ost = Offset(poslist = loop)
					except:
						print 1
						continue
					_loop_newpos = ost.getNEWPlistByOffset(_newoffset)
					if _loop_newpos:
						if type(_loop_newpos[0][0]) == float:
							re.append(_loop_newpos)
						elif  type(_loop_newpos[0][0]) == list:
							re.extend(_loop_newpos)
				if len(re) == 1:
					re = re[0]
				return re
			# return ost.getNEWPlistByOffset(_newoffset)
		pass



	@staticmethod
	def refresh():
		RadialLine.refresh()
		Point.refresh()
		geometryLine.refresh()

	@staticmethod
	def solveCrossLoop(looplist):
		"""
		:type looplist: list
		"""
		# print '|---solveCrossLoop START!',
		t1 = time()
		debug = 0
		'''将相交loop分裂成孤立loop'''
		_looplist = looplist[:]
		_MergedPIDs = []
		i,j=[0,1]
		a=0
		# if len(looplist)==2:
		# 	if len(looplist[0])==14 and len(looplist[1])==64:
		# 		debug = True
		# 		pass
		IfLoopCrossByPIDList_SumTime = 0
		while True:
			a+=1
			if len(_looplist) <= 1 : break
			_list1,_list2 = _looplist[i], _looplist[j]
			# if len(_list1) == 8 and len(_list2) == 8:
			# 	debug = 1
			# 	pass
			if len(_list1) < 3 :
				_looplist.remove(_list1)
				i, j = [0, 1]
				continue
			if len(_list2) < 3 :
				_looplist.remove(_list2)
				i, j = [0, 1]
				continue
			t3 = time()
			_crossline = Point.IfLoopCrossByPIDList(_list1,_list2)
			IfLoopCrossByPIDList_SumTime += time() - t3
			# if debug:
			# 	print Point.IfPointsInLine(PIDList=[11313, 13470, 11314])
				# print 'solveCrossLoop._crossline1=',_crossline
			# print 'solveCrossLoop._looplist=',_looplist
			# print 'solveCrossLoop  i,j:',i,j
			_filted_crossline = []
			for _crsline in _crossline:
				for _merged in _MergedPIDs:
					if all(map(lambda p: p in _merged, _crsline[:-1])):
						_filted_crossline.append(_crsline)
						# print '_escape'
						# break
			_crossline = [_csline for _csline in _crossline if _csline not in  _filted_crossline]
			# print 'solveCrossLoop._crossline2=', _crossline
			if _crossline:
				try:
					_mergedloop = Point.GetMergedLoopsByLoops(_list1,_list2,_crossline)
				except:
					pass
				# print ''
				# def testloop(pos):
				# 	if -316<pos[0]<-310 and 39<pos[1]<43:
				# 		return True
				# 	else:
				# 		return False
				#
				# print  all(map(testloop, map(lambda pid:Point.PointDict[pid].getPOS(),_list1)))
				#
				# if all(map(testloop, map(lambda pid:Point.PointDict[pid].getPOS(),_list2))):
				# 	pass
				_looplist.remove(_list1)
				_looplist.remove(_list2)
				_looplist.extend(_mergedloop)
				_MergedPIDs.extend(_crossline)
				'''20181005: debug here'''
				i, j = [0, 1]
				continue
			j += 1
			if j == len(_looplist):
				i += 1
				j = i + 1
			if i >= len(_looplist) - 1 and j >= len(_looplist):
				break
		# print IfLoopCrossByPIDList_SumTime
		# print "1solveCrossLoop:OK", time() - t1
		'''得到各孤立loop的嵌套关系'''
		outloops,inloops = Point.GetLoopOutOrIn(_looplist)
		# for i in inloops:
		# 	ReadIGESFiles.IGESFile.drawPointIntoIGESFile(
		# 		r"G:\test\pidlist_in_%s-%s.igs" % (['Backforward','Forward'][Point.IfLoopClockwise(PIDList=i)],str(i)[:20]),
		# 		map(lambda pid: Point.PointDict[pid].getPOS(), i))
		# for i in outloops:
		# 	ReadIGESFiles.IGESFile.drawPointIntoIGESFile(
		# 		r"G:\test\pidlist_out_%s-%s.igs" % (['Backforward','Forward'][Point.IfLoopClockwise(PIDList=i)],str(i)[:20]),
		# 		map(lambda pid: Point.PointDict[pid].getPOS(), i))

		# print outloops,inloops
		re = []
		# 外侧为逆时针
		re.extend(filter(lambda loop: loop if not Point.IfLoopClockwise(PIDList=loop) else None,outloops))
		# 内侧为顺时针
		re.extend(filter(lambda loop: loop if Point.IfLoopClockwise(PIDList=loop) else None, inloops))
		# print "2solveCrossLoop:OK",time()-t1

		# print '|---solveCrossLoop ', time() - t1
		return re

	@staticmethod
	def solveCrossLoopByCut(looplist):

		'''将相交loop分裂成孤立loop'''
		_looplist = looplist[:]
		_MergedPIDs = []
		i, j = [0, 1]
		while True:
			if len(_looplist) <= 1: break
			_list1, _list2 = _looplist[i], _looplist[j]
			if len(_list1) < 3:
				_looplist.remove(_list1)
				i, j = [0, 1]
				continue
			if len(_list2) < 3:
				_looplist.remove(_list2)
				i, j = [0, 1]
				continue
			_crossline = Point.IfLoopCrossByPIDList(_list1, _list2)

			_filted_crossline = []
			for _crsline in _crossline:
				for _merged in _MergedPIDs:
					if all(map(lambda p: p in _merged, _crsline[:-1])):
						_filted_crossline.append(_crsline)

			_crossline = [_csline for _csline in _crossline if _csline not in _filted_crossline]

			if _crossline:
				_mergedloop = Point.GetMergedLoopsByLoops(_list1, _list2, _crossline)

				_looplist.remove(_list1)
				_looplist.remove(_list2)
				_looplist.extend(_mergedloop)
				_MergedPIDs.extend(_crossline)
				i, j = [0, 1]
				continue
			j += 1
			if j == len(_looplist):
				i += 1
				j = i + 1
			if i >= len(_looplist) - 1 and j >= len(_looplist):
				break

		'''得到各孤立loop的嵌套关系'''
		outloops, inloops = Point.GetLoopOutOrIn(_looplist)

		re = []
		# 保留外侧为顺时针的loop
		re.extend(filter(lambda loop: loop if  Point.IfLoopClockwise(PIDList=loop) else None, outloops))
		# 保留内侧为逆时针的loop
		re.extend(filter(lambda loop: loop if not Point.IfLoopClockwise(PIDList=loop) else None, inloops))
		# print "solveCrossLoop:OK",time()-t1
		return re


if __name__ == '__main__':
	# ost = Offset([[0,0,0],[40,0,0],[40,25,0],[0,25,0]])
	ost = Offset([[0, 0, 0], [50, 0, 0], [50, 20, 0], [25, 5, 0], [0, 20, 0]])
	poslist = ost.getNEWPlistByOffset(-3)
	# print poslist
	ost.solveCrossLine(poslist)
