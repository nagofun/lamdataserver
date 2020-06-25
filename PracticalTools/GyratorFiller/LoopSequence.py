# -*- coding: utf-8 -*-
from math import *

NearbyLoopNum = 3

class Sequence:
	SequenceID = 0
	SequenceDict = {}
	def __init__(self,p):
		if type(p)==list:
			self.x=p[0]
			self.y=p[1]
			self.z=p[2]
		else:
			self.x,self.y,self.z = p.getPOS()
		self.id = self.__class__.SequenceID
		self.__class__.SequenceID = self.__class__.SequenceID + 1
		self.__class__.SequenceDict[self.id]=self

	def getPos(self):
		return [self.x,self.y,self.z]
	@staticmethod
	def getdistance(s1,s2):
		# sqrt((s1.x-s2.x)**2 +(s1.y-s2.y)**2 +(s1.z-s2.z)**2)
		return sqrt(sum(map(lambda a,b:(a-b)**2 , s1.getPos(),s2.getPos()  )))
	@staticmethod
	def makeDistanceDict():
		DistanceDict = {}
		for i in range(len(Sequence.SequenceDict)-1):
			for j in range(i+1,len(Sequence.SequenceDict)):
				# key = ['%d-%d'%(i,j),'%d-%d'%(j,i)][i>j]
				# # print key
				if i not in DistanceDict:DistanceDict[i]={}
				if j not in DistanceDict:DistanceDict[j]={}

				DistanceDict[i][j] = Sequence.getdistance(Sequence.SequenceDict[i],Sequence.SequenceDict[j])
				DistanceDict[j][i] = Sequence.getdistance(Sequence.SequenceDict[i],Sequence.SequenceDict[j])
				
				# DistanceDict[key] = Sequence.getdistance(Sequence.SequenceDict[i],Sequence.SequenceDict[j])
				# print i,j
		# print DistanceDict
		return DistanceDict


	@staticmethod
	def refresh():
		Sequence.SequenceID = 0
		Sequence.SequenceDict = {}

		# for p in self.LoopsCenterList:
		# 	Sequence(p)

class LoopSequence:
	def __init__(self,pointslist):
		self.DistanceDict = {}
		list(map(Sequence,pointslist))
	def makeDistanceDict(self):
		def start_from_one_point(nearbylist_dict,startpid):
			'''从指定一点出发，找到最近的下一点，再以此为起点继续寻找最近的下一点'''
			re_seqlist = []
			re_distance = 0.0
			thispid = startpid
			while True:
				re_seqlist.append(thispid)

				if len(re_seqlist)==len(nearbylist_dict):break
				for pid in nearbylist_dict[thispid]:
					if pid in re_seqlist:continue
					re_distance+=self.DistanceDict[thispid][pid]
					thispid = pid

					break

				
				pass
			return re_seqlist,re_distance
		global NearbyLoopNum
		'''初始化DistanceDict，根据两点id可获取两点间距'''
		if len(Sequence.SequenceDict)<1:
			return []
		if len(Sequence.SequenceDict)==1:
			# print Sequence.SequenceDict[0].getPos()
			return 	[Sequence.SequenceDict[0].getPos()]
		self.DistanceDict = Sequence.makeDistanceDict()
		# print self.DistanceDict
		
		'''按距离排序，获取每个点周围最近若干点的列表'''
		point_nearbylist_dict = {}
		for p_id in self.DistanceDict:
			point_nearbylist_dict[p_id] = []
			nearby_dict = self.DistanceDict[p_id]

			temp = sorted(nearby_dict.items(), key=lambda d: d[1])  #[:NearbyLoopNum]
			point_nearbylist_dict[p_id] = map(lambda x:x[0],temp)
		
		'''获得每一个点作为起点时的路径长度，选取长度最短的组合'''
		seq_and_distance = map(lambda pid:start_from_one_point(point_nearbylist_dict,pid),self.DistanceDict)
		nearest_sequence = sorted(seq_and_distance,key = lambda d:d[1])[0][0]
		# print nearest_sequence

		return map(lambda pid:Sequence.SequenceDict[pid].getPos(),nearest_sequence)

		'''获取所有可能的组合'''
		# SequenceIds = Sequence.SequenceDict.keys()
		# order = '('
		# order_for = ''
		# order_if = ''
		# for i in SequenceIds:
		# 	order += 'P%d,'%i
		# 	order_for += ' for P%d in SequenceIds'%i
		# order = order[:-1]+')'
		# order = '[' + order + order_for + ' if len(%s)==len(set(%s))'%(str(order),str(order)) +']'
		# _seq_lists = eval(order)
		# print len(_seq_lists)

		pass
if __name__ == "__main__":
	pointslist = [[0.0, 0.0, 0.0], [175.3089709528, 29.310573597899996, 0.0], [30.1435161902116, 90.84487052168642, 0.0], [-174.18993950419937, 35.954116968664785, 0.0], [-65.994517110467, -87.50387943469696, 0.0], [81.69642635905447, -34.82877415718088, 0.0], [-109.27351961678096, 82.43673613598246, 0.0], [-89.11715260463292, -26.588139310331734, 0.0], [-37.834366278999994, 98.78997941239997, 0.0], [93.03419024195, 82.06232579445, 0.0], [134.6520647802779, 67.11952248146662, 0.0], [198.9070659713, 95.088621911, 0.0], [124.43838388843353, -63.19162878632765, 0.0], [17.2559842696, -75.79496347675, 0.0], [-157.2432591341266, -40.475490546998515, 0.0], [-58.524371513428015, 32.83162628570558, 0.0], [-15.843962809665225, 164.84699701170123, 0.0], [-86.300762568, 183.74111026975, 0.0], [-149.81347553915, 129.4716768082, 0.0], [80.09985546318006, 155.57530827929511, 0.0], [152.7699700127, 144.7762440017, 0.0], [40.30239384508927, 192.06375885744052, 0.0], [40.716297273658796, 32.19694628381023, 0.0], [160.93075723167954, -5.747182106836016, 0.0], [49.05137407408613, -26.65845328226868, 0.0], [-222.95690796514995, 70.04390240194999, 0.0], [-196.07695472733752, 125.42869030790733, 0.0], [-15.971867740128378, 295.3387152483445, 0.0], [-51.22062213529613, 245.4625254244397, 0.0], [44.306370033147005, 261.649315250323, 0.0], [74.68241532687226, 223.48341984724436, 0.0], [143.05308756722917, 214.3175470836175, 0.0]]
	MyLoopSequence = LoopSequence(pointslist)
	MyLoopSequence.makeDistanceDict()