#!/usr/bin/env python
#coding:utf-8
from math import sqrt,acos,pi
import random
from time import *
import itertools
# from decorator_demo import *
from decimal import Decimal

# EQUAL_ACCURACY = 10**(-5)
# EQUAL_ACCURACY = Decimal(0)
EQUAL_ACCURACY = 0



class Point():
    ID = 1
    PointDict = {}
    POSDict = {}
    DEBUG_TIME1 = 0
    DEBUG_TIME2 = 0
    DEBUG_TIME3 = 0
    def __init__(self,pos):
        self.pos = list(map(float, map(lambda i: round(i, 9), pos)))
        if len(self.pos)>=3:
            self.x,self.y,self.z = self.pos[:3]
        self.ID = Point.ID
        # if self.ID == 3991:
        # 	pass
        Point.ID+=1
        Point.PointDict[self.ID] = self
        # try:
        # 	key = '%d-%d-%d'%tuple(pos)
        # except Exception, e:
        # 	print pos
        # 	return
        key = '%d-%d-%d'%tuple(self.pos)
        if key in Point.POSDict:
            Point.POSDict[key].append(self.ID)
        else:
            Point.POSDict[key] = [self.ID]
        # return self.ID

    def getID(self):
        return self.ID

    def setPOS(self,pos):
        self.pos = map(float,pos)
        if len(self.pos)>=3:
            self.x,self.y,self.z = self.pos[:3]

    def getPOSbyDecimal(self):
        return map(Decimal,self.pos)

    def getPOS(self):
        # return map(float,self.pos)
        return self.pos

    def getDistence(self,p):
        return ((self.pos[0]-p.pos[0])**2+(self.pos[1]-p.pos[1])**2)**0.5

    def getDistenceByPOS(self,pos):
        return ((self.pos[0]-pos[0])**2+(self.pos[1]-pos[1])**2)**0.5
    
    def getDistenceToLineByID(self,PID1,PID2):
        '''
        a for PID1,b for PID2
        c for self
        
        :param PID1:
        :param PID2:
        :return:
        '''
        P1_pos = Point.PointDict[PID1].getPOS()
        P2_pos = Point.PointDict[PID2].getPOS()
        vector_ab = list(map(lambda x,y:x-y,P2_pos,P1_pos))
        vector_ac = list(map(lambda x,y:x-y,self.getPOS(),P1_pos))
        f = sum(list(map(lambda i,j:i*j,vector_ab,vector_ac)))
        if f < 0: return self.getDistenceByPOS(P1_pos)
        d = sum(list(map(lambda i,j:i*j,vector_ab,vector_ab)))
        if f > d: return self.getDistenceByPOS(P2_pos)
        f = f/d
        footP = Point(list(map(lambda a, ab : a+f*ab, P1_pos, vector_ab)))
        return self.getDistence(footP)

    def getDistenceToLoop(self,PList):
        _distance = 100000000000000000000
        PList2 = PList[:]
        PList2.insert(0, PList2.pop())
        _tupleP = zip(PList2, PList)
        for tp in _tupleP:
            # if _distance >= max(abs(self.x-tp[0].x),abs(self.y-tp[0].y),abs(self.x-tp[1].x),abs(self.y-tp[1].y)):

            _distance = min(_distance,self.getDistenceToLineByID(tp[0].getID(),tp[1].getID()))
            # pass
        return _distance

    def getXYZone(self):
        return '%d-%d'%(self.pos[0],self.pos[1])

    @staticmethod
    def getDistencebyID(pid1,pid2):
        return Point.PointDict[pid1].getDistence(Point.PointDict[pid2])

    @staticmethod
    def getPoint(pos):
        pos = list(map(float,pos))
        key = '%d-%d-%d'%tuple(pos)
        if key == '183--241-0':
            pass
        # if key not in Point.POSDict:
        # 	return Point(pos)
        if key in Point.POSDict:
            for _id in Point.POSDict[key]:
                # if Point.PointDict[_id].getDistenceByPOS(pos) == 0.0:
                if sum(map(lambda a,b:a==b,pos,Point.PointDict[_id].getPOS()))==len(pos):
                # if sum(map(lambda a,b:a-b,pos,Point.PointDict[_id].getPOS()))==0:
                    return Point.PointDict[_id]
        return Point(pos)

    @staticmethod
    def getDifferentPoint(pos):
        pos = map(float, pos)
        key = '%d-%d-%d' % tuple(pos)
        if key in Point.POSDict:
            for _id in Point.POSDict[key]:
                if sum(map(lambda a, b: a == b, pos, Point.PointDict[_id].getPOS())) == len(pos):
                    _pos = pos[:]
                    _pos[:2] = map(lambda a: a + random.uniform(1, 10) * (10 ** (-3)), pos[:2])
                    return Point(_pos)
        return Point(pos)

    @staticmethod
    def ChangePointSmallStep(pid):
        _pos = Point.PointDict[pid].getPOS()
        _pos = [random.choice([-1, 1]) * random.random() / 100 + _pos[0],
                random.choice([-1, 1]) * random.random() / 100 + _pos[1],
                _pos[2]]
        Point.PointDict[pid].setPOS(_pos)

    @staticmethod
    def getPosRangeOfPIDList(PIDlist):
        PosRange = [Point.PointDict[p].getPOS() for p in PIDlist]
        _XRange,_YRange = zip(*PosRange)[:2]
        return [[min(_XRange),max(_XRange)],[min(_YRange),max(_YRange)]]

    @staticmethod
    def refresh():
        Point.ID = 1
        Point.PointDict = {}
        Point.POSDict = {}

    @staticmethod
    def IfPointNearLoop(PIDlist,Pid,distance):
        '''
        根据ID，判断点是否在loop附近，以distance为界
        :param PIDlist:
        :param Pid:
        :param distance:
        :return:
        '''
        for i in range(len(PIDlist)):
            j = [i + 1, 0][i == len(PIDlist) - 1]
            if Point.PointDict[Pid].getDistenceToLineByID(PIDlist[i],PIDlist[j]) <= distance:
                return True
        return False

    @staticmethod
    def IfLineParallelAndNearLoop(PIDlist,P1,P2,distance):
        '''
        给定两点连成的线段是否与Loop中某一条边平行且距离不超过给定distance
        考虑自愈性，设计Pid1与Pid2分别距离Loop某一线段距离不超过给定distance来判断
        :param PIDlist:
        :param Pid1:
        :param Pid2:
        :param distance:
        :return:
        '''
        re = False
        for i in range(len(PIDlist)):
            j = [i + 1, 0][i == (len(PIDlist) - 1)]
            if P1.getDistenceToLineByID(PIDlist[i].getID(), PIDlist[j].getID()) <= distance and P2.getDistenceToLineByID(PIDlist[i].getID(), PIDlist[j].getID()) <= distance:
                re = True
                break
        return re

    @staticmethod
    def IfLoopConnectedWithLoop(PIDlist1,PIDlist2,distance):
        
        pass
        
    @staticmethod
    def IfLoopClockwise(PList=[],PIDList=[]):
        if len(PIDList)>0:
            try:
                plist = map(lambda pid:Point.PointDict[pid],PIDList)
            except:
                print('===', PIDList)
        else:
            plist = PList

        Xlist = map(lambda p:p.getPOS()[0],plist)

        maxX_p = filter(lambda i,x:x == max(Xlist),list(enumerate(Xlist)))[0][0]
        maxX_p_i = [len(Xlist)-1,maxX_p-1][maxX_p>0]
        maxX_p_j = [0,maxX_p+1][maxX_p<len(Xlist)-1]
        [x,y] = plist[maxX_p].getPOS()[:2]
        [x_i,y_i] = plist[maxX_p_i].getPOS()[:2]
        [x_j,y_j] = plist[maxX_p_j].getPOS()[:2]
        if (x - x_i) * (y_j - y) - (y - y_i) * (x_j - x)>0:
            '''逆时针loop'''
            return False
        else:
            '''顺时针loop'''
            return True

    @staticmethod
    def IfLoopContainPointByPID(PIDlist,PID):
        '''return Out,In,On'''
        _Xrange,_Yrange = Point.getPosRangeOfPIDList(PIDlist)
        _point = Point.PointDict[PID]
        if _point.x < _Xrange[0] or _point.x > _Xrange[1] or _point.y < _Yrange[0] or _point.y > _Yrange[1]:
            return 'Out'

        _loop_y_values = map(lambda pid: Point.PointDict[pid].y ,PIDlist)
        _orininY = _point.y
        while True:
            if _point.y in _loop_y_values:
                _point.y += random.random() * 0.0001
            else:
                break
        nCross = 0
        for i in range(len(PIDlist)):
            j = [i + 1, 0][i == (len(PIDlist) - 1)]
            p1 = Point.PointDict[PIDlist[i]]
            p2 = Point.PointDict[PIDlist[j]]

            if Point.IfPointsInLine(PList=[p1,_point,p2]):
	            if p1.getDistence(p2) == p1.getDistence(_point) + p2.getDistence(_point):
	                return 'On'
            if _point.y < min(p1.y, p2.y):
                continue
            if _point.y > max(p1.y, p2.y):
                continue
            if p1.y == p2.y:
                '''p1.y==p2.y==pos[1]'''
                m = [len(PIDlist) - 1, i - 1][i != 0]
                n = [0, j + 1][j != (len(PIDlist) - 1)]
                p3 =  Point.PointDict[PIDlist[m]]
                p4 =  Point.PointDict[PIDlist[n]]
                if (p3.y - p2.y) * (p4.y - p2.y) < 0:
                    nCross += 1
                continue
            if p1.y == _point.y:
                m = [len(PIDlist) - 1, i - 1][i != 0]
                p3 = Point.PointDict[PIDlist[m]]
                if (p3.y - p1.y) * (p2.y - p1.y) < 0 and p1.x > _point.x:
                    nCross += 0.5
                continue
            if p2.y == _point.y:
                n = [0, j + 1][j != (len(PIDlist) - 1)]
                p4 = Point.PointDict[PIDlist[n]]
                if (p1.y - p2.y) * (p4.y - p2.y) < 0 and p1.x > _point.x:
                    nCross += 0.5
                continue
            x = 1.0 * ( _point.y - p1.y) * (p2.x - p1.x) / (p2.y - p1.y) + p1.x
            if x >  _point.x:
                nCross += 1

        _point.y = _orininY
        return ['Out','In'][(nCross % 2 == 1)]
        # if : return 'In' else: return 'Out'

    @staticmethod
    def IfLoopContainLoopByPIDs(PIDlist1, PIDlist2):
        '''
        PIDlist1 是否包含PIDlist2
        return True: PIDlist1 contain PIDlist2
                False : not contain
        '''
        LMD_contain = lambda pid: [False, True][Point.IfLoopContainPointByPID(PIDlist1, pid) in ['In', 'On']]
        # LMD_contain2 = lambda pid: [False,True][Point.IfLoopContainLoopByPIDs(PIDlist2, pid) in ['In','On']]
        new_PIDlist2 = PIDlist2[:]
        for i in range(len(PIDlist2)):
            j = [i + 1, 0][i == len(PIDlist2) - 1]
            new_PIDlist2.append(Point.getPoint(
                map(lambda a, b: (a + b) * 0.5, Point.PointDict[PIDlist2[i]].getPOS(),
                    Point.PointDict[PIDlist2[j]].getPOS())).getID())
            new_PIDlist2.append(Point.getPoint(
                map(lambda a, b: 0.25*a + 0.75*b, Point.PointDict[PIDlist2[i]].getPOS(),
                    Point.PointDict[PIDlist2[j]].getPOS())).getID())
            new_PIDlist2.append(Point.getPoint(
                map(lambda a, b: 0.75 * a + 0.25 * b, Point.PointDict[PIDlist2[i]].getPOS(),
                    Point.PointDict[PIDlist2[j]].getPOS())).getID())
        # re = map(LMD_contain,new_PIDlist2)
        outnum = 0
        innum = 0
        for pid in new_PIDlist2:
            relation = Point.IfLoopContainPointByPID(PIDlist1, pid)
            # print relation
            if relation == 'Out':
                outnum += 1
            elif relation == 'In':
                innum += 1
        if outnum > innum:
            return False
        else:
            return True
        return True

    @staticmethod
    def IfLoopContainLoopByPIDs_NoOutPoint(PIDlist1, PIDlist2):
        '''暂未使用
        PIDlist1 与 PIDlist2 是否存在至少1处公共节点
        return True: PIDlist1 contain PIDlist2
                False : not contain
        '''
        LMD_contain = lambda pid: [False, True][Point.IfLoopContainPointByPID(PIDlist1, pid) in ['Out']]
        # LMD_contain2 = lambda pid: [False,True][Point.IfLoopContainLoopByPIDs(PIDlist2, pid) in ['In','On']]
        new_PIDlist2 = PIDlist2[:]
        for i in range(len(PIDlist2)):
            j = [i + 1, 0][i == len(PIDlist2) - 1]
            new_PIDlist2.append(
                Point.getPoint(map(lambda a, b: (a + b) * 0.5, Point.PointDict[PIDlist2[i]].getPOS(),
                                   Point.PointDict[PIDlist2[j]].getPOS())).getID())
        re = map(LMD_contain, new_PIDlist2)
        # if not any(re):
        #     print re,not any(re)
        return not any(re)

    @staticmethod
    def IfLoopContainLoopByPIDs_absoluteIN(PIDlist1, PIDlist2):
        '''
        PIDlist1 是否包含PIDlist2
        return True: PIDlist1 contain PIDlist2
                False : not contain
        '''
        LMD_contain = lambda pid: [False, True][Point.IfLoopContainPointByPID(PIDlist1, pid) in ['In']]
        # LMD_contain2 = lambda pid: [False,True][Point.IfLoopContainLoopByPIDs(PIDlist2, pid) in ['In','On']]
        new_PIDlist2 = PIDlist2[:]
        for i in range(len(PIDlist2)):
            j = [i + 1, 0][i == len(PIDlist2) - 1]
            new_PIDlist2.append(
                Point.getPoint(map(lambda a, b: (a + b) * 0.5, Point.PointDict[PIDlist2[i]].getPOS(),
                                   Point.PointDict[PIDlist2[j]].getPOS())).getID())
        re = map(LMD_contain, new_PIDlist2)
        return all(re)

    @staticmethod
    def IfLoopsContain_Or_Not_Or_Cross_Line(loops,tuplePID,Pid1,Pid2):
        '''
        线段P1P2与轮廓outloops、inloops判断相交，
            如无交点，则
                P1被包含奇数次                返回contain
                P1被包含偶数次                返回notcontain

                P1在外轮廓内且在内轮廓外       返回contain
                P1在外轮廓外或在内轮廓内       返回notcontain
            如有交点，则记录交点信息？            返回cross
        :param outloops: 外轮廓
        :param inloops: 内轮廓
        :param P1: Point实体
        :param P2: Point实体
        :return:关系
        '''
        #
        re = None
        ifcrs = None
        crossinfo = []
        # 1. 判断是否相交
        for pid1,pid2 in tuplePID:
            ifcrs = Point.IfCrossByPID(pid1,pid2,Pid1,Pid2)
            if ifcrs:
                re = 'cross'
                crossinfo.append([pid1,pid2])
                # break
        if re == None:
            # 2.判断是否包含
            containnum = 0
            for loop in loops:
                # if 408 <Point.PointDict[Pid1].getPOS()[0] < 468 and 20 <Point.PointDict[Pid1].getPOS()[1] < 100:
                #     pass
                if Point.IfLoopContainPointByPID(loop,Pid1) == 'In':
                    containnum += 1

            if containnum== 0:
                pass
            re = ['notcontain','contain'][containnum % 2 == 1]
        return [re,crossinfo]

    @staticmethod
    def IfLoopCrossByPIDList(PIDlist1,PIDlist2):
        """

        :rtype: object
        """
        t1=time()
        List1_X, List1_Y = Point.getPosRangeOfPIDList(PIDlist1)
        List2_X, List2_Y = Point.getPosRangeOfPIDList(PIDlist2)
        if List1_X[0]>List2_X[1] or List1_X[1]<List2_X[0] \
            or List1_Y[0]>List2_Y[1] or List1_Y[1]<List2_Y[0]:
            return []
        '''依次取两loop中线段比较 20160724'''
        _pIDlist = PIDlist1[:]
        _pIDlist.insert(0, _pIDlist.pop())
        _tuplePID1 = zip(_pIDlist,PIDlist1)
        _pIDlist = PIDlist2[:]
        _pIDlist.insert(0, _pIDlist.pop())
        _tuplePID2 = zip(_pIDlist, PIDlist2)
        t2 = time()
        '''20181031'''
        # _tuplePID1=[(PIDlist1[i],PIDlist1[[0,i+1][i<len(PIDlist1)-1]]) for i in range(len(PIDlist1))]
        # _tuplePID2=[(PIDlist2[i],PIDlist2[[0,i+1][i<len(PIDlist2)-1]]) for i in range(len(PIDlist2))]
        # [P1,P2,Q1,Q2,Point.GetCrossPointByPID(P1,P2,Q1,Q2)]
        # return [[P1, P2, Q1, Q2, Point.GetCrossPointByPID(P1, P2, Q1, Q2)] for P1, P2 in _tuplePID1 \
        #         for Q1, Q2 in _tuplePID2 if Point.IfCrossByPID(P1, P2, Q1, Q2)]
        '''20181101'''
        # re = [   (P1,P2,Q1,Q2,_cross)   for P1,P2 in _tuplePID1 \
        #     for Q1,Q2 in _tuplePID2 if Point.IfCrossByPID(P1,P2,Q1,Q2) for _cross in Point.GetCrossPointByPID(P1,P2,Q1,Q2) ]
        re = []
        for i in itertools.product(_tuplePID1, _tuplePID2):
            if Point.IfCrossByPID(i[0][0],i[0][1],i[1][0],i[1][1]):
                for _cross in Point.GetCrossPointByPID(i[0][0],i[0][1],i[1][0],i[1][1]):
                    re.append((i[0][0],i[0][1],i[1][0],i[1][1],_cross  ))
        t3 = time()
        filter_re = filter(lambda l: Point.PointDict[l[4]].getPOS() != Point.PointDict[l[0]].getPOS() or Point.PointDict[l[4]].getPOS() != Point.PointDict[l[2]].getPOS()  , re)
        # print re
        t4 = time()


        Point.DEBUG_TIME1 += t2 - t1
        Point.DEBUG_TIME2 += t3 - t2
        Point.DEBUG_TIME3 += t4 - t3
        return filter_re



    @staticmethod
    def IfCrossByPID(P1_id,P2_id,Q1_id,Q2_id,Accuracy=EQUAL_ACCURACY):
        '''得到不相邻两直线组,直线由两点ID表示
        如果线段P1P2和直线Q1Q2相交，则P1P2跨立Q1Q2，
        即：( P1 - Q1 ) × ( Q2 - Q1 ) * ( Q2 - Q1 ) × ( P2 - Q1 ) >= 0。
        '''
        # while Point.IfPointsInLine(PIDList=[P1_id, P2_id, Q1_id, Q2_id]):
        # 	_pos = Point.PointDict[P1_id].getPOS()
        # 	_pos[:2] = map(lambda a: a + random.uniform(1, 10)*(10**(-4)),_pos[:2])
        # 	Point.PointDict[P1_id].setPOS( _pos )
        #
        # 	_pos = Point.PointDict[P2_id].getPOS()
        # 	_pos[:2] = map(lambda a: a + random.uniform(1, 10)*(10**(-4)), _pos[:2])
        # 	Point.PointDict[P2_id].setPOS(_pos)
        #
        # 	_pos = Point.PointDict[Q1_id].getPOS()
        # 	_pos[:2] = map(lambda a: a + random.uniform(1, 10)*(10**(-4)), _pos[:2])
        # 	Point.PointDict[Q1_id].setPOS(_pos)
        #
        # 	_pos = Point.PointDict[Q2_id].getPOS()
        # 	_pos[:2] = map(lambda a: a + random.uniform(1, 10)*(10**(-4)), _pos[:2])
        # 	Point.PointDict[Q2_id].setPOS(_pos)

        P1,P2,Q1,Q2 = map(lambda i: Point.PointDict[i].getPOS()[:2],(P1_id,P2_id,Q1_id,Q2_id))
        if (P1_id, P2_id, Q1_id, Q2_id) == (47,48,51,52):
            pass
        # P1, P2, Q1, Q2 = map(lambda i: Point.PointDict[i].getPOSbyDecimal()[:2], (P1_id, P2_id, Q1_id, Q2_id))
        # lmd_outer = lambda p1,p2:(p1[0]*p2[1]-p1[1]*p2[0])
        lmd_outer = lambda p1, p2: (0, (p1[0] * p2[1] - p1[1] * p2[0]))[abs(p1[0] * p2[1] - p1[1] * p2[0]) > Accuracy]
        lmd_subduct = lambda a,b:(0, a-b)[abs(a-b) > Accuracy]
        # if (lmd_outer(map(lambda a,b:a-b,P1,Q1), map(lambda a,b:a-b,Q2,Q1)) * \
        #     lmd_outer(map(lambda a,b:a-b,Q2,Q1), map(lambda a,b:a-b,P2,Q1)) >0) \
        #     and \
        #     (lmd_outer(map(lambda a,b:a-b,Q1,P1), map(lambda a,b:a-b,P2,P1)) * \
        #     lmd_outer(map(lambda a,b:a-b,P2,P1), map(lambda a,b:a-b,Q2,P1)) >0):
        #     '''此处存在问题'''

        if (lmd_outer(map(lmd_subduct, P1, Q1), map(lmd_subduct, Q2, Q1)) * \
                    lmd_outer(map(lmd_subduct, Q2, Q1), map(lmd_subduct, P2, Q1)) > 0) \
                and \
                (lmd_outer(map(lmd_subduct, Q1, P1), map(lmd_subduct, P2, P1)) * \
                         lmd_outer(map(lmd_subduct, P2, P1), map(lmd_subduct, Q2, P1)) > 0):
            return 1
        else:
            def between(a,b,c):
                return True if (a < b < c or a > b > c) and (abs(a-b) > 10e-4 and abs(b-c) > 10e-4) else False
            # 共点但不共线：
            # |-首首相遇                            7处理，返回起点
            if not Point.IfPointsInLine(PIDList=(P1_id, P2_id, Q1_id, Q2_id)) and P1 == Q1:
                return 7
            # 三点共线: 一条线段的起点与另一条线段共线，且落入其中，终点不共线     2处理  返回落入的起点
            if Point.IfPointsInLine(PIDList=(P1_id, P2_id, Q1_id)) and (between(P1[0], Q1[0], P2[0]) or between(P1[1], Q1[1], P2[1])) and not Point.IfPointsInLine(PIDList=(P1_id, P2_id, Q2_id)) \
                    or Point.IfPointsInLine(PIDList=(Q1_id, Q2_id, P1_id)) and (between(Q1[0], P1[0], Q2[0]) or between(Q1[1], P1[1], Q2[1])) and not Point.IfPointsInLine(PIDList=(Q1_id, Q2_id, P2_id)):
                return 2
            # 四点共线：
            # |-1.端点重合：
            # |----1.1首尾相衔成环                       3处理  返回两端点
            # |----1.2首尾相衔不成环,起点居中              4处理  返回起点
            # |----1.3首尾相衔不成环,终点居中              0暂时不处理
            # |----1.4首首相遇                          5处理  返回起点
            # |-2.端点不重合
            # |----2.1起点被包含                        6处理  返回被包含方起点
            #                                           错：测试此处按0返回比较合适 N2 全轮廓填充 0182.igs
            if Point.IfPointsInLine(PIDList=[P1_id, P2_id, Q1_id, Q2_id]):
                # |----1.1首尾相衔成环
                if P1 == Q2 and P2 == Q1:
                    # 首尾相衔成环 进行处理
                    return 3
                # |----1.2首尾相衔不成环，起点居中
                elif P1 == Q2 and (between(P1[0], Q1[0], P2[0]) or between(P1[1], Q1[1], P2[1]))\
                        or P2 == Q1 and (between(Q1[0], P1[0], Q2[0]) or between(Q1[1], P1[1], Q2[1])):
                    return 4
                # |----1.3首尾相衔不成环,终点居中
                elif P1 == Q2 and (between(Q1[0], P2[0], Q2[0]) or between(Q1[1], P2[1], Q2[1])) \
                        or P2 == Q1 and (between(P1[0], Q1[0], P2[0]) or between(P1[1], Q1[1], P2[1])):
                    return 0
                # |----1.4首首相遇
                elif P1 == Q1:
                    # 首首相遇 进行处理
                    return 5
                # |----2.1起点被包含
                # 即P1、Q1被包含
                elif between(Q1[0], P1[0], Q2[0]) or between(Q1[1], P1[1], Q2[1]) or between(P1[0], Q1[0], P2[0]) or between(P1[1], Q1[1], P2[1]):
                    return 6
                    # '''临时测试由6改为0'''
                    # return 6
                else:
                    return 0
            else:
                return 0
            # elif P1 == Q2 and not P2 == Q1 \
            #         or P2 == Q1 and not P1 == Q2:
            #     # 首尾相衔不成环 不处理
            #     return False
            # elif P1 == Q2 and not Point.IfPointsInLine(PIDList=[P1_id, P2_id, Q1_id]) \
            #         or P2 == Q1 and not Point.IfPointsInLine(PIDList=[Q1_id, Q2_id, P1_id]):
            #     # 首尾相衔不成环 不处理
            #     return 0
            # elif Point.IfPointsInLine(PIDList=[P1_id,P2_id,Q1_id,Q2_id]) \
            #         and \
            #         ( P2 == Q1 and (between(Q1[0], P1[0], Q2[0]) or between(Q1[1], P1[1], Q2[1])) \
            #           or P1 == Q2 and (between(P1[0], Q1[0], P2[0]) or between(P1[1], Q1[1], P2[1]))  ):
            #     # 首尾相衔且共线 居中的点为起点则处理
            #     # P2=Q1: P1居中为T, Q2居中为F
            #     # Q2=P1: Q1居中为T, P2居中为F
            #     return True
            # elif Point.IfPointsInLine(PIDList=[P1_id,Q1_id,Q2_id]) and not Point.IfPointsInLine(PIDList=[P2_id,Q1_id,Q2_id]) and (between(Q1[0], P1[0], Q2[0]) or between(Q1[1], P1[1], Q2[1]))\
            #     or Point.IfPointsInLine(PIDList=[Q1_id,P1_id,P2_id]) and not Point.IfPointsInLine(PIDList=[Q2_id,P1_id,P2_id]) and (between(P1[0], Q1[0], P2[0]) or between(P1[1], Q1[1], P2[1])):
            #     # 一个线段起点顶到另一线段中部    进行处理
            #     return True
            # # print Point.IfPointsInLine(PIDList=[P1_id,P2_id,Q1_id,Q2_id])
            #
            # if between(Q1[0], P1[0], Q2[0]) or between(Q1[1], P1[1], Q2[1]) or \
            #     between(Q1[0], P2[0], Q2[0]) or between(Q1[1], P2[1], Q2[1]) or\
            #     between(P1[0], Q1[0], P2[0]) or between(P1[1], Q1[1], P2[1]) or\
            #     between(P1[0], Q2[0], P2[0]) or between(P1[1], Q2[1], P2[1]):
            #
            #     if Point.IfPointsInLine(PIDList=[P1_id,P2_id,Q1_id,Q2_id]):
            #         return True
            # # if sorted([P1[0],P2[0]]) == sorted([Q1[0],Q2[0]]) and sorted([P1[1],P2[1]]) == sorted([Q1[1],Q2[1]]):
            # #     return True
            # return 0

    @staticmethod
    def IfPointsInLine(PList=[], PIDList=[], Accuracy=1e-5):
        if len(PIDList) > 0:
            plist = map(lambda pid: Point.PointDict[pid], PIDList)
        else:
            plist = PList
        Point.RemoveSAMEPOSPoint(plist)
        if len(plist) < 3: return True
        lst1 = plist[1:]
        lst2 = plist[:-1]
        pos_sub = map(lambda A,B:map(lambda a,b:a-b,A.getPOS(),B.getPOS()),lst1,lst2)
        # pos_sub = map(lambda A, B: map(lambda a, b: a - b, A.getPOSbyDecimal(), B.getPOSbyDecimal()), lst1, lst2)
        if sum(map(lambda a,b:abs(a[0]*b[1]-a[1]*b[0])>Accuracy,pos_sub[1:],pos_sub[:-1])) >0:
            return False
        else:
            return True


    @staticmethod
    def IfCrossByPoint(P1,P2,Q1,Q2):
        '''得到不相邻两直线组,直线由两点ID表示
        如果线段P1P2和直线Q1Q2相交，则P1P2跨立Q1Q2，
        即：( P1 - Q1 ) × ( Q2 - Q1 ) * ( Q2 - Q1 ) × ( P2 - Q1 ) >= 0。
        '''
        POS_P1,POS_P2,POS_Q1,POS_Q2 = map(lambda p:p.getPOS()[:2],(P1,P2,Q1,Q2))
        # P1,P2,Q1,Q2 = map(lambda i: Point.PointDict[i].getPOS()[:2],(P1_id,P2_id,Q1_id,Q2_id))
        lmd_outer = lambda p1,p2:(p1[0]*p2[1]-p1[1]*p2[0])
        if lmd_outer(map(lambda a,b:a-b,POS_P1,POS_Q1), map(lambda a,b:a-b,POS_Q2,POS_Q1)) * \
            lmd_outer(map(lambda a,b:a-b,POS_Q2,POS_Q1), map(lambda a,b:a-b,POS_P2,POS_Q1)) >0:
            return True
        else:
            return False

    @staticmethod
    def GetCrossPointByPID(P1_id,P2_id,Q1_id,Q2_id, IfCrossFlag=-1, Accuracy=EQUAL_ACCURACY):
        # 共点但不共线：
        # |-首首相遇                                7处理，返回起点
        # 三点共线:
        # |-0.一条线段的起点与另一条线段共线，且落入其中，终点不共线     2处理  返回落入的起点
        # 四点共线：
        # |-1.端点重合：
        # |----1.1首尾相衔成环                       3处理  返回两端点
        # |----1.2首尾相衔不成环,起点居中              4处理  返回起点
        # |----1.3首尾相衔不成环,终点居中              0暂时不处理
        # |----1.4首首相遇                          5处理  返回起点
        # |-2.端点不重合
        # |----2.1起点被包含                        6处理  返回被包含方起点
        x1,y1,z1 = Point.PointDict[P1_id].getPOS()
        x2,y2,z2 = Point.PointDict[Q1_id].getPOS()
        i1,j1,k1 = map(lambda i,j:i-j,Point.PointDict[P1_id].getPOS(),Point.PointDict[P2_id].getPOS())
        i2,j2,k2 = map(lambda i,j:i-j,Point.PointDict[Q1_id].getPOS(),Point.PointDict[Q2_id].getPOS())
        '''如果存在共线的两个线段且两线段重合，则约定将重合部分的两端点视为交点'''

        def between(a, b, c):
            a = map(lambda i: round(i, 9), a)
            b = map(lambda i: round(i, 9), b)
            c = map(lambda i: round(i, 9), c)
            if a[0] < b[0] < c[0] or a[1] < b[1] < c[1] or \
                    a[0] > b[0] > c[0] or a[1] > b[1] > c[1]:
                return True
            else:
                return False

        def equal(a, b):
            a = map(lambda i: round(i, 9), a)
            b = map(lambda i: round(i, 9), b)
            return a == b

        '''2018.10.05--------------------------------------------------------------------'''

        if IfCrossFlag == -1:
            IfCrossFlag = Point.IfCrossByPID(P1_id, P2_id, Q1_id, Q2_id)
        if IfCrossFlag>1:
            P1, P2, Q1, Q2 = map(lambda i: Point.PointDict[i].getPOS()[:2], (P1_id, P2_id, Q1_id, Q2_id))
            if IfCrossFlag == 2:
                if Point.IfPointsInLine(PIDList=(P1_id, P2_id, Q1_id)) and \
                        between(P1, Q1, P2) and not Point.IfPointsInLine( \
                        PIDList=(P1_id, P2_id, Q2_id)):
                    _pos = [
                        Point.PointDict[Q1_id].getPOS(),
                    ]
                elif Point.IfPointsInLine(PIDList=(Q1_id, Q2_id, P1_id)) and \
                        between(Q1, P1, Q2) and not Point.IfPointsInLine( \
                        PIDList=(Q1_id, Q2_id, P2_id)):
                    _pos = [
                        Point.PointDict[P1_id].getPOS(),
                    ]
            elif IfCrossFlag in [3, 5, 7]:
                # |----1.1首尾相衔成环                       3处理  返回两端点
                # |----1.4首首相遇                          5处理  返回起点
                # |-首首相遇,四点不共线                                7处理，返回起点
                '''若P1P2与Q1Q2首尾向衔，则返回各线段起点'''
                _pos = [
                    (P1[0], P1[1], z1), (Q1[0], Q1[1], z1)
                ]
            elif IfCrossFlag == 4:
                # |----1.2首尾相衔不成环，起点居中
                if P1 == Q2 and between(P1, Q1, P2) :
                    _pos = [
                        Point.PointDict[Q1_id].getPOS(),
                    ]
                elif P2 == Q1 and between(Q1, P1, Q2) :
                    _pos = [
                        Point.PointDict[P1_id].getPOS(),
                    ]
            elif IfCrossFlag == 6:
                # |----2.1起点被包含     返回被包含方起点
                _pos = []
                if between(Q1, P1, Q2):
                    _pos.append(Point.PointDict[P1_id].getPOS())
                if between(P1, Q1, P2):
                    _pos.append(Point.PointDict[Q1_id].getPOS())
            return map(lambda pos: Point(pos).getID(), _pos)
        else:
            a = (i2 * (y2 - y1) - j2 * (x2 - x1)) / (i2 * j1 - i1 * j2)
            x, y = x1 + i1 * a, y1 + j1 * a
            return [Point([x, y, z1]).getID()]

        '''--------------------------------------------------------------------'''
        # if Point.IfPointsInLine(PIDList=[P1_id,P2_id,Q1_id,Q2_id]):
        # # if abs(i2 * j1 - i1 * j2) < Accuracy and Point.IfPointsInLine(PIDList=[P1_id, P2_id, Q1_id, Q2_id]):
        #
        #     '''如果存在共线的两个线段且两线段重合，则约定将重合部分的两端点视为交点'''
        #     def between(a, b, c):
        #         a = map(lambda i: round(i, 9), a)
        #         b = map(lambda i: round(i, 9), b)
        #         c = map(lambda i: round(i, 9), c)
        #         if a[0] < b[0] < c[0] or a[1] < b[1] < c[1] or \
        #                 a[0] > b[0] > c[0] or a[1] > b[1] > c[1]:
        #             return True
        #         else:
        #             return False
        #     def equal(a, b):
        #         a = map(lambda i: round(i, 9), a)
        #         b = map(lambda i: round(i, 9), b)
        #         return a == b
        #
        #
        #     P1, P2, Q1, Q2 = map(lambda i: Point.PointDict[i].getPOS()[:2], (P1_id, P2_id, Q1_id, Q2_id))
        #     # _pos = []
        #     # print between(Q1, P2, Q2)
        #     if between(Q1, P1, Q2) and between(Q1, P2, Q2):
        #         # P1,P2在Q1，Q2中间
        #         _pos = [
        #             Point.PointDict[P1_id].getPOS(),
        #             # Point.PointDict[P2_id].getPOS()
        #
        #             # ((P1[0] + P2[0]) * 0.33, (P1[1] + P2[1]) * 0.33, z1),
        #             # ((P1[0] + P2[0]) * 0.67, (P1[1] + P2[1]) * 0.67, z1)
        #         ]
        #         # _pos = [P1[0],P1[1],z1]
        #         # return [P1_id]
        #     elif between(P1, Q1, P2) and between(P1, Q2, P2):
        #         # Q1，Q2在P1,P2中间
        #         _pos = [
        #             Point.PointDict[Q1_id].getPOS(),
        #             # Point.PointDict[Q2_id].getPOS()
        #
        #             # ((Q1[0] + Q2[0]) * 0.33, (Q1[1] + Q2[1]) * 0.33, z1),
        #             # ((Q1[0] + Q2[0]) * 0.67, (Q1[1] + Q2[1]) * 0.67, z1)
        #         ]
        #         # # _pos = [Q1[0], Q1[1], z1]
        #         # return [Q1_id]
        #     elif equal(P1, Q2) and equal(P2, Q1) or equal(P1, Q1):
        #         '''若P1P2与Q1Q2首尾向衔，则返回各线段起点'''
        #         _pos = [
        #             (P1[0], P1[1], z1), (Q1[0], Q1[1], z1)
        #         ]
        #         # return [P1_id, Q1_id]
        #     elif equal(P1, Q1):
        #         _pos = [
        #             (P1[0], P1[1], z1), (Q1[0], Q1[1], z1)
        #         ]
        #         # return [P1_id, Q1_id]
        #     elif equal(P2, Q1) and between(Q1, P1, Q2):
        #         # 首尾相衔且共线 居中的点为起点则处理
        #         # P2=Q1: P1居中 返回P1
        #         _pos = [
        #             Point.PointDict[P1_id].getPOS(),
        #         ]
        #     elif equal(P1, Q2) and between(P1, Q1, P2):
        #         # 首尾相衔且共线 居中的点为起点则处理
        #         # Q2=P1: Q1居中 返回Q1
        #         _pos = [
        #             Point.PointDict[Q1_id].getPOS(),
        #         ]
        #     else:
        #         _p = [P1,P2][between(Q1, P2, Q2)]
        #         _q = [Q1,Q2][between(P1, Q2, P2)]
        #         _pos = [
        #             (_p[0],_p[1],z1),(_q[0],_q[1],z1)
        #             # ((_p[0] + _q[0]) * 0.33, (_p[1] + _q[1]) * 0.33, z1),
        #             # ((_p[0] + _q[0]) * 0.67, (_p[1] + _q[1]) * 0.67, z1)
        #         ]
        #         # _pos = [_p[0],_p[1],z1]
        #         pass
        #     # return map(lambda pos:Point.getPoint(pos).getID(),_pos)
        #     return map(lambda pos: Point(pos).getID(), _pos)
        #
        #     # if between(Q1[0],P1[0],Q2[0]) or between(Q1[1],P1[1],Q2[1]): return P1_id
        #     # if between(Q1[0], P2[0], Q2[0]) or between(Q1[1], P2[1], Q2[1]): return P2_id
        #     # if between(P1[0], Q1[0], P2[0]) or between(P1[1], Q1[1], P2[1]): return Q1_id
        #     # if between(P1[0], Q2[0], P2[0]) or between(P1[1], Q2[1], P2[1]): return Q2_id
        #         # if Point.IfPointsInLine(PIDList=[P1_id,P2_id,Q1_id,Q2_id]):
        #         # 	return True
        # # try:
        # # 	a = (i2*(y2-y1)-j2*(x2-x1))/(i2*j1 - i1*j2)
        # # except:
        # # 	pass
        # a = (i2*(y2-y1)-j2*(x2-x1))/(i2*j1 - i1*j2)
        # # b = (j1*(x1-x2)-i1*(y1-y2))/(i2*j1 - i1*j2)
        # x, y = x1+i1*a, y1+j1*a
        #
        # # return [Point.getPoint([x,y,z1]).getID()]
        # return [Point([x, y, z1]).getID()]

    @staticmethod
    def GetSliceOfList(pointIDs,P1_id,P2_id):
        '''在pointIDs中得到由两个元素P1_id,P2_id分割的切片列表'''
        # print 'GetSliceOfList,pointIDs',pointIDs
        # print P1_id,P2_id
        i_P1,i_P2 = map(lambda i:pointIDs.index(i),[P1_id,P2_id])
        i_P1,i_P2 = [[i_P1,i_P2],[i_P2,i_P1]][i_P1>i_P2]

        return [pointIDs[i_P1:i_P2+1] , pointIDs[i_P2:]+pointIDs[:i_P1+1]]

    @staticmethod
    def RemoveSAMEPOSPoint(PList, Accuracy = (10 ** (-8))):
        i = 0
        # PList = map(lambda pid: Point.PointDict[pid], self.pIDlist)
        while True:
            if len(PList) == 0: break
            j = [0, i + 1][i < len(PList) - 1]
            try:
                dx, dy = PList[i][0] - PList[j][0], PList[i][1] - PList[j][1]
            except:
                dx, dy = PList[i].x - PList[j].x, PList[i].y - PList[j].y
            if dx * dx + dy * dy <= Accuracy:
                del PList[j]
                i = 0
                continue
            if j == 0: break
            i += 1
    @staticmethod
    def RemoveSAMEPoint_id(PidList, Accuracy = (10 ** (-8))):
        '''PList为id'''
        PList = map(lambda pid: Point.PointDict[pid], PidList)

        i = 0
        # PList = map(lambda pid: Point.PointDict[pid], self.pIDlist)
        while True:
            if len(PList) == 0: break
            j = [0, i + 1][i < len(PList) - 1]
            dx, dy = PList[i].x - PList[j].x, PList[i].y - PList[j].y
            if dx * dx + dy * dy <= Accuracy:
                del PList[j]
                del PidList[i]
                i = 0
                continue
            if j == 0: break
            i += 1

    @staticmethod
    def RemoveSAMEPoint(PList,Accuracy=(10**(-7)),MinAngle = 0.5,MinPointArea=0.0):
        '''PList为pos'''
        '''去掉重复的点：退化得到的点'''
        i=0
        while True:
            if len(PList) == 0: return
            j=[0,i+1][i<len(PList)-1]
            # if type(PList[i])==list:
            # 	dx,dy = PList[i][0]-PList[j][0],PList[i][1]-PList[j][1]
            # else:
            # 	dx,dy = PList[i].x-PList[j].x,PList[i].y-PList[j].y
            try:
                dx,dy = PList[i][0]-PList[j][0],PList[i][1]-PList[j][1]
            except:
                try:
                    dx,dy = PList[i].x-PList[j].x,PList[i].y-PList[j].y
                except:
                    pass
            # if _min>abs(dx) or _min>abs(dy):_min = min(abs(dx),abs(dy))
            if dx * dx + dy * dy <= Accuracy:
            # if abs(dx) <= Accuracy and abs(dy) <= Accuracy:
                try:
                    del PList[j]
                except:
                    pass
                i=0
                continue
            if j==0: break
            i += 1
        # print '_min',_min
        '''去掉尖锐的点'''
        i = 0
        while True:
            if len(PList) == 0: break
            j = [0, i + 1][i < len(PList) - 1]
            k = [0, j + 1][j < len(PList) - 1]

            try:
                x_i, y_i, z_i = PList[i].getPOS()
                x_j, y_j, z_j = PList[j].getPOS()
                x_k, y_k, z_k = PList[k].getPOS()
            except:
                x_i, y_i, z_i = PList[i]
                x_j, y_j, z_j = PList[j]
                x_k, y_k, z_k = PList[k]
            # if type(PList[i]) == list:
            # 	x_i, y_i, z_i = PList[i]
            # 	x_j, y_j, z_j = PList[j]
            # 	x_k, y_k, z_k = PList[k]
            # else:
            # 	x_i, y_i, z_i = PList[i].getPOS()
            # 	x_j, y_j, z_j = PList[j].getPOS()
            # 	x_k, y_k, z_k = PList[k].getPOS()
            '''由J点指向IK点，获得两向量'''
            i1, j1 = x_i - x_j, y_i - y_j
            i2, j2 = x_k - x_j, y_k - y_j


            '''根据点坐标得到三点围成三角形面积
            S=(1/2)*(x1y2+x2y3+x3y1-x1y3-x2y1-x3y2)
            '''
            S = 0.5*(x_i * y_j + x_j * y_k + x_k * y_i - x_i * y_k - x_j * y_i - x_k * y_j)

            if (i1, j1) == (0, 0) or (i2, j2) == (0, 0)\
                    or  (i1 * i2 + j1 * j2) / (sqrt(i1 ** 2 + j1 ** 2) * sqrt(i2 ** 2 + j2 ** 2))>=1.0:
                del PList[j]
                i = 0
                continue
            if abs(S) <= MinPointArea:
                del PList[j]
                i = 0
                continue
            try:
                if 0.0 <= acos((i1 * i2 + j1 * j2) / (sqrt(i1 ** 2 + j1 ** 2) * sqrt(i2 ** 2 + j2 ** 2)))*180 / pi < MinAngle\
                    or 180-MinAngle < acos((i1 * i2 + j1 * j2) / (sqrt(i1 ** 2 + j1 ** 2) * sqrt(i2 ** 2 + j2 ** 2)))*180 / pi <= 180:
                    del PList[j]
                    i = 0
                    continue
            except:
                pass
            if j==0: break
            i += 1
        pass

    @staticmethod
    def InsertCrossPointIntoPointlistByPID(pointIDs,P1_id,P2_id,cross_id):
        '''在pointIDs中增加交点cross_id'''

        i_P1,i_P2 = map(lambda i:pointIDs.index(i),[P1_id,P2_id])
        i_P1,i_P2 = [[i_P1,i_P2],[i_P2,i_P1]][i_P1>i_P2]

        Pids_1 = pointIDs[i_P1:i_P2+1]
        Pids_2 = pointIDs[i_P2:] + pointIDs[:i_P1+1]
        Pids_1,Pids_2 = Point.GetSliceOfList(pointIDs,P1_id,P2_id)

        if len(Pids_1) == 2:
            pointIDs.insert(i_P1+1,cross_id)
            return
        if len(Pids_2) == 2:
            pointIDs.insert(i_P2+1,cross_id)
            return
        # print Pids_1,Pids_2

        Pids = [Pids_2,Pids_1][Point.IfPointsInLine(PIDList=Pids_1)]
        distance_cross = Point.getDistencebyID(Pids[0],cross_id)
        distance_exist = map(lambda pid:Point.getDistencebyID(Pids[0],pid),Pids)
        cross_sort = len([i for i in distance_exist if i < distance_cross])

        # try:
        # pointIDs.insert(pointIDs.index(Pids[cross_sort])+i_P1,cross_id)
        # i_P1, i_P2 = map(lambda i: pointIDs.index(i), [P1_id, P2_id])
        pointIDs.insert(cross_sort + [i_P1,i_P2][Pids==Pids_2], cross_id)

        # pointIDs =
        # except:
            # print Pids[cross_sort]
            # pass
        # '''对于平行线相交问题，认为交点为线段段点，且相交两次，此处将原段点去掉'''
        # if Point.PointDict[cross_id].getPOS() == Point.PointDict[P1_id].getPOS():
        # 	pointIDs.remove(P1_id)
        # if Point.PointDict[cross_id].getPOS() == Point.PointDict[P2_id].getPOS():
        # 	pointIDs.remove(P2_id)
        # print pointIDs

        # try:
        # 	pointIDs.insert(pointIDs.index(Pids[cross_sort]),cross_id)
        # except Exception, e:
        #
        # 	print distance_cross
        # 	print distance_exist
        # 	print P1_id,P2_id,cross_id
        # 	print Point.PointDict[P1_id].getPOS(),Point.PointDict[P2_id].getPOS(),Point.PointDict[cross_id].getPOS()
        # 	exit()

    @staticmethod
    def GetSimpleLoopsByCrossLoop(_WithcrossPIDs,_crossPIDs):
        '''根据一个自相交的loop各顺点，得到若干孤立的简单loop'''
        _newloops = []
        _currentloop = []
        _currentpid = 0
        _ifreaded = [False]*len(_WithcrossPIDs)

        while True:
            if _WithcrossPIDs[_currentpid] not in _currentloop :
                if not _ifreaded[_currentpid]:
                    _currentloop.append(_WithcrossPIDs[_currentpid])
            else:
                _newloops.append(_currentloop)
                _currentloop = []
            if _ifreaded[_currentpid]:
                _currentpid = [_currentpid+1,0][_currentpid+1==len(_WithcrossPIDs)]
                continue
            _ifreaded[_currentpid] = True

            '''get next'''
            if _WithcrossPIDs[_currentpid] not in _crossPIDs:
                _currentpid = [_currentpid+1,0][_currentpid+1==len(_WithcrossPIDs)]
            else:
                _idx = [i for i, x in enumerate(_WithcrossPIDs) if x == _WithcrossPIDs[_currentpid] and i != _currentpid][0]
                _currentpid = [_idx+1,0][_idx+1==len(_WithcrossPIDs)]

            if sum(_ifreaded) == len(_WithcrossPIDs):
                _newloops.append(_currentloop)
                break
        return _newloops

    @staticmethod
    def GetSimpleLoopsByCrossLoops(_WithcrossPIDsLoops, _crossPIDs):
        pass

    @staticmethod
    def GetMergedLoopsByLoops(loopPID1,loopPID2,crossLines):
        '''crossLines = [P1,P2,Q1,Q2,Point.GetCrossPointByPID(P1,P2,Q1,Q2)]
        P1,P2 from loopPID1 while Q1,Q2 from loopPID2
        '''
        _loopPID1 = loopPID1[:]
        _loopPID2 = loopPID2[:]
        debug = False
        # if _loopPID1 == [1,10,15,53,46,47,54,18]:
        #     debug = True
        #     pass

        LMD_INSERT1 = lambda crosslines: \
            Point.InsertCrossPointIntoPointlistByPID(_loopPID1,crosslines[0],crosslines[1],crosslines[4])
        LMD_INSERT2 = lambda crosslines: \
            Point.InsertCrossPointIntoPointlistByPID(_loopPID2, crosslines[2], crosslines[3], crosslines[4])

        map(LMD_INSERT1, crossLines)
        map(LMD_INSERT2, crossLines)

        '''对于平行线相交问题，认为交点为线段段点，且相交两次，此处将原段点去掉'''
        # try:
        _ParallelLintsCrossPIDs = []
        for _crosslines in crossLines:
            if Point.IfPointsInLine(PIDList=_crosslines[:4]):
                _ParallelLintsCrossPIDs.append(_crosslines[-1])
                if Point.PointDict[_crosslines[0]].getPOS() == Point.PointDict[_crosslines[-1]].getPOS():
                    try:
                        _loopPID1.remove(_crosslines[0])
                    except:
                        pass
                if Point.PointDict[_crosslines[1]].getPOS() == Point.PointDict[_crosslines[-1]].getPOS():
                    try:
                        _loopPID1.remove(_crosslines[1])
                    except:
                        pass
                if Point.PointDict[_crosslines[2]].getPOS() == Point.PointDict[_crosslines[-1]].getPOS():
                    try:
                        _loopPID2.remove(_crosslines[2])
                    except:
                        pass
                if Point.PointDict[_crosslines[3]].getPOS() == Point.PointDict[_crosslines[-1]].getPOS():
                    try:
                        _loopPID2.remove(_crosslines[3])
                    except:
                        pass

        # except:
        #     pass
        # print _loopPID1,_loopPID2
        # loop中pid是否已访问
        _IfReadedOfLoop1,_IfReadedOfLoop2 = [False]*len(_loopPID1),[False]*len(_loopPID2)
        # 最终得到的loops
        _newloops = []
        # 当前获得的loop
        _currentloop = []
        # 当前所考察的loop序号
        _currentPrimitiveLoop = 0
        # 当前所考察的pid序号
        _currentpid1,_currentpid2 = 0,0
        # if debug:
        #     pass
        while True:
            if all(_IfReadedOfLoop1) and all(_IfReadedOfLoop2):
                break
            _currentpid = [_currentpid1,_currentpid2][_currentPrimitiveLoop]
            _IfReadedOfLoop = [_IfReadedOfLoop1,_IfReadedOfLoop2][_currentPrimitiveLoop]
            # 已插入交叉点的looppid
            _loopPID = [_loopPID1,_loopPID2][_currentPrimitiveLoop]
            # 未插入交叉点的looppid
            _primitiveLoopPID = [loopPID1,loopPID2][_currentPrimitiveLoop]
            if not _IfReadedOfLoop[_currentpid]:
                _currentloop.append(_loopPID[_currentpid])
                _IfReadedOfLoop[_currentpid]=True
            else:
                pass
            if _loopPID[_currentpid] in _primitiveLoopPID:
                '''假如当前点不是交点，则试探当前loop下一点'''
                _nextPID = _loopPID[[0,_currentpid+1][_currentpid+1<len(_loopPID)]]
            else:
                '''假如当前点是交点，则跳转loop后试探该loop下一点'''
                try:
                    if debug:
                        pass
                    _nextPID = [_loopPID1,_loopPID2][[1,0][_currentPrimitiveLoop]].index(_loopPID[_currentpid])+1
                    _nextPID = [0,_nextPID][_nextPID<len([_loopPID1,_loopPID2][[1,0][_currentPrimitiveLoop]])]
                    #  insert at 20180724
                    _nextPID = [_loopPID1,_loopPID2][[1,0][_currentPrimitiveLoop]][_nextPID]
                except:
                    pass
            if _nextPID in _currentloop and _nextPID not in _ParallelLintsCrossPIDs:
                # if debug:
                #     pass
                _newloops.append(_currentloop)
                _currentloop = []
            if _loopPID[_currentpid] not in _primitiveLoopPID:
                _pid = _loopPID[_currentpid]
                _currentPrimitiveLoop = [1,0][_currentPrimitiveLoop]
                _loopPID = [_loopPID1, _loopPID2][_currentPrimitiveLoop]
                if _currentPrimitiveLoop :
                    _currentpid2 = [0, _loopPID.index(_pid) + 1][_loopPID.index(_pid) + 1 < len(_loopPID)]
                else:
                    _currentpid1 = [0, _loopPID.index(_pid) + 1][_loopPID.index(_pid) + 1 < len(_loopPID)]
                _currentpid = [_currentpid1, _currentpid2][_currentPrimitiveLoop]
                if _loopPID[_currentpid] in _currentloop and _loopPID[_currentpid] not in _ParallelLintsCrossPIDs:
                    # if debug:
                    #     pass
                    _newloops.append(_currentloop)
                    _currentloop = []

            if _currentPrimitiveLoop:
                if False in _IfReadedOfLoop2[_currentpid2:]:
                    _currentpid2 = _IfReadedOfLoop2[_currentpid2:].index(False)+_currentpid2
                elif False in _IfReadedOfLoop2[:_currentpid2]:
                    _currentpid2 = _IfReadedOfLoop2[:_currentpid2].index(False)
            else:
                if False in _IfReadedOfLoop1[_currentpid1:]:
                    _currentpid1 = _IfReadedOfLoop1[_currentpid1:].index(False)+_currentpid1
                elif False in _IfReadedOfLoop1[:_currentpid1]:
                    _currentpid1 = _IfReadedOfLoop1[:_currentpid1].index(False)
        return _newloops

    @staticmethod
    def GetLoopOutOrIn(looplist):
        '''将looplist根据嵌套关系分类 返回外侧loop及内侧loop'''
        _loopdict = {id:looplist[id] for id in range(len(looplist))}
        _loopids = [(i,j) for i in range(len(looplist)) for j in range(len(looplist)) if i<j]
        # print _loopids,_loopdict
        _contain = {id:[] for id in range(len(looplist))}
        _outloopnum = {id:0 for id in range(len(looplist))}

        def addcontain(loopid1, loopid2):
            # debug 0001.igs 调用IfLoopContainLoopByPIDs_absoluteIN出错，调用IfLoopContainLoopByPIDs正确，偏移-4,-8,-12...
            # debug 0314.igs 调用IfLoopContainLoopByPIDs_absoluteIN出错，调用IfLoopContainLoopByPIDs正确，
            # debug 0312.igs 调用IfLoopContainLoopByPIDs_absoluteIN出错，调用IfLoopContainLoopByPIDs出错，偏移-4.5,-9
            # debug 0031.igs 调用IfLoopContainLoopByPIDs_absoluteIN且不去除错误外圈为正确
            '''☆首先计算所有共点包含及完全包含的loop，再自外向内检查loop，若该loop不符合外逆内顺规律，则将其包含的共点loop的被包含次数-1'''

            if Point.IfLoopContainLoopByPIDs(_loopdict[loopid1], _loopdict[loopid2]):
            # if Point.IfLoopContainLoopByPIDs_absoluteIN(_loopdict[loopid1], _loopdict[loopid2]):
            # if Point.IfLoopContainLoopByPIDs_NoOutPoint(_loopdict[loopid1], _loopdict[loopid2]):
                _outloopnum[loopid2] += 1
                _contain[loopid1].append(loopid2)
        for _loopid in _loopids:
            addcontain(_loopid[0], _loopid[1])
            addcontain(_loopid[1], _loopid[0])

        # 对_contain中包含loop的数量进行排序，自外向内进行处理
        _contain_num = _contain.copy()
        for i in _contain_num:
            _contain_num[i] = len(_contain_num[i])
        _contain_num_list = sorted(_contain_num.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
        # 自外向内，查看loop点位顺逆序与被包含次数的符合性
        for loopid,contain_num  in _contain_num_list:
        #     loop的id，loop包含他人的数量
            '''1.判断自身是否不符合外逆内顺的规律'''
            if (Point.IfLoopClockwise(PIDList=_loopdict[loopid]) and _outloopnum[loopid] % 2 == 0) or (not Point.IfLoopClockwise(PIDList=_loopdict[loopid]) and _outloopnum[loopid] % 2 == 1):
                '''2.对不符合的进行处理：将所包含的loop中，与本错误loop存在共点的loop的被包含数量-1'''
                if len(_contain[loopid])>0:
                    for _contained_loopid in _contain[loopid]:
                        LMD_On = lambda pid: [False, True][Point.IfLoopContainPointByPID(_loopdict[loopid], pid) in ['On']]
                        re = map(LMD_On, _loopdict[_contained_loopid])
                        if any(re):
                            _outloopnum[_contained_loopid] -= 1

        return [looplist[loopid] for loopid in _contain if _outloopnum[loopid] % 2 == 0],[looplist[loopid] for loopid in _contain if _outloopnum[loopid] % 2 == 1]


    @staticmethod
    def GetAreaOfLoopByPIDList(loopPID):
        '''设O为平面内零点，Pi与Pi+1为LoopPID内相邻两点，依次计算OPiPi+1三角形面积，并根据其顺逆冠以正负号，累加求和得到多边形Loop的面积'''
        Triangle_Area = lambda x1,y1,x2,y2:abs(x1*y2-x2*y1)*0.5
        if len(loopPID)<=2: return -1
        P0 = Point.getPoint([0,0,0])
        If_Loop_Clockwise = Point.IfLoopClockwise(PIDList=loopPID)
        S = 0
        for i in range(len(loopPID)):
            j = [0,i+1][i < len(loopPID) - 1]
            flag = [-1, 1][If_Loop_Clockwise == Point.IfLoopClockwise(PIDList=[P0.getID(),loopPID[i],loopPID[j]])]
            x1, y1 = Point.PointDict[loopPID[i]].getPOS()[:2]
            x2, y2 = Point.PointDict[loopPID[j]].getPOS()[:2]
            S += flag * Triangle_Area(x1, y1, x2, y2)
        return S

    @staticmethod
    def GetLoopOrder(loopidDict):
        pass


class geometryLine():
    ID = 1
    LineDict = {}
    def __init__(self,P1,P2,color=[255,255,255],flyDistance = 0):
        self.P1 = P1
        self.P2 = P2
        self.Color = color
        self.flyDistance = flyDistance

        self.ID = geometryLine.ID
        geometryLine.ID+=1
        geometryLine.LineDict[self.ID] = self
    def setFlyDistance(self,flydistance):
        self.flyDistance = flydistance
    def getID(self):
        return self.ID
    def getLength(self):
        Vector = map(lambda a,b:a-b, self.P1.getPOS(),self.P2.getPOS())
        return sum(map((lambda i:i**2),Vector))**0.5

    @staticmethod
    def refresh():
        geometryLine.ID = 1
        geometryLine.PointDict = {}
        geometryLine.POSDict = {}

    # @staticmethod
    # def breakLine(Line,step=0.2):
    #


# poslist = [[0,0,0],[25,0,0],[50,0,0],[50,20,0],[25,5,0],[0,20,0]]

# plist = map(lambda pos:Point.getPoint(pos),poslist)
# pidlist = map(lambda p:p.getID(),plist)
# print pidlist
# Point.getPoint([27,0,0])
# Point.InsertCrossPointIntoPointlistByPID(pidlist,4,3,7)
# print pidlist

# lst = [0,1,2,3,12,5]
# Point.InsertCrossPointIntoPointlistByPID(lst,1,0,7)
# print lst

# class LineSegment():
#     ID = 1
#     LineSegmentDict = {}
#     def __init__(self,Point1,Point2):
#         self.Point1 = Point1
#         self.Point2 = Point2

class RadialLine():
    ID = 1
    RadialLineDict = {}
    def __init__(self,pointIDs,startpID):
        self.pointIDs = pointIDs
        self.startpID = startpID
        point_O = Point.PointDict[self.startpID].getPOS()
        point_A = Point.PointDict[self.pointIDs[0]].getPOS()
        point_B = Point.PointDict[self.pointIDs[1]].getPOS()
        # print point_O,point_A,point_B
        OA = map(lambda o,a:a-o,point_O,point_A)
        _length = (sum(map(lambda a:float(a)**2,OA)))**(0.5)
        OA = map(lambda d:float(d)/_length,OA)

        OB = map(lambda o,a:a-o,point_O,point_B)
        _length = (sum(map(lambda a:float(a)**2,OB)))**(0.5)
        OB = map(lambda d:float(d)/_length,OB)

        # print OB
        direction = map(lambda a,b:(a+b)*(0.5),OA,OB)
        _length = (sum(map(lambda a:float(a)**2,direction)))**(0.5)
        if _length==0:
            direction = [-OA[1],OA[0],0]
            # x = -y0;
            # y  =x0;
        else:
            direction = map(lambda d:float(d)/_length,direction)

        '''a×b = x1*y2-x2*y1'''
        AO = map(lambda a:-a,OA)

        # print OA,AO
        if AO[0]*OB[1]-AO[1]*OB[0] <0:
            direction = map(lambda a:-a,direction)
        # print point_A,point_O,point_B
        # print direction
        self.IN_direction = direction
        self.OUT_direction = map(lambda a:-a,direction)

        self.ID = RadialLine.ID
        RadialLine.ID+=1
        RadialLine.RadialLineDict[self.ID] = self

    @staticmethod
    def refresh():
        RadialLine.ID = 1
        RadialLine.RadialLineDict = {}

# P1 = Point.getPoint([15.514473919999999, -342.01465923524466, 0.0])
# P2 = Point.getPoint([87.9849039434718, -342.0018616226561, 0.0])
# Q1 = Point.getPoint([-220.32669349240956, -389.6953521645902, 0.0])
# Q2 = Point.getPoint([-220.73469897364305, -389.7664742175838, 0.0])
# print Point.IfCrossByPID(P1.getID(),P2.getID(),Q1.getID(),Q2.getID())
if __name__ == '__main__':
    # P1 = Point.getPoint([15.514473919999999, -342.01465923524466, 0.0])
    P1 = Point.getPoint([383.8, 42.55, 0.0])
    P2 = Point.getPoint([242.590847809, 42.55, 0.0])
    Q1 = Point.getPoint([322.982337649, 46.95, 0.0])
    Q2 = Point.getPoint([332.2, 37.732337649, 0.0])
    flag = Point.IfCrossByPID(P1.getID(),P2.getID(),Q1.getID(),Q2.getID())
    Point.GetCrossPointByPID(P1.getID(),P2.getID(),Q1.getID(),Q2.getID())
    pass
