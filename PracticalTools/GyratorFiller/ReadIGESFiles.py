# -*- coding: utf-8 -*-
# 2014-01-24 ReadIGESFiles
# from math import *
from decimal import *
from time import *
from math import atan, cos, sin, tan, pi
import copy
from random import *
# from offset import *
from geometry import Point, geometryLine
from functools import reduce
# from connectloop import *
# import Block
import LoopSequence
import pdb
import sys, os


def cur_file_dir():
	# 获取脚本路径
    path = sys.path[0]
	# 判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)

def checkflydistance(looppoints, theta, MaxFlyDistance):
    '''
	给定一角度，求填充时悬空的长度
	20160531
	'''
    POSROTATE = lambda p: [cos(-theta) * p.getPOS()[0] - sin(-theta) * p.getPOS()[1],
                           cos(-theta) * p.getPOS()[1] + sin(-theta) * p.getPOS()[0]]
    rotated_looppoints = map(POSROTATE, looppoints)

    rotated_pos_deltaX = []
    _preX = rotated_looppoints[-1][0]
    dx = 0.0

    for rot_p in rotated_looppoints:
        _curX = rot_p[0]

        if dx * (_curX - _preX) > 0:
            dx += _curX - _preX
        elif dx * (_curX - _preX) < 0:
            rotated_pos_deltaX.append(dx)
            dx = _curX - _preX
        elif dx * (_curX - _preX) == 0:
            if dx == 0.0:
                dx = _curX - _preX
        _preX = _curX

    rotated_pos_deltaX.append(dx)

    if rotated_pos_deltaX[-1] * rotated_pos_deltaX[0] > 0:
        rotated_pos_deltaX[0] += rotated_pos_deltaX.pop()

    delnum = 0
    for dx in rotated_pos_deltaX:
        if abs(dx) < MaxFlyDistance:
            delnum += 2
    if len(rotated_pos_deltaX) - delnum <= 2:
        return True
    else:
        return False
# class Point:
# 	def __init__(self,x,y,z):
# 		self.x=float(x)
# 		self.y=float(y)
# 		self.z=float(z)

# 		# self.LineNUM=0
# 		# self.LinesLIST=[]
# 	# def checkPOS(self,x,y,z):
# 	# 	return True if [self.x,self.y,self.z]==[x,y,z] else False
# 	def setPOS(self,pos):
# 		self.x,self.y,self.z=pos[:3]
# 	def getPOS(self):
# 		return [self.x,self.y,self.z]
# 	def getDistence(self,p):
# 		return sqrt((self.x-p.x)**2+(self.y-p.y)**2+(self.z-p.z)**2)
# 	def getXYZone(self):
# 		return '%d-%d'%(self.x,self.y)

# def getLineNUM(self):
# 	return self.LineNUM
# def addLine(self,id):
# 	if id in self.LinesLIST:
# 		return 
# 	self.LinesLIST.append(id)
# 	self.LineNUM+=1
class Line:
    # XYZONE = set()
    XYZONEDict = {}
    LINE_DIC = {}
    DEVIATION = 0.001

    # Deviation
    def __init__(self, Substance, id):
        # self.P1=Point(x1,y1,z1)
        # self.P2=Point(x2,y2,z2)
        self.adjustLine = ([], [])
        self.id = id
        self.substance = Substance
        self.type = Substance.MenuIndex[0]
        self.P_list = []
        self.K_list = []  # 存储相邻两点直线与X轴夹角：-90：90
        self.posZone = []
        if self.type == '110':
            x1, y1, z1, x2, y2, z2 = self.substance.ParameterData[1:7]
            self.P1 = Point.getPoint([x1, y1, z1])
            self.P2 = Point.getPoint([x2, y2, z2])
            self.P_list.append(self.P1)
            self.P_list.append(self.P2)
        elif self.type == '106':
            # print self.substance.MenuIndex
            if self.substance.ParameterData[1] == '1':
                '''1 =x,y pairs, common z'''
                Pcount = int(self.substance.ParameterData[2])
                common_Z = float(self.substance.ParameterData[3])
                for i in range(Pcount):
                    P = Point.getPoint([float(self.substance.ParameterData[4 + i * 2]), \
                                        float(self.substance.ParameterData[5 + i * 2]), \
                                        common_Z])
                    if i == 0:
                        self.P1 = P
                    self.P2 = P
                    self.P_list.append(P)

            elif self.substance.ParameterData[1] == '2':
                '''2 =x,y,z coordinates'''
                pass
            elif self.substance.ParameterData[1] == '3':
                '''3 =x,y,z coordinates and i,j,k vectors'''
                pass
            pass
        for p in self.P_list:
            zone = p.getXYZone()
            if zone not in self.posZone: self.posZone.append(zone)
            # self.__class__.XYZONE.add(zone)
            if zone in self.__class__.XYZONEDict:
                self.__class__.XYZONEDict[zone].append(self.id)
            else:
                self.__class__.XYZONEDict[zone] = [self.id]
            pass
        Line.LINE_DIC[self.id] = self

    def getPoints(self):
        return [self.P1.getPOS(), self.P2.getPOS()]

    def getXRange(self):
        # minX = None
        # maxX = None
        Xlist = reduce(lambda a, b: a + b, map(lambda p: [p.getPOS()[0]], self.P_list))

        # for p in self.P_list:
        # 	_pos = p.getPOS()
        # 	if not minX or minX>_pos[0]:minX = _pos[0]
        # 	if not maxX or maxX<_pos[0]:maxX = _pos[0]

        return [min(Xlist), max(Xlist)]

    def getPointXYZ(self):
        # if self.type == '110':
        # 	return self.P1.getPOS()+self.P2.getPOS()
        # elif self.type == '106':
        re = []
        for p in self.P_list:
            re += p.getPOS()
        return re

    @staticmethod
    def checkLine(line):
        # print 'line.posZone',line.posZone
        # print 'Line.XYZONEDict',Line.XYZONEDict
        for zone in line.posZone:
            for existed_lineid in Line.XYZONEDict[zone]:
                if existed_lineid == line.id: continue
                existed_line = Line.LINE_DIC[existed_lineid]

                for i, p in enumerate(line.getPoints()):
                    for j, P in enumerate(existed_line.getPoints()):
                        # if (abs(p[0]-P[0])<Line.DEVIATION and abs(p[1]-P[1])<Line.DEVIATION ) or p==P:
                        if p == P:
                            # print line.id,i,p
                            # print existed_line.id,j,P
                            # exit()
                            if existed_line.adjustLine[j] == []: existed_line.adjustLine[j].append(line.id)
                            if line.adjustLine[i] == []: line.adjustLine[i].append(existed_lineid)
                        if line.adjustLine[0] != [] and line.adjustLine[1] != []: break

        pass

    @staticmethod
    def Clear():
        Line.XYZONEDict = {}
        Line.LINE_DIC = {}

    # def checkLine(self,line):
    # 	'''已作废'''
    # 	p1,p2=line.getPoints()
    # 	for i,p in enumerate(line.getPoints()):
    # 		for j,P in enumerate(self.getPoints()):
    # 			if p==P:
    # 				self.adjustLine[j].append(line.id)
	# 				line.adjustLine[i].append(self.id)
    # 				# print i,p,j,P
    # 				# exit()
    def getDisconnectedPoint(self):
        re = []
        if self.adjustLine[0] == []:
            re.append(self.P1)
        if self.adjustLine[1] == []:
            re.append(self.P2)
        return re

    def getLength(self):
        return self.P1.getDistence(self.P2)



class Circle:
    CIRCLE_DIC = {}
    def __init__(self, Substance, id):
        # self.P1=Point(x1,y1,z1)
        # self.P2=Point(x2,y2,z2)
        # self.adjustLine = ([], [])
        self.id = id
        self.substance = Substance

        Circle.CIRCLE_DIC[self.id] = self

class Label:
    def __init__(self, Substance, id):
        self.id = id
        self.substance = Substance
        [x, y, z] = self.substance.ParameterData[10:13]
        self.P = Point.getPoint([x, y, z])
        self.size = self.substance.ParameterData[3:5]

        STR = self.substance.ParameterData[13]
        if STR == '' or 'H' not in STR:
            STR = ''
        else:
            i = STR.find('H')
            j = int(STR[0:i])
            STR = STR[i + 1:i + j + 1]
        self.text = STR

    def getSize(self):
        return self.size

    def getPoint(self):
        return self.P

    def getText(self):
        return self.text


class Substance:
    # LinesList=[]
    def __init__(self):
        self.MenuIndex = ['' for i in range(20)]
        self.ParameterData = []
        self.ID = ''
        self.Point = 0  # Point To ParameterLine, useless

        # [OT,PD,St,LS,Ly, Ve,TM,Lb,Cd,ID1,	OT,LW,Co,PL,Fm, N1,N2,SI1,SI2,ID2]
        '''
		ObjectType	ParameterData	Structure	LineStyle	Layer
		View	TransMatrix	Label	Condition	Index1
		ObjectType	Linewidth	Color	ParameterLine	Format
		NULL	NULL	SubstanceID1	SubstanceID2 Index2
		'''

    def SetMenuData(self, index, value):
        self.MenuIndex[index] = value
        if index == 1:
            self.Point = int(value)
        if index == 9:
            # print value
            if type(value) == type('') and value[0] == 'D':
                value = int(value[1:])
            self.ID = value

    def AddParameterData(self, valuelist):
        self.ParameterData += valuelist

    def Instantiate(self, l_list, label_list, singlepoint_list):
        if self.MenuIndex[0] == '110':
            '''Line1'''
            # print self.ParameterData
            # x1,y1,z1,x2,y2,z2=self.ParameterData[1:7]
            self.l = Line(self, self.ID)
            Line.checkLine(self.l)
            # for i in l_list:
            # 	i.checkLine(self.l)
            l_list.append(self.l)
        if self.MenuIndex[0] == '106' and self.MenuIndex[3] != '4':
            self.l = Line(self, self.ID)
            Line.checkLine(self.l)
            # for i in l_list:
            # 	i.checkLine(self.l)
            l_list.append(self.l)
        if self.MenuIndex[0] == '212':
            label = Label(self, self.ID)
            label_list.append(label)
        if self.MenuIndex[0] == '116':
            # print '116',self.ParameterData[1],self.ParameterData[2],self.ParameterData[3]
            sgpoint = Point.getPoint([self.ParameterData[1], self.ParameterData[2], self.ParameterData[3]])
            singlepoint_list.append(sgpoint)

    def Refresh_ParameterData(self):
        if self.MenuIndex[0] == '110':
            self.ParameterData[1:7] = self.l.getPointXYZ()
        if self.MenuIndex[0] == '106':
            if self.ParameterData[1] == '1':
                self.ParameterData[2] = len(self.l.P_list)
                self.ParameterData[3] = self.l.P_list[0].z
                self.ParameterData = self.ParameterData[:4]

                for p in self.l.P_list:
                    self.ParameterData.append('%s' % p.x)
                    self.ParameterData.append('%s' % p.y)
        pass


class IGESFile:
    Color_Dic = {'RED': '2' \
        , 'YELLOW': '5' \
        , 'GREEN': '3' \
        , 'CYAN': '7' \
        , 'BLUE': '4' \
        , 'MAGENTA': '6' \
        , 'DEFAULT': '8' \
        , '2': 'RED' \
        , '5': 'YELLOW' \
        , '3': 'GREEN' \
        , '7': 'CYAN' \
        , '4': 'BLUE' \
        , '6': 'MAGENTA' \
        , '8': 'DEFAULT' \
                 }

    def __init__(self, filename, MinPointArea=0.001, NearPointDistance=0.001):
        # type: (object, object, object) -> object
        Line.Clear()
        # try:
        # filehandle = open(filename,'r')
        # self.RecordsList = filehandle.readlines()
        # except Exception, e:
        # filehandle = open(filename,'w')
		# self.RecordsList = filehandle.readlines()

        self.FilePath, self.FileName = os.path.split(filename)
        if self.FileName == 'blank.igs':
            self.RecordsList = [
				'IGES file generated by ChenBo                                           S      1\n',
                '1H,,1H;,,39HF:\\chenbo\\1-program\\4-Rotator\\blank.igs,38HCAXA Electronic BG      1\n',
				'oard 2001 for Windows,3H1.0,32,38,6,308,15,35HF:\\chenbo\\1-program\\4-RotaG      2\n',
				'tor\\blank,1.,2,2HMM,20000,200.,13H160506.060545,0.0001,200.,,,9,0,13H160G      3\n',
                '506.060545;                                                             G      4\n',
                '     106       1       0       4       0       0       0       000010100D      1\n',
                '     106       0       2       1      20                                D      2\n',
                '106,1,2,0.0,0.0,-200.,0.0,200.;                                        1P      1\n',
                'S      1G      4D      2P      1                                        T      1\n']
        # print "blank.igs"
        else:
            filehandle = open(filename, 'r')
            self.RecordsList = filehandle.readlines()
            filehandle.close()
        # self.RecordsList = filehandle.readlines()
        # filehandle.close()
        self.base_records = {}
        self.start_STR = ""
        self.end_STR = ""
        self.global_parameter_STR = ""
        self.global_parameter_INITED = False

        self.parameters_split = ""
        self.records_split = ""
        self.parameters = {}
        self.substances = {}
        self.LinesList = []
        self.LinesDic = {}
        self.LoopsList = []
        self.CirclesDic = {}
        self.CirclesList = []
        self.LabelList = []
        self.SinglePointList = []
        self.LoopPointsListDict = {}  # record the Points of the Loop
        self.LoopIDdict = {}
        self.LoopINFODict = {}
        self.S_shapedLoopList = []
        self.inlinePointID = []
        # self.LoopCenterDict = {}

        self.MinPointArea = MinPointArea  # 当loop中任意相邻三点连成三角形面积小于该值，则认为中间点为多余点，可去除
        self.NearPointDistance = NearPointDistance  # 当两点接近时，认为该两点坐标相等的最大距离
        self.MaxFlyDistance = 3  # 计算最佳旋转角度时，排除掉悬空长度超过该值的角度
        self.LoopRotateDict = {}  # 自getLoopRotate()赋值，记录每个loop最佳旋转角度
        self.LoopSequenceList = []  # 自getLoopSequence()赋值，记录每个标签的顺序及坐标
        self.LoopStartPoint = {}  # 记录Loop中填充扫描起始点
        self.LoopStartLabel = {}  # 记录Loop中填充的起始点标志，getLoopStartPoint()中赋值

        self.MaxID_of_DLine = 0  # help to add new records, for examples, LABELs.

        self.OffsetPointDicts = {}  # 增加偏移offset后，以此记录偏移后的点坐标信息
        self.ZValue = 0.0

        for i in self.RecordsList:
            self.base_records.update(self.ReadLine(i))
        # self.make_global_parameters()
        # print "__init__1:%s" % clock()
        t0 = time()

        self.init_Lines()
        t1 = time()

    # print '__init__',t1-t0
    # print "__init__2:%s" % clock()
    def ReadLine(self, line):
        if line[-1] == '\n':
            line = line[:-1]
        # print line
        index = line[-8:].replace(" ", "")
        line = line[:-8]
        if index[0] in ['B', 'C']:
            pass
        elif index[0] == 'S':
            self.start_STR += line

        elif index[0] == 'G':
            self.global_parameter_STR += line

        elif index[0] == 'D':
            '''INIT the Global Parameters'''
            if not self.global_parameter_INITED:
                self.make_global_parameters()

            DLine_ID = int(index[1:])
            menuindex = []
            while line:
                menuindex.append(line[:8].lstrip())
                line = line[8:]

            menuindex += [index]
            if DLine_ID % 2 == 0:
                sub = self.substances[DLine_ID - 1]
                for i in range(10, 20):
                    sub.SetMenuData(i, menuindex[i - 10])
            else:
                sub = Substance()
                for i in range(10):
                    sub.SetMenuData(i, menuindex[i])
                self.substances[DLine_ID] = sub
        elif index[0] == 'P':
            '''get and then pop the index of each line'''
            index = line[-8:]
            line = line[:-8]
            '''split each DATA'''
            line = line.replace(self.records_split, '').replace(' ', '').split(self.parameters_split)
            if '' in line:
                line.remove('')

            sub = self.substances[int(index[1:])]
            sub.AddParameterData(line)

        elif index[0] == 'T':
            self.end_STR += line
            self.MaxID_of_DLine = int(line[17:24])
        return {index: line}

    def init_Lines(self):
        t0 = time()
        for i in self.substances.values():
            i.Instantiate(self.LinesList, self.LabelList, self.SinglePointList)
        t1 = time()
        # print 'init_Lines',t1-t0
        self.LinesDic = {l.id: l for l in self.LinesList}

    def get_global_parameters_list(self):
        result = []
        for i in self.parameters:
            # print 
            result.append(self.writeSTR(self.parameters[i]))
        return result

    def make_global_parameters(self):
        # print self.global_parameter_STR
        i = self.global_parameter_STR.find('H')
        j = int(self.global_parameter_STR[0:i])

        self.parameters_split = self.global_parameter_STR[i + 1:i + j + 1]
        ps = self.global_parameter_STR[0:j + i + 2]
        self.parameters[1] = self.parameters_split

        self.global_parameter_STR = self.global_parameter_STR[j + i + 2:]
        gp = self.global_parameter_STR.split(self.parameters_split)
        gp.insert(0, ps[:-1])
        self.records_split = self.readSTR(gp[1])

        for i in range(2, len(gp)):
            strP = gp[i]
            x = strP.find(self.records_split)
            if x > 0:
                gp[i] = gp[i][:x]
        # print gp

        self.parameters[2] = self.records_split

        self.parameters[3] = self.readSTR(gp[2])
        self.parameters[4] = self.readSTR(gp[3])
        self.parameters[5] = self.readSTR(gp[4])
        self.parameters[6] = self.readSTR(gp[5])

        self.parameters[7] = int(gp[6])
        self.parameters[8] = int(gp[7])
        self.parameters[9] = int(gp[8])
        self.parameters[10] = int(gp[9])
        self.parameters[11] = int(gp[10])
        self.parameters[12] = self.readSTR(gp[11])

        self.parameters[13] = float(gp[12])
        self.parameters[14] = int(gp[13])
        self.parameters[15] = self.readSTR(gp[14])
        self.parameters[16] = int(gp[15])
        self.parameters[17] = float(gp[16])
        self.parameters[18] = self.readSTR(gp[17])
        self.parameters[19] = float(gp[18])
        self.parameters[20] = float(gp[19])
        self.parameters[21] = self.readSTR(gp[20])
        self.parameters[22] = self.readSTR(gp[21])
        self.parameters[23] = int(gp[22])
        self.parameters[24] = int(gp[23])
        self.global_parameter_INITED = True

    def readSTR(self, STR):
        if STR == '' or 'H' not in STR:
            return ""
        i = STR.find('H')
        j = int(STR[0:i])
        return STR[i + 1:i + j + 1]

    def writeSTR(self, STR):
        result = ''
        if type(STR) == type(''):
            result = '%dH%s' % (len(STR), STR) if len(STR) != 0 else ''
        elif type(STR) == type(0) or type(0.0):
            result = str(STR)
        else:
            print(result)
        return result

    def getMaxCoordinate(self):
        return self.parameters[20]

    def setAuthorName(self, STR):
        self.parameters[21] = STR

    def setAuthorInstitution(self, STR):
        self.parameters[22] = STR

    def make_saving_string_in_72(self, flag, STR):
        '''STR:List or String'''
        resultlines = []

        # STR=STR
        if flag in ['B', 'C', 'S']:
            _line_len = 72
            while len(STR) > _line_len:
                resultlines.append(STR[:_line_len])
                STR = STR[_line_len:]
            resultlines.append(('%-' + str(_line_len) + 's') % STR)
        elif flag in ['G', 'P']:
            '''transform STR into a LIST and rebulid a new STRING'''
            _line_len = (72 if flag == 'G' else 64)

            if type(STR) == type(''):
                STR = STR.strip()
                # print STR
                if STR[-1] == self.records_split:
                    STR = STR[:-1]
                # print STR
                STR = STR.split(self.parameters_split)

            tem = ''

            while len(STR) > 0:
                currentITEM = STR.pop(0)
                '''split_code'''
                if len(STR) == 0:
                    i = self.records_split
                else:
                    i = self.parameters_split
                if len(tem + str(currentITEM) + i) <= _line_len:
                    '''SAME LINE'''
                    tem += str(currentITEM) + i
                else:
                    '''ANOTHER LINE'''
                    tem += ' ' * (_line_len - len(tem))
                    resultlines.append(tem)
                    tem = str(currentITEM) + i
            '''END LINE'''
            tem += ' ' * (_line_len - len(tem))
            resultlines.append(tem)
        elif flag in ['D']:
            if type(STR) == type([]):
                tem = ["%8s" * 9 % tuple([i for i in STR[:9]]), "%8s" * 9 % tuple([i for i in STR[10:19]])]
                resultlines += tem
            pass
        return resultlines

    def saveIGES(self, filepath):
        results = ''

        # print len(self.substances)
        # print 'saveIGES--0'
        # print self.substances[233].MenuIndex
        # print self.substances[233].ParameterData
        _S = self.make_saving_string_in_72('S', 'IGES file generated by Python Program')
        _G = self.make_saving_string_in_72('G', self.get_global_parameters_list())
        _DP = []

        # print 'saveIGES--1'
        # print self.substances[233].MenuIndex
        # print self.substances[233].ParameterData

        _substancelist = sorted(self.substances.values(), key=lambda d: d.ID)
        # for i in self.substances.values():
        # print map(lambda x:x.ID,_substancelist)
        # print self.substances
        # print 'saveIGES--2'
        # print self.substances[233].MenuIndex
        # print self.substances[233].ParameterData
        for i in _substancelist:
            ''' 0:the value after 'D' / 'D-Index';	del:(0.5:i.Point,)
				1:the list of D;
				2:the list of P;  '''
            _DP.append([i.ID, self.make_saving_string_in_72('D', i.MenuIndex), \
                        self.make_saving_string_in_72('P', i.ParameterData[:])])
        # print [i.ID,self.make_saving_string_in_72('D',i.MenuIndex),\
        # 	self.make_saving_string_in_72('P',i.ParameterData[:])]
        # print i
        '''S'''
        line_id = 0
        for i in _S:
            line_id += 1
            results += i + 'S%7d' % line_id + '\n'
        lineNUM_S = line_id
        '''G'''
        line_id = 0
        for i in _G:
            line_id += 1
            results += i + 'G%7d' % line_id + '\n'
        lineNUM_G = line_id

        results_P = ''
        results_D = ''
        auto_id_P = 1
        curr_id_p = 1
        lineNUM_D = 0
        lineNUM_P = 0
        for i in _DP:
            lineNUM_D += 2
            '''curr_id_p is ID for each Record,
				auto_id_P is ID for each Line'''

            '''P'''
            curr_id_p = auto_id_P
            for j in i[2]:
                # print [j+'%8d'%i[0]+'P%7s'%auto_id_P+'\n']
                results_P += j + '%8d' % i[0] + 'P%7s' % auto_id_P + '\n'
                auto_id_P += 1
            '''D'''
            d = i[1]
            d[0] = d[0][:8] + '%8s' % curr_id_p + d[0][16:]
            results_D += d[0] + 'D%7d' % i[0] + '\n' \
                         + d[1] + 'D%7d' % (i[0] + 1) + '\n'
        lineNUM_P = auto_id_P - 1
        results += results_D + results_P

        # print results_P

        '''T'''
        results += 'S%7d' % lineNUM_S + 'G%7d' % lineNUM_G + \
                   'D%7d' % lineNUM_D + 'P%7d' % lineNUM_P + \
                   ' ' * 40 + 'T%7d\n' % 1
        # print results
        filehandle = open(filepath, 'w')
        filehandle.writelines(results)
        filehandle.close()

    # def getDisconnected_Lines(self):
    # 	Disconnect_LINES=[i for i in self.LinesList if len(i.adjustLine[0])*len(i.adjustLine[1])==0]

    def IfClosed(self):
        re = True
        # print self.LinesList
        # print '3941:',Line.LINE_DIC[3941].adjustLine
        # print '3941:',map(lambda p:p.getPOS(),Line.LINE_DIC[3941].P_list)
        # print '3943:',Line.LINE_DIC[3943].adjustLine
        # print '3943:',map(lambda p:p.getPOS(),Line.LINE_DIC[3943].P_list)
        for i in self.LinesList:
            if len(i.adjustLine[0]) * len(i.adjustLine[1]) == 0:
                re = False
                # print i.adjustLine,i.id
                print("OPEN AT Point(%f,%f,%f) - Point(%f,%f,%f)" % tuple(i.P1.pos + i.P2.pos))
                break

        # exit()
        return re

    def SolveDisconnected_LINES(self):
        while True:
            Disconnect_LINES = [i for i in self.LinesList if len(i.adjustLine[0]) * len(i.adjustLine[1]) == 0]
            # print 'SolveDisconnected_LINES',Disconnect_LINES
            # nullp_list={}
            if len(Disconnect_LINES) < 2:
                break
            # print Disconnect_LINES
            minDistence = 0
            minLines = []

            for i in Disconnect_LINES:
                for j in Disconnect_LINES:
                    if i == j:
                        continue
                    i_plist = i.getDisconnectedPoint()
                    j_plist = j.getDisconnectedPoint()

                    plist = [(m, n) for m in i_plist for n in j_plist]
                    # fine each nearest point-point
                    for k in plist:
                        D = k[0].getDistence(k[1])
                        if len(minLines) == 0 or D < minDistence:
                            minDistence = D
                            minLines = [k[0], k[1], i, j]
            # print 
            self.Connecting_LINES(minLines[0], minLines[1], minLines[2], minLines[3])
            minLines[2].substance.Refresh_ParameterData()
            minLines[3].substance.Refresh_ParameterData()

    def Connecting_LINES(self, p1, p2, L1, L2):
        len1 = L1.getLength()
        len2 = L2.getLength()
        k1, k2 = len1 / (len1 + len2), len2 / (len1 + len2)
        x = p1.x * k1 + p2.x * k2
        y = p1.y * k1 + p2.y * k2
        z = p1.z * k1 + p2.z * k2

        midPoint = Point.getPoint([x, y, z])

        if L1.P1.getPOS() == p1.getPOS():
            # print '1'+L1.P1.getPOS(),p1.getPOS()
            L1.P1 = midPoint
            L1.adjustLine[0].append(L2.id)
        else:
            # print '2'+L1.P2.getPOS(),p1.getPOS()
            L1.P2 = midPoint
            L1.adjustLine[1].append(L2.id)
        if L2.P1.getPOS() == p2.getPOS():
            # print '1'+L2.P1.getPOS(),p1.getPOS()
            L2.P1 = midPoint
            L2.adjustLine[0].append(L1.id)
        else:
            # print L2.P2.getPOS(),p2.getPOS()
            L2.P2 = midPoint
            L2.adjustLine[1].append(L1.id)
        L1.P_list[0] = L1.P1
        L1.P_list[-1] = L1.P2

        L2.P_list[0] = L2.P1
        L2.P_list[-1] = L2.P2

    def breakLineAtPoint(self, LineID, p):
        # print line.P_list
        line = self.LinesDic[LineID]

        adjustL1 = self.LinesDic[line.adjustLine[0][0]]
        adjustL2 = self.LinesDic[line.adjustLine[1][0]]
        _Rflag = 0

        if line.P1 in [adjustL1.P1, adjustL1.P2]:
            left_l = adjustL1
            right_l = adjustL2
            _Rflag = 1
        else:
            left_l = adjustL2
            right_l = adjustL1
            _Rflag = 0

        for i in range(len(line.P_list) - 1):

            _p1 = line.P_list[i].getPOS()
            _p2 = line.P_list[i + 1].getPOS()
            dx1 = _p1[0] - p[0]
            dx2 = p[0] - _p2[0]
            dy1 = _p1[1] - p[1]
            dy2 = p[1] - _p2[1]

            # print dx1,dy2,':', p[1],_p2[1], dx2,dy1 , dx1*dx2>=0 , dy1*dy2>=0
            if dx1 * dy2 == dx2 * dy1 and dx1 * dx2 >= 0 and dy1 * dy2 >= 0:
                end_i = i
                next_start_i = i + 1
                break
            else:
                end_i, next_start_i = [-1, -1]
        plist = [p] + [_p.getPOS() for _p in line.P_list[next_start_i:]]

        AddLine_id = self.AddLineList(plist, LineID, right_l)
        line.adjustLine[_Rflag].remove(right_l.id)
        line.adjustLine[_Rflag].append(AddLine_id[0])

        _p = Point.getPoint(p[0], p[1], p[2])
        # print p.getPOS()
        line.P_list = line.P_list[:next_start_i] + [_p]
        line.P2 = line.P_list[-1]
        line.substance.Refresh_ParameterData()

        if line.id == right_l.adjustLine[0][0]:
            right_l.adjustLine[0].remove(line.id)
            right_l.adjustLine[0].append(AddLine_id[1])
        else:
            right_l.adjustLine[1].remove(line.id)
            right_l.adjustLine[1].append(AddLine_id[1])

    def AddLineList(self, plist, num1, num2, col='DEFAULT'):
        '''l1.num1+plist+l2.num2'''
        left_id = num1
        right_id = -1
        l_list = []
        for i in range(len(plist) - 1):
            p1 = plist[i]
            p2 = plist[i + 1]
            l_list.append(self.AddSingleLine(p1, p2, col))
        for i, l in enumerate(l_list):
            l.adjustLine[0].append(left_id)
            if i > 0:
                l_list[i - 1].adjustLine[1].append(l.id)
            if l == l_list[-1]:
                l.adjustLine[1].append(num2)
            left_id = l.id
        return [l_list[0].id, l_list[-1].id]

    def AddSingleLine(self, p1, p2, col='DEFAULT', colvalue=None):
        new_sub = Substance()
        new_sub.SetMenuData(0, '110')
        new_sub.SetMenuData(2, '0')
        new_sub.SetMenuData(3, '1')
        new_sub.SetMenuData(4, '0')
        new_sub.SetMenuData(5, '0')
        new_sub.SetMenuData(6, '0')
        new_sub.SetMenuData(7, '0')
        new_sub.SetMenuData(8, '00000000')
        new_sub.SetMenuData(10, '110')
        new_sub.SetMenuData(11, '70')
        new_sub.SetMenuData(13, '2')
        new_sub.SetMenuData(14, '0')

        if colvalue == None:
            col_id = IGESFile.Color_Dic[col.upper()]
            new_sub.SetMenuData(12, col_id)

        new_sub.AddParameterData(['110'] + p1 + p2)
        '''13记录参数行数'''
        txt = new_sub.ParameterData[:]
        plinenum = self.getLineNumberOfParam(txt)
        new_sub.SetMenuData(13, '%d' % plinenum)

        new_sub.ID = self.MaxID_of_DLine + 1
        self.MaxID_of_DLine += 2
        self.substances[new_sub.ID] = new_sub
        line = Line(new_sub, new_sub.ID)
        self.LinesList.append(line)
        self.LinesDic[line.id] = line
        # print '-----',self.MaxID_of_DLine
        # if p1 == [164.945188516,250.052486793,0.0]:print '+++'
        # print p1
        return line
    def AddSingleCircle(self, centerP, StartP, EndP, col='DEFAULT', colvalue=None):
        new_sub = Substance()
        '''
             100       1       0       1       0       0       0       000000000D      1
             100      70       8       1       0                                D      2
        '''
        new_sub.SetMenuData(0, '100')
        new_sub.SetMenuData(2, '0')
        new_sub.SetMenuData(3, '1')
        new_sub.SetMenuData(4, '0')
        new_sub.SetMenuData(5, '0')
        new_sub.SetMenuData(6, '0')
        new_sub.SetMenuData(7, '0')
        new_sub.SetMenuData(8, '00000000')
        new_sub.SetMenuData(10, '100')
        new_sub.SetMenuData(11, '70')
        new_sub.SetMenuData(13, '1')
        new_sub.SetMenuData(14, '0')

        if colvalue == None:
            col_id = IGESFile.Color_Dic[col.upper()]
            new_sub.SetMenuData(12, col_id)

        new_sub.AddParameterData(['100'] + centerP[2:] + centerP[:2] + StartP[:2] + EndP[:2])
        '''13记录参数行数'''
        txt = new_sub.ParameterData[:]
        plinenum = self.getLineNumberOfParam(txt)
        new_sub.SetMenuData(13, '%d' % plinenum)

        new_sub.ID = self.MaxID_of_DLine + 1
        self.MaxID_of_DLine += 2
        self.substances[new_sub.ID] = new_sub
        circle = Circle(new_sub, new_sub.ID)
        self.CirclesList.append(circle)
        self.CirclesDic[circle.id] = circle
        # print '-----',self.MaxID_of_DLine
        # if p1 == [164.945188516,250.052486793,0.0]:print '+++'
        # print p1
        return circle

    def AddSplineLine(self, length, col='DEFAULT'):
        new_sub = Substance()
        new_sub.SetMenuData(0, '102')
        new_sub.SetMenuData(2, '0')
        new_sub.SetMenuData(3, '0')
        new_sub.SetMenuData(4, '0')
        new_sub.SetMenuData(5, '0')
        new_sub.SetMenuData(6, '0')
        new_sub.SetMenuData(7, '0')
        new_sub.SetMenuData(8, '00000000')
        new_sub.SetMenuData(10, '102')
        new_sub.SetMenuData(11, '70')
        new_sub.SetMenuData(13, '1')
        new_sub.SetMenuData(14, '0')

        col_id = IGESFile.Color_Dic[col.upper()]
        new_sub.SetMenuData(12, col_id)

        _param = []
        for i in range(length):
            _param += [str(i * 2 + 3)]

        _param += ['0'] + ['0']

        new_sub.AddParameterData(['102'] + ['%d' % length] + _param)
        '''13记录参数行数'''
        txt = new_sub.ParameterData[:]
        plinenum = self.getLineNumberOfParam(txt)
        new_sub.SetMenuData(13, '%d' % plinenum)

        new_sub.ID = self.MaxID_of_DLine + 1
        self.MaxID_of_DLine += 2
        self.substances[new_sub.ID] = new_sub
        print('AddSplineLine')
        pass

    def AddLabel(self, substance, pos=[0, 0, 0]):
        new_sub = Substance()
        new_sub.MenuIndex = substance.MenuIndex[:]
        new_sub.ParameterData = substance.ParameterData[:]
        new_sub.ParameterData[10:13] = pos
        new_sub.ID = self.MaxID_of_DLine + 1
        self.MaxID_of_DLine += 2

        self.substances[new_sub.ID] = new_sub

        label = Label(new_sub, new_sub.ID)
        self.LabelList.append(label)
        # print self.substances[51].ParameterData
        pass

    def getLabelList(self):
        return self.LabelList

    def getLoopCenterPoint(self, loop):
        '''
		根据loop的X中间坐标mid_X，求x=mid_X 与loop交点的中间点
		'''

        # print map(lambda line_id: self.LinesDic[line_id].getXRange() ,loop)
        px_list = reduce(lambda a, b: a + b, map(lambda line_id: self.LinesDic[line_id].getXRange(), loop))

        # print '---',map(lambda line_id:self.LinesDic[line_id].getPointXYZ(),loop)
        # px_list = map(lambda line_id:self.LinesDic[line_id].getPoints()[0][0],loop)
        Z = self.LinesDic[loop[0]].getPoints()[0][2]

        mid_X = (max(px_list) + min(px_list)) * float(0.5)
        while True:
            if mid_X not in px_list:
                break
            mid_X += uniform(-0.1, 0.1)

        cross_Y_list = []
        for l_id in loop:
            # pos1,pos2 = self.LinesDic[l_id].getPoints()
            for i in range(len(self.LinesDic[l_id].P_list) - 1):
                pos1 = self.LinesDic[l_id].P_list[i].getPOS()
                pos2 = self.LinesDic[l_id].P_list[i + 1].getPOS()
                # print '+++',pos1,pos2
                if (pos1[0] - mid_X) * (pos2[0] - mid_X) < 0:
                    '''根据每条线的两点X坐标，当前点在其中时求交点Y值并列表crosspoints中
							y = y0+(x-x0)*(y1-y0)/(x1-x0)
					'''
                    x0, y0 = pos1[:-1]
                    x1, y1 = pos2[:-1]
                    cross_Y_list.append(y0 + (mid_X - x0) * (y1 - y0) / (x1 - x0))
        cross_Y_list.sort()
        if len(cross_Y_list) >= 2:
            return [mid_X, (cross_Y_list[0] + cross_Y_list[1]) * float(0.5), Z]
        else:
            return False

    def MakeLineLoop(self, makeorder=True):
        '''此函数在MakeLoopOrder()中已调用
		存在安全隐患，若loop为凹图形，中心点有可能不在loop中--已解决
		self.LoopsCenterList不允许删除元素
		'''
        self.LoopsList = []
        self.LoopsCenterList = []

        # def make_one_loop(loop,linedic,l):
        # 	loop.append(l.id)
        # 	for i in l.adjustLine:
        # 		if i[0] in loop:
        # 			continue
        # 		else:
        # 			make_one_loop(loop,linedic,linedic[i[0]])
        def make_one_loop(loop, linedic, l):
            _current_id = l.id
            while True:
                loop.append(_current_id)
                try:
                    _current_id = [i for i in linedic[_current_id].adjustLine if i[0] not in loop][-1][0]
                except:
                    break
            pass

        linelist = self.LinesList[:]
        linedic = self.LinesDic
        while linelist:
            l = linelist[0]
            loop = []
            make_one_loop(loop, linedic, l)

            cenX, cenY, cenZ = [0, 0, 0]
            sumlength = 0
            for l_id in loop:
                try:
                    linelist.remove(linedic[l_id])
                except:
                    pass
                length = float(linedic[l_id].getLength())
                cenX += length * (linedic[l_id].getPoints()[0][0] + linedic[l_id].getPoints()[1][0])
                cenY += length * (linedic[l_id].getPoints()[0][1] + linedic[l_id].getPoints()[1][1])
                cenZ += length * (linedic[l_id].getPoints()[0][2] + linedic[l_id].getPoints()[1][2])
                sumlength += length
            cenX /= float(2.0) * sumlength
            cenY /= float(2.0) * sumlength
            cenZ /= float(2.0) * sumlength

            if len(loop) > 2:
                self.LoopsList.append(loop)
                self.LoopsCenterList.append(self.getLoopCenterPoint(loop))
        # self.LoopsCenterList.append([cenX,cenY,cenZ])
        if makeorder:
            '''将loop顶点最近排序，更新LoopsCenterList及LoopsList'''
            LoopSequence.Sequence.refresh()
            LoopSequenceList = list(LoopSequence.LoopSequence(self.LoopsCenterList).makeDistanceDict())
            _LoopcenterList_ordered = []
            _LoopsList_ordered = []
            for loopid in range(len(self.LoopsList)):
                loopid_in_Oldlist = self.LoopsCenterList.index(LoopSequenceList[loopid])
                _LoopsList_ordered.append(self.LoopsList[loopid_in_Oldlist])
                _LoopcenterList_ordered.append(self.LoopsCenterList[loopid_in_Oldlist])
            self.LoopsList = _LoopsList_ordered
            self.LoopsCenterList = _LoopcenterList_ordered

    def MakeLoopClockwise(self, looplayerDict):
        '''
		关于如何判定多边形是顺时针还是逆时针对于凸多边形而言，只需对某一个点计算cross product = ((xi - xi-1),(yi - yi-1)) x ((xi+1 - xi),(yi+1 - yi)) 
		= (xi - xi-1) * (yi+1 - yi) - (yi - yi-1) * (xi+1 - xi)
		如果上式的值为正，逆时针；为负则是顺时针
		而对于一般的简单多边形，则需对于多边形的一个凸点计算上述值即可，此处选取X值最大点。

		为了保证outer多边形能向内offset，inner多边形能向外offset，这里需要保证outer多边形是逆时针方向旋转的，inner多边形是顺时针方向旋转的。
		'''
        anticlockwise_loop_list = []
        clockwise_loop_list = []
        for loopid in self.LoopPointsListDict:
            loop_points_list = self.LoopPointsListDict[loopid]
            Xlist = list(map(lambda p: p.getPOS()[0], loop_points_list))

            # print map(lambda p:p.getPOS(),loop_points_list)
            # print list(enumerate(Xlist))
            try:
                # maxX_p = list(filter(lambda i, x: x == max(Xlist), list(enumerate(Xlist)))[0][0])
                maxX_p = list(filter(lambda item: item[1] == max(Xlist), list(enumerate(Xlist))))[0][0]
            except:
                print('%s ERROR:(FUN:MakeLoopClockwise)\n' % self.FileName)
            # print maxX_p
            maxX_p_i = [len(Xlist) - 1, maxX_p - 1][maxX_p > 0]
            maxX_p_j = [0, maxX_p + 1][maxX_p < len(Xlist) - 1]
            [x, y] = loop_points_list[maxX_p].getPOS()[:2]
            [x_i, y_i] = loop_points_list[maxX_p_i].getPOS()[:2]
            [x_j, y_j] = loop_points_list[maxX_p_j].getPOS()[:2]
            if (x - x_i) * (y_j - y) - (y - y_i) * (x_j - x) > 0:
                '''记录逆时针loop'''
                anticlockwise_loop_list.append(loopid)
            else:
                '''记录顺时针loop'''
                clockwise_loop_list.append(loopid)

        # print self.LoopPointsListDict
        '''统一为顺时针    统一为外逆内顺'''
        for outloopid in looplayerDict:
            if outloopid in clockwise_loop_list:
                self.LoopPointsListDict[outloopid].reverse()
            for inloopid in looplayerDict[outloopid]:
                if inloopid in anticlockwise_loop_list:
                    self.LoopPointsListDict[inloopid].reverse()
        # map(lambda loopid:self.LoopPointsListDict[loopid].reverse(),anticlockwise_loop_list)
        # print self.LoopPointsListDict
        pass

    def MakeInnerlinePointIDList(self, distance):
        '''
		为outlinePointID赋值，格式为[[P1id, P2id, ...], ...]
		:return:
		'''
        self.inlinePointID = []
        for loopid in self.LoopPointsListDict:
            # 对所有Loop遍历
            _loopPids = self.LoopPointsListDict[loopid]
            for i in range(len(_loopPids)):
                # 遍历当前loop的相邻两点
                j = [i + 1, 0][i == (len(_loopPids) - 1)]
                for otherloopPids in [self.LoopPointsListDict[id] for id in self.LoopPointsListDict if id != loopid]:
                    if Point.IfLineParallelAndNearLoop(otherloopPids, _loopPids[i], _loopPids[j], distance):
                        self.inlinePointID.append([_loopPids[i].getID(), _loopPids[j].getID()])
        pass

    def PointIfInLoop(self, pos, loop):
        nCross = 0
        for i in loop:
            line = self.LinesDic[i]
            # print line
            for i in range(len(line.P_list) - 1):
                j = i + 1
                p1 = line.P_list[i]
                p2 = line.P_list[j]

                if p1.y == p2.y:
                    continue
                if pos[1] < min(p1.y, p2.y):
                    continue
                if pos[1] > max(p1.y, p2.y):
                    continue
                x = 1.0 * (pos[1] - p1.y) * (p2.x - p1.x) / (p2.y - p1.y) + p1.x
                if x > pos[0]:
                    nCross += 1
        return (nCross % 2 == 1)

    def PointIfInLoop2(self, pos, loopid, rangeX, rangeY):
        '''edit at 2016-02-15'''

        if pos[0] < rangeX[0] or pos[0] > rangeX[1] or pos[1] < rangeY[0] or pos[1] > rangeY[1]: return False

        def check(_pos):
            nCross = 0
            _PointList = self.LoopPointsListDict[loopid]
            for i in range(len(_PointList)):
                # if i==2:
                # 	pdb.set_trace()
                j = [i + 1, 0][i == (len(_PointList) - 1)]
                # j = i+1
                # if j == len(_PointList): j = 0
                p1 = _PointList[i]
                p2 = _PointList[j]

                if _pos[1] < min(p1.y, p2.y):
                    continue
                if _pos[1] > max(p1.y, p2.y):
                    continue
                if p1.y == p2.y:
                    '''p1.y==p2.y==pos[1]'''
                    m = [len(_PointList) - 1, i - 1][i != 0]
                    n = [0, j + 1][j != (len(_PointList) - 1)]
                    p3 = _PointList[m]
                    p4 = _PointList[n]
                    if (p3.y - p2.y) * (p4.y - p2.y) < 0:
                        nCross += 1
                    continue
                if p1.y == _pos[1]:
                    m = [len(_PointList) - 1, i - 1][i != 0]
                    p3 = _PointList[m]
                    if (p3.y - p1.y) * (p2.y - p1.y) < 0 and p1.x > _pos[0]:
                        nCross += 0.5
                    continue
                if p2.y == _pos[1]:
                    n = [0, j + 1][j != (len(_PointList) - 1)]
                    p4 = _PointList[n]
                    if (p1.y - p2.y) * (p4.y - p2.y) < 0 and p1.x > _pos[0]:
                        nCross += 0.5
                    continue

                x = 1.0 * (_pos[1] - p1.y) * (p2.x - p1.x) / (p2.y - p1.y) + p1.x
                if x > _pos[0]:
                    nCross += 1
            return (nCross % 2 == 1)

        # poslist = [map(lambda a,b:a+b, pos,[choice([-1,1])*random.random()/100,choice([-1,1])*random.random()/100,choice([-1,1])*random.random()/100]) for i in range(10)]
        # return sum(map(check,poslist))>=5
        pos = [choice([-1, 1]) * random() / 100 + pos[0], choice([-1, 1]) * random() / 100 + pos[1],
               choice([-1, 1]) * random() / 100 + pos[2]]
        return (check(pos) % 2 == 1)

    # def MovePointIntoLoop(self,pos,loopid):
    # 	_PointList=self.LoopPointsListDict[loopid]
    # 	print _PointList
    # 	pass
    def SmoothLoop(self):
        '''
		此函数为去除loop中临近点
		'''
        self.SolveDisconnected_LINES()
        if not self.IfClosed():
            print('%s ERROR:LOOP OPEN!(FUN:SmoothLoop)\n' % self.FileName)
            return

        self.MakeLineLoop()

        _loopdict = {}
        _loopINFOdict = {}
        _loopContainDict = {}
        '''initialize _loopdict, self.LoopIDdict, self.LoopPointsListDict and _loopINFOdict'''
        for i in range(len(self.LoopsList)):
            _loopdict[i] = self.LoopsList[i]
            self.LoopIDdict[i] = self.LoopsList[i]
            _temPoints = []
            for j in _loopdict[i]:
                if _temPoints == []:
                    _temPoints += self.LinesDic[j].P_list
                else:
                    if self.LinesDic[j].P_list[0].getPOS() == _temPoints[-1].getPOS():
                        _temPoints += self.LinesDic[j].P_list[1:]
                    elif self.LinesDic[j].P_list[-1].getPOS() == _temPoints[-1].getPOS():
                        _temPoints += self.LinesDic[j].P_list[::-1][1:]
                    elif self.LinesDic[j].P_list[0].getPOS() == _temPoints[0].getPOS():
                        _temPoints.reverse()
                        _temPoints += self.LinesDic[j].P_list[1:]
                    # print 'self.LinesDic[j].P_list[0] == _temPoints[0]:'
                    elif self.LinesDic[j].P_list[-1].getPOS() == _temPoints[0].getPOS():
                        _temPoints.reverse()
                        _temPoints += self.LinesDic[j].P_list[::-1][1:]
                    # print 'self.LinesDic[j].P_list[-1] == _temPoints[0]:'
                    else:
                        print('%s ERROR: Unknown Error (FUN:SmoothLoop)!\n' % self.FileName)
            _temPoints = _temPoints[:-1]

            '''remove Y-EQUAL and X-EQUAL Pointss '''
            m, n, o = 0, 1, 2
            while True:
                '''check'''
                if abs(_temPoints[m].x - _temPoints[n].x) < 10 ** (-2) and abs(
                        _temPoints[m].y - _temPoints[n].y) < 10 ** (-2):
                    # print '~~~', m,n,o
                    _temPoints.pop(n)
                    m, n, o = 0, 1, 2

                if (abs(_temPoints[m].x - _temPoints[n].x) < 10 ** (-2) and abs(
                        _temPoints[n].x - _temPoints[o].x) < 10 ** (-2)) or (
                        abs(_temPoints[m].y - _temPoints[n].y) < 10 ** (-2) and abs(
                        _temPoints[n].y - _temPoints[o].y) < 10 ** (-2)):
                    _temPoints.pop(n)
                    m, n, o = 0, 1, 2
                '''根据三角形面积，判断是否去除中间点，面积过小，则判定可将两线段合并
				面积公式：S = x1y2+x2y3+x3y1-x1y3-x2y1-x3y2'''
                S = _temPoints[m].x * _temPoints[n].y + _temPoints[n].x * _temPoints[o].y + _temPoints[o].x * \
                    _temPoints[m].y \
                    - _temPoints[m].x * _temPoints[o].y - _temPoints[n].x * _temPoints[m].y - _temPoints[o].x * \
                    _temPoints[n].y
                if abs(S) < self.MinPointArea:
                    # print S
                    _temPoints.pop(n)
                    m, n, o = 0, 1, 2

                if o == 1: break
                '''change'''
                m, n, o = map(lambda x: [x + 1, 0][x + 1 > len(_temPoints) - 1], [m, n, o])

            self.LoopPointsListDict[i] = _temPoints

    def MakeLoopOrder(self, makeorder=True):
        ''' Make the Order of each LOOP '''
        '''此函数为获取各loop的嵌套关系，部分功能与SmoothLoop重复'''
        # def checkcenterY(pos,loopid,x1,x2,y1,y2):
        # 	pass
        # 	if self.PointIfInLoop2(pos,loopid,[x1,x2],[y1,y2]):
        # 		return True
        # 	else:
        # 		if pos
        self.SolveDisconnected_LINES()
        if not self.IfClosed():
            print('%s ERROR:Loop Open(FUN:MakeLoopOrder)\n' % self.FileName)
            return
        self.MakeLineLoop(makeorder=makeorder)

        # print self.LinesDic

        _loopdict = {}
        _loopINFOdict = {}
        _loopContainDict = {i: [] for i in range(len(self.LoopsList))}
        '''initialize _loopdict, self.LoopIDdict, self.LoopPointsListDict and _loopINFOdict'''
        for i in range(len(self.LoopsList)):
            _loopdict[i] = self.LoopsList[i]
            self.LoopIDdict[i] = self.LoopsList[i]
            _temPoints = []
            for j in _loopdict[i]:
                if _temPoints == []:
                    _temPoints += self.LinesDic[j].P_list
                else:
                    if self.LinesDic[j].P_list[0].getPOS() == _temPoints[-1].getPOS():
                        _temPoints += self.LinesDic[j].P_list[1:]
                    elif self.LinesDic[j].P_list[-1].getPOS() == _temPoints[-1].getPOS():
                        _temPoints += self.LinesDic[j].P_list[::-1][1:]
                    elif self.LinesDic[j].P_list[0].getPOS() == _temPoints[0].getPOS():
                        _temPoints.reverse()
                        _temPoints += self.LinesDic[j].P_list[1:]
                    # print 'self.LinesDic[j].P_list[0] == _temPoints[0]:'
                    elif self.LinesDic[j].P_list[-1].getPOS() == _temPoints[0].getPOS():
                        _temPoints.reverse()
                        _temPoints += self.LinesDic[j].P_list[::-1][1:]
                    # print 'self.LinesDic[j].P_list[-1] == _temPoints[0]:'
                    else:
                        print('%s ERROR: Unknown Error(FUN:MakeLoopOrder)\n' % self.FileName)

            _temPoints = _temPoints[:-1]
            if not _temPoints:
                break
            '''remove Y-EQUAL and X-EQUAL Points '''
            m, n, o = 0, 1, 2
            _temEmpty = False
            while True:
                '''check'''
                if not _temPoints:
                    _temEmpty = True
                    break
                if len(_temPoints) < 3:
                    _temEmpty = True
                    break
                if len(_temPoints)==5 and -224<_temPoints[0].getPOS()[0]<-219:
                    pass
                # print _temPoints
                if abs(_temPoints[m].x - _temPoints[n].x) < self.NearPointDistance and abs(
                        _temPoints[m].y - _temPoints[n].y) < self.NearPointDistance:
                    # print '~~~', m,n,o
                    # if i ==12:
                    # 	pass
                    _temPoints.pop(n)
                    # print "1_temPoints.pop(n)"
                    m, n, o = 0, 1, 2
                    # if not _temPoints:
                    #     break
                    if _temPoints == []:
                        pass
                if len(_temPoints) < 3:
                    _temEmpty = True
                    break
                try:
                    if (abs(_temPoints[m].x - _temPoints[n].x) < self.NearPointDistance and abs(
                            _temPoints[n].x - _temPoints[o].x) < self.NearPointDistance) or (
                            abs(_temPoints[m].y - _temPoints[n].y) < self.NearPointDistance and abs(
                            _temPoints[n].y - _temPoints[o].y) < self.NearPointDistance):
                        _temPoints.pop(n)
                        # print "2_temPoints.pop(n)"
                        m, n, o = 0, 1, 2
                    if len(_temPoints) < 3:
                        _temEmpty = True
                        break
                except:
                    print('%s ERROR:(FUN:MakeLoopOrder)\n' % self.FileName)
                '''根据三角形面积，判断是否去除中间点，面积过小，则判定可将两线段合并
				面积公式：S = x1y2+x2y3+x3y1-x1y3-x2y1-x3y2'''

                try:
                    S = _temPoints[m].x * _temPoints[n].y + _temPoints[n].x * _temPoints[o].y + _temPoints[o].x * \
                        _temPoints[m].y \
                        - _temPoints[m].x * _temPoints[o].y - _temPoints[n].x * _temPoints[m].y - _temPoints[o].x * \
                        _temPoints[n].y
                except:
                    print('%s ERROR:(FUN:MakeLoopOrder)\n' % self.FileName)
                if abs(S) < self.MinPointArea:
                    # print S
                    _temPoints.pop(n)

                    # print "3_temPoints.pop(n)"
                    m, n, o = 0, 1, 2
                    if len(_temPoints) < 3:
                        _temEmpty = True
                        break
                    # if not _temPoints:
                    #     break

                if o == 1: break
                '''change'''
                m, n, o = list(map(lambda x: [x + 1, 0][x + 1 > len(_temPoints) - 1], [m, n, o]))
            if _temEmpty: continue
            self.LoopPointsListDict[i] = _temPoints

            '''get Max and Min value of X,Y, and write to _loopINFOdict'''
            try:
                _X = list(map(lambda x: x.getPOS()[0], self.LoopPointsListDict[i]))
                _Y = list(map(lambda x: x.getPOS()[1], self.LoopPointsListDict[i]))
                _loopINFOdict[i] = {'OutsideLoopList': [], 'RangeX': [min(_X), max(_X)], 'RangeY': [min(_Y), max(_Y)],
                                    'Center': []}
            except:
                print('%s ERROR:(FUN:MakeLoopOrder)\n' % self.FileName)
        # _centerx = (min(_X)+max(_X))/2
        # _centery = (min(_Y)+max(_Y))/2

        self.LoopINFODict = _loopINFOdict
        '''initialize "OutsideLoopList" of _loopINFOdict'''

        for i in _loopdict:
            # for i in range(len(self.LoopsList)):
            _pos = self.LinesDic[_loopdict[i][0]].P_list[0].getPOS()
            for j in _loopdict:
                if i == j: continue

                if i not in _loopINFOdict: continue
                if j not in _loopINFOdict: continue
                if i == 2 and j == 0:
                    pass
                if self.PointIfInLoop2(_pos, j, _loopINFOdict[j]['RangeX'], _loopINFOdict[j]['RangeY']):
                    _loopINFOdict[i]['OutsideLoopList'].append(j)

        # print '\n_loopINFOdict:  ',_loopINFOdict

        for i in _loopINFOdict:
            for j in _loopINFOdict[i]['OutsideLoopList']:
                if j in _loopContainDict:
                    _loopContainDict[j].append(i)
                else:
                    _loopContainDict[j] = [i]
        # print '\n_loopContainDict:  ',_loopContainDict

        '''filter'''
        _headloopIDList = []
        _subloopIDList = []
        _removedloopIDList = []
        _remainloopIDList = []
        _temploopContainDict = {}
        for i in _loopContainDict:
            _inside = []
            for j in _loopContainDict[i]:
                if j not in _loopContainDict: continue
                _inside += _loopContainDict[j]

            _temploopContainDict[i] = list(set(_loopContainDict[i]) - set(_inside))
            _subloopIDList += _temploopContainDict[i]

        _subloopIDList = list(set(_subloopIDList))
        _headloopIDList = list(set(_loopContainDict.keys()) - set(_subloopIDList))

        _remainloopIDList = _headloopIDList[:]
        _sumloop = list(_loopContainDict.keys())[:]
        _currentloopIDList = _headloopIDList[:]
        # print '_loopContainDict:  ',_loopContainDict
        # print '_temploopContainDict:  ',_temploopContainDict
        while len(_sumloop) > 0:
            _nextloopIDList = []
            for i in _currentloopIDList:
                if i in _remainloopIDList:
                    _removedloopIDList += _temploopContainDict[i]
                else:
                    _remainloopIDList += _temploopContainDict[i]
                _sumloop.remove(i)
                _nextloopIDList += _temploopContainDict[i]
            _currentloopIDList = _nextloopIDList
            pass
        re = {i: _temploopContainDict[i] for i in _temploopContainDict if i in _remainloopIDList}
        return re

    def MakeOFFSETLoops(self, offset):
        '''
		本函数为各loop增加偏移量offset，正值向内扩展
		'''
        # print 'MakeOFFSETLoops'
        _currentOFFSETLoops = []
        for loopid, looppoints in self.LoopPointsListDict.items():
            ost = Offset(plist=looppoints)
            poslist = ost.getNEWPlistByOffset(offset)
            if poslist:
                pidlist = ost.solveCrossLine(map(lambda pos: Point.getPoint(pos), poslist))
                _currentOFFSETLoops.extend(pidlist)
        self.OffsetPointDicts[offset] = Offset.solveCrossLoop(_currentOFFSETLoops)
        # print 'OK'
        return self.OffsetPointDicts[offset]

    def MakeOneOFFSETLoops(self, offset, loopslist):
        _currentOFFSETLoops = []
        # t1=time()
        for looppoints in loopslist:
            ost = Offset(pidlist=looppoints)
            poslist = ost.getNEWPlistByOffset(offset)
            # print poslist
            if poslist:
                if type(poslist[0][0]) == float:
                    pidlist = ost.solveCrossLine(map(lambda pos: Point.getPoint(pos), poslist))
                    _currentOFFSETLoops.extend(pidlist)
                elif type(poslist[0][0]) == list:
                    # re = []
                    for loop in poslist:
                        pidlist = ost.solveCrossLine(map(lambda pos: Point.getPoint(pos), loop))
                        _currentOFFSETLoops.extend(pidlist)
        # print 'MakeOneOFFSETLoops before solveCrossLoop ', time() - t1
        return Offset.solveCrossLoop(_currentOFFSETLoops)

    def MakeOFFSETListLoops(self, offsetlist, IfComplexFill=False, ComplexFillArea_alert_lowValue=150,
                            ComplexFillArea_alert_highValue=4000, ComplexFillWidth_alert_lowValue=6,
                            ComplexFillWidth_alert_highValue=30, ComplexFillWidth_alert_low_Length=15,
                            ComplexFillWidth_alert_high_Length=15):
        '''根据offsetlist，基于上一个offset结果得到当前offset结果，节约资源
		offsetlist = [-8,-6,-10,-3,5,-1,4,6,3,8]
		'''
        # print 'MakeOFFSETListLoops START!'
        t1 = time()
        offsetlist_positive = sorted(filter(lambda a: [None, a][a > 0], offsetlist))
        offsetlist_negative = sorted(filter(lambda a: [None, a][a < 0], offsetlist), reverse=True)

        def GetOffsetsPointDicts(_offsetlist, _loopslist):
            _pre_offset = 0
            _pre_loopslist = _loopslist
            for offset in _offsetlist:
                # print 'MakeOFFSETListLoops:',offset
                # if abs(offset -(-2.4))<0.001:
	             #    pass
                _crt_offset = offset - _pre_offset
                # if (int)(_crt_offset) == (int)(-5.2):
                #     for pidlist in _pre_loopslist:
                #         ReadIGESFiles.IGESFile.drawPointIntoIGESFile(
                #             r"G:\test\pidlist_in_%s-%s.igs" % (
                #             ['Backforward', 'Forward'][Point.IfLoopClockwise(PIDList=pidlist)], str(pidlist)[:20]),
                #             map(lambda pid: Point.PointDict[pid].getPOS(), pidlist))
                t2 = time()
                _crt_offsetloopslist = self.MakeOneOFFSETLoops(_crt_offset, _pre_loopslist)
                # print 'MakeOneOFFSETLoops :OK', offset, time() - t2

                if not _crt_offsetloopslist: continue
                for _looppids in _crt_offsetloopslist:
                    # print Point.GetAreaOfLoopByPIDList(_looppids)
                    if IfComplexFill and not Point.IfLoopClockwise(
                            PIDList=_looppids) and ComplexFillArea_alert_lowValue < Point.GetAreaOfLoopByPIDList(
                            _looppids) < ComplexFillArea_alert_highValue:
                        # 若小于规定面积，则单独存储loop
                        _rotateinfo = self.IfLoopScanable(_looppids, ComplexFillWidth_alert_lowValue,
                                                          ComplexFillWidth_alert_highValue)
                        # print _rotateinfo
                        if _rotateinfo and _rotateinfo[1][0] < ComplexFillWidth_alert_low_Length and _rotateinfo[1][
                            1] < ComplexFillWidth_alert_high_Length:
                            self.S_shapedLoopList.append(_looppids)
                            continue

                    if offset in self.OffsetPointDicts:
                        self.OffsetPointDicts[offset].append(_looppids)
                    else:
                        self.OffsetPointDicts[offset] = [_looppids]

                # 若仍存在loop，则继续向下偏移
                if offset in self.OffsetPointDicts:
                    _pre_offset = offset
                    _pre_loopslist = self.OffsetPointDicts[offset]
                else:
                    _pre_loopslist = []

        # print 'GetOffsetsPointDicts:OK'

        _ori_PIDList = map(lambda plists: [p.getID() for p in plists], self.LoopPointsListDict.values())
        # print _ori_PIDList
        # print 'GetOffsetsPointDicts START!'
        GetOffsetsPointDicts(offsetlist_positive, _ori_PIDList)
        GetOffsetsPointDicts(offsetlist_negative, _ori_PIDList)
        # print 'GetOffsetsPointDicts END!'
        # print 'MakeOFFSETListLoops:OK',time()-t1
        # for i in self.S_shapedLoopList:
        # 	ReadIGESFiles.IGESFile.drawPointIntoIGESFile(
        # 		r"G:\test\pidlist_in_%s-%s.igs" % (['Backforward','Forward'][Point.IfLoopClockwise(PIDList=i)],str(i)[:20]),
        # 		map(lambda pid: Point.PointDict[pid].getPOS(), i))
        # print 'MakeOFFSETListLoops END!'
        pass

    def MakeOneOFFSETLoops_NoSolveCrossLoop(self, offset, loopslist):
        _currentOFFSETLoops = []
        # t1 = time()
        if loopslist == [[1,2,3,4,5,6,7,8]]:
            pass
        for looppoints in loopslist:
            ost = Offset(pidlist=looppoints)
            poslist = ost.getNEWPlistByOffset(offset)
            # print poslist
            if poslist:
                try:
                    pidlist = ost.solveCrossLine(map(lambda pos: Point.getPoint(pos), poslist))
                    # pidlist = [map(lambda pos: Point.getPoint(pos).getID(), poslist)]
                    # pidlist = ost.solveCrossLine(map(lambda pos: Point.getDifferentPoint(pos), poslist))
                    _currentOFFSETLoops.extend(pidlist)
                except:
                    for _plist in poslist:
                        pidlist = ost.solveCrossLine(map(lambda pos: Point.getPoint(pos), _plist))
                        _currentOFFSETLoops.extend(pidlist)
        # print 'MakeOneOFFSETLoops:OK',time()-t1
        # print _currentOFFSETLoops,'111'
        # print Offset.solveCrossLoop(_currentOFFSETLoops) ,'222'
        return _currentOFFSETLoops

    def MakeEachOFFSETLoops(self, offsetIn, offsetOut):
        '''根据offsetlist，基于上一个offset结果得到当前offset结果，节约资源
		offsetlist = [-8,-6,-10,-3,5,-1,4,6,3,8]
		'''
        t1 = time()
        # offsetlist_positive = sorted(filter(lambda a:[None,a][a>0],offsetlist))
        # offsetlist_negative = sorted(filter(lambda a:[None,a][a<0],offsetlist),reverse=True)

        _ori_PIDList = map(lambda plists: [p.getID() for p in plists], self.LoopPointsListDict.values())
        newloops_in = []
        newloops_out = []
        for PIDList in _ori_PIDList:
            # print PIDList
            if Point.IfLoopClockwise(PIDList=PIDList):

                # 内轮廓需暂时转换为逆时针点序，伪装成外轮廓
                PIDList.reverse()
                newloops_in.extend(self.MakeOneOFFSETLoops_NoSolveCrossLoop(-1 * offsetIn, [PIDList]))
            # print True

            else:
                if offsetOut != None:
                    newloops_out.extend(self.MakeOneOFFSETLoops_NoSolveCrossLoop(offsetOut, [PIDList]))
                # print False
        # self.OffsetPointDicts['out_%1f_in_%1f'%(offsetOut,offsetIn)]=Offset.solveCrossLoop(newloops)
        tem_solved_Loop_in = Offset.solveCrossLoop(newloops_in)
        # print tem_solved_Loop_in

        if offsetOut != None:
            for loop in tem_solved_Loop_in:
                loop.reverse()
            tem_solved_Loop_out = Offset.solveCrossLoop(newloops_out)
            tem_solved_Loop_in.extend(tem_solved_Loop_out)
        # self.OffsetPointDicts['out_%s_in_%s'%(offsetOut,offsetIn)] = Offset.solveCrossLoop(tem_solved_Loop_in)
        self.OffsetPointDicts['out_in'] = Offset.solveCrossLoop(tem_solved_Loop_in)
        pass

    def MakeColorByPreLoop(self, preloop_P, BiasVector=[0.0, 0.0, -1.0]):
        BiasVector_L = sum(map((lambda i: i ** 2), BiasVector)) ** 0.5
        BiasVector = [BiasVector[0] / BiasVector_L, BiasVector[1] / BiasVector_L, BiasVector[2] / BiasVector_L]
        print(BiasVector)
        crtpreloop_P = self.LoopPointsListDict.values()

        def checkPositionToPreLoop(P1, P2):
            for one_pre_loop in preloop_P:
                _cross = Point.IfLoopCrossByPIDList(map(lambda P: P.getID(), one_pre_loop), [P1.getID(), P2.getID()])
                if _cross != []:
                    return ['cross', _cross]
            ifctn = 0
            for one_pre_loop in preloop_P:
                if Point.IfLoopContainPointByPID(map(lambda P: P.getID(), one_pre_loop), P1.getID()):
                    ifctn += 1
            if ifctn % 2 == 0:
                return ["out"]
            else:
                return ["in"]

        def breakLine(Line, step=0.2):
            P1 = Line.P1
            P2 = Line.P2

            _length = Line.getLength()
            _P_num = (int)(_length / step)
            delta = map(lambda a, b: 1.0 * (b - a) / _P_num, P1.getPOS(), P2.getPOS())
            _PList = [Point(map(lambda a, b: a + b, P1.getPOS(), map(lambda a, i: a * i, delta, [i] * 3))) for i in
					  range(_P_num)]
            _PList.append(P2)
            return _PList

        def getColorbyDistance(P):
            if P.getID() == 2162:
                pass
            distance = min(map(lambda loop: P.getDistenceToLoop(loop), preloop_P))
            distance = min(distance, 2.0)
            K = (int)(distance / 0.2)
            if 255 - K * 25 == 80:
                pass
            return [255, 255 - K * 25, 255 - K * 25]

        t1 = time()
        newLineList = []
        for one_crt_loop in crtpreloop_P:
            _plist = one_crt_loop[:]
            _plist.insert(0, _plist.pop())
            _tupleP = zip(_plist, one_crt_loop)
            for P1, P2 in _tupleP:
                _revise_P1 = Point(map(lambda a, b: a + b, P1.getPOS(), BiasVector))
                _revise_P2 = Point(map(lambda a, b: a + b, P2.getPOS(), BiasVector))

                _position = checkPositionToPreLoop(_revise_P1, _revise_P2)
                _L = geometryLine(P1, P2)
                if _position[0] == "in":
                    newLineList.append(_L)
                elif _position[0] == "out":
                    _PList = breakLine(_L)
                    _colorList = map(getColorbyDistance, _PList)
                    print(_colorList)
                    pass
                elif _position[0] == "cross":

                    pass

        print(time() - t1)
        pass

    def MakeColorByPreLoop_offset(self, preIGES, BiasVector=[0.0, 0.0, -1.0], offsetlist=[0.2 * i for i in range(5)]):
        t1 = time()
        classifyedLine = {}
        originLine = [geometryLine(l.P1, l.P2) for l in self.LinesList]

        # 判断关系
        def checkPositionToPreLoop(P1, P2, boundaryPlist, boundaryP_TupleLists=[]):

            if boundaryP_TupleLists == []:
                # _temp_P1list = [P1] * len(boundaryPlist[0])
                # _temp_P2list = [P2] * len(boundaryPlist[0])
                for one_pre_loop in boundaryPlist:
                    plist1 = one_pre_loop[:]
                    plist2 = plist1[:]
                    plist2.insert(0, plist2.pop())
                    ifcross = map(Point.IfCrossByPoint, [P1] * len(one_pre_loop), [P2] * len(one_pre_loop), plist1,
                                  plist2)
                    if any(ifcross):
                        return 'cross'
            else:
                # _temp_P1list = [P1] * len(boundaryPlist[0])
                # _temp_P2list = [P2] * len(boundaryPlist[0])
                for one_pre_loop in boundaryP_TupleLists:
                    ifcross = map(Point.IfCrossByPoint, [P1] * len(one_pre_loop[0]), [P2] * len(one_pre_loop[0]),
                                  one_pre_loop[0],
                                  one_pre_loop[1])
                    if any(ifcross):
                        return 'cross'
            ifctn = 0
            for one_pre_loop in boundaryPlist:
                if Point.IfLoopContainPointByPID(map(lambda P: P.getID(), one_pre_loop), P1.getID()) == 'In':
                    ifctn += 1
            if ifctn % 2 == 0:
                return "out"
            else:
                return "in"

        def classify_linelist(geo_linelist, boundaryPlists, crtDistance, boundaryP_TupleLists=[]):
            if crtDistance not in classifyedLine:
                classifyedLine[crtDistance] = []
            for line in geo_linelist:
                # _revise_P1 = Point(map(lambda a, b: a + b, line.P1.getPOS(), BiasVector))
                # _revise_P2 = Point(map(lambda a, b: a + b, line.P2.getPOS(), BiasVector))
                # _position = checkPositionToPreLoop(_revise_P1, _revise_P2, boundaryPlists)

                _position = checkPositionToPreLoop(Point(map(lambda a, b: a + b, line.P1.getPOS(), BiasVector)),
                                                   Point(map(lambda a, b: a + b, line.P2.getPOS(), BiasVector)),
                                                   boundaryPlists, boundaryP_TupleLists=boundaryP_TupleLists)
                if _position == 'in':
                    line.setFlyDistance(crtDistance)
                    classifyedLine[crtDistance].append(line)
            for line in classifyedLine[crtDistance]:
                try:
                    geo_linelist.remove(line)
                except:
                    pass

        def breakLine(geo_line, step=0.2):
            P1 = geo_line.P1
            P2 = geo_line.P2

            _length = P1.getDistence(P2)
            _P_num = (int)(_length / step)
            delta = map(lambda a, b: 1.0 * (b - a) / _P_num, P1.getPOS(), P2.getPOS())
            _PList = [Point(map(lambda a, b: a + b, P1.getPOS(), map(lambda a, i: a * i, delta, [i] * 3))) for i in
                      range(_P_num)]
            _PList.append(P2)
            return _PList

        def remove_ONLINEPoint(geo_line_list):
            P_lists = []
            _p_list = []
            for geo_line in geo_line_list:
                pass
            pass

        classify_linelist(originLine, preIGES.LoopPointsListDict.values(), 0)
        '''将相交线段破碎，并更新至originLine中'''
        originLine_break = []
        for line in originLine:
            newPlist = breakLine(line)
            for i in range(len(newPlist) - 1):
                j = i + 1
                originLine_break.append(geometryLine(newPlist[i], newPlist[j]))
        originLine = originLine_break
        print("break line:%f" % (time() - t1))
        classify_linelist(originLine, preIGES.LoopPointsListDict.values(), 0)
        print("classify_linelist_0:%f" % (time() - t1))
        # self.DrawColorfulIGES(classifyedLine, r'G:\1-program\4-Rotator\color\output_%s.igs' % '1617')
        for _offset_value in offsetlist:
            t2 = time()
            if _offset_value == 0.0: continue
            boundaryPidlist = preIGES.MakeOFFSETLoops(_offset_value)
            boundaryPlist = []
            for one_loop in boundaryPidlist:
                boundaryPlist.append(map(lambda pid: Point.PointDict[pid], one_loop))

            _boundaryP_TupleLists = []
            for one_pre_loop in boundaryPlist:
                plist1 = one_pre_loop[:]
                plist2 = plist1[:]
                plist2.insert(0, plist2.pop())
                _boundaryP_TupleLists.append([plist1, plist2])
            for line in originLine:
                ifctn = 0
                for one_pre_loop in boundaryPidlist:
                    if Point.IfLoopContainPointByPID(one_pre_loop, line.P1.getID()) == 'In':
                        ifctn += 1
                if ifctn % 2 == 1:
                    classify_linelist(originLine, boundaryPlist, _offset_value,
                                      boundaryP_TupleLists=_boundaryP_TupleLists)
            print("classify_linelist_%f:%f" % (_offset_value, (time() - t2)))
        if len(originLine) > 0:
            classifyedLine[_offset_value].extend(originLine)

        # self.DrawColorfulIGES(classifyedLine, r'G:\1-program\4-Rotator\color\output_%s.igs'%str(_offset_value))
        # map(lambda pid:Point.PointDict[pid],)
        '''合并共线同色点originLine'''
        for offset in classifyedLine.keys():
            remove_ONLINEPoint(classifyedLine[offset])
        # map(remove_ONLINEPoint,classifyedLine)
        self.DrawColorfulIGES(classifyedLine, r'G:\1-program\4-Rotator\color\output.igs')
        print(time() - t1)

    def MakeColorByPreLoop_offset_cut(self, preIGESfilename, BiasVector=[0.0, 0.0, -1.0],
                                      offsetlist=[0.2 * i for i in range(6)]):
        t1 = time()
        classifyedLine = {}
        tempfilename = 'temp.igs'
        print(time() - t1)
        # prePointsListDict = preIGES.LoopPointsListDict.values()
        preIGES = IGESFile(preIGESfilename, MinPointArea=0.01, NearPointDistance=0.01)
        cut_looplayerDict = preIGES.MakeLoopOrder(makeorder=False)
        preIGES.MakeLoopClockwise(cut_looplayerDict)
        # 落在上层轮廓内部的线段
        classifyedLine[0] = preIGES.CutLoopsByLooplist_regeoLinelist(self.LoopPointsListDict.values(), 'SmoothLine')
        print(time() - t1)
        # 由上层轮廓逐渐外扩，分类截得的线段
        for i in range(len(offsetlist) - 1):
            preIGES = IGESFile(preIGESfilename, MinPointArea=0.01, NearPointDistance=0.01)
            cut_looplayerDict = preIGES.MakeLoopOrder(makeorder=False)
            preIGES.MakeLoopClockwise(cut_looplayerDict)
            preIGES.MakeInnerlinePointIDList(distance=5.5)
            preIGES.MakeOFFSETListLoops(offsetlist[i:i + 2])
            preIGES.ReSaveIGES(tempfilename, showOffset=True, showOrigin=[False, True][0.0 in offsetlist[i:i + 2]],
                               outlineColor='Default')

            preIGES = IGESFile(tempfilename, MinPointArea=0.01, NearPointDistance=0.01)
            looplayerDict = preIGES.MakeLoopOrder(makeorder=False)
            preIGES.MakeLoopClockwise(looplayerDict)
            preIGES.MakeInnerlinePointIDList(distance=5.5)
            classifyedLine[offsetlist[i + 1]] = preIGES.CutLoopsByLooplist_regeoLinelist(
                self.LoopPointsListDict.values(), 'SmoothLine')
            print(time() - t1)
            pass
        # 在范围以外的区域，按最大外延色着色
        preIGES = IGESFile(preIGESfilename, MinPointArea=0.01, NearPointDistance=0.01)
        cut_looplayerDict = preIGES.MakeLoopOrder(makeorder=False)
        preIGES.MakeLoopClockwise(cut_looplayerDict)
        preIGES.MakeInnerlinePointIDList(distance=5.5)
        preIGES.MakeEachOFFSETLoops(0, offsetlist[-1])
        newPList = [Point.getPoint([10 ** 5, 10 ** 5, 0]), \
                    Point.getPoint([10 ** 5, -1 * 10 ** 5, 0]), \
                    Point.getPoint([-1 * 10 ** 5, -1 * 10 ** 5, 0]), \
                    Point.getPoint([-1 * 10 ** 5, 10 ** 5, 0])]
        preIGES.ReSaveIGES(tempfilename, showOffset=True, showOrigin=False, outlineColor='Default',
                           additionPoints=newPList)

        preIGES = IGESFile(tempfilename, MinPointArea=0.01, NearPointDistance=0.01)
        looplayerDict = preIGES.MakeLoopOrder(makeorder=False)
        preIGES.MakeLoopClockwise(looplayerDict)
        preIGES.MakeInnerlinePointIDList(distance=5.5)
        classifyedLine[offsetlist[-1]].extend(preIGES.CutLoopsByLooplist_regeoLinelist(self.LoopPointsListDict.values(),
                                                                                       'SmoothLine'))
        self.DrawColorfulIGES(classifyedLine, r'G:\1-program\4-Rotator\color\output.igs')
        print(time() - t1)

    def CutLoopsByLooplist_regeoLinelist(self, splitloop_P, mode='ColorLine'):
        '''返回值为geometryLine元素列表'''
        _ori_PIDList = map(lambda plists: [p.getID() for p in plists], splitloop_P)
        _self_PIDList = map(lambda plists: [p.getID() for p in plists], self.LoopPointsListDict.values())
        #
        # _ori_PIDList.extend(splitloop_P)

        '''得到各孤立loop的嵌套关系   PIDlist'''
        # outloops, inloops = Point.GetLoopOutOrIn(_ori_PIDList)
        _tuplePID = []
        for _loop in _ori_PIDList:
            _pIDlist = _loop[:]
            _pIDlist.insert(0, _pIDlist.pop())
            _tuplePID.extend(zip(_loop, _pIDlist))

        '''遍历igs中的线段，判断是否在cutigs之内（考虑内外轮廓的因素，外逆内顺）
        '''
        _containlinelist = []
        _crosslinelist = []  # [_line, [p1id,p2id]]
        for _line in self.LinesList:
            # 'cross','notcontain','contain'
            _relation, _crossinfo = Point.IfLoopsContain_Or_Not_Or_Cross_Line(_ori_PIDList, _tuplePID, _line.P1.getID(),
                                                                              _line.P2.getID())
            if _relation == 'contain':
                _containlinelist.append(_line)
            elif _relation == 'cross':
                _crosslinelist.append([_line, _crossinfo])

        '''遍历cutigs边界，根据_crosslinelist求相交线段
        '''
        cutcrossPIDlist = []  # 记录相交信息cutP1,cutP2，crsP
        _cutcross_TuplePID_list = []  # igs中截下的线段
        _cutnew_TuplePID_list = []  # cutigs中截下的线段
        for _crsinfo in _crosslinelist:
            # [igs.line,[cutigs.P1id,cutigs.P2id]]
            igsP1 = _crsinfo[0].P1.ID
            igsP2 = _crsinfo[0].P2.ID
            for cutigsP in _crsinfo[1]:
                cutigsP1 = cutigsP[0]
                cutigsP2 = cutigsP[1]
                crsPid = Point.GetCrossPointByPID(igsP1, igsP2, cutigsP1, cutigsP2)[0]
                cutcrossPIDlist.append([cutigsP1, cutigsP2, crsPid])

            # 将cutigs内部的一半存入_cutcross_TuplePID_list中
            containnum = 0
            for loop in _ori_PIDList:
                if Point.IfLoopContainPointByPID(loop, igsP1) == 'In':
                    containnum += 1
            _cutcross_TuplePID_list.append([[igsP2, crsPid], [igsP1, crsPid]][containnum % 2 == 1])

        # 将交叉点插入cutLoop中，识别哪些线段存入图形
        for _loop in _ori_PIDList:
            _insertedCrossPLoop = _loop[:]
            cutcrossPIDlist_for_thisloop = [item for item in cutcrossPIDlist if item[0] in _loop]
            INSERT = lambda PIDs: Point.InsertCrossPointIntoPointlistByPID(_insertedCrossPLoop, PIDs[0], PIDs[1],
                                                                           PIDs[2])
            map(INSERT, cutcrossPIDlist_for_thisloop)

            # 识别线段
            # ---组合点组
            _pIDlist = _insertedCrossPLoop[:]
            _pIDlist.insert(0, _pIDlist.pop())
            _thiscutloop_tuplePID = []
            _thiscutloop_tuplePID.extend(zip(_insertedCrossPLoop, _pIDlist))
            # ---判断点组
            for tpPID in _thiscutloop_tuplePID:
                centerPos = map(lambda a, b: (a + b) * 0.5, Point.PointDict[tpPID[0]].getPOS(),
                                Point.PointDict[tpPID[1]].getPOS())

                containnum = 0
                for self_loop in _self_PIDList:
                    if Point.IfLoopContainPointByPID(self_loop, Point.getPoint(centerPos).getID()) == 'In':
                        containnum += 1
                if containnum % 2 == 1:
                    _cutnew_TuplePID_list.append(tpPID)

        re = []
        if mode == 'ClosedLoop':
            for line in _containlinelist:
                re.append(geometryLine(line.P1, line.P2))
            for line in _cutcross_TuplePID_list:
                re.append(geometryLine(Point.PointDict[line[0]], Point.PointDict[line[1]]))
            for line in _cutnew_TuplePID_list:
                re.append(geometryLine(Point.PointDict[line[0]], Point.PointDict[line[1]]))
        elif mode == 'SmoothLine':
            for line in _cutnew_TuplePID_list:
                re.append(geometryLine(Point.PointDict[line[0]], Point.PointDict[line[1]]))
        elif mode == 'ColorLine':
            for line in _containlinelist:
                re.append(geometryLine(line.P1, line.P2))
            for line in _cutcross_TuplePID_list:
                re.append(geometryLine(Point.PointDict[line[0]], Point.PointDict[line[1]]))
        # for line in _cutnew_TuplePID_list:
        # 	re.append(geometryLine(Point.PointDict[line[0]], Point.PointDict[line[1]]))

        return re

    def CutLoopsByLooplist(self, splitloop_P, outputfilename, mode='ClosedLoop'):
        _ori_PIDList = map(lambda plists: [p.getID() for p in plists], splitloop_P)
        _self_PIDList = map(lambda plists: [p.getID() for p in plists], self.LoopPointsListDict.values())
        #
        # _ori_PIDList.extend(splitloop_P)

        '''得到各孤立loop的嵌套关系   PIDlist'''
        # outloops, inloops = Point.GetLoopOutOrIn(_ori_PIDList)
        _tuplePID = []
        for _loop in _ori_PIDList:
            _pIDlist = _loop[:]
            _pIDlist.insert(0, _pIDlist.pop())
            _tuplePID.extend(zip(_loop, _pIDlist))

        '''遍历igs中的线段，判断是否在cutigs之内（考虑内外轮廓的因素，外逆内顺）
		'''
        _containlinelist = []
        _crosslinelist = []  # [_line, [p1id,p2id]]
        for _line in self.LinesList:
            # 'cross','notcontain','contain'
            _relation, _crossinfo = Point.IfLoopsContain_Or_Not_Or_Cross_Line(_ori_PIDList, _tuplePID, _line.P1.getID(),
                                                                              _line.P2.getID())
            if _relation == 'contain':
                _containlinelist.append(_line)
            elif _relation == 'cross':
                _crosslinelist.append([_line, _crossinfo])

        '''遍历cutigs边界，根据_crosslinelist求相交线段
		'''
        cutcrossPIDlist = []  # 记录相交信息cutP1,cutP2，crsP
        _cutcross_TuplePID_list = []  # igs中截下的线段
        _cutnew_TuplePID_list = []  # cutigs中截下的线段
        for _crsinfo in _crosslinelist:
            # [igs.line,[cutigs.P1id,cutigs.P2id]]
            igsP1 = _crsinfo[0].P1.ID
            igsP2 = _crsinfo[0].P2.ID
            for cutigsP in _crsinfo[1]:
                cutigsP1 = cutigsP[0]
                cutigsP2 = cutigsP[1]
                crsPid = Point.GetCrossPointByPID(igsP1, igsP2, cutigsP1, cutigsP2)[0]
                cutcrossPIDlist.append([cutigsP1, cutigsP2, crsPid])

            # 将cutigs内部的一半存入_cutcross_TuplePID_list中
            containnum = 0
            for loop in _ori_PIDList:
                if Point.IfLoopContainPointByPID(loop, igsP1) == 'In':
                    containnum += 1
            _cutcross_TuplePID_list.append([[igsP2, crsPid], [igsP1, crsPid]][containnum % 2 == 1])

        # 将交叉点插入cutLoop中，识别哪些线段存入图形
        for _loop in _ori_PIDList:
            _insertedCrossPLoop = _loop[:]
            cutcrossPIDlist_for_thisloop = [item for item in cutcrossPIDlist if item[0] in _loop]
            INSERT = lambda PIDs: Point.InsertCrossPointIntoPointlistByPID(_insertedCrossPLoop, PIDs[0], PIDs[1],
                                                                           PIDs[2])
            map(INSERT, cutcrossPIDlist_for_thisloop)

            # 识别线段
            # ---组合点组
            _pIDlist = _insertedCrossPLoop[:]
            _pIDlist.insert(0, _pIDlist.pop())
            _thiscutloop_tuplePID = []
            _thiscutloop_tuplePID.extend(zip(_insertedCrossPLoop, _pIDlist))
            # ---判断点组
            for tpPID in _thiscutloop_tuplePID:
                centerPos = map(lambda a, b: (a + b) * 0.5, Point.PointDict[tpPID[0]].getPOS(),
                                Point.PointDict[tpPID[1]].getPOS())

                containnum = 0
                for self_loop in _self_PIDList:
                    if Point.IfLoopContainPointByPID(self_loop, Point.getPoint(centerPos).getID()) == 'In':
                        containnum += 1
                if containnum % 2 == 1:
                    _cutnew_TuplePID_list.append(tpPID)

        _igs = IGESFile(cur_file_dir() + r"\blank.igs")

        if mode == 'ClosedLoop':
            for line in _containlinelist:
                _igs.AddSingleLine(line.P1.getPOS(), line.P2.getPOS())
            for line in _cutcross_TuplePID_list:
                _igs.AddSingleLine(Point.PointDict[line[0]].getPOS(), Point.PointDict[line[1]].getPOS())
            for line in _cutnew_TuplePID_list:
                _igs.AddSingleLine(Point.PointDict[line[0]].getPOS(), Point.PointDict[line[1]].getPOS())
        elif mode == 'SmoothLine':
            for line in _cutnew_TuplePID_list:
                _igs.AddSingleLine(Point.PointDict[line[0]].getPOS(), Point.PointDict[line[1]].getPOS())

        # for looppidlist in newLooplist:
        # 	for i in range(len(looppidlist)):
        # 		j = [i + 1, 0][i == len(looppidlist) - 1]
        # 		p1 = Point.PointDict[looppidlist[i]].getPOS()
        # 		p2 = Point.PointDict[looppidlist[j]].getPOS()
        # 		_igs.AddSingleLine(p1, p2)
        _igs.saveIGES(outputfilename)

        pass

    def CutLoopsByLooplist2(self, splitloop_P, outputfilename):
        '''未生效'''
        _ori_PIDList = map(lambda plists: [p.getID() for p in plists], splitloop_P)
        _self_PIDList = map(lambda plists: [p.getID() for p in plists], self.LoopPointsListDict.values())
        #
        # _ori_PIDList.extend(splitloop_P)

        '''得到各孤立loop的嵌套关系   PIDlist'''
        # outloops, inloops = Point.GetLoopOutOrIn(_ori_PIDList)
        _tuplePID = []
        for _loop in _ori_PIDList:
            _pIDlist = _loop[:]
            _pIDlist.insert(0, _pIDlist.pop())
            _tuplePID.extend(zip(_loop, _pIDlist))

        '''遍历igs中的线段，判断是否在cutigs之内（考虑内外轮廓的因素，外逆内顺）
		'''
        _containlinelist = []
        _crosslinelist = []  # [_line, [p1id,p2id]]
        for _line in self.LinesList:
            # 'cross','notcontain','contain'
            _relation, _crossinfo = Point.IfLoopsContain_Or_Not_Or_Cross_Line(_ori_PIDList, _tuplePID, _line.P1.getID(),
                                                                              _line.P2.getID())
            if _relation == 'contain':
                _containlinelist.append(_line)
            elif _relation == 'cross':
                _crosslinelist.append([_line, _crossinfo])

        '''遍历cutigs边界，根据_crosslinelist求相交线段
		'''
        cutcrossPIDlist = []  # 记录相交信息cutP1,cutP2，crsP
        _cutcross_TuplePID_list = []  # igs中截下的线段
        _cutnew_TuplePID_list = []  # cutigs中截下的线段
        for _crsinfo in _crosslinelist:
            # [igs.line,[cutigs.P1id,cutigs.P2id]]
            igsP1 = _crsinfo[0].P1.ID
            igsP2 = _crsinfo[0].P2.ID
            for cutigsP in _crsinfo[1]:
                cutigsP1 = cutigsP[0]
                cutigsP2 = cutigsP[1]
                crsPid = Point.GetCrossPointByPID(igsP1, igsP2, cutigsP1, cutigsP2)[0]
                cutcrossPIDlist.append([igsP1, igsP2, cutigsP1, cutigsP2, crsPid])

        '''----------------------------------------------------------------'''
        _ori_insertCrossP_PIDList = copy.deepcopy(_ori_PIDList)
        _self_insertCrossP_PIDList = copy.deepcopy(_self_PIDList)
        _crossPIDs = []
        _WithcrossPIDs = []
        for [P1_id, P2_id, Q1_id, Q2_id, cross_id] in cutcrossPIDlist:
            # for  in _cross:
            for self_loop_P in _self_insertCrossP_PIDList:
                if P1_id in self_loop_P:
                    Point.InsertCrossPointIntoPointlistByPID(self_loop_P, P1_id, P2_id, cross_id)
            for cut_loop_P in _ori_insertCrossP_PIDList:
                if Q1_id in cut_loop_P:
                    Point.InsertCrossPointIntoPointlistByPID(cut_loop_P, Q1_id, Q2_id, cross_id)
            _crossPIDs.append(cross_id)

        for self_loop_P in _self_insertCrossP_PIDList:
            _WithcrossPIDs.append(self_loop_P)
        for cut_loop_P in _ori_insertCrossP_PIDList:
            _WithcrossPIDs.append(cut_loop_P)

        _newloops = Point.GetSimpleLoopsByCrossLoops(_WithcrossPIDs, _crossPIDs)
        # for self_loop_P in _self_PIDList:
        #
        # 	for (P1_id, P2_id), (Q1_id, Q2_id), cross_id in cutcrossPIDlist:
        # 		Point.InsertCrossPointIntoPointlistByPID(self_loop_P, P1_id, P2_id, cross_id)
        #
        # for cut_loop_P in _ori_PIDList:
        # 	for (P1_id, P2_id), (Q1_id, Q2_id), cross_id in cutcrossPIDlist:
        # 		Point.InsertCrossPointIntoPointlistByPID(cut_loop_P, Q1_id, Q2_id, cross_id)

        # Point.InsertCrossPointIntoPointlistByPID(_WithcrossPIDs, Q1_id, Q2_id, cross_id)
        # _crossPIDs.append(cross_id)
        pass

    def MakeLoopsConnected(self):
        '''
		本函数为本iges图形联通若干相邻loop成为一个loop
		:return:
		'''

        pass

    def MakeBlocks(self, looplayerDict):
        '''
		本函数为本iges图形切割孤立封闭的block块
		'''
        blk = Block.layer(self.LoopPointsListDict, looplayerDict)
        blk.BreakLoopsIntoOneLoop()
        pass

    def WriteLoopInfomation(self, filename, looplayerDict):
        fp = open(filename, 'w')
        for outloopID in looplayerDict:
            fp.write('<outside\n')
            _text = ''
            for _p in self.LoopPointsListDict[outloopID]:
                _text += '\t%.3f,%.3f,%.3f\n' % tuple(_p.getPOS())
            fp.write(_text)

            inloopIDList = looplayerDict[outloopID]
            for _loopid in inloopIDList:
                fp.write('\t<inside\n')
                _text = ''
                for _p in self.LoopPointsListDict[_loopid]:
                    _text += '\t\t%.3f,%.3f,%.3f\n' % tuple(_p.getPOS())
                fp.write(_text)
                fp.write('\tinside>\n')

            fp.write('outside>\n')
        fp.close()

    def getLoopPointsListDict(self):
        return self.LoopPointsListDict

    def getLoopIDList(self):
        return self.LoopIDdict.keys()

    def getLoopRotate(self):
        '''此函数为获取各loop最佳旋转角度
			应经过iges.MakeLoopOrder()处理之后调用
		'''

        def checkAllLines(looppoints):
            '''
			根据一个loop内的各顶点信息，遍历各直线
			y = k*x 以及 x=0
			Ax+By=0

			返回值为直线与X轴夹角-弧度
			'''

            def checkOneLine(looppoints, A, B):
                '''
				求一个直线的各点到该直线距离最小范围
				'''
                delta = (A ** 2 + B ** 2) ** 0.5
                distance = lambda p: (p.getPOS()[0] * A + p.getPOS()[1] * B) / delta
                Distances = map(distance, looppoints)
                return max(Distances) - min(Distances)

            def checkflydistance(looppoints, theta):
                '''
				给定一角度，求填充时悬空的长度
				20160531
				'''
                # def checkpoint(pos):
                # 	'''已作废'''
                # 	'''
                # 	根据pos ，判断该点附近的两点是否横跨loop轮廓
                # 	'''
                # 	# print '----------------------------pos:',pos
                # 	x0 = pos[0]
                # 	'''获取pos周围两点，且X分量与其他顶点不同'''
                # 	while True:
                # 		d1 = uniform(x0-0.01,x0)
                # 		d2 = uniform(x0,x0+0.01)
                # 		tem = map(lambda x:[0,1][d1 == x[0] or d2 == x[0]],rotated_looppoints)
                # 		if sum(tem) ==0:
                # 			break
                # 	crosspoints_y1 = []
                # 	crosspoints_y2 = []
                # 	for i in range(len(rotated_looppoints)):
                # 		'''根据每条线的两点X坐标，当前点在其中时求交点Y值并列表crosspoints中
                # 		y = y0+(x-x0)*(y1-y0)/(x1-x0)
                # 		'''
                # 		j = [i+1,0][i==(len(rotated_looppoints)-1)]
                # 		x0,y0 = rotated_looppoints[i]
                # 		x1,y1 = rotated_looppoints[j]
                # 		if (d1 - rotated_looppoints[i][0])*(d1 - rotated_looppoints[j][0])<0:							
                # 			d1_y = y0+(d1-x0)*(y1-y0)/(x1-x0)
                # 			crosspoints_y1.append(d1_y)
                # 		if (d2 - rotated_looppoints[i][0])*(d2 - rotated_looppoints[j][0])<0:
                # 			d2_y = y0+(d2-x0)*(y1-y0)/(x1-x0)
                # 			crosspoints_y2.append(d2_y)
                # 	if len(crosspoints_y1)<4 and len(crosspoints_y2)<4 : return True
                # 	if len(crosspoints_y1)%2!=0 or len(crosspoints_y2)%2!=0 :return False
                # 	crosspoints_y1.sort()
                # 	crosspoints_y2.sort()
                # 	'''
                # 	a=[0,1,2,3,4,5]
                # 	2-1,4-3
                # 	len(a) = 6
                # 	i = range(len(a)/2-1) = 0,1
                # 	2*i+2,2*i+1 = (2,1) (4,3) 

                # 	a=[0,1,2,3]
                # 	2-1
                # 	len(a) = 4
                # 	i = range(len(a)/2-1) = 0
                # 	2*i+2,2*i+1 = (2,1) 

                # 	'''
                # 	flydistance = max([crosspoints_y1[2*i+2]-crosspoints_y1[2*i+1] for i in range(len(crosspoints_y1)/2-1)]+[crosspoints_y2[2*i+2]-crosspoints_y2[2*i+1] for i in range(len(crosspoints_y2)/2-1)])
                # 	if flydistance > self.MaxFlyDistance:
                # 		return False
                # 	else:
                # 		return True					
                # 	pass

                POSROTATE = lambda p: [cos(-theta) * p.getPOS()[0] - sin(-theta) * p.getPOS()[1],
                                       cos(-theta) * p.getPOS()[1] + sin(-theta) * p.getPOS()[0]]
                rotated_looppoints = map(POSROTATE, looppoints)

                rotated_pos_deltaX = []
                _preX = rotated_looppoints[-1][0]
                dx = 0.0

                for rot_p in rotated_looppoints:
                    _curX = rot_p[0]

                    if dx * (_curX - _preX) > 0:
                        dx += _curX - _preX
                    elif dx * (_curX - _preX) < 0:
                        rotated_pos_deltaX.append(dx)
                        dx = _curX - _preX
                    elif dx * (_curX - _preX) == 0:
                        if dx == 0.0:
                            dx = _curX - _preX
                    _preX = _curX

                rotated_pos_deltaX.append(dx)

                if rotated_pos_deltaX[-1] * rotated_pos_deltaX[0] > 0:
                    rotated_pos_deltaX[0] += rotated_pos_deltaX.pop()
                # print 'rotated_pos_deltaX', rotated_pos_deltaX
                # print 'theta',theta*180/pi
                delnum = 0
                for dx in rotated_pos_deltaX:
                    if abs(dx) < self.MaxFlyDistance:
                        delnum += 2
                if len(rotated_pos_deltaX) - delnum <= 2:
                    # print 'rotated_pos_deltaX', rotated_pos_deltaX
                    # print theta
                    return True
                else:
                    return False

            def checkRange(m, n, h):
                '''
				在角度m~n中(step=1/h)遍历，求出最小间距
				返回值为(直线斜率,该直线间距)
				'''
                _Distances = {}
                for i in range(m * h, n * h):
                    # print 1.0*i/h
                    k = tan(i * pi / (180 * h))
                    if not checkflydistance(looppoints, i * pi / (180 * h)): continue
                    _Distances[k] = checkOneLine(looppoints, k, -1)

                if checkflydistance(looppoints, pi / 2):
                    _Distances['x=0'] = checkOneLine(looppoints, 1, 0)
                if outline_K:
                    _Distances[outline_K] = outline_Distance
                return sorted(_Distances.items(), key=lambda d: d[1])[0]

            '''
			1.首先根据各边线与X轴夹角，验证是否合适，
			'''
            '''计算各边斜率'''
            k_list = []
            for i in range(len(looppoints)):
                j = [i + 1, 0][i == (len(looppoints) - 1)]
                if looppoints[i].getPOS()[0] == looppoints[j].getPOS()[0]:
                    continue
                x0, y0 = looppoints[i].getPOS()[:-1]
                x1, y1 = looppoints[j].getPOS()[:-1]
                k = (y1 - y0) / (x1 - x0)
                # k = float("%.3f" % float(k))
                k_list.append(k)
            # theta = atan((y1-y0)/(x1-x0))*180/pi
            # print i,j,(y1-y0)/(x1-x0)
            # print x0,y0,x1,y1,theta

            # k_list=list(set(k_list))
            # print k_list
            '''遍历各斜率及垂直斜率'''
            _Distances = {}
            k_list = list(set(k_list))
            for k in k_list:
                # print k,atan(k),atan(k)*180/pi
                # print '0'
                if checkflydistance(looppoints, atan(k)):
                    _Distances[k] = checkOneLine(looppoints, k, -1)
                # print '1'
                if k != 0.0:
                    # print '2'
                    if checkflydistance(looppoints, atan(1 / k)):
                        # print '3'
                        _Distances[1 / k] = checkOneLine(looppoints, 1 / k, -1)
            # print _Distances.items(),looppoints
            # print k_list
            outline_K = None
            outline_Distance = None
            if len(_Distances) > 0:
                outline_K, outline_Distance = sorted(_Distances.items(), key=lambda d: d[1])[0]
            # print 'outline',outline_K,outline_Distance
            '''
			2.再均匀验证夹角
			'''

            '''一级求解'''
            min_k = checkRange(-90, 90, 1)
            # print min_k
            '''二级求解'''
            if min_k[0] == 'x=0':
                min_k = checkRange(89, 90, 20)
            else:
                # print min_k
                theta = int(atan(min_k[0]) * 180 / pi)
                min_k = checkRange(theta - 1, theta + 1, 4)
            # print min_k
            return pi / 2 if min_k[0] == 'x=0' else atan(min_k[0])

        # [atan(min_k[0]),pi/2][min_k[0]=='x=0']
        '''此函数正文'''
        if not self.IfClosed():
            print('%s ERROR: Loop Open(FUN:getLoopRotate)\n' % self.FileName)
            return
        for loopid in self.LoopPointsListDict:
            looppoints = self.LoopPointsListDict[loopid]
            self.LoopRotateDict[loopid] = checkAllLines(looppoints)
        # print looppoints
        pass
    def addLoopRotate_by_givenTheta_or_scanableAngle(self, givenTheta, nextThetaStep = -5.7):
        '''根据给定的Theta，为igs中每个loop增加角度注释，如不能旋转则按nextThetaStep调整'''
        if not self.IfClosed():
            print('%s ERROR: Loop Open(FUN:getLoopRotate)\n' % self.FileName)
            return
        for loopid in self.LoopPointsListDict:
            looppoints = self.LoopPointsListDict[loopid]
            _theta = givenTheta
            counttimes = 0
            while True:
                if checkflydistance(looppoints, _theta, self.MaxFlyDistance):
                    break
                _theta = _theta + nextThetaStep
                # _theta = _theta % 360
                counttimes += 1
                if counttimes > 360:
                    print('%s ERROR: Cannot find Theta(FUN:getLoopRotate)\n' % self.FileName)
                    break
            if counttimes <= 360:
                self.AddAngleLabel(looppoints[0], looppoints[1], _theta)

    def IfLoopScanable(self, pidlist, alert_lowValue, alert_highValue):
        '''
		判断loop是否可弓字填充，成功则返回旋转角度及该旋转角度线平行线切割loop的交点间距小于alert_lowValue的loop分量长度，该直线平行线切割loop的交点间距大于于alert_highValue的loop分量长度，失败则返回False
		'''

        def checkAllLines(looppoints, alert_lowValue, alert_highValue):
            '''
            根据一个loop内的各顶点信息，遍历各直线
            y = k*x 以及 x=0
            Ax+By=0

            返回值为直线与X轴夹角-弧度
            '''

            def checkOneLine(looppoints, A, B):
                '''
                求一个直线的各点到该直线距离最小范围
                '''
                delta = (A ** 2 + B ** 2) ** 0.5
                distance = lambda p: (p.getPOS()[0] * A + p.getPOS()[1] * B) / delta
                Distances = map(distance, looppoints)
                return max(Distances) - min(Distances)

            def checkflydistance(looppoints, theta):
                '''
                给定一角度，求填充时悬空的长度
                20160531
                '''
                POSROTATE = lambda p: [cos(-theta) * p.getPOS()[0] - sin(-theta) * p.getPOS()[1],
                                       cos(-theta) * p.getPOS()[1] + sin(-theta) * p.getPOS()[0]]
                rotated_looppoints = map(POSROTATE, looppoints)

                rotated_pos_deltaX = []
                _preX = rotated_looppoints[-1][0]
                dx = 0.0

                for rot_p in rotated_looppoints:
                    _curX = rot_p[0]

                    if dx * (_curX - _preX) > 0:
                        dx += _curX - _preX
                    elif dx * (_curX - _preX) < 0:
                        rotated_pos_deltaX.append(dx)
                        dx = _curX - _preX
                    elif dx * (_curX - _preX) == 0:
                        if dx == 0.0:
                            dx = _curX - _preX
                    _preX = _curX

                rotated_pos_deltaX.append(dx)

                if rotated_pos_deltaX[-1] * rotated_pos_deltaX[0] > 0:
                    rotated_pos_deltaX[0] += rotated_pos_deltaX.pop()
                # print 'rotated_pos_deltaX', rotated_pos_deltaX
                # print 'theta',theta*180/pi
                delnum = 0
                for dx in rotated_pos_deltaX:
                    if abs(dx) < self.MaxFlyDistance:
                        delnum += 2
                if len(rotated_pos_deltaX) - delnum <= 2:
                    # print 'rotated_pos_deltaX', rotated_pos_deltaX
                    # print theta
                    return True
                else:
                    return False

            def checkRange(m, n, h):
                '''
                在角度m~n中(step=1/h)遍历，求出最小间距
                返回值为(直线斜率,该直线间距)
                '''
                _Distances = {}
                for i in range(m * h, n * h):
                    # print 1.0*i/h
                    k = tan(i * pi / (180 * h))
                    if not checkflydistance(looppoints, i * pi / (180 * h)): continue
                    _Distances[k] = checkOneLine(looppoints, k, -1)

                if checkflydistance(looppoints, pi / 2):
                    _Distances['x=0'] = checkOneLine(looppoints, 1, 0)
                if outline_K:
                    _Distances[outline_K] = outline_Distance
                return sorted(_Distances.items(), key=lambda d: d[1])[0]

            def getCrossDistance(looppoints, theta, alert_lowValue, alert_highValue):
                # 返回值为(该直线平行线切割loop的交点间距小于alert_lowValue的loop分量长度，该直线平行线切割loop的交点间距大于于alert_highValue的loop分量长度)
                POSROTATE = lambda p: [cos(-theta) * p.getPOS()[0] - sin(-theta) * p.getPOS()[1],
                                       cos(-theta) * p.getPOS()[1] + sin(-theta) * p.getPOS()[0]]
                rotated_looppoints = map(POSROTATE, looppoints)
                X_Values = map(lambda p: p[0], rotated_looppoints)
                max_X, min_X = [max(X_Values), min(X_Values)]
                deltaY = [0, 0]  # min,max
                for _10x in range(int(min_X * 10) + 1, int(max_X * 10)):
                    _x = _10x * 0.1
                    _deltay = []
                    for i in range(len(rotated_looppoints)):
                        j = [i + 1, 0][i == (len(rotated_looppoints) - 1)]
                        # 若与此_x相交，则记录交点
                        xi, yi = rotated_looppoints[i]
                        xj, yj = rotated_looppoints[j]
                        if (xi - _x) * (xj - _x) <= 0:
                            if xi == xj:
                                _y = yi
                            else:
                                _y = yi + (1.0 * (yj - yi) / (xj - xi)) * (_x - xi)
                            _deltay.append(_y)
                    _temdeltaY = abs(max(_deltay) - min(_deltay))
                    if _temdeltaY <= alert_lowValue:  deltaY[0] += 0.1
                    if _temdeltaY >= alert_highValue: deltaY[1] += 0.1

                return deltaY

            '''--------------------------------------------------------------------------'''
            '''
            1.首先根据各边线与X轴夹角，验证是否合适，
            '''
            '''计算各边斜率'''
            k_list = []
            for i in range(len(looppoints)):
                j = [i + 1, 0][i == (len(looppoints) - 1)]
                if looppoints[i].getPOS()[0] == looppoints[j].getPOS()[0]:
                    continue
                x0, y0 = looppoints[i].getPOS()[:-1]
                x1, y1 = looppoints[j].getPOS()[:-1]
                k = (y1 - y0) / (x1 - x0)
                k_list.append(k)
            '''遍历各斜率及垂直斜率'''
            _Distances = {}
            k_list = list(set(k_list))
            for k in k_list:
                # print k,atan(k),atan(k)*180/pi
                # print '0'
                if checkflydistance(looppoints, atan(k)):
                    _Distances[k] = checkOneLine(looppoints, k, -1)
                # print '1'
                if k != 0.0:
                    # print '2'
                    if checkflydistance(looppoints, atan(1 / k)):
                        # print '3'
                        _Distances[1 / k] = checkOneLine(looppoints, 1 / k, -1)

            outline_K = None
            outline_Distance = None
            if len(_Distances) > 0:
                outline_K, outline_Distance = sorted(_Distances.items(), key=lambda d: d[1])[0]
            '''
            2.再均匀验证夹角
            '''

            '''一级求解'''
            min_k = checkRange(-90, 90, 1)
            # print min_k
            '''二级求解'''
            if min_k[0] == 'x=0':
                min_k = checkRange(89, 90, 20)
            else:
                # print min_k
                theta = int(atan(min_k[0]) * 180 / pi)
                min_k = checkRange(theta - 1, theta + 1, 4)
            # print min_k

            # return [pi / 2 if min_k[0] == 'x=0' else atan(min_k[0]),min_k[1]]
            _theta = pi / 2 if min_k[0] == 'x=0' else atan(min_k[0])
            return [_theta, getCrossDistance(looppoints, _theta, alert_lowValue, alert_highValue)]

        '''此函数正文'''
        looppoints = [Point.PointDict[pid] for pid in pidlist]
        try:
            return checkAllLines(looppoints, alert_lowValue, alert_highValue)
        except:
            return False

    def getLoopStartPoint(self, defaultLabel=5, defaultLabelList=[5, 6]):
        '''
		此函数为根据各Loop中孤立点坐标，确定该Loop填充时的起始点，此函数在getLoopSequence()之前调用
		self.LoopStartPoint = {}
		self.SinglePointList = []
		'''
        '''将各个孤立点分配给所在的LOOP中，self.LoopStartPoint记录loop中心点'''
        _single_point_dict = {}

        for loopid in self.LoopIDdict:
            # print self.LoopsCenterList[loopid]
            tem_loop_pointpos_list = map(lambda p: p.getPOS()[:-1], self.LoopPointsListDict[loopid])
            self.LoopStartPoint[loopid] = Point(
                [self.LoopsCenterList[loopid][0], self.LoopsCenterList[loopid][1], self.LoopsCenterList[loopid][2]])
            # _single_point_dict[loopid] = self.LoopStartPoint[loopid]
            for point in self.SinglePointList:
                # print tem_loop_pointpos_list,point.getPOS()
                if self.PointIfInLoop2(point.getPOS(), loopid, self.LoopINFODict[loopid]['RangeX'],
                                       self.LoopINFODict[loopid]['RangeY']) \
                        or point.getPOS()[:-1] in tem_loop_pointpos_list:
                    # tem_Point = map(lambda a,b:a*0.9+b*0.1,point.getPOS(),self.LoopStartPoint[loopid].getPOS())

                    # self.MovePointIntoLoop(point,loopid)
                    # self.LoopStartPoint[loopid] = Point(tem_Point[0],tem_Point[1],tem_Point[2])
                    # self.LoopStartPoint[loopid] = point
                    _single_point_dict[loopid] = point
                    break

        # exit()

        '''
		x1=cos(angle)*x-sin(angle)*y
		y1=cos(angle)*y+sin(angle)*x;
		'''
        POSROTATE = lambda x, y, a: [cos(-a) * x - sin(-a) * y, cos(-a) * y + sin(-a) * x]

        '''遍历loop中各定点，得到旋转后的坐标范围
		判断经旋转后的孤立点偏向哪个方向，并记录在self.LoopStartLabel中
		'''
        for loopid in self.LoopIDdict:
            _rangeX = None
            _rangeY = None

            for point in self.LoopPointsListDict[loopid]:
                pos = point.getPOS()[:-1]
                theta = self.LoopRotateDict[loopid]
                if theta < 0: theta = pi + theta
                newpos = POSROTATE(pos[0], pos[1], theta)
                # print 'pos:', pos,newpos,theta
                # print
                if not _rangeX: _rangeX = [newpos[0], newpos[0]]
                if not _rangeY: _rangeY = [newpos[1], newpos[1]]
                # print _rangeX,theta
                _rangeX = [min(_rangeX[0], newpos[0]), max(_rangeX[1], newpos[0])]
                _rangeY = [min(_rangeY[0], newpos[1]), max(_rangeY[1], newpos[1])]
            # print 'loopid',loopid,_rangeX,_rangeY
            if loopid in _single_point_dict and _single_point_dict[loopid] != None:
                # print _single_point_dict[loopid]
                startpos = _single_point_dict[loopid].getPOS()
                newpos = POSROTATE(startpos[0], startpos[1], theta)

                self.LoopStartLabel[loopid] = defaultLabelList[
                    abs(newpos[0] - _rangeX[0]) > abs(newpos[0] - _rangeX[1])]
            else:
                self.LoopStartLabel[loopid] = defaultLabel

            # print loopid,pos,theta
            # print 
            # [  for loopid in self.LoopIDdict for point in self.LoopPointsListDict[loopid] \
            #  ]
            pass
        # print self.SinglePointList
        # print 'self.LoopINFODict',self.LoopINFODict
        # print self.LoopStartPoint
        pass

    def getLoopSequence(self):
        '''此函数为获取各loop最佳排序
			应经过iges.MakeLoopOrder()处理之后调用
		'''
        # LoopSequence.MyLoopSequence = LoopSequence.LoopSequence(self.LoopStartPoint.values())
        # self.LoopSequenceList = LoopSequence.MyLoopSequence.makeDistanceDict()
        LoopSequence.Sequence.refresh()
        self.LoopSequenceList = LoopSequence.LoopSequence(self.LoopStartPoint.values()).makeDistanceDict()
        # print self.LoopSequenceList
        pass

    def getLineNumberOfParam(self, txt):
        # print self.make_saving_string_in_72('P',txt)
        return len(self.make_saving_string_in_72('P', txt))

    def makeLoopContainOrder(self, looporderMode=1, showOrigin=False):
        # 对offset排序 20180421
        all_offset_Loop_pidlist = []
        for i in self.OffsetPointDicts.values():
            all_offset_Loop_pidlist.extend(i)
        if showOrigin:
            all_offset_Loop_pidlist.extend(
                [[p.getID() for p in loopPoints] for loopPoints in self.LoopPointsListDict.values()])

        # loopid:[pointids]
        all_offset_Loop_pidDict = {}
        for i in range(len(all_offset_Loop_pidlist)):
            all_offset_Loop_pidDict[i] = all_offset_Loop_pidlist[i]

        _contain = {id: [] for id in range(len(all_offset_Loop_pidlist))}
        _outloopnum = {id: 0 for id in range(len(all_offset_Loop_pidlist))}

        def addcontain(loopid1, loopid2):
            if Point.IfLoopContainLoopByPIDs_absoluteIN(all_offset_Loop_pidDict[loopid1],
                                                        all_offset_Loop_pidDict[loopid2]):
                _outloopnum[loopid2] += 1
                _contain[loopid1].append(loopid2)

        _loopids = [(i, j) for i in range(len(all_offset_Loop_pidlist)) for j in range(len(all_offset_Loop_pidlist))
                    if i < j]
        for _loopid in _loopids:
            addcontain(_loopid[0], _loopid[1])
            addcontain(_loopid[1], _loopid[0])

        _directcontain = {}
        _not_OutlineLoop = []
        for loopid in _contain:
            def fn(x, y):
                return x + _contain[y]

            if not _contain[loopid]:
                _directcontain[loopid] = []
                continue
            temp = [_contain[_contain[loopid][0]]]
            temp.extend(_contain[loopid][1:])
            _all_subloop_contains = list(set(reduce(fn, temp)))
            _directcontain[loopid] = [id for id in _contain[loopid] if id not in _all_subloop_contains]
            _not_OutlineLoop.extend(_contain[loopid])
            pass
        # for subloopid in _contain[loopid]:
        # _directcontain记录了loop包含的相邻loopid信息
        # 应获取源头，即最外loop
        _not_OutlineLoop = list(set(_not_OutlineLoop))
        _outlineLoop = [i for i in all_offset_Loop_pidDict.keys() if i not in _not_OutlineLoop]
        _Ordered_LoopIdList = []

        def InsertContainedLoop(loopid):
            # 参数为刚刚压入的loopid，操作为将该loop所直接包含的子loopid压入_Ordered_LoopIdList
            if loopid not in _Ordered_LoopIdList:
                _Ordered_LoopIdList.append(loopid)
            for containedloopid in _directcontain[loopid]:
                _Ordered_LoopIdList.insert(_Ordered_LoopIdList.index(loopid) + 1, containedloopid)
                InsertContainedLoop(containedloopid)

        # while True:
        # 	if len(_Ordered_LoopIdList) == len(all_offset_Loop_pidDict): break
        for outloopid in _outlineLoop:
            InsertContainedLoop(outloopid)
        if looporderMode == 1:
            pass
        elif looporderMode == 2:
            _1st_looplist = [_Ordered_LoopIdList[i] for i in range(0, len(_Ordered_LoopIdList), 2)]
            _2nd_looplist = [i for i in _Ordered_LoopIdList if i not in _1st_looplist]
            _Ordered_LoopIdList = _1st_looplist + _2nd_looplist
        elif looporderMode == 3:
            _1st_looplist = [_Ordered_LoopIdList[i] for i in range(0, len(_Ordered_LoopIdList), 2)]
            _2nd_looplist = [i for i in _Ordered_LoopIdList if i not in _1st_looplist]
            _2nd_looplist.reverse()
            _Ordered_LoopIdList = _1st_looplist + _2nd_looplist
        return [all_offset_Loop_pidDict[loopid] for loopid in _Ordered_LoopIdList]

    def AddSequenceLabel(self, p, txt):
        '''
		插入注释文本（第13项为参数区行数，重要）
			212       1       0       1       0       0       0       000000100D      1
			212       0       3       2       0                                D      2
			212,1,3,5.7388319537,3.653712841,14,1.5707963268,0.0,0,0,              1P      1
			2.7617386224,3.5988811261,0.0,3H1-1;                                   1P      2
		'''
        '''212  总注释'''
        new_sub = Substance()
        new_sub.SetMenuData(0, '212')
        new_sub.SetMenuData(2, '0')
        new_sub.SetMenuData(3, '1')
        new_sub.SetMenuData(4, '0')
        new_sub.SetMenuData(5, '0')
        new_sub.SetMenuData(6, '0')
        new_sub.SetMenuData(7, '0')
        new_sub.SetMenuData(8, '00000100')
        new_sub.SetMenuData(10, '212')
        new_sub.SetMenuData(11, '0')
        new_sub.SetMenuData(12, '3')
        new_sub.SetMenuData(13, '2')
        new_sub.SetMenuData(14, '0')

        new_sub.AddParameterData(
            ['212,1'] + ['%d' % len(txt)] + ['%d' % (len(txt) * 3)] + ['5'] + ['14,1.5707963268,0.0,0,0'] + p + [
                self.writeSTR(txt)])
        new_sub.ID = self.MaxID_of_DLine + 1
        self.MaxID_of_DLine += 2
        self.substances[new_sub.ID] = new_sub

        txt = new_sub.ParameterData[:]
        plinenum = self.getLineNumberOfParam(txt)
        new_sub.SetMenuData(13, '%d' % plinenum)

    def AddAngleLabel(self, p1, p2, theta):

        '''
		     106       2       0       4       0       0       0       000000100D      3
		     106       0       2       1      20                                D      4
		     214       3       0       1       0       0       0       000010100D      5
		     214       0       3       1       3                                D      6
		     214       4       0       1       0       0       0       000010100D      7
		     214       0       3       2       3                                D      8
		     212       6       0       1       0       0       0       000010100D      9
		     212       0       3       2       0                                D     10
		     202       8       0       1       0       0       0       000000100D     11
		     202       0       3       1       0                                D     12

		106,1,2,0.0,0.0,0.0,42.1452409581,0.0;                                 3P      2
		214,1,4.,1.,0.0,27.2018125932,0.0,26.2749333057,7.0403471604;          5P      3
		214,1,4.,1.,0.0,23.5574607347,13.6009062966,26.2749333057,             7P      4
		7.0403471604;                                                          7P      5
		212,1,3,7.09653,3.5,1003,1.5707963268,4.9741883682,0,0,                9P      6
		25.960278388,10.6294698656,0.0,3H30~;                                  9P      7
		202,9,0,0,0.0,0.0,27.2018125932,5,7;                                  11P      8

		＜AOB
		假设对任意点(x,y)，绕一个坐标点(rx0,ry0)逆时针旋转a角度后的新的坐标设为(x0, y0)，有公式：
		x0= (x - rx0)*cos(a) - (y - ry0)*sin(a) + rx0 ;
		y0= (x - rx0)*sin(a) + (y - ry0)*cos(a) + ry0 ;


		p1     ---   loop中一点
		p2     ---   loop中一点
		theta  ---   loop旋转角弧度
		'''
        # print theta
        # theta = -1*theta
        theta = pi + theta
        theta = -theta
        # print theta
        if theta <= -pi:
            theta = theta + pi
        if theta >= pi:
            theta = theta - pi
        # print 'theta-pi',theta
        # print theta
        p_A = p1.getPOS()
        p_O = p2.getPOS()
        p_B = [(p_A[0] - p_O[0]) * cos(theta) - (p_A[1] - p_O[1]) * sin(theta) + p_O[0], \
               (p_A[0] - p_O[0]) * sin(theta) + (p_A[1] - p_O[1]) * cos(theta) + p_O[1], p_O[2]]
        note_Point = [(p_A[0] - p_O[0]) * cos(theta * 0.5) - (p_A[1] - p_O[1]) * sin(theta * 0.5) + p_O[0], \
                      (p_A[0] - p_O[0]) * sin(theta * 0.5) + (p_A[1] - p_O[1]) * cos(theta * 0.5) + p_O[1], p_O[2]]
        note_pA = map(lambda o, a: (a - o) * 0.1 + o, p_O, p_A)
        note_pB = map(lambda o, a: (a - o) * 0.1 + o, p_O, p_B)
        note_Point = map(lambda o, a: (a - o) * 0.1 + o, p_O, note_Point)

        pLineID = {}

        '''106  辅助中心线'''
        new_sub = Substance()
        new_sub.SetMenuData(0, '106')
        new_sub.SetMenuData(2, '0')
        new_sub.SetMenuData(3, '1')
        new_sub.SetMenuData(4, '0')
        new_sub.SetMenuData(5, '0')
        new_sub.SetMenuData(6, '0')
        new_sub.SetMenuData(7, '0')
        new_sub.SetMenuData(8, '00000100')
        new_sub.SetMenuData(10, '106')
        new_sub.SetMenuData(11, '0')
        new_sub.SetMenuData(12, '2')
        new_sub.SetMenuData(13, '1')
        new_sub.SetMenuData(14, '20')

        new_sub.AddParameterData(['106,1,2'] + ['%f,%f,%f,%f,%f' % (p_O[2], p_O[0], p_O[1], note_pB[0], note_pB[1])])
        txt = new_sub.ParameterData[:]
        plinenum = self.getLineNumberOfParam(txt)
        new_sub.SetMenuData(13, '%d' % plinenum)

        new_sub.ID = self.MaxID_of_DLine + 1
        self.MaxID_of_DLine += 2
        self.substances[new_sub.ID] = new_sub

        '''214  角度标注箭头'''
        new_sub = Substance()
        new_sub.SetMenuData(0, '214')
        new_sub.SetMenuData(2, '0')
        new_sub.SetMenuData(3, '4')
        new_sub.SetMenuData(4, '0')
        new_sub.SetMenuData(5, '0')
        new_sub.SetMenuData(6, '0')
        new_sub.SetMenuData(7, '0')
        new_sub.SetMenuData(8, '00000100')
        new_sub.SetMenuData(10, '214')
        new_sub.SetMenuData(11, '0')
        new_sub.SetMenuData(12, '3')
        new_sub.SetMenuData(13, '1')
        new_sub.SetMenuData(14, '3')

        new_sub.AddParameterData(
            ['214,1,2.,1.'] + ['%f,%f,%f,%f,%f' % (note_pA[2], note_pA[0], note_pA[1], note_Point[0], note_Point[1])])
        txt = new_sub.ParameterData[:]
        plinenum = self.getLineNumberOfParam(txt)
        new_sub.SetMenuData(13, '%d' % plinenum)

        new_sub.ID = self.MaxID_of_DLine + 1
        self.MaxID_of_DLine += 2
        self.substances[new_sub.ID] = new_sub
        pLineID['214_1'] = new_sub.ID
        # print '2',self.MaxID_of_DLine

        '''214  角度标注箭头'''
        new_sub = Substance()
        new_sub.SetMenuData(0, '214')
        new_sub.SetMenuData(2, '0')
        new_sub.SetMenuData(3, '4')
        new_sub.SetMenuData(4, '0')
        new_sub.SetMenuData(5, '0')
        new_sub.SetMenuData(6, '0')
        new_sub.SetMenuData(7, '0')
        new_sub.SetMenuData(8, '00000100')
        new_sub.SetMenuData(10, '214')
        new_sub.SetMenuData(11, '0')
        new_sub.SetMenuData(12, '3')
        new_sub.SetMenuData(13, '1')
        new_sub.SetMenuData(14, '3')

        new_sub.AddParameterData(
            ['214,1,2.,1.'] + ['%f,%f,%f,%f,%f' % (note_pB[2], note_pB[0], note_pB[1], note_Point[0], note_Point[1])])
        txt = new_sub.ParameterData[:]
        plinenum = self.getLineNumberOfParam(txt)
        new_sub.SetMenuData(13, '%d' % plinenum)

        new_sub.ID = self.MaxID_of_DLine + 1
        self.MaxID_of_DLine += 2
        self.substances[new_sub.ID] = new_sub
        pLineID['214_2'] = new_sub.ID
        # print '3',self.MaxID_of_DLine

        '''212  总注释'''
        new_sub = Substance()
        new_sub.SetMenuData(0, '212')
        new_sub.SetMenuData(2, '0')
        new_sub.SetMenuData(3, '1')
        new_sub.SetMenuData(4, '0')
        new_sub.SetMenuData(5, '0')
        new_sub.SetMenuData(6, '0')
        new_sub.SetMenuData(7, '0')
        new_sub.SetMenuData(8, '00010100')
        new_sub.SetMenuData(10, '212')
        new_sub.SetMenuData(11, '0')
        new_sub.SetMenuData(12, '3')
        new_sub.SetMenuData(13, '2')
        new_sub.SetMenuData(14, '0')

        txt_theta = str(abs(theta * 180.0 / pi)) + '~'
        # self.writeSTR('%f~'%theta*180/pi)

        new_sub.AddParameterData(['212,1'] + ['%d' % len(txt_theta)] + ['%d' % (len(txt_theta) * 3)] + ['5'] + [
            '1003,1.5707963268,0.0,0,0'] + note_Point + [self.writeSTR(txt_theta)])
        txt = new_sub.ParameterData[:]
        plinenum = self.getLineNumberOfParam(txt)
        new_sub.SetMenuData(13, '%d' % plinenum)

        new_sub.ID = self.MaxID_of_DLine + 1
        self.MaxID_of_DLine += 2
        self.substances[new_sub.ID] = new_sub
        pLineID['212'] = new_sub.ID
        # print '4',self.MaxID_of_DLine

        '''202  角度注释'''
        new_sub = Substance()
        new_sub.SetMenuData(0, '202')
        new_sub.SetMenuData(2, '0')
        new_sub.SetMenuData(3, '1')
        new_sub.SetMenuData(4, '0')
        new_sub.SetMenuData(5, '0')
        new_sub.SetMenuData(6, '0')
        new_sub.SetMenuData(7, '0')
        new_sub.SetMenuData(8, '00000100')
        new_sub.SetMenuData(10, '202')
        new_sub.SetMenuData(11, '0')
        new_sub.SetMenuData(12, '3')
        new_sub.SetMenuData(13, '1')
        new_sub.SetMenuData(14, '0')

        new_sub.AddParameterData(['202'] + ['%d' % pLineID['212']] + ['0,0'] + p_O[:2] + [
            '%f' % (((p_O[0] - note_pA[0]) ** 2 + (p_O[1] - note_pA[1]) ** 2) ** 0.5)] + [
                                     '%d,%d' % (pLineID['214_1'], pLineID['214_2'])])
        txt = new_sub.ParameterData[:]
        plinenum = self.getLineNumberOfParam(txt)
        new_sub.SetMenuData(13, '%d' % plinenum)
        # new_sub.AddParameterData(['202']+['%d'%pLineID['212']]+['0,0']+p_O[:2]+['%f'%(((p_O[0]-note_pA[0])**2+(p_O[1]-note_pA[1])**2)**0.5)]+['0,0'])
        new_sub.ID = self.MaxID_of_DLine + 1
        self.MaxID_of_DLine += 2
        self.substances[new_sub.ID] = new_sub

    def ReSaveIGES(self, savefile, addOutlinepath=None, showOrigin=True, showOffset=False, showAngle=True,
                   showSequence=True, defaultLabel=5, moveStartPoint=0, looporderMode=1, outlineColor='BLUE',
                   additionPoints=None):
        '''
		经过iges.MakeLineLoop()、iges.MakeLoopOrder()之后，根据LoopPointsListDict，将去除多余点的图形另存为IGES文件
		looporderMode: 0-默认顺序  1-顺序自外而内  2-间隔自外而内 回填  3-间隔自外而内 不回填
		'''

        def saveOrigin_Outline():
            for loopid in self.LoopPointsListDict:
                loop = self.LoopPointsListDict[loopid]
                lengthDic = {}  # 获得最大间距的相邻两点
                for i in range(len(loop)):
                    _move_i = (moveStartPoint + i + len(loop) / 3) % len(loop)
                    j = [_move_i + 1, 0][_move_i == len(loop) - 1]
                    p1 = loop[_move_i]
                    p2 = loop[j]
                    _igs.AddSingleLine(p1.getPOS(), p2.getPOS())
                    lengthDic[(_move_i, j)] = p1.getDistence(p2)
                if showAngle:
                    i, j = sorted(lengthDic.items(), key=lambda d: d[1])[-1][0]
                    if len(self.LoopRotateDict) > 0:
                        _igs.AddAngleLabel(loop[i], loop[j], self.LoopRotateDict[loopid])

        def ImportOrigin_Outline(igs, targetigs, col):
            targetigs.OffsetPointDicts[0] = []
            for loopid in igs.LoopPointsListDict:
                # loop = igs.LoopPointsListDict[loopid]
                # lengthDic = {}  # 获得最大间距的相邻两点
                targetigs.OffsetPointDicts[0].append([P.getID() for P in igs.LoopPointsListDict[loopid]])
            # for i in range(len(loop)):
            # 	_move_i = (moveStartPoint + i + len(loop) / 3) % len(loop)
            # 	j = [_move_i + 1, 0][_move_i == len(loop) - 1]
            # 	p1 = loop[_move_i]
            # 	p2 = loop[j]
            # 	_igs.AddSingleLine(p1.getPOS(), p2.getPOS(), col = col)
            # 	lengthDic[(_move_i, j)] = p1.getDistence(p2)

        _igs = IGESFile(cur_file_dir() + r"\blank.igs")
        OriginLoopPointID = []
        if additionPoints != None:
            for i in range(len(additionPoints)):
                j = [i + 1, 0][i == len(additionPoints) - 1]
                _igs.AddSingleLine(additionPoints[i].getPOS(), additionPoints[j].getPOS())
        if addOutlinepath != None:
            _igs_outline = IGESFile(addOutlinepath)
            looplayerDict = _igs_outline.MakeLoopOrder()
            _igs_outline.MakeLoopClockwise(looplayerDict)
            ImportOrigin_Outline(_igs_outline, self, 'BLUE')
            [OriginLoopPointID.extend(i) for i in
             [[p.getID() for p in loopPoints] for loopPoints in _igs_outline.LoopPointsListDict.values()]]
        elif addOutlinepath == None:
            [OriginLoopPointID.extend(i) for i in
             [[p.getID() for p in loopPoints] for loopPoints in self.LoopPointsListDict.values()]]

        if showOffset:
            if looporderMode in [1, 2, 3]:
                LoopPointList = self.makeLoopContainOrder(looporderMode, showOrigin=showOrigin)

                for loopindex, looppoints in enumerate(LoopPointList):
                    _simpleloop = looppoints
                    # 识别出Originloop，仅对OriginLoop进行颜色区分
                    ifOutLoop = [False, True][_simpleloop[0] in OriginLoopPointID]
                    if moveStartPoint != 0:
                        _moveStartPoint = (3*loopindex + moveStartPoint) % (len(looppoints)) + len(looppoints) / 3
                        _simpleloop = looppoints[_moveStartPoint:] + looppoints[:_moveStartPoint]
                    for i in range(len(looppoints)):
                        j = [i + 1, 0][i == len(_simpleloop) - 1]
                        p1 = Point.PointDict[_simpleloop[i]].getPOS()
                        p2 = Point.PointDict[_simpleloop[j]].getPOS()
                        if ifOutLoop:
                            try:

                                ifOutline = [True, False][
                                    [_simpleloop[i], _simpleloop[j]] in self.inlinePointID or [_simpleloop[j],
                                                                                               _simpleloop[
                                                                                                   i]] in self.inlinePointID]
                            except:
                                pass
                            _col = ['DEFAULT', outlineColor][ifOutline]
                        else:
                            _col = 'DEFAULT'
                        _igs.AddSingleLine(p1, p2, col=_col)

                pass
            elif looporderMode == 0:
                for item in sorted(self.OffsetPointDicts.iteritems(), key=lambda dic: dic[0], reverse=False):
                    # print 'ReSaveIGES offset',item[0]
                    loops = item[1]
                    for loopindex, simpleloop in enumerate(loops):
                        if simpleloop == []: continue
                        _simpleloop = simpleloop[:]
                        if moveStartPoint != 0:
                            _moveStartPoint = (3*loopindex + moveStartPoint) % (len(_simpleloop)) + len(_simpleloop) / 3
                            _simpleloop = simpleloop[_moveStartPoint:] + simpleloop[:_moveStartPoint]
                            pass
                        for i in range(len(_simpleloop)):
                            j = [i + 1, 0][i == len(_simpleloop) - 1]
                            p1 = Point.PointDict[_simpleloop[i]].getPOS()
                            p2 = Point.PointDict[_simpleloop[j]].getPOS()
                            _igs.AddSingleLine(p1, p2)
                saveOrigin_Outline()

        elif showOrigin:
            saveOrigin_Outline()
            '''
			本注释无用，仅供参考：
			对i,j点重新排序，确保loop上 j->i 为顺时针,j点为AddAngleLabel()中的旋转中心
			设A(x1,y1),B(x2,y2),C(x3,y3),则三角形两边的矢量分别是：
				AB=(x2-x1,y2-y1), AC=(x3-x1,y3-y1)
			则AB和AC的叉积为：(2*2的行列式)
				|x2-x1, y2-y1|
				|x3-x1, y3-y1|
			值为：(x2-x1)*(y3-y1) - (y2-y1)*(x3-x1)
			利用右手法则进行判断：
			如果AB*AC>0,则三角形ABC是逆时针的
			如果AB*AC<0,则三角形ABC是顺时针的
			如果AB*AC=0，则说明三点共线，
			'''

        if showSequence:
            for i in range(len(self.LoopSequenceList)):
                # print self.LoopSequenceList[i]
                label = defaultLabel
                for j in self.LoopStartPoint:
                    if self.LoopSequenceList[i] == self.LoopStartPoint[j].getPOS():
                        label = self.LoopStartLabel[j]
                _igs.AddSequenceLabel(self.LoopSequenceList[i], '%d-%d' % ((i + 1), label))

        _igs.saveIGES(savefile)

    def DrawSshapeIGES(self, Sshape_outputpath):
        # if not self.S_shapedLoopList:return
        _igs = IGESFile(cur_file_dir() + r"\blank.igs")
        for looppidlist in self.S_shapedLoopList:
            for i in range(len(looppidlist)):
                j = [i + 1, 0][i == len(looppidlist) - 1]
                p1 = Point.PointDict[looppidlist[i]].getPOS()
                p2 = Point.PointDict[looppidlist[j]].getPOS()
                _igs.AddSingleLine(p1, p2)
        _igs.saveIGES(Sshape_outputpath)
        pass

    def DrawColorfulIGES(self, classifyedLine, outputpath):
        _igs = IGESFile(cur_file_dir() + r"\blank.igs")
        color_id = 1
        for offset in sorted(classifyedLine.keys()):
            # print offset
            for _geoLine in classifyedLine[offset]:
                p1 = _geoLine.P1.getPOS()
                p2 = _geoLine.P2.getPOS()
                # print _geoLine.Color
                if offset == 0:
                    _igs.AddSingleLine(p1, p2, col="DEFAULT")
                else:
                    _igs.AddSingleLine(p1, p2, col=IGESFile.Color_Dic[str(color_id)])
            # print color_id
            color_id = min(color_id + 1, 7)
        _igs.saveIGES(outputpath)
        pass

    @staticmethod
    def drawPointIntoIGESFile(savefile, posList):
        if not posList: return
        _igs = IGESFile(cur_file_dir() + r"\blank.igs")
        if type(posList[0][0]) == float:
            for i in range(len(posList)):
                j = [i + 1, 0][i == len(posList) - 1]
                p1 = posList[i]
                p2 = posList[j]
                _igs.AddSingleLine(p1, p2)
        elif type(posList[0][0]) == list:
            for loop in posList:
                for i in range(len(loop)):
                    j = [i + 1, 0][i == len(loop) - 1]
                    p1 = loop[i]
                    p2 = loop[j]
                    _igs.AddSingleLine(p1, p2)
        _igs.saveIGES(savefile)
    @staticmethod
    def drawEmptyIGESFile(savefile):
        _igs = IGESFile(cur_file_dir() + r"\blank.igs")
        _igs.saveIGES(savefile)
# def WriteANSYSLog(self,filename,looplayerDict):
# 	fp = open(filename,'w')
# 	for outloopID in looplayerDict:
# 		fp.write('<outside\n') 
# 		_text=''
# 		for _p in self.LoopPointsListDict[outloopID]:
# 			_text += '\t%.3f,%.3f,%.3f\n'%tuple(_p.getPOS())
# 		fp.write(_text)

# 		inloopIDList = looplayerDict[outloopID]
# 		for _loopid in inloopIDList:
# 			fp.write('\t<inside\n')
# 			_text=''
# 			for _p in self.LoopPointsListDict[_loopid]:
# 				_text += '\t\t%.3f,%.3f,%.3f\n'%tuple(_p.getPOS())
# 			fp.write(_text)
# 			fp.write('\tinside>\n')

# 		fp.write('outside>\n') 
# 	fp.close()

# for h in t2:
# 	fp.write('%.2f,%.2f,%.2f\n'%tuple(h)) 
# fp.close()


if __name__ == '__main__':
    t = time()
    # iges = IGESFile(r"G:\1-program\4-Rotator\0004.igs",MinPointArea=0.01,NearPointDistance=0.01)
    # '''
    # # -1----------批量转化细小线段
    # # '''
    # for i in range(206,206):
    # 	_filename = r"C:\Users\ChenBo\Desktop\CWZB3\block1\igs\%04d.igs"%i
    # 	iges = IGESFile(_filename, MinPointArea=0.01,NearPointDistance=0.01)
    # 	iges.MakeLoopOrder()
    # 	iges.ReSaveIGES(r"C:\U bmsers\ChenBo\Desktop\CWZB3\block1\igs\LCigs\%04d.igs"%i)

    # '''
    # 0--------
    # '''
    #
    # for i in range(139):
    # 	_path = r'F:\temp\block1\%04d.igs'%i
    # 	iges = IGESFile(_path, MinPointArea=0.01, NearPointDistance=0.01)
    # 	iges.MakeLoopOrder()
    # 	iges.getLoopRotate()
    # 	iges.getLoopStartPoint(defaultLabelList = [5,6])
    # 	iges.getLoopSequence()
    # 	iges.ReSaveIGES(r"F:\temp\block1\LCigs\%04d.igs" % i)
    # iges.getLoopStartPoint(defaultLabelList = [6,5])
    # iges.getLoopSequence()
    # iges.ReSaveIGES(r"F:\temp\block2\%04d.igs" % i)
    # #
    # #
    # # iges = IGESFile(r"G:\1-program\6-GCodeGenerator_note\block1\0000.igs", MinPointArea=0.01, NearPointDistance=0.01)
    # # # iges = IGESFile(r"G:\1-program\4-Rotator\HDK04-0001.igs", MinPointArea=0.01, NearPointDistance=0.01)
    # # # iges = IGESFile(r"F:\2 - 技术文件\临时数控程序(LCX)\MPM - LCX - 2016 - 000 后端框第3分体件\1 - Face + _step1\block1\0000.igs", MinPointArea=0.01, NearPointDistance=0.01)
    # #
    # # '''
    # # 1---------
    # # 给指定iges文件优化细小线段、闭合loop、添加注释、添加旋转
    # # '''
    # # '''iges.SmoothLoop()'''
    # #
    # # # t0 = time()
    # # iges.MakeLoopOrder()
    # # # t1 = time()
    # # # print 'MakeLoopOrder',t1-t0
    # # iges.getLoopRotate()
    # # # t2 = time()
    # # # print 'getLoopRotate',t2-t1
    # # iges.getLoopStartPoint()
    # # # t3 = time()
    # # # print 'getLoopStartPoint',t3-t2
    # # iges.getLoopSequence()
    # # # t4 = time()
    # # # print 'getLoopSequence',t4-t3
    # # # iges.ReSaveIGES(r"G:\1-program\4-Rotator\ReSaveIGES2.igs")
    # # iges.ReSaveIGES(r"G:\1-program\6-GCodeGenerator_note\block1\0000-2.igs")
    # # # t5 = time()
    # # # print 'ReSaveIGES',t5-t4
    # # #
    # # '''---------1'''
    # #
    # #

    # '''
    # 2---------
    # 给指定iges文件优化细小线段、闭合loop、根据构建的loop嵌套关系调整loop定点顺逆序、loop外扩指定宽度
    # '''
    # '''2.1 start 指定偏移'''
    # for i in range(0,220):
    # 	_filename = r"F:\temp\JJC3\%04d.igs"%i
    # 	_filename = r"F:\temp\WGZJT\%04d.igs" % i
    #
    # 	# _filename = r"%04d.igs"%i
    # 	print _filename
    # 	Offset.refresh()
    # 	# Point.refresh()
    # 	# from geometry import RadialLine
    #    #
    # 	# RadialLine.refresh()
    # 	iges = IGESFile(_filename, MinPointArea=0.01,NearPointDistance=0.01)
    # 	# print len(iges.LinesList)
    # 	# print len(iges.LinesDic)
    # 	# iges.MakeLoopOrder()
    # 	looplayerDict = iges.MakeLoopOrder()
    # 	iges.MakeLoopClockwise(looplayerDict)
    # 	# iges.MakeOFFSETListLoops(range(-8,-2,-2))
    #    # iges.MakeOFFSETListLoops([-26, -32, -34, -36, -38, -40, -42, -44, -46, -48, -50, -52, -54, -56, -58, -60])
    #    # iges.MakeOFFSETListLoops([-1.1,-2.1,-3.1,-4.1,-5.1,-6.1,])
    # 	# iges.MakeOFFSETLoops(2)
    # 	# offsetlist = [0]+list(range(-4,-90,-4))
    #
    # 	# 填充
    # 	offsetlist = list(range(-4.5,-40,-4.5))
    # 	# iges.MakeOFFSETListLoops(offsetlist)
    # 	# iges.MakeOFFSETListLoops([-2.25,-6.75,-11.25,-15.75])
    # 	# iges.MakeOFFSETListLoops([-4.5, -9.0, -13.5, -18.0])
    #
    # 	# iges.MakeOFFSETListLoops([-7, -11, -15, -19, -23, -27])
    # 	# iges.MakeOFFSETListLoops(list(range(-0, -90, -4)))
    # 	# iges.MakeOFFSETListLoops(list(range(-4,-10,-4)))
    # 	# iges.MakeOFFSETListLoops([-5, -9, -13, -17, -21, -25, -29, -33, -37, -41, -45, -49, -53, -57])
    # 	# iges.MakeEachOFFSETLoops(-8,4.5)
    #
    #
    #
    #
    # 	iges.ReSaveIGES(r"F:\temp\JJC3\new\%04d.igs"%i,showOffset=True,showOrigin=False)
    # 	# iges.ReSaveIGES(r"F:\temp\WGZJT\new\%04d.igs" % i, showOffset=True, showOrigin=False,moveStartPoint=i*3)
    #
    #
    # 	#
    #    #
    # 	# iges.OffsetPointDicts = {}
    # 	# iges.MakeEachOFFSETLoops(-3.999,None)
    # 	# iges.ReSaveIGES(r"F:\temp\JJC3\new\onlyinloop\%04d.igs"%i,showOffset=True,showOrigin=False)
    #
    #
    # '''2.1 end'''

    # looplayerDict =iges.MakeLoopOrder()
    # iges.MakeLoopClockwise(looplayerDict)
    # t0 = time()
    # # iges.MakeOFFSETListLoops(range(10,26))
    # # iges.MakeOFFSETListLoops([5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100, -5, -10, -15, -20, -25, -30, -35,-40, -45, -50])
    # # iges.MakeOFFSETListLoops([-7.5])
    # # iges.MakeOFFSETListLoops(range(-2, -10, -2))
    # # iges.MakeOFFSETListLoops(range(10,50,2))
    # iges.MakeOFFSETListLoops([3])
    #
    # # iges.MakeOFFSETListLoops([5])
    # # iges.MakeOFFSETLoops(-7)
    # t1 = time()
    # print 'iges.MakeOFFSETListLoops',t1-t0
    # print 'iges.ALL', t1 - t

    # map(lambda offset: iges.MakeOFFSETLoops(offset), range(1, 16, 1))
    # iges.MakeOFFSETLoops(2.7968581081)
    # map(lambda offset: iges.MakeOFFSETLoops(offset), range(1, 6, 2))
    # iges.MakeOFFSETLoops(8)
    # iges.MakeOFFSETLoops(6)
    # iges.MakeOFFSETLoops(-1)
    # map(lambda offset: iges.MakeOFFSETLoops(offset) ,range(-80,0,10))
    # map(lambda offset: iges.MakeOFFSETLoops(offset), range(0, 2, 1))
    # iges.ReSaveIGES(r"G:\1-program\4-Rotator\ReSaveIGES.igs",showOffset=True,showOrigin=False)
    '''---------2'''
# #
# #
# # '''
# # 3---------
# # 给指定iges文件优化细小线段、闭合loop、分块
# # '''
# # # looplayerDict =iges.MakeLoopOrder()
# # # iges.MakeLoopClockwise(looplayerDict)
# # # # print iges.LoopPointsListDict
# # # # print looplayerDict
# # # iges.MakeBlocks(looplayerDict)
# #
# #
# # # iges.ReSaveIGES(r"F:\chenbo\1-program\4-Rotator\ReSaveIGES.igs",showOffset=True)
# # '''---------3'''


# print iges.LoopIDdict

# print "clock1:%s" % clock()
# iges = IGESFile(r"F:\chenbo\1-program\1-ReWriteAreaInfo\0001.igs")
# print "clock2:%s" % clock()
# looplayerDict = iges.MakeLoopOrder()
# iges.WriteLoopInfomation(r"F:\chenbo\1-program\1-ReWriteAreaInfo\0001.txt",looplayerDict)

# print "clock3:%s" % clock()

''' 2016-02-14 '''
# print iges.LinesDic
# for i in iges.LinesDic:
# 	print i,iges.LinesDic[i].type
# print l.id


# iges.breakLineAtPoint(9,[15,0,0])


# iges.saveIGES(r"E:\temp\_ABC.igs")
# iges.AddLineList([[1,2,0],[7,5,0],[7,2,0],[8,3,0]],'Red',)
# print iges.LinesList[0].substance.MenuIndex
# iges.AddSingleLine([0,0,0],[1,1,0],'red')


# iges.saveIGES(r"E:\temp\_ABC.igs")


# # iges.AddLabel(iges.LabelList[0].substance,pos=[1,1,1])
# # iges.setAuthorName('Chen')
# # iges.setAuthorInstitution('BUAA')

# # iges.SolveDisconnected_LINES()
# iges.MakeLineLoop()
# for i in iges.LoopsList:
# 	print iges.PointIfInLoop([-97.30477642282304, -84.2631204093565, 0.0],i)

# # print iges.LabelList[0].getText()
# # iges.saveIGES(r"E:\temp\_ABC.igs")
# # print self.substances[51].ParameterData
# # print __name__