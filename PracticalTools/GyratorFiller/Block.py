#!/usr/bin/env python
#coding:utf-8
from math import *
from time import *
from geometry import Point

# class Point():
# 	ID = 1
# 	PointDict = {}
# 	PosDict = {}
# 	def __init__(self,pos):
# 		self.pos = pos
# 		self.x=pos[0]
# 		self.y=pos[1]
# 		self.z=pos[2]

# 		self.ID = Point.ID
# 		Point.ID+=1
# 		Point.PointDict[self.ID] = self
# 		# return self.ID
		
# 	def getPOS(self):
# 		return self.pos
# 	def getDistence(self,p):
# 		return sqrt((self.pos[0]-p.pos[0])**2+(self.pos[1]-p.pos[1])**2)
# 	def getDistenceByPOS(self,pos):
# 		return sqrt((self.pos[0]-pos[0])**2+(self.pos[1]-pos[1])**2)

# 	@staticmethod
# 	def refresh():
# 		Point.ID = 1
# 		Point.PointDict = {}
# 	@staticmethod
# 	def getPoint(pos):
# 		return Point(pos)
# 		pass
# 		# _key = '%d,%d,%d'%tuple(pos)
# 		# if _key in Point.PosDict:
# 		# 	Point.PosDict.append()

class layer():
	def __init__(self,LoopPointsListDict,LoopLayerDict,BLOCKSTEP = 5,MINBIGLINE = 2):

		self.LoopPointsListDict = LoopPointsListDict.copy()
		self.LoopLayerDict = LoopLayerDict.copy()
		self.BlockStep = BLOCKSTEP
		self.MinBigLine = MINBIGLINE

		self.LoopBigLineListDict = {}
		# print self.LoopLayerDict
		# print self.LoopPointsListDict
		# for loopid in self.LoopPointsListDict:
		# 	print map(lambda p:p.getPOS(),self.LoopPointsListDict[loopid])
	def __getDistanceOfSegments__(self,P1,P2,Q1,Q2):
		def PointToSegment(O,M,N):
			'''求O点到线段MN的距离'''
			_MN = map(lambda a,b:a-b,N.getPOS(),M.getPOS())
			_NM = map(lambda a,b:a-b,M.getPOS(),N.getPOS())
			_MO = map(lambda a,b:a-b,O.getPOS(),M.getPOS())
			_NO = map(lambda a,b:a-b,O.getPOS(),N.getPOS())
			if sum(map(lambda a,b:a*b,_NM,_NO)) <= 0:
				return [O.getDistence(N),O,N]
			if sum(map(lambda a,b:a*b,_MN,_MO)) <= 0:
				return [O.getDistence(M),O,M]

			'''r = cross / d2
			double cross = (x2 - x1) * (x - x1) + (y2 - y1) * (y - y1);
			double d2 = (x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1);
			double r = cross / d2;
			double px = x1 + (x2 - x1) * r;
			double py = y1 + (y2 - y1) * r;
			'''
			cross = sum(map(lambda a,b:a*b,_MN,_MO))
			d2 = sum(map(lambda a,b:a*b,_MN,_MN))
			r =  cross/d2
			NewPOS = map(lambda a,b:a+(b-a)*r,M.getPOS(),N.getPOS())
			NewP = Point.getPoint(NewPOS)
			return [O.getDistence(NewP),O,NewP]


		'''
		FUNCTION __getDistanceOfSegments__ START
		'''	
		'''得到两线段间最短距离，假定两线段不相交'''
		distance = []
		distance.append(PointToSegment(P1,Q1,Q2))
		distance.append(PointToSegment(P2,Q1,Q2))
		distance.append(PointToSegment(Q1,P1,P2))
		distance.append(PointToSegment(Q2,P1,P2))
		return sorted(distance,key=lambda d:d[0])[0]
		

	def getBigLine(self):
		for loopid in self.LoopPointsListDict:
			self.LoopBigLineListDict[loopid] = []
			_points = self.LoopPointsListDict[loopid]

			_id1_m = range(len(_points))
			_id1_n = _id1_m[:]
			_id1_n.insert(0,_id1_n.pop())
			for i,j in zip(_id1_m,_id1_n):
				if _points[i].getDistence(_points[j]) > self.MinBigLine:
					self.LoopBigLineListDict[loopid].append([_points[i],_points[j]])
				# print i,j
		# print self.LoopBigLineListDict 	
	def BreakLoopsIntoOneLoop(self):
		def getLoopDistance(loopid1,loopid2):
			'''FUNCTION getLoopDistance START'''
			'''loopid1应为内部loop，则顶点按顺时针排序'''
			self.LoopBigLineListDict
			loop1_pointslist = self.LoopBigLineListDict[loopid1]
			loop2_pointslist = self.LoopBigLineListDict[loopid2]
			distancelist = []
			for P1,P2 in loop1_pointslist:
				for Q1,Q2 in loop2_pointslist:
					distancelist.append(self.__getDistanceOfSegments__(P1,P2,Q1,Q2))
			# print sorted(distancelist,key=lambda d:d[0])[0][2].getPOS()
			
			pass
			'''FUNCTION END'''
		
		'''FUNCTION BreakLoopsIntoOneLoop START'''
		self.getBigLine()
		for outloopid in self.LoopLayerDict:
			_accessed = []
			for inloopid in self.LoopLayerDict[outloopid]:
				# 对每个内部的loop的各定点均计算一遍最近相邻loop距离
				getLoopDistance(inloopid,outloopid)
				for other_inloopid in [i for i in self.LoopLayerDict[outloopid] if i != inloopid]:
					if '%d,%d'%(other_inloopid,inloopid) in _accessed: break
					getLoopDistance(inloopid,other_inloopid)
					_accessed.append('%d,%d'%(inloopid,other_inloopid))
					_accessed.append('%d,%d'%(other_inloopid,inloopid))

					# print outloopid,inloopid
		# 	# print map(lambda p:p.getPOS(),self.LoopPointsListDict[outloopid])
		pass