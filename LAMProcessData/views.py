# coding=utf-8
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse

from django.db.models import Q
from django.db.models import F
from django.db import connection
from django.shortcuts import render, render_to_response

from django.contrib import messages
# from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Group
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings
from django_lock import lock
from django.template import loader, RequestContext
from django.template import Context, Template
# from django.template.defaulttags import register
from django.views.decorators.cache import cache_page
from django.core.cache import cache
import numpy as np
import cv2
from LAMProcessData.models import *
from LAMProcessData.forms import *
# from models import *
# from forms import *
# from LAMProcessData.permission import check_permission

from django.views.generic import View
import os
import shutil
import datetime
import time
import re
# from lamdataserver.settings import logger
import logging
from logging.handlers import TimedRotatingFileHandler
from lamdataserver.settings import ImageSectionInfo_dict, MEDIA_LOGFLE_URL
# from ImageRecognition.ImageRecognition import cleanup, MakeStandardizedLineImage
import tempfile
import pytesseract
import LAMProcessData.realtime_records as RealtimeRecord
import LAMProcessData.process_realtime_finedata as RT_FineData
from apscheduler.scheduler import Scheduler
import json
# import LAMProcessData.checkmd5
# import sys
# import lamdataserver.settings.DEBUG as DEBUG
# import LAMProcessData.realtime_records

# sys.path.append("..")
# import ImageRecognition.ImageRecognition as IMR

# logger = logging.getLogger(__name__)





'''cache MAP'''
'''     datatype: 'oxygen', 'laser'， 'cncstatus'        '''
'''     'DATA_WS%s_D%d_TP%s' % (worksection.id, dateint, datatype)   ->   数据列表，以逗号分隔       '''
# 为获取当前的index状态
'''     getkey='index_WS%s_DATE%d_TP%s'%(worksection.id, dateint, datatype)'''
	# 更新index时，根据setkey找到数据库对应条目，写入
'''     setkey='setkey_%s'%getkey                ->  index id             '''
'''     getkey_start = '%s_start'%getkey         ->  startid              '''
'''     getkey_finish = '%s_finish'%getkey       ->  finishid             '''
'''     'Record_LastTime_WS%s_TP%s'%(worksection.id， datatype)      ->  记录最新数据采集的时间   '''

''''''

def CacheOperator(operateType, ifget, ParamSet,data=None):
	'''
	:param operateType:
		'recordLastTime'
		'CleanUpTime'
		'ProgressBarValue_CompleteInspect_MissionId'    由process_realtime_finedata中的CacheOperator进行赋值
	:param ifget:
	:param ParamSet:    (worksectionid,datatype)
		datatype:laser, oxygen, cncstatus
	:param data:
	:return:
	'''
	revalue = None

	if operateType == 'recordLastTime':
		# 最新数据采集时间戳
		worksectionid = ParamSet[0]
		datatype = ParamSet[1]
		key = 'Record_LastTime_WS%s_TP%s'%(worksectionid, datatype)
		if not ifget:
			# set cache
			cache.set(key,data)
		else:
			# get cache
			revalue = RealtimeRecord.Realtime_Records.getlastrecord_time(worksectionid, datatype)
			# revalue = cache.get(key)

	elif operateType == 'CleanUpTime':
		# 上次清理缓存时间戳
		key = "TempfileCleanupTime"
		if not ifget:
			# set cache
			cache.set(key,data)
		else:
			# get cache
			revalue = cache.get(key)
	elif operateType == 'ProgressBarValue_CompleteInspect_MissionId':
		missionid = ParamSet
		key = 'PBR_Insp_MsID%s' % (missionid)
		if not ifget:
			cache.set(key, data)
		else:
			revalue = cache.get(key)

	return revalue

# 差值感知算法 adarray数组
def dHash_ndarray(array):
	hash_str = ''
	shape = array.shape
	newarray = array.reshape(1, shape[0] * shape[1])[0]
	for i in newarray:
		# print(hash_str + '1' if i > 125 else hash_str + '0', hash_str + ['0', '1'][i>125])
		hash_str = hash_str + '1' if i > 125 else hash_str + '0'
		# hash_str = hash_str + ['0', '1'][i>125]
	return hash_str

def changeColorBlackBackWhiteFront(image):
	# 统一颜色 黑底白字
	height, width = image.shape[:2]
	max = image.max()
	if np.mean(image) > 127.5:
		for y in range(0, height):
			for x in range(0, width):
				image[y, x] = max - image[y, x]

def MakeStandardizedLineImage(image,re_img, Type='common'):
	'''常用图像操作'''
	kernel = np.ones((2, 2), np.uint8)
	# 加边框 黑底白字
	MakeBorder = lambda img: cv2.copyMakeBorder(img, 5, 5, 5, 5, cv2.BORDER_CONSTANT, value=0)
	# 膨胀
	Dilate = lambda img: cv2.dilate(img, kernel, iterations=1)
	# Dilate2 = lambda img: cv2.dilate(img, kernel, iterations=2)
	# Dilate3 = lambda img: cv2.dilate(img, kernel, iterations=3)
	# Dilate4 = lambda img: cv2.dilate(img, kernel, iterations=4)
	# 腐蚀
	Erode = lambda img: cv2.erode(img, kernel, iterations=1)
	# 二值化
	# Threshold = lambda img: cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
	# 锐化
	kernel_Filter = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], np.float32)
	# Filter2D = lambda img: cv2.filter2D(img, -1, kernel=kernel_Filter)
	# 高斯平滑
	GaussianBlur = lambda img: cv2.GaussianBlur(img, (9, 9), 2)

	try:
		'''截去多余区域'''
		# image = changeColorBlackBackWhiteFront(image)
		changeColorBlackBackWhiteFront(image)
		height, width = image.shape[:2]
		# cv2.imshow("image0", image)
		# 投影在Y轴，得到h列表，最终得到字符真实高度
		h = [(i, sum(image[i])) for i in range(0, height)]
		mappedOnY = [item[0] for item in h if item[1] > 0]
		minh, maxh = min(mappedOnY), max(mappedOnY) + 1
		real_height = maxh - minh

		# 投影在X轴，得到w列表，最终得到字符真实宽度
		w = [(i, sum(image[0:height, i])) for i in range(0, width)]
		mappedOnX = [item[0] for item in w if item[1] > 0]
		minw, maxw = min(mappedOnX), max(mappedOnX) + 1
		real_width = maxw - minw

		re_img = MakeBorder(image[minh:maxh, minw: maxw])
	except ValueError:
		real_height, real_width = image.shape[:2]
		re_img = MakeBorder(image)
	del image
	del w
	del h
	del mappedOnX
	del mappedOnY
	del minh
	del maxh
	del height
	del width
	# gc.collect()
	if 'resize' in Type:
		_height, _width = re_img.shape[:2]
		re_img = cv2.resize(re_img, (_width * 6, _height * 6), interpolation=cv2.INTER_CUBIC)
		re_img = Erode(re_img)
	if 'blod' in Type:
		re_img = Dilate(re_img)
	if 'blur' in Type:
		re_img = GaussianBlur(re_img)
	# if 'common' in Type:
	#     re_img = MakeBorder(re_img)

	del MakeBorder
	del Dilate
	del Erode
	del GaussianBlur

	'''Page segmentation modes:                                         '''
	'''0    Orientation and script detection (OSD) only.                '''
	'''1    Automatic page segmentation with OSD.                       '''
	'''2    Automatic page segmentation, but no OSD, or OCR.            '''
	'''3    Fully automatic page segmentation, but no OSD. (Default)    '''
	'''4    Assume a single column of text of variable sizes.           '''
	'''5    Assume a single uniform block of vertically aligned text.   '''
	'''6    Assume a single uniform block of text.                      '''
	'''7    Treat the image as a single text line.                      '''
	'''8    Treat the image as a single word.                           '''
	'''9    Treat the image as a single word in a circle.               '''
	'''10    Treat the image as a single character.                     '''
	'''11    Sparse text. Find as much text as possible in no particular order.                               '''
	'''12    Sparse text with OSD.                                                                            '''
	'''13    Raw line. Treat the image as a single text line, bypassing hacks that are Tesseract-specific.    '''
	return (6, 7)[real_width > real_height], re_img

# 清理缓存目录
def cleanup():
	filelist = os.listdir(tempfile.gettempdir())
	# 3min
	Del_time = time.time()-3*60
	for filename in filelist:
		filepath = tempfile.gettempdir()+'\\'+filename
		try:
			if filename.startswith('tess') and Del_time >= os.path.getatime(filepath) :
				# delete
				os.remove(filepath)
		except:
			pass
	for root, dirs, files in os.walk(tempfile.gettempdir()):
		try:
			for dir in dirs:
				_path = root + '\\' + dir
				if dir.startswith('tmp') and Del_time >= os.path.getatime(_path):
					shutil.rmtree(_path, True)
		except:
			pass


'''
常规时间转换为时间戳
test1 = '2019-8-01 00:00:00'
'''
def time_data1(time_sj):  # 传入单个时间比如'2019-8-01 00:00:00'，类型为str
	if type(time_sj)==str:
		data_sj = time.strptime(time_sj, "%Y-%m-%d %H:%M:%S")  # 定义格式
		time_int = int(time.mktime(data_sj))
	elif type(time_sj)==datetime.datetime:
		time_int = int(time.mktime(time_sj.timetuple()))
	elif type(time_sj)==time.struct_time:
		time_int = int(time.mktime(time_sj))
		# time_int = time.strftime("%Y-%m-%d %H:%M:%S", data_sj)  # 时间戳转换正常时间
	# data_sj = time.strptime(time_sj, "%Y-%m-%d %H:%M:%S")  # 定义格式
	# time_int = int(time.mktime(data_sj))
	return time_int  # 返回传入时间的时间戳，类型为int

'''
时间戳转换年月日时间格式
test2 = 1564588800
'''
def time_data2(time_sj):  # 传入参数
	data_sj = time.localtime(time_sj)
	time_str = time.strftime("%Y-%m-%d %H:%M:%S", data_sj)  # 时间戳转换正常时间
	return time_str  # 返回日期，格式为str

# @cache_page(60 * 15)
@login_required
def Index(request):
	return render(request, 'Index.html', {'Common_URL': Common_URL})

# def WriteLog(level, msg):
# 	# print('.' + settings.MEDIA_LOGFLE_URL + time.strftime('%Y/%m/%d.log', time.localtime()))
# 	logging.basicConfig(level=logging.DEBUG,
# 	                    filename='.'+settings.MEDIA_LOGFLE_URL+time.strftime('%Y-%m-%d.log', time.localtime()),
# 	                    # filename='outlog.log',
# 	                    filemode='a',
# 	                    datefmt='%Y-%m-%d %a %H:%M:%S',
# 	                    format='%(asctime)s %(filename)s %(funcName)s %(lineno)d - %(levelname)s - %(message)s')
# 	logger = logging.getLogger(__name__)
#
# 	# logger.FileHandler('.'+settings.MEDIA_LOGFLE_URL+time.strftime('%Y/%m/', time.localtime()))
# 	if level == 'info':
# 		logger.info(msg)
# 	if level == 'debug':
# 		logger.debug(msg)
# 	if level == 'warning':
# 		logger.warning(msg)
# 	if level == 'error':
# 		logger.error(msg)
# 	if level == 'critical':
# 		logger.critical(msg)
#
# 	# with open('.\LAMDATAServer.log', 'a') as logfilehandle:
# 	# 	logfilehandle.write(time.strftime('%Y-%m-%d %H:%M:%S\t', time.localtime())+text+'\n')

# def Check_Is_authenticated(request):
# 	if request.user.is_authenticated():
# 		pass
# 	else:
#
# 		return render(request, 'login.html', {'errormsg': '操作超时，请重新登录！'})

'''============================================================================'''
# 添加页面
Common_URL = {
	'ProcessPath': '/LAMProcessData/',
}
Common_URL['Logout'] = Common_URL['ProcessPath'] + 'logout/'
Common_URL['Login'] = Common_URL['ProcessPath'] + 'login/'
Common_URL['UserProfile'] = Common_URL['ProcessPath'] + 'userProfile/'
Common_URL['ResetPassword'] = Common_URL['ProcessPath'] + 'resetPassword/'
Common_URL['403'] = Common_URL['ProcessPath'] + '403/'

# 基本信息
Common_URL['EditBasicInfomation'] = Common_URL['ProcessPath'] + 'EditBasicInfomation/'
# 生产记录
Common_URL['ProcessRecords'] = Common_URL['ProcessPath'] + 'ProcessRecords/'
# 检验记录
Common_URL['InspectionRecords'] = Common_URL['ProcessPath'] + 'InspectionRecords/'

# 基本信息--分支
Common_URL['Back_URL_workshop'] = Common_URL['EditBasicInfomation'] + 'Workshop/'
Common_URL['Back_URL_worksection'] = Common_URL['EditBasicInfomation'] + 'Worksection/'
Common_URL['Back_URL_computer'] = Common_URL['EditBasicInfomation'] + 'Computer/'
Common_URL['Back_URL_cncstatuscategory'] = Common_URL['EditBasicInfomation'] + 'CNCStatusCategory/'

Common_URL['Back_URL_productcategory'] = Common_URL['EditBasicInfomation'] + 'ProductCategory/'
Common_URL['Back_URL_lammaterial'] = Common_URL['EditBasicInfomation'] + 'LAMMaterial/'
Common_URL['Back_URL_rawstockcategory'] = Common_URL['EditBasicInfomation'] + 'RawStockCategory/'
Common_URL['Back_URL_lamproductionworktype'] = Common_URL['EditBasicInfomation'] + 'LAMProductionWorkType/'
Common_URL['Back_URL_lamtechniqueinstruction'] = Common_URL['EditBasicInfomation'] + 'LAMTechniqueInstruction/'
Common_URL['Back_URL_lamprocessparameters'] = Common_URL['EditBasicInfomation'] + 'LAMProcessParameters/'

Common_URL['Back_URL_lamtechinstserial'] = Common_URL['EditBasicInfomation'] + 'LAMTechInstSerial/'
# Common_URL['Back_URL_lamprodcate_techinst'] = Common_URL['EditBasicInfomation'] + 'LAMProdCate_TechInst/'
Common_URL['Back_URL_samplingposition'] = Common_URL['EditBasicInfomation'] + 'SamplingPosition/'
Common_URL['Back_URL_samplingdirection'] = Common_URL['EditBasicInfomation'] + 'SamplingDirection/'
Common_URL['Back_URL_heattreatmentstate'] = Common_URL['EditBasicInfomation'] + 'HeatTreatmentState/'

# 子窗
Common_URL['SubWindow_URL_LAMProcessParameters_Add'] = Common_URL['Back_URL_lamprocessparameters'] + 'AddLAMParameter/'
Common_URL['SubWindow_URL_LAMProcessParameters_Edit'] = Common_URL['Back_URL_lamprocessparameters'] + 'EditLAMParameter/'
Common_URL['SubWindow_URL_LAMProcessParametersConditionalCell_Add'] = Common_URL['Back_URL_lamprocessparameters'] + 'AddConditionalCell/'
Common_URL['SubWindow_URL_LAMProcessParametersConditionalCell_Edit'] = Common_URL['Back_URL_lamprocessparameters'] + 'EditConditionalCell/'
Common_URL['SubWindow_URL_LAMProcessParametersTechInstSerial_Edit'] = Common_URL['Back_URL_lamprocessparameters'] + 'EditTechInstSerial/'

# 提交数据
Common_URL['Update_URL_LAMProcessParametersTechInstSerial_Save'] = Common_URL['Back_URL_lamprocessparameters'] + 'SaveTechInstSerial/'




# 过程记录--分支
Common_URL['Back_URL_lamproduct'] = Common_URL['ProcessRecords'] + 'LAMProduct/'
Common_URL['Back_URL_rawstock'] = Common_URL['ProcessRecords'] + 'RawStock/'
Common_URL['Back_URL_rawstockflow'] = Common_URL['ProcessRecords'] + 'RawStockFlow/'
Common_URL['Back_URL_lamprocessmission'] = Common_URL['ProcessRecords'] + 'LAMProcessMission/'


# 检验记录--分支
Common_URL['Back_URL_InspectionRecords_ProductPhyChemTest'] = Common_URL[
	                                                              'InspectionRecords'] + 'PhysicochemicalTest/Product/'
Common_URL['Back_URL_InspectionRecords_RawStockPhyChemTest'] = Common_URL[
	                                                               'InspectionRecords'] + 'PhysicochemicalTest/RawStock/'

Common_URL['SubWindow_URL_InspectionRecords_TensileTest_Add'] = Common_URL[
	                                                                'InspectionRecords'] + 'PhysicochemicalTest/AddTensile/'
Common_URL['SubWindow_URL_InspectionRecords_TensileTest_Edit'] = Common_URL[
	                                                                 'InspectionRecords'] + 'PhysicochemicalTest/EditTensile/'
Common_URL['SubWindow_URL_InspectionRecords_ToughnessTest_Add'] = Common_URL[
	                                                                  'InspectionRecords'] + 'PhysicochemicalTest/AddToughness/'
Common_URL['SubWindow_URL_InspectionRecords_ToughnessTest_Edit'] = Common_URL[
	                                                                   'InspectionRecords'] + 'PhysicochemicalTest/EditToughness/'
Common_URL['SubWindow_URL_InspectionRecords_ChemicalElement_Add'] = Common_URL[
	                                                                    'InspectionRecords'] + 'PhysicochemicalTest/AddChemicalElement/'
Common_URL['SubWindow_URL_InspectionRecords_ChemicalElement_Edit'] = Common_URL[
	                                                                     'InspectionRecords'] + 'PhysicochemicalTest/EditChemicalElement/'

# 过程记录过检
# 激光成形过程
Common_URL['Back_URL_InspectionRecords_ProcessMissionInspection_LAMProcess'] = Common_URL[
	                                                              'InspectionRecords'] + 'ProcessMissionInspection/LAMProcess/'
Common_URL['SubWindow_URL_InspectionRecords_ProcessMissionInspection_LAMProcess'] = Common_URL[
				'Back_URL_InspectionRecords_ProcessMissionInspection_LAMProcess'] + 'ByMissionID/'



# 激光成形现场操作

# Common_URL['Back_URL_'] = Common_URL[
# 	                                                              'InspectionRecords'] + 'PhysicochemicalTest/Product/'

ECharts_Color = {
	'oxygen_markLine_color': "#8A0808",
	'laser_markLine_color': "#0B2161",
}


'''在目录中增加工段URL'''
_allWorksection_list = Worksection.objects.filter(available=True).order_by('code')
Common_URL['Back_URL_WorkSection_List'] = []
# Common_URL['Back_URL_WorkSection_List'] = [_allWorksection_list.count()]

for _wc in _allWorksection_list:
	Common_URL['Back_URL_WorkSection_List'].append([Common_URL['ProcessRecords'] + 'WorksectionOperate_by_id/%d/'%(_wc.id), _wc.code, _wc.name])
	RealtimeRecord.Realtime_Records.addWorksection(str(_wc.id))

	# Common_URL['Back_URL_Worksection_Operate'] = Common_URL['ProcessRecords'] + 'WorksectionOperate_by_id/%d/'%(_wc.id)
	# Common_URL['Back_URL_WorkSection_List'][_wc.code] = [Common_URL['ProcessRecords'] + _wc.code+'/', _wc.code, _wc.name]
del _allWorksection_list


# 查询
Common_URL['Query_LAMTechInst_Preview'] = Common_URL['ProcessPath'] + 'QueryData/PreviewTable/LAMTechniqueInstruction/'
Common_URL['Query_LAMProductMission_Preview'] = Common_URL['ProcessPath'] + 'QueryData/PreviewTable/LAMProductMission/'

# Common_URL['Query_LAMTechInst_By_ProductCategory'] = Common_URL['ProcessPath'] + 'QueryData/LAMTechniqueInstruction_By_ProductCategory/'

Common_URL['Query_LAMTechniqueInstruction_By_ProductCode'] = Common_URL['ProcessPath'] + 'QueryData/LAMTechniqueInstruction_By_ProductCode/'
Common_URL['Query_WorkType_By_LAMTechInst'] = Common_URL['ProcessPath'] + 'QueryData/WorkType_By_LAMTechInst/'
Common_URL['Query_Product_By_ProductCategory'] = Common_URL['ProcessPath'] + 'QueryData/Product_By_ProductCategory/'
Common_URL['Query_ProductID_By_ProductCode'] = Common_URL['ProcessPath'] + 'QueryData/ProductID_By_ProductCode/'
Common_URL['Query_WorksectionId_By_MissionID'] = Common_URL['ProcessPath'] + 'QueryData/WorksectionId_By_MissionID/'
Common_URL['Query_StartFinishTime_By_MissionID'] = Common_URL['ProcessPath'] + 'QueryData/StartFinishTime_By_MissionID/'
Common_URL['Query_ArrangementDate_By_MissionID'] = Common_URL['ProcessPath'] + 'QueryData/ArrangementDate_By_MissionID/'
Common_URL['Query_Oxydata_By_WorkSectionDatetime'] = Common_URL['ProcessPath'] + 'QueryData/Oxydata_By_WorkSectionDatetime/'
Common_URL['Query_Oxydata_By_MissionDatetime'] = Common_URL['ProcessPath'] + 'QueryData/Oxydata_By_MissionDatetime/'
Common_URL['Query_Data_By_WorkSectionDatetime'] = Common_URL['ProcessPath'] + 'QueryData/Data_By_WorkSectionDatetime/'
Common_URL['Query_Mission_By_ProductCode'] = Common_URL['ProcessPath'] + 'QueryData/Mission_By_ProductCode/'
Common_URL['Query_RecordLastTime_By_WorksectionID'] = Common_URL['ProcessPath'] + 'QueryData/RecordLastTime_by_WorksectionID/'
Common_URL['Query_RealTimeRecord_By_WorksectionID'] = Common_URL['ProcessPath'] + 'QueryData/RealTimeRecord_by_WorksectionID/'
Common_URL['Query_ConditionalCell_By_ProcessParameterID'] = Common_URL['ProcessPath'] + 'QueryData/LAMProcessParameterConditionalCell_By_ProcessParameterID/'
Common_URL['Query_ProcessParameterTechInstSerial_By_ProcessParameterID'] = Common_URL['ProcessPath'] + 'QueryData/LAMProcessParameter_TechInstSerial_By_ProcessParameterID/'
Common_URL['Query_ProcessParameterTechInstSerial'] = Common_URL['ProcessPath'] + 'QueryData/LAMProcessParameter_TechInstSerial/'
Common_URL['Query_ProcessFineData_By_MissionID'] = Common_URL['ProcessPath'] + 'QueryData/FineData_By_MissionID/'

Common_URL['Query_ProgressBarValue'] = Common_URL['ProcessPath'] +'QueryData/ProgressBarValue/'
Common_URL['Query_ProgressBarValue_InspectionLAMRecords_By_MissionID'] = Common_URL['Query_ProgressBarValue'] + 'InspectionLAMRecords_By_MissionID/'
Common_URL['Query_InspectLAMProcessRecords_By_MissionID'] = Common_URL['ProcessPath'] + 'QueryData/InspectLAMProcessRecords/Complete/'


Common_URL['LamProcessMission_TimeCutRecords'] = Common_URL['Back_URL_lamprocessmission'] + 'CutRecordsByTime/'

GLOBAL_Worksection_Dict = {}


# LogText = ''


def loginview(request):
	if request.method == "POST":
		username = request.POST.get('username')
		password = request.POST.get('password')

		# print(username)
		# print(password)
		user = auth.authenticate(username=username, password=password)
		if user is not None and user.is_active:
			auth.login(request, user)
			return redirect(Common_URL['ProcessPath'])
		# A backend authenticated the credentials
		else:
			return render(request, 'login.html', {'errormsg': '用户名或密码错误！'})
	# No backend authenticated the credentials
	logout(request)
	return render(request, 'login.html')


def logoutview(request):
	logout(request)
	return redirect(Common_URL['Login'])


# 更新index信息 type: 'laser', 'oxygen', 'cncstatus'
def updateProcessDataIndexingInfo(worksection, dateint, datatype, data_id):
	# 为获取当前的index状态
	getkey='index_WS%s_DATE%s_TP%s'%(worksection.id, dateint, datatype)
	# 更新index时，根据setkey找到数据库对应条目，写入
	setkey='setkey_%s'%getkey
	getkey_start = '%s_start'%getkey
	getkey_finish = '%s_finish'%getkey
	result_startid = cache.get(getkey_start)
	result_finishid = cache.get(getkey_finish)
	result_setkeyid = cache.get(setkey)

	if datatype == 'laser':
		indexing_model = Process_Laserdata_Date_Worksection_indexing
	elif datatype == 'oxygen':
		indexing_model = Process_Oxygendata_Date_Worksection_indexing
	elif datatype == 'cncstatus':
		indexing_model = Process_CNCStatusdata_Date_Worksection_indexing

	if not result_setkeyid or not result_startid or not result_finishid:
		# 有任意一项不在缓冲池中，则重新加载
		qset = (Q(work_section=worksection) & Q(index_date_int=dateint))
		indexing_re = indexing_model.objects.filter(qset)
		if indexing_re.count() == 0:
			# 不存在则新建
			date_str = str(dateint)
			_date = '%s-%s-%s' % (date_str[:4], date_str[4:6], date_str[6:])
			_index = indexing_model(
				work_section=worksection,
				index_date=_date,
				index_date_int=dateint,
				data_start_id=data_id,
				data_finish_id=data_id
			)
			_index.save()
			cache.set(getkey_start, data_id)
			cache.set(getkey_finish, data_id)
			cache.set(setkey, _index.id)
		else:
			# 已存在，则从数据库中读取
			cache.set(getkey_start, indexing_re[0].data_start_id)
			cache.set(getkey_finish, indexing_re[0].data_finish_id)
			cache.set(setkey, indexing_re[0].id)
			pass

	else:
		# 缓冲池中有数据，则直接读取
		if data_id < result_startid:
			cache.set(getkey_start, data_id)
			_index = indexing_model.objects.get(id=result_setkeyid)
			_index.data_start_id = data_id
			_index.save()
		if data_id > result_finishid:
			cache.set(getkey_finish, data_id)
			_index = indexing_model.objects.get(id=result_setkeyid)
			_index.data_finish_id=data_id
			_index.save()



def getWorksectionByCNCMacAddress(mac_address):
	global GLOBAL_Worksection_Dict
	if mac_address not in GLOBAL_Worksection_Dict:
		computer = Computer.objects.get(mac_address=mac_address)
		worksection = Worksection.objects.get(cnc_computer=computer)
		GLOBAL_Worksection_Dict[mac_address] = worksection
	return GLOBAL_Worksection_Dict[mac_address]

def getWorksectionByDesktopMacAddress(mac_address):
	global GLOBAL_Worksection_Dict
	if mac_address not in GLOBAL_Worksection_Dict:
		computer = Computer.objects.get(mac_address=mac_address)
		worksection = Worksection.objects.get(desktop_computer=computer)
		GLOBAL_Worksection_Dict[mac_address] = worksection
	return GLOBAL_Worksection_Dict[mac_address]

@login_required
def userprofile(request):
	current_user_set = request.user
	current_group_set = Group.objects.get(user=current_user_set)
	current_group_permissions = current_user_set.get_group_permissions()
	current_group_permissions_list = list(current_group_permissions)
	current_group_permissions_list.sort()
	# print(current_group_set)
	# print(current_user_set.get_group_permissions())
	return render(request, 'UserProfile.html', {'Common_URL': Common_URL,
	                                            'Group_Set_Name': current_group_set,
	                                            'Group_Permissions': current_group_permissions_list})


@login_required
def resetpassword(request):
	renderDict = {'Common_URL': Common_URL}
	if request.method == "POST":
		old_password = request.POST.get('oldpswd')
		new_password = request.POST.get('pswd')
		if request.user.check_password(old_password):
			# 	true
			request.user.set_password(new_password)
			request.user.save()
			renderDict['save_success'] = True
			renderDict['success_messages'] = '密码更改成功！'
		else:
			# 	false
			renderDict['save_success'] = False
			renderDict['error_messages'] = '密码错误，请重新输入！'

	return render(request, 'UserResetPassword.html', renderDict)


def errorview_403(request):
	return render(request, '403.html', {'Login_URL': Common_URL['Login'], 'Index_URL': Common_URL['ProcessPath']})


# def getUser(request):
# 	current_user_set = request.user
# 	current_group_set = Group.objects.get(user=current_user_set)


# 新建页面
@login_required
def BasicInformation_New(request, ModelForm, modelname, TableType='common', isvalidType='default', customfunction=None):
	# Check_Is_authenticated(request)
	# inst表示实例
	# 如果不是POST方法访问
	save_success = None
	if request.method != 'POST':
		# 创建一个空表单在页面显示
		_form_inst = ModelForm()
	else:
		# 否则为POST方式
		# request.POST方法，将会获取到表单中我们输入的数据
		_form_inst = ModelForm(request.POST)
		# 验证其合法性，使用is_valid()方法
		_isValid = True
		if isvalidType == 'default':
			_isValid = _form_inst.is_valid()
		elif isvalidType == 'custom':
			_isValid = _form_inst.is_valid_custom()
		if _isValid:
			# 验证通过，使用save()方法保存数据
			_form_inst.save()
			# 若有自定义函数，则执行
			if customfunction:
				customfunction(_form_inst)
			# _temp = int(_form_inst.data['technique_instruction'])
			# print(_temp)
			save_success = 'True'
			_form_inst = ModelForm(request.POST)
		else:
			save_success = 'False'
	# 保存成功，使用redirect()跳转到指定页面
	# return redirect('/LAMProcessData/EditBasicInfomation/Workshop/')
	# return HttpResponseRedirect(reverse('/LAMProcessData/EditBasicInfomation/Workshop/', args=[111, 222]))
	# return HttpResponseRedirect(reverse('/LAMProcessData/EditBasicInfomation/Workshop/', kwargs={'success': 'True'}))
	# return render(request, 'EditForm_Workshop.html', {'form': form})
	# print(save_success)
	if TableType == 'common':
		templateFileName = 'EditForm_BasicInformation.html'
	elif TableType == 'advanced':
		templateFileName = 'EditForm_BasicInformation_InputSelect_Tables.html'
	return render(request, templateFileName,
	              {'form': _form_inst,
	               'operate': '新建',
	               'save_success': save_success,
	               'Common_URL': Common_URL,
	               'Back_URL': Common_URL['Back_URL_' + modelname]})


# 编辑修改页面
@login_required
def BasicInformation_Edit(request, Model, ModelForm, modelname, TableType='common', isvalidType='default',
                          SaveMethod='default'):
	# Check_Is_authenticated(request)
	item_id = request.GET.get('item_id')
	save_success = None
	# 查询到指定的数据
	try:
		_model_inst = Model.objects.get(id=item_id)
	except:
		messages.success(request, "未找到此条记录！")
		return redirect(Common_URL['Back_URL_' + modelname])
	if request.method != 'POST':
		# 如果不是post,创建一个表单，并用instance=article当前数据填充表单
		_form_inst = ModelForm(instance=_model_inst)
		_form_inst.itemid = item_id
	else:
		# 如果是post,instance=article当前数据填充表单，并用data=request.POST获取到表单里的内容
		_form_inst = ModelForm(instance=_model_inst, data=request.POST)
		try:
			if SaveMethod == 'default':
				_form_inst.save()  # 保存
			elif SaveMethod == 'custom':
				_form_inst.save_custom()  # 保存
			_form_inst.itemid = item_id

			_isValid = True
			if isvalidType == 'default':
				_isValid = _form_inst.is_valid()
			elif isvalidType == 'custom':
				_isValid = _form_inst.is_valid_custom()
			if _isValid:  # 验证
				save_success = 'True'
			else:
				_form_inst.error_messages = _form_inst.errors.get_json_data()
				save_success = 'False'
		except:
			save_success = 'False'
			_form_inst.error_messages = _form_inst.errors.get_json_data()
	if TableType == 'common':
		templateFileName = 'EditForm_BasicInformation.html'
	elif TableType == 'advanced':
		templateFileName = 'EditForm_BasicInformation_InputSelect_Tables.html'
	# elif TableType == 'subWindow_table':
	# 	templateFileName = 'SubWindow_SimpleForm.html'
	# elif TableType == 'subWindow_table_with_label':
	# 	templateFileName = 'SubWindow_SimpleForm_with_label.html'
	return render(request, templateFileName, {'form': _form_inst,
	                                          'operate': '编辑',
	                                          'save_success': save_success,
	                                          'Common_URL': Common_URL,
	                                          'Back_URL': Common_URL['Back_URL_' + modelname]})


@login_required
def BasicInformation_Delete(request, Model, modelname):
	# Check_Is_authenticated(request)
	# if not DEBUG:
	# 	messages.success(request, "非调试模式下无权删除！")
	item_id = request.POST.get('id')
	try:
		_model_inst = Model.objects.get(id=item_id)
	except:
		messages.success(request, "未找到此条记录！")
		return redirect(Common_URL['Back_URL_' + modelname])

	try:
		if request.method == 'POST':
			_model_inst.available = False
			_model_inst.save()
		# _model_inst.delete()
		messages.success(request, "冻结成功！若要激活此条记录请联系维护人员。")
	except:
		messages.success(request, "冻结失败！")
	return redirect(Common_URL['Back_URL_' + modelname])


@login_required
def BasicInformation_OperateData(request, Model, ModelForm, TableType='common', attlist=None, qset=(Q(available=True))):
	# Check_Is_authenticated(request)
	# all_entries = Model.objects.all()
	try:
		all_entries = Model.objects.filter(qset)
		_modelfilednames = [f.attname for f in Model._meta.fields]
		if not attlist:
			attlist = [f.attname for f in Model._meta.fields]
	except:
		pass
	# if 'available' in attlist:
	# 	attlist.remove('available')
	# all_entries_dict = [{att: str(i.__getattribute__(att.replace('_id', ''))) for att in attlist} for i in all_entries]

	# all_entries_dict = [{att: str(i.__getattribute__(att.replace('_id', ''))) if att in Model._meta.fields else str(i.__getattribute__(att).all()) for att in attlist} for i in all_entries]

	all_entries_dict = []
	for i in all_entries:
		_dict = {}
		for att in attlist:
			if att in _modelfilednames:
				# 替换_id, 从而获得外键实例的名称
				_dict[att] = str(i.__getattribute__(att.replace('_id', '')))
			else:
				_dict[att] = list(map(str, list(i.__getattribute__(att).all())))
		all_entries_dict.append(_dict)

	# print([{att: str(i.chemicalelements.all()) for att in attlist} for i in all_entries])
	if request.method == 'POST':
		_form_inst = ModelForm(request.POST)
		if _form_inst.is_valid():
			try:
				_form_inst.save()
				_form_inst = ModelForm()
				_form_inst.posted = True
				_form_inst.save_success = True
			except:
				_form_inst.save_success = False
		else:
			# 点上get_json_data()它，打印的错误信息会以json方式显示
			_form_inst.save_success = False
			_form_inst.error_messages = _form_inst.errors.get_json_data()
	else:
		_form_inst = ModelForm()
	# print(_form_inst.title)
	if TableType == 'common':
		templateFileName = 'OperateForm_BasicInfomation.html'
	elif TableType == 'advanced':
		templateFileName = 'OperateForm_BasicInfomation_AdvancedTables.html'
	elif TableType == 'test':
		templateFileName = 'OperateForm_BasicInfomation_AdvancedTables1.html'
	return render(request, templateFileName, {'form': _form_inst,
	                                          'all_entries': all_entries_dict,
	                                          'Common_URL': Common_URL})


def OperateData_workshop(request):
	return BasicInformation_OperateData(request, Model=Workshop, ModelForm=WorkshopForm)


@permission_required('LAMProcessData.add_workshop', login_url=Common_URL['403'])
def new_workshop(request):
	return BasicInformation_New(request, ModelForm=WorkshopForm, modelname='workshop')


@permission_required('LAMProcessData.change_workshop', login_url=Common_URL['403'])
def edit_workshop(request):
	return BasicInformation_Edit(request, Model=Workshop, ModelForm=WorkshopForm, modelname='workshop')


@permission_required('LAMProcessData.change_workshop', login_url=Common_URL['403'])
def del_workshop(request):
	return BasicInformation_Delete(request, Model=Workshop, modelname='workshop')


'''============================================================================'''


def OperateData_computer(request):
	return BasicInformation_OperateData(request, Model=Computer, ModelForm=ComputerForm)


@permission_required('LAMProcessData.add_computer', login_url=Common_URL['403'])
def new_computer(request):
	return BasicInformation_New(request, ModelForm=ComputerForm, modelname='computer')


@permission_required('LAMProcessData.change_computer', login_url=Common_URL['403'])
def edit_computer(request):
	return BasicInformation_Edit(request, Model=Computer, ModelForm=ComputerForm, modelname='computer')


@permission_required('LAMProcessData.change_computer', login_url=Common_URL['403'])
def del_computer(request):
	return BasicInformation_Delete(request, Model=Computer, modelname='computer')


'''============================================================================'''


def OperateData_worksection(request):
	return BasicInformation_OperateData(request, Model=Worksection, ModelForm=WorksectionForm)


@permission_required('LAMProcessData.add_worksection', login_url=Common_URL['403'])
def new_worksection(request):
	def insertworksection_current_mission(_form_inst):
		_worksection_crtmission_obj = Worksection_Current_LAMProcessMission(work_section = _form_inst.instance)
		_worksection_crtmission_obj.save()
		pass
	return BasicInformation_New(request, ModelForm=WorksectionForm, modelname='worksection',customfunction=insertworksection_current_mission)


@permission_required('LAMProcessData.change_worksection', login_url=Common_URL['403'])
def edit_worksection(request):
	return BasicInformation_Edit(request, Model=Worksection, ModelForm=WorksectionForm, modelname='worksection')


@permission_required('LAMProcessData.change_worksection', login_url=Common_URL['403'])
def del_worksection(request):
	return BasicInformation_Delete(request, Model=Worksection, modelname='worksection')


'''============================================================================'''


def OperateData_lammaterial(request):
	attlist = [
		'id',
		'material_name',
		'material_code',
		'nominal_composition',
		'chemicalelements',
		'available',
	]
	return BasicInformation_OperateData(request, Model=LAMMaterial, ModelForm=LAMMaterialForm, attlist=attlist)


@permission_required('LAMProcessData.add_lammaterial', login_url=Common_URL['403'])
def new_lammaterial(request):
	return BasicInformation_New(request, ModelForm=LAMMaterialForm, modelname='lammaterial')


@permission_required('LAMProcessData.change_lammaterial', login_url=Common_URL['403'])
def edit_lammaterial(request):
	return BasicInformation_Edit(request, Model=LAMMaterial, ModelForm=LAMMaterialForm, modelname='lammaterial')


@permission_required('LAMProcessData.change_lammaterial', login_url=Common_URL['403'])
def del_lammaterial(request):
	return BasicInformation_Delete(request, Model=LAMMaterial, modelname='lammaterial')


'''============================================================================'''


def OperateData_rawstockcategory(request):
	return BasicInformation_OperateData(request, Model=RawStockCategory, ModelForm=RawStockCategoryForm)


def new_rawstockcategory(request):
	return BasicInformation_New(request, ModelForm=RawStockCategoryForm, modelname='rawstockcategory')


def edit_rawstockcategory(request):
	return BasicInformation_Edit(request, Model=RawStockCategory, ModelForm=RawStockCategoryForm,
	                             modelname='rawstockcategory')


def del_rawstockcategory(request):
	return BasicInformation_Delete(request, Model=RawStockCategory, modelname='rawstockcategory')


'''============================================================================'''


def OperateData_lamproductionworktype(request):
	return BasicInformation_OperateData(request, Model=LAMProductionWorkType, ModelForm=LAMProductionWorkTypeForm)


def new_lamproductionworktype(request):
	return BasicInformation_New(request, ModelForm=LAMProductionWorkTypeForm, modelname='lamproductionworktype')


def edit_lamproductionworktype(request):
	return BasicInformation_Edit(request, Model=LAMProductionWorkType, ModelForm=LAMProductionWorkTypeForm,
	                             modelname='lamproductionworktype')


def del_lamproductionworktype(request):
	return BasicInformation_Delete(request, Model=LAMProductionWorkType, modelname='lamproductionworktype')


'''============================================================================'''


# 工序在工艺文件中实例化

def OperateData_lamtechinstserial(request):
	return BasicInformation_OperateData(request, Model=LAM_TechInst_Serial, ModelForm=LAMTechInstSerialForm_Browse,
	                                    TableType='advanced')


def new_lamtechinstserial(request):
	return BasicInformation_New(request, ModelForm=LAMTechInstSerialForm, modelname='lamtechinstserial',
	                            TableType='advanced', isvalidType='custom')


def edit_lamtechinstserial(request):
	return BasicInformation_Edit(request, Model=LAM_TechInst_Serial, ModelForm=LAMTechInstSerialForm_Edit,
	                             modelname='lamtechinstserial')


def del_lamtechinstserial(request):
	return BasicInformation_Delete(request, Model=LAM_TechInst_Serial, modelname='lamtechinstserial')

'''============================================================================'''

# def edit_lamprocessparameters(request):
# 	# Check_Is_authenticated(request)
# 	# inst表示实例
# 	# 如果不是POST方法访问
# 	save_success = None
# 	isvalidType = 'custom'
# 	if request.method != 'POST':
# 		# 创建一个空表单在页面显示
# 		_form_inst = ModelForm()
# 	else:
# 		# 否则为POST方式
# 		# request.POST方法，将会获取到表单中我们输入的数据
# 		_form_inst = ModelForm(request.POST)
# 		# 验证其合法性，使用is_valid()方法
# 		_isValid = True
# 		if isvalidType == 'default':
# 			_isValid = _form_inst.is_valid()
# 		elif isvalidType == 'custom':
# 			_isValid = _form_inst.is_valid_custom()
# 		if _isValid:
# 			# 验证通过，使用save()方法保存数据
# 			_form_inst.save()
# 			# 若有自定义函数，则执行
# 			if customfunction:
# 				customfunction(_form_inst)
# 			# _temp = int(_form_inst.data['technique_instruction'])
# 			# print(_temp)
# 			save_success = 'True'
# 			_form_inst = ModelForm(request.POST)
# 		else:
# 			save_success = 'False'
# 	# 保存成功，使用redirect()跳转到指定页面
# 	# return redirect('/LAMProcessData/EditBasicInfomation/Workshop/')
# 	# return HttpResponseRedirect(reverse('/LAMProcessData/EditBasicInfomation/Workshop/', args=[111, 222]))
# 	# return HttpResponseRedirect(reverse('/LAMProcessData/EditBasicInfomation/Workshop/', kwargs={'success': 'True'}))
# 	# return render(request, 'EditForm_Workshop.html', {'form': form})
# 	# print(save_success)
# 	if TableType == 'common':
# 		templateFileName = 'EditForm_BasicInformation.html'
# 	elif TableType == 'advanced':
# 		templateFileName = 'EditForm_BasicInformation_InputSelect_Tables.html'
# 	return render(request, templateFileName,
# 	              {'form': _form_inst,
# 	               'operate': '新建',
# 	               'save_success': save_success,
# 	               'Common_URL': Common_URL,
# 	               'Back_URL': Common_URL['Back_URL_' + modelname]})

'''============================================================================'''


def OperateData_cncstatuscategory(request):
	return BasicInformation_OperateData(request, Model=CNCStatusCategory, ModelForm=CNCStatusCategoryForm)


def new_cncstatuscategory(request):
	return BasicInformation_New(request, ModelForm=CNCStatusCategoryForm, modelname='cncstatuscategory')


def edit_cncstatuscategory(request):
	return BasicInformation_Edit(request, Model=CNCStatusCategory, ModelForm=CNCStatusCategoryForm,
	                             modelname='cncstatuscategory')


def del_cncstatuscategory(request):
	return BasicInformation_Delete(request, Model=CNCStatusCategory, modelname='cncstatuscategory')


'''============================================================================'''


def OperateData_lamproductcategory(request):
	return BasicInformation_OperateData(request, Model=LAMProductCategory, ModelForm=LAMProductCategoryForm)


def new_lamproductcategory(request):
	return BasicInformation_New(request, ModelForm=LAMProductCategoryForm, modelname='productcategory')


def edit_lamproductcategory(request):
	return BasicInformation_Edit(request, Model=LAMProductCategory, ModelForm=LAMProductCategoryForm,
	                             modelname='productcategory')


def del_lamproductcategory(request):
	return BasicInformation_Delete(request, Model=LAMProductCategory, modelname='productcategory')


'''============================================================================'''


def test1(request):
	return BasicInformation_OperateData(request, Model=LAMTechniqueInstruction, ModelForm=LAMTechniqueInstructionForm,
	                                    TableType='test')


def OperateData_lamtechniqueinstruction(request):
	attlist = [
		'id',
		'instruction_code',
		'instruction_name',
		'version_code',
		'version_number',
		'product_category',
		'product',
		'temporary',
		'filed',
		'available',
	]
	return BasicInformation_OperateData(request, Model=LAMTechniqueInstruction, ModelForm=LAMTechniqueInstructionForm,
	                                    TableType='advanced', attlist=attlist)


def new_lamtechniqueinstruction(request):
	return BasicInformation_New(request, ModelForm=LAMTechniqueInstructionForm, modelname='lamtechniqueinstruction')


def edit_lamtechniqueinstruction(request):
	return BasicInformation_Edit(request, Model=LAMTechniqueInstruction, ModelForm=LAMTechniqueInstructionForm,
	                             modelname='lamtechniqueinstruction')


def del_lamtechniqueinstruction(request):
	return BasicInformation_Delete(request, Model=LAMTechniqueInstruction, modelname='lamtechniqueinstruction')


'''============================================================================'''


def OperateData_lamprodcate_techinst(request):
	return BasicInformation_OperateData(request, Model=LAMProdCate_TechInst, ModelForm=LAMProdCate_TechInstForm)


def new_lamprodcate_techinst(request):
	return BasicInformation_New(request, ModelForm=LAMProdCate_TechInstForm, modelname='lamprodcate_techinst')


def edit_lamprodcate_techinst(request):
	return BasicInformation_Edit(request, Model=LAMProdCate_TechInst, ModelForm=LAMProdCate_TechInstForm,
	                             modelname='lamprodcate_techinst')


def del_lamprodcate_techinst(request):
	return BasicInformation_Delete(request, Model=LAMProdCate_TechInst, modelname='lamprodcate_techinst')


'''============================================================================'''


def OperateData_lamproduct(request):
	return BasicInformation_OperateData(request, Model=LAMProduct, ModelForm=LAMProductForm)


def new_lamproduct(request):
	return BasicInformation_New(request, ModelForm=LAMProductForm, modelname='lamproduct')


def edit_lamproduct(request):
	return BasicInformation_Edit(request, Model=LAMProduct, ModelForm=LAMProductForm,
	                             modelname='lamproduct')


def del_lamproduct(request):
	return BasicInformation_Delete(request, Model=LAMProduct, modelname='lamproduct')


'''============================================================================'''


# 取样部位
def OperateData_samplingposition(request):
	return BasicInformation_OperateData(request, Model=SamplingPosition, ModelForm=SamplingPositionForm)


@permission_required('LAMProcessData.add_samplingposition', login_url=Common_URL['403'])
def new_samplingposition(request):
	return BasicInformation_New(request, ModelForm=SamplingPositionForm, modelname='samplingposition')


@permission_required('LAMProcessData.change_samplingposition', login_url=Common_URL['403'])
def edit_samplingposition(request):
	return BasicInformation_Edit(request, Model=SamplingPosition, ModelForm=SamplingPositionForm,
	                             modelname='samplingposition')


@permission_required('LAMProcessData.change_samplingposition', login_url=Common_URL['403'])
def del_samplingposition(request):
	return BasicInformation_Delete(request, Model=SamplingPosition, modelname='samplingposition')


'''============================================================================'''


# 取样方向
def OperateData_samplingdirection(request):
	return BasicInformation_OperateData(request, Model=SamplingDirection, ModelForm=SamplingDirectionForm)


@permission_required('LAMProcessData.add_samplingdirection', login_url=Common_URL['403'])
def new_samplingdirection(request):
	return BasicInformation_New(request, ModelForm=SamplingDirectionForm, modelname='samplingdirection')


@permission_required('LAMProcessData.change_samplingdirection', login_url=Common_URL['403'])
def edit_samplingdirection(request):
	return BasicInformation_Edit(request, Model=SamplingDirection, ModelForm=SamplingDirectionForm,
	                             modelname='samplingdirection')


@permission_required('LAMProcessData.change_samplingdirection', login_url=Common_URL['403'])
def del_samplingdirection(request):
	return BasicInformation_Delete(request, Model=SamplingDirection, modelname='samplingdirection')


'''============================================================================'''


# 热处理状态
def OperateData_heattreatmentstate(request):
	return BasicInformation_OperateData(request, Model=HeatTreatmentState, ModelForm=HeatTreatmentStateForm)


@permission_required('LAMProcessData.add_heattreatmentstate', login_url=Common_URL['403'])
def new_heattreatmentstate(request):
	return BasicInformation_New(request, ModelForm=HeatTreatmentStateForm, modelname='heattreatmentstate')


@permission_required('LAMProcessData.change_heattreatmentstate', login_url=Common_URL['403'])
def edit_heattreatmentstate(request):
	return BasicInformation_Edit(request, Model=HeatTreatmentState, ModelForm=HeatTreatmentStateForm,
	                             modelname='heattreatmentstate')


@permission_required('LAMProcessData.change_heattreatmentstate', login_url=Common_URL['403'])
def del_heattreatmentstate(request):
	return BasicInformation_Delete(request, Model=HeatTreatmentState, modelname='heattreatmentstate')


'''============================================================================'''


def OperateData_rawstock(request):
	return BasicInformation_OperateData(request, Model=RawStock, ModelForm=RawStockForm,
	                                    TableType='advanced')


def new_rawstock(request):
	return BasicInformation_New(request, ModelForm=RawStockForm, modelname='rawstock')


def edit_rawstock(request):
	return BasicInformation_Edit(request, Model=RawStock, ModelForm=RawStockForm_Edit,
	                             modelname='rawstock')


'''============================================================================'''


def rawstockflow(request):
	return BasicInformation_OperateData(request, Model=RawStockSendRetrieve, ModelForm=RawStockSendForm,
	                                    TableType='advanced')


def del_rawstock(request):
	return BasicInformation_Delete(request, Model=RawStock, modelname='rawstockflow')


def send_rawstockflow(request):
	return BasicInformation_New(request, ModelForm=RawStockSendForm, modelname='rawstockflow')


# # Check_Is_authenticated(request)
# # inst表示实例
# # 如果不是POST方法访问
# save_success = None
# if request.method != 'POST':
# 	# 创建一个空表单在页面显示
# 	_form_inst = RawStockSendForm()
# else:
# 	# 否则为POST方式
# 	# request.POST方法，将会获取到表单中我们输入的数据
# 	_form_inst = RawStockSendForm(request.POST)
# 	# 验证其合法性，使用is_valid()方法
# 	_isValid = _form_inst.is_valid()
# 	if _isValid:
# 		# 验证通过，使用save()方法保存数据
# 		_form_inst.save()
# 		save_success = 'True'
# 		_form_inst = RawStockSendForm(request.POST)
# 	else:
# 		save_success = 'False'
# # 保存成功，使用redirect()跳转到指定页面
# # return redirect('/LAMProcessData/EditBasicInfomation/Workshop/')
# # return HttpResponseRedirect(reverse('/LAMProcessData/EditBasicInfomation/Workshop/', args=[111, 222]))
# # return HttpResponseRedirect(reverse('/LAMProcessData/EditBasicInfomation/Workshop/', kwargs={'success': 'True'}))
# # return render(request, 'EditForm_Workshop.html', {'form': form})
# # print(save_success)
#
# templateFileName = 'EditForm_RawStockFlow_InputSelect_Tables.html'
#
# return render(request, templateFileName,
#               {'form': _form_inst,
#                'operate': '原材料发放回收',
#                'save_success': save_success,
#                'Common_URL': Common_URL,
#                'Back_URL': Common_URL['Back_URL_rawstockflow']})

def retrieve_rawstockflow(request):
	# return BasicInformation_New(request, ModelForm=RawStockRetrieveForm, modelname='rawstockflow')
	return BasicInformation_Edit(request, Model=RawStockSendRetrieve, ModelForm=RawStockRetrieveForm,
	                             modelname='rawstockflow')


def edit_rawstockflow(request):
	return BasicInformation_Edit(request, Model=RawStockSendRetrieve, ModelForm=RawStockSendForm,
	                             modelname='rawstockflow')


def del_rawstockflow(request):
	return BasicInformation_Delete(request, Model=RawStockSendRetrieve, modelname='rawstockflow')


'''============================================================================'''


# 生产任务
def OperateData_lamprocessmission(request):
	return BasicInformation_OperateData(request, Model=LAMProcessMission, ModelForm=LAMProcessMissionForm_Browse,
	                                    TableType='advanced')


def new_lamprocessmission(request):
	def insertprocessmission_timecutrecords(_form_inst):
		_timecut_obj = Process_Mission_timecut(process_mission = _form_inst.instance)
		_timecut_obj.save()
		pass
	return BasicInformation_New(request,
	                            ModelForm=LAMProcessMissionForm_Edit,
	                            modelname='lamprocessmission',
	                            TableType='advanced',
	                            isvalidType='custom',
	                            customfunction=insertprocessmission_timecutrecords)


def finish_lamprocessmission(request):
	# if request.method == 'POST':
	# 	pass
	return BasicInformation_Edit(request, Model=LAMProcessMission,
	                             ModelForm=LAMProcessMissionForm_Finish,
	                             modelname='lamprocessmission', SaveMethod='custom')


def del_lamprocessmission(request):
	return BasicInformation_Delete(request, Model=LAMProcessMission, modelname='lamprocessmission')


'''============================================================================'''

'''======☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆======'''
'''======                             检验记录                              ======'''
'''======☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆======'''


def OperateData_ProductPhyChemTest(request):
	# 注意'id'项，注意外键增加'_id'
	attlist = [
		'id',
		'LAM_product_id',
		'LAM_techinst_serial_id',
		'commission_date',
		'heat_treatment_state_id',
		'mechanicaltest_tensile',
		'mechanicaltest_toughness',
		'chemicaltest']
	return BasicInformation_OperateData(request, Model=PhysicochemicalTest_Mission,
	                                    ModelForm=ProductPhyChemTestForm_Browse,
	                                    TableType='advanced',
	                                    attlist=attlist,
	                                    qset=(Q(available=True) & Q(RawStock_id=None))
	                                    )


def OperateData_RawStockPhyChemTest(request):
	# 注意'id'项，注意外键增加'_id'
	attlist = [
		'id',
		'RawStock_id',
		'LAM_techinst_serial_id',
		'commission_date',
		'heat_treatment_state_id',
		'mechanicaltest_tensile',
		'mechanicaltest_toughness',
		'chemicaltest']
	return BasicInformation_OperateData(request, Model=PhysicochemicalTest_Mission,
	                                    ModelForm=RawStockPhyChemTestForm_Browse,
	                                    TableType='advanced',
	                                    attlist=attlist,
	                                    qset=(Q(available=True) & Q(LAM_product_id=None))
	                                    )

def BrowseData_MissionLAMProcessInspection(request):
	# return BasicInformation_OperateData(request, Model=LAMProcessMission, ModelForm=LAMProcessMissionForm_Browse,
	#                                     TableType='advanced')

	attlist = None
	qset = (Q(available=True))
	Model = LAMProcessMission
	ModelForm = LAMProcessMissionForm_Browse
	try:
		all_entries = Model.objects.filter(qset)
		_modelfilednames = [f.attname for f in Model._meta.fields]
		if not attlist:
			attlist = [f.attname for f in Model._meta.fields]
	except:
		pass
	# if 'available' in attlist:
	# 	attlist.remove('available')
	# all_entries_dict = [{att: str(i.__getattribute__(att.replace('_id', ''))) for att in attlist} for i in all_entries]

	# all_entries_dict = [{att: str(i.__getattribute__(att.replace('_id', ''))) if att in Model._meta.fields else str(i.__getattribute__(att).all()) for att in attlist} for i in all_entries]

	all_entries_dict = []
	for i in all_entries:
		_dict = {}
		for att in attlist:
			if att in _modelfilednames:
				# 替换_id, 从而获得外键实例的名称
				_dict[att] = str(i.__getattribute__(att.replace('_id', '')))
			else:
				_dict[att] = list(map(str, list(i.__getattribute__(att).all())))
		all_entries_dict.append(_dict)

	_form_inst = ModelForm()
	_form_inst.title = '激光成形过程记录过检'
	# print(_form_inst.title)

	templateFileName = 'BrowseData_MissionLAMProcessInspection.html'
	return render(request, templateFileName, {'form': _form_inst,
	                                          'all_entries': all_entries_dict,
	                                          'Common_URL': Common_URL})

def Inspect_MissionLAMProcessInspection(request, MissionItemID):
	_mission = LAMProcessMission.objects.get(id = MissionItemID)
	_mission_timecut = Process_Mission_timecut.objects.get(process_mission = _mission)
	_start_datetime = _mission_timecut.process_start_time
	_finish_datetime = _mission_timecut.process_finish_time

	_datetime_list = [(_start_datetime+datetime.timedelta(days=i)).strftime('%Y-%m-%d') for i in range((_finish_datetime - _start_datetime).days)]
	if _finish_datetime.strftime('%Y-%m-%d') not in _datetime_list:
		_datetime_list.append(_finish_datetime.strftime('%Y-%m-%d'))

	_h_delta=2
	_time_dict = {str(i): '%02d:00~%02d:00' % (i, i + _h_delta) for i in range(0, 24, _h_delta)}
	_first_date = _start_datetime.strftime('%Y-%m-%d')
	_first_time_hour = int(float(_start_datetime.strftime('%H'))/_h_delta)*_h_delta
	_first_time_text = _time_dict[str(_first_time_hour)]

	return render(request, 'SubWindow_SimpleForm_with_graph.html',
	              {
		              # 'form': _form_inst,
		              # 'all_entries': all_entries_dict,
		              'missionID':MissionItemID,
		              'title': '激光成形过程记录',
		              'smalltitle': '%s/%s/%s[%s-%s]'%(_mission.LAM_product.product_code,
		                                        _mission.work_section,
		                                        _mission.LAM_techinst_serial.technique_instruction.instruction_code,
		                                        _mission.LAM_techinst_serial.serial_number,
		                                        _mission.LAM_techinst_serial.serial_note),
		              'datetime_list':_datetime_list,   # 对话框中日期列表
		              'time_dict':_time_dict,           # 对话框中时间列表
		              'first_date':_first_date,
		              'first_time_hour':_first_time_hour,
		              'first_time_text':_first_time_text,
		              'Common_URL': Common_URL})


# def Inspect_Complete_MissionLAMProcessRecords(request, MissionItemID):
# 	RT_FineData.Realtime_FineData.inspect_complete_processRecord(MissionItemID)


'''============================================================================'''


def getTestDataList(all_entries, testModel, manytomanykey):
	# all_entries = _model_inst.mechanicaltest_tensile.order_by('sample_number')
	attlist = [f.attname for f in testModel._meta.fields]
	# attlist.remove('id')
	# manytomanykey = []
	datalist = []
	for i in all_entries:
		_dict = {}
		for att in attlist:
			_dict[att] = str(i.__getattribute__(att.replace('_id', '')))
			if att in manytomanykey:
				_dict[att] = list(map(str, list(i.__getattribute__(att).all())))
			else:
				_dict[att] = str(i.__getattribute__(att.replace('_id', '')))
		datalist.append(_dict)
	return datalist


def edit_TemplatePhyChemTest(request, IfProductTest, EditForm):
	item_id = request.GET.get('item_id')
	save_success = None
	# 查询到指定的数据
	try:
		_model_inst = PhysicochemicalTest_Mission.objects.get(id=item_id)
	except:
		messages.success(request, "未找到此条记录！")
		return redirect(Common_URL['Back_URL_InspectionRecords_RawStockPhyChemTest'])

	# _form_tensile_data = _model_inst.mechanicaltest_tensile

	# 该检测任务内的拉伸数据
	all_entries = _model_inst.mechanicaltest_tensile.order_by('sample_number')
	tensile_datalist = getTestDataList(all_entries, MechanicalTest_Tensile, [])
	# 该检测任务内的冲击数据
	all_entries = _model_inst.mechanicaltest_toughness.order_by('sample_number')
	toughness_datalist = getTestDataList(all_entries, MechanicalTest_Toughness, [])

	# 该检测任务内的化学成分测试数据
	# |--首先获得应检测的化学成分项目
	# 元素
	# element_items = _model_inst.LAM_product.product_category.material.chemicalelements.all().order_by('id')
	if bool(IfProductTest):
		element_items = _model_inst.LAM_product.product_category.material.chemicalelements.all().order_by('id')
	else:
		element_items = _model_inst.RawStock.material.chemicalelements.all().order_by('id')
	# 表格表头
	chemical_items = ['试样编号', '取样部位'] + [str(chem) + '/%' for chem in element_items]
	# |--再获取化学成分元素测试值
	all_chem_mission_entries = _model_inst.chemicaltest.all()
	chemical_datalist = []
	for chemical_mission in all_chem_mission_entries:
		chemical_data = {'id': chemical_mission.id,
		                 'sample_number': chemical_mission.sample_number,
		                 'sampling_position': chemical_mission.sampling_position,
		                 'test_value': []}
		_temp_dict = {}
		for element in chemical_mission.elements.all():
			_temp_dict[str(element.element)] = element.value
		# chemical_data[str(element.element)] = element.value
		for element in [str(chem) for chem in element_items]:
			if element not in _temp_dict:
				chemical_data['test_value'].append('-')
			else:
				chemical_data['test_value'].append(_temp_dict[element])
		chemical_datalist.append(chemical_data)
	# |--结束

	# chemical_datalist = getTestDataList(all_chem_mission_entries, ChemicalTest_Element, [])

	if request.method != 'POST':
		# 如果不是post,创建一个表单，并用instance=article当前数据填充表单
		_form_inst = EditForm(instance=_model_inst)
		# _form_Tensile = MechanicalTest_TensileForm()
		_form_inst.itemid = item_id
	else:
		# 如果是post,instance=article当前数据填充表单，并用data=request.POST获取到表单里的内容
		_form_inst = EditForm(instance=_model_inst, data=request.POST)

		# _form_Tensile = MechanicalTest_TensileForm()
		try:
			_form_inst.save()  # 保存
			_form_inst.itemid = item_id
			_isValid = _form_inst.is_valid()
			if _isValid:  # 验证
				save_success = 'True'
			else:
				_form_inst.error_messages = _form_inst.errors.get_json_data()
				save_success = 'False'
		except:
			save_success = 'False'
			_form_inst.error_messages = _form_inst.errors.get_json_data()
	if bool(IfProductTest):
		BackURL = Common_URL['Back_URL_InspectionRecords_ProductPhyChemTest']
	else:
		BackURL = Common_URL['Back_URL_InspectionRecords_RawStockPhyChemTest']
	return render(request, "EditForm_PhyChemTest.html",
	              {'form': _form_inst,
	               'tensile_datalist': tensile_datalist,
	               'toughness_datalist': toughness_datalist,
	               'chemical_datalist': chemical_datalist,
	               'chemical_items': chemical_items,
	               'operate': 'edit',
	               'save_success': save_success,
	               'Common_URL': Common_URL,
	               'Back_URL': BackURL,
	               'If_Product_Test': IfProductTest})


# 产品理化检测 新建
def new_ProductPhyChemTest(request):
	save_success = None
	if request.method != 'POST':
		# 创建一个空表单在页面显示
		_form_inst = ProductPhyChemTestForm_New()
	else:
		# 否则为POST方式
		# request.POST方法，将会获取到表单中我们输入的数据
		_form_inst = ProductPhyChemTestForm_New(request.POST)
		# 验证其合法性，使用is_valid()方法
		_isValid = True
		_isValid = _form_inst.is_valid()

		if _isValid:
			# 验证通过，使用save()方法保存数据
			_form_inst.save()
			# _temp = int(_form_inst.data['technique_instruction'])
			# print(_temp)
			save_success = 'True'
			_form_inst = ProductPhyChemTestForm_New(request.POST)
		else:
			save_success = 'False'

	return render(request, "EditForm_PhyChemTest.html",
	              {'form': _form_inst,
	               'operate': 'new',
	               'save_success': save_success,
	               'Common_URL': Common_URL,
	               'Back_URL': Common_URL['Back_URL_InspectionRecords_ProductPhyChemTest']})


def edit_ProductPhyChemTest(request):
	# def getTestDataList(all_entries, testModel, manytomanykey):
	# 	# all_entries = _model_inst.mechanicaltest_tensile.order_by('sample_number')
	# 	attlist = [f.attname for f in testModel._meta.fields]
	# 	# attlist.remove('id')
	# 	# manytomanykey = []
	# 	datalist = []
	# 	for i in all_entries:
	# 		_dict = {}
	# 		for att in attlist:
	# 			_dict[att] = str(i.__getattribute__(att.replace('_id', '')))
	# 			if att in manytomanykey:
	# 				_dict[att] = list(map(str, list(i.__getattribute__(att).all())))
	# 			else:
	# 				_dict[att] = str(i.__getattribute__(att.replace('_id', '')))
	# 		datalist.append(_dict)
	# 	return datalist
	#
	# # Check_Is_authenticated(request)
	# item_id = request.GET.get('item_id')
	# save_success = None
	# # 查询到指定的数据
	# try:
	# 	_model_inst = PhysicochemicalTest_Mission.objects.get(id=item_id)
	# except:
	# 	messages.success(request, "未找到此条记录！")
	# 	return redirect(Common_URL['Back_URL_InspectionRecords_ProductPhyChemTest'])
	#
	# # _form_tensile_data = _model_inst.mechanicaltest_tensile
	#
	# # 该检测任务内的拉伸数据
	# all_entries = _model_inst.mechanicaltest_tensile.order_by('sample_number')
	# tensile_datalist = getTestDataList(all_entries, MechanicalTest_Tensile, [])
	# # 该检测任务内的冲击数据
	# all_entries = _model_inst.mechanicaltest_toughness.order_by('sample_number')
	# toughness_datalist = getTestDataList(all_entries, MechanicalTest_Toughness, [])
	#
	# # 该检测任务内的化学成分测试数据
	# # |--首先获得应检测的化学成分项目
	# # 元素
	# element_items = _model_inst.LAM_product.product_category.material.chemicalelements.all().order_by('id')
	# # 表格表头
	# chemical_items = ['试样编号', '取样部位']+[str(chem)+'/%' for chem in element_items]
	# # |--再获取化学成分元素测试值
	# all_chem_mission_entries = _model_inst.chemicaltest.all()
	# chemical_datalist = []
	# for chemical_mission in all_chem_mission_entries:
	# 	chemical_data = {'id': chemical_mission.id,
	# 	                        'sample_number': chemical_mission.sample_number,
	# 	                        'sampling_position': chemical_mission.sampling_position,
	# 	                        'test_value': []}
	# 	_temp_dict = {}
	# 	for element in chemical_mission.elements.all():
	# 		_temp_dict[str(element.element)] = element.value
	# 		# chemical_data[str(element.element)] = element.value
	# 	for element in [str(chem) for chem in element_items]:
	# 		if element not in _temp_dict:
	# 			chemical_data['test_value'].append('-')
	# 		else:
	# 			chemical_data['test_value'].append(_temp_dict[element])
	# 	chemical_datalist.append(chemical_data)
	# # |--结束
	#
	# # chemical_datalist = getTestDataList(all_chem_mission_entries, ChemicalTest_Element, [])
	#
	# if request.method != 'POST':
	# 	# 如果不是post,创建一个表单，并用instance=article当前数据填充表单
	# 	_form_inst = ProductPhyChemTestForm_Edit(instance=_model_inst)
	# 	# _form_Tensile = MechanicalTest_TensileForm()
	# 	_form_inst.itemid = item_id
	# else:
	# 	# 如果是post,instance=article当前数据填充表单，并用data=request.POST获取到表单里的内容
	# 	_form_inst = ProductPhyChemTestForm_Edit(instance=_model_inst, data=request.POST)
	#
	# 	# _form_Tensile = MechanicalTest_TensileForm()
	# 	try:
	# 		_form_inst.save()  # 保存
	# 		_form_inst.itemid = item_id
	# 		_isValid = _form_inst.is_valid()
	# 		if _isValid:  # 验证
	# 			save_success = 'True'
	# 		else:
	# 			_form_inst.error_messages = _form_inst.errors.get_json_data()
	# 			save_success = 'False'
	# 	except:
	# 		save_success = 'False'
	# 		_form_inst.error_messages = _form_inst.errors.get_json_data()
	#
	# return render(request, "EditForm_PhyChemTest.html",
	#               {'form': _form_inst,
	#                'tensile_datalist': tensile_datalist,
	#                'toughness_datalist':toughness_datalist,
	#                'chemical_datalist':chemical_datalist,
	#                'chemical_items':chemical_items,
	#                'operate': 'edit',
	#                'save_success': save_success,
	#                'Common_URL': Common_URL,
	#                'Back_URL': Common_URL['Back_URL_InspectionRecords_ProductPhyChemTest']})
	return edit_TemplatePhyChemTest(request, 1, ProductPhyChemTestForm_Edit)


'''============================================================================'''


# 原材料理化检测 新建
def new_RawStockPhyChemTest(request):
	save_success = None
	if request.method != 'POST':
		# 创建一个空表单在页面显示
		_form_inst = RawStockPhyChemTestForm_New()
	else:
		# 否则为POST方式
		# request.POST方法，将会获取到表单中我们输入的数据
		_form_inst = RawStockPhyChemTestForm_New(request.POST)
		# 验证其合法性，使用is_valid()方法
		_isValid = _form_inst.is_valid()

		if _isValid:
			# 验证通过，使用save()方法保存数据
			_form_inst.save()
			save_success = 'True'
			_form_inst = RawStockPhyChemTestForm_New(request.POST)
		else:
			save_success = 'False'

	return render(request, "EditForm_PhyChemTest.html",
	              {'form': _form_inst,
	               'operate': 'new',
	               'save_success': save_success,
	               'Common_URL': Common_URL,
	               'Back_URL': Common_URL['Back_URL_InspectionRecords_RawStockPhyChemTest']})


def edit_RawStockPhyChemTest(request):
	return edit_TemplatePhyChemTest(request, 0, RawStockPhyChemTestForm_Edit)


'''============================================================================'''


# 弹出增加数据的子窗口
def PhyChemTest_AddSingleTestData(request, MissionItemID, ModelForm, func):
	save_success = None
	if request.method != 'POST':
		# 创建一个空表单在页面显示
		_form_inst = ModelForm()
	else:
		# 否则为POST方式
		# request.POST方法，将会获取到表单中我们输入的数据
		_form_inst = ModelForm(request.POST)
		# 验证其合法性，使用is_valid()方法
		_isValid = _form_inst.is_valid()
		if _isValid:
			func(_form_inst, MissionItemID)
			save_success = 'True'
			_form_inst = ModelForm(request.POST)
		else:
			save_success = 'False'

	return render(request, "SubWindow_SimpleForm.html",
	              {'form': _form_inst,
	               'operate': 'new',
	               'save_success': save_success,
	               'Common_URL': Common_URL,
	               })


# 弹出修改数据的子窗口
def PhyChemTest_EditSingleTestData(request, SingleTestID, ModelForm, Model):
	save_success = None
	if request.method != 'POST':
		# 创建一个表单在页面显示
		_form_inst = ModelForm(instance=Model.objects.get(id=SingleTestID))
	else:
		# 否则为POST方式
		# request.POST方法，将会获取到表单中我们输入的数据
		SingleTest_obj = Model.objects.get(id=SingleTestID)
		_form_inst = ModelForm(instance=SingleTest_obj, data=request.POST)
		# 验证其合法性，使用is_valid()方法
		_isValid = _form_inst.is_valid()

		if _isValid:
			# 验证通过，使用save()方法保存数据
			_form_inst.save()

			save_success = 'True'
			_form_inst = ModelForm(request.POST)
		else:
			save_success = 'False'

	return render(request, "SubWindow_SimpleForm.html",
	              {'form': _form_inst,
	               'operate': 'edit',
	               'save_success': save_success,
	               'Common_URL': Common_URL,
	               })


'''============================================================================'''


# 新建拉伸数据
def PhyChemTest_AddTensile(request, MissionItemID):
	def func(_form_inst, MissionItemID):
		test_tensile = MechanicalTest_Tensile.objects.create(
			sample_number=_form_inst.cleaned_data['sample_number'],
			sampling_position=_form_inst.cleaned_data['sampling_position'],
			sampling_direction=_form_inst.cleaned_data['sampling_direction'],
			test_temperature=_form_inst.cleaned_data['test_temperature'],
			tensile_strength=_form_inst.cleaned_data['tensile_strength'],
			yield_strength=_form_inst.cleaned_data['yield_strength'],
			elongation=_form_inst.cleaned_data['elongation'],
			areareduction=_form_inst.cleaned_data['areareduction'],
			modulus=_form_inst.cleaned_data['modulus'],
			available=_form_inst.cleaned_data['available']
		)
		test_mission = PhysicochemicalTest_Mission.objects.get(id=MissionItemID)
		test_mission.mechanicaltest_tensile.add(test_tensile.id)
		test_mission.save()

	return PhyChemTest_AddSingleTestData(request, MissionItemID, MechanicalTest_TensileForm, func)


# 编辑拉伸数据
def PhyChemTest_EditTensile(request, TensileID):
	return PhyChemTest_EditSingleTestData(request, TensileID, MechanicalTest_TensileForm, MechanicalTest_Tensile)


# 新建冲击数据
def PhyChemTest_AddToughness(request, MissionItemID):
	def func(_form_inst, MissionItemID):
		test_toughness = MechanicalTest_Toughness.objects.create(
			sample_number=_form_inst.cleaned_data['sample_number'],
			sampling_position=_form_inst.cleaned_data['sampling_position'],
			sampling_direction=_form_inst.cleaned_data['sampling_direction'],
			test_temperature=_form_inst.cleaned_data['test_temperature'],
			toughness=_form_inst.cleaned_data['toughness'],
			available=_form_inst.cleaned_data['available']
		)
		test_mission = PhysicochemicalTest_Mission.objects.get(id=MissionItemID)
		test_mission.mechanicaltest_toughness.add(test_toughness.id)
		test_mission.save()

	return PhyChemTest_AddSingleTestData(request, MissionItemID, MechanicalTest_ToughnessForm, func)


# 编辑冲击数据
def PhyChemTest_EditToughness(request, ToughnessID):
	return PhyChemTest_EditSingleTestData(request, ToughnessID, MechanicalTest_ToughnessForm, MechanicalTest_Toughness)


# 新建化学元素数据
def PhyChemTest_AddChemicalElement(request, MissionItemID, IfProductTest):
	save_success = None
	_model_inst = PhysicochemicalTest_Mission.objects.get(id=MissionItemID)
	if bool(int(IfProductTest)):
		chemical_items = _model_inst.LAM_product.product_category.material.chemicalelements.all().order_by('id')
	else:
		chemical_items = _model_inst.RawStock.material.chemicalelements.all().order_by('id')
	# chemical_items = [str(chem) for chem in chemical_items]
	if request.method != 'POST':
		# 创建一个空表单在页面显示
		_form_inst = MechanicalTest_ChemicalForm()
		_form_inst.addElementFields(chemical_items)
	else:
		# 否则为POST方式
		# request.POST方法，将会获取到表单中我们输入的数据
		_form_inst = MechanicalTest_ChemicalForm(request.POST)
		_form_inst.addElementFields(chemical_items)
		# 验证其合法性，使用is_valid()方法
		_isValid = _form_inst.is_valid()
		if _isValid:
			test_chemical = ChemicalTest.objects.create(
				sample_number=_form_inst.cleaned_data['sample_number'],
				sampling_position=_form_inst.cleaned_data['sampling_position'],
			)
			for element in chemical_items:
				if _form_inst.cleaned_data[element.element_code]:
					test_chemical_element = ChemicalTest_Element.objects.create(
						element=element,
						value=_form_inst.cleaned_data[element.element_code],
					)
					test_chemical.elements.add(test_chemical_element)
			test_mission = PhysicochemicalTest_Mission.objects.get(id=MissionItemID)
			test_mission.chemicaltest.add(test_chemical)
			test_mission.save()

			save_success = 'True'
			_form_inst = MechanicalTest_ChemicalForm(request.POST)
			_form_inst.addElementFields(chemical_items)
		else:
			save_success = 'False'

	return render(request, "SubWindow_SimpleForm.html",
	              {'form': _form_inst,
	               'operate': 'new',
	               'save_success': save_success,
	               'Common_URL': Common_URL,
	               })


def PhyChemTest_EditChemicalElement(request, MissionItemID, ChemicalItemID, IfProductTest):
	save_success = None
	# 理化测试任务实例
	_model_inst = PhysicochemicalTest_Mission.objects.get(id=MissionItemID)
	# 化学测试任务实例
	chemicaltest_inst = ChemicalTest.objects.get(id=ChemicalItemID)
	# 化学成分测试项
	if bool(int(IfProductTest)):
		chemical_items = _model_inst.LAM_product.product_category.material.chemicalelements.all().order_by('id')
	else:
		chemical_items = _model_inst.RawStock.material.chemicalelements.all().order_by('id')
	# chemical_items = [str(chem) for chem in chemical_items]
	if request.method != 'POST':
		# 创建一个空表单在页面显示
		_form_inst = MechanicalTest_ChemicalForm(instance=chemicaltest_inst)
		_form_inst.addElementFields(chemical_items)
		_form_inst.refreshValue(chemicaltest_inst.elements.all())
	else:
		# 否则为POST方式
		# request.POST方法，将会获取到表单中我们输入的数据
		_form_inst = MechanicalTest_ChemicalForm(request.POST)
		_form_inst.addElementFields(chemical_items)
		# 验证其合法性，使用is_valid()方法
		_isValid = _form_inst.is_valid()
		if _isValid:
			# test_chemical = chemicaltest_inst
			chemicaltest_inst.sample_number = _form_inst.cleaned_data['sample_number']
			chemicaltest_inst.sampling_position = _form_inst.cleaned_data['sampling_position']
			chemicaltest_inst.save()
			for element in chemical_items:

				if _form_inst.cleaned_data[element.element_code]:
					# 如果提交的数据存在本元素
					if element in map(lambda p: p.element, chemicaltest_inst.elements.all()):
						# 如果本元素之前已存在测试值，则更改
						element_test_obj = chemicaltest_inst.elements.get(element=element)
						element_test_obj.value = _form_inst.cleaned_data[element.element_code]
						element_test_obj.save()
					else:
						# 否则，新建该元素测试值
						element_test_obj = ChemicalTest_Element.objects.create(
							element=element,
							value=_form_inst.cleaned_data[element.element_code],
						)
						chemicaltest_inst.elements.add(element_test_obj)
						chemicaltest_inst.save()
				else:
					# 如果提交的数据为空数据
					if element in map(lambda p: p.element, chemicaltest_inst.elements.all()):
						# 如果本元素之前已存在测试值，则删除
						element_test_obj = chemicaltest_inst.elements.get(element=element)
						chemicaltest_inst.elements.remove(element_test_obj)
						chemicaltest_inst.save()
						element_test_obj.delete()

			# test_mission = PhysicochemicalTest_Mission.objects.get(id=MissionItemID)
			# test_mission.chemicaltest.add(test_chemical)
			# test_mission.save()
			# _form_inst.save()

			save_success = 'True'
			_form_inst = MechanicalTest_ChemicalForm(request.POST)
			_form_inst.addElementFields(chemical_items)
		else:
			save_success = 'False'

	return render(request, "SubWindow_SimpleForm.html",
	              {'form': _form_inst,
	               'operate': 'edit',
	               'save_success': save_success,
	               'Common_URL': Common_URL,
	               })


# def func(_form_inst, MissionItemID):
# 	test_chemical = ChemicalTest.objects.create(
# 		sample_number = _form_inst.cleaned_data['sample_number'],
# 		sampling_position=_form_inst.cleaned_data['sampling_position'],
# 	)
#
# 	test_chemical_element = ChemicalTest_Element.objects.create(
# 		element = _form_inst.cleaned_data['element'],
# 		value = _form_inst.cleaned_data['value'],
# 		)
# 	test_chemical
#
# 	test_mission = PhysicochemicalTest_Mission.objects.get(id=MissionItemID)
# 	test_mission.mechanicaltest_toughness.add(test_chemical_element.id)
# 	test_mission.save()
#
# return PhyChemTest_AddSingleTestData(request, MissionItemID, MechanicalTest_ChemicalForm, func)


'''============================================================================'''


def LAMProcessData_UpdateCNCData(request):
	if request.method == 'POST':
		pass
	else:
		pass
	# try:
	# 	if request.method == 'POST':
	# 		re = 'Save Success!'
	# 	else:
	# 		re = 'No POST!'
	# except:
	# 	re = 'Save Failed!'
	# # html = "MACAddress:%s,OxygenValue:%f,OxygenSensorValue:%f,InternalPressureValue:%f" % (MACAddress,OxygenValue,OxygenSensorValue,InternalPressureValue)
	#
	# return HttpResponse(re)
	pass


# # 如果是GET请求，那么返回一个空的表单
# def get(self, request):
# 	form = WorkshopForm()
# 	return render(request, 'one/index.html', {'form': form})
#
# # 如果是POST请求，那么将提交上来的数据进行校验
# def post(self, request):
# 	form = WorkshopForm(request.POST)
# 	if form.is_valid():
# 		name = form.cleaned_data.get('name')
# 		code = form.cleaned_data.get('code')
# 		print('=' * 30)
# 		print(name)
# 		print(code)
# 		print('=' * 30)
# 		return HttpResponse('success')
# 	else:
# 		# 点上get_json_data()它，打印的错误信息会以json方式显示
# 		print(form.errors.get_json_data())
# 		return HttpResponse('fail')

def current_datetime(request):
	now = datetime.datetime.now()
	html = "<html><body>It is now %s.</body></html>" % now
	return HttpResponse(html)


def test(request):
	t1 = time.time()
	# d0 = datetime.datetime(1949, 10, 1)
	d0 = 19491001
	for i in range(100000):
	# for i in range(1000):
		# Cost Time 0.600030.
		d=datetime.datetime(2019, 11, 9)
		x=int(d.strftime('%Y%m%d'))-d0
		# print()

		# Cost Time 1.472624.
		# d=datetime.datetime(2019, 11, 9)
		# x=(d-d0).days

		# Cost Time 4.029904.
		# timeArray = time.strptime("2019-11-29 20:35:00", "%Y-%m-%d %H:%M:%S")
		# timestamp = int(time.mktime(timeArray))


	# re =d.strftime('%Y%m%d')
	print(time.time()-t1)

	html = "<html><body>Cost Time %f.</body></html>" % (time.time()-t1)
	return HttpResponse(html)


def current_datetime_item(request):
	tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst = time.gmtime(time.time())

	return HttpResponse(
		"%d,%d,%d,%d,%d,%d,%d,%d,%d" % (tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst))


def GetLAMProcessData_Oxygen(request, MACAddress, OxygenValue, OxygenSensorValue, InternalPressureValue, md5Key):
	try:
		OxygenValue = float(OxygenValue)
		OxygenSensorValue = float(OxygenSensorValue)
		InternalPressureValue = float(InternalPressureValue)
		if checkmd5.md5([MACAddress, '%.1f' % OxygenValue]) == md5Key:
			computer = Computer.objects.get(mac_address=MACAddress)
			worksection = Worksection.objects.get(computer=computer)

			o1 = Oxygendata(work_section=worksection,
			                acquisition_time=datetime.datetime.now(),
			                oxygen_value=OxygenValue,
			                oxygen_sensor_value=OxygenSensorValue,
			                internal_pressure_value=InternalPressureValue)
			o1.save()
			re = 'Save Success!'
		else:
			re = 'md5 Key Error!'
	except:
		re = 'Save Failed!'
	# html = "MACAddress:%s,OxygenValue:%f,OxygenSensorValue:%f,InternalPressureValue:%f" % (MACAddress,OxygenValue,OxygenSensorValue,InternalPressureValue)

	return HttpResponse(re)


def GetLAMProcessData_Laser(request, MACAddress, LaserTime, LaserPowerValue, LaserLightpathTemperatureValue,
                            LaserLaserTemperatureValue, md5Key):
	try:
		_y, _m, _d, _hour, _min, _sec = map(int, LaserTime.split('_'))
		LaserTime = datetime.datetime(_y, _m, _d, _hour, _min, _sec)

		LaserPowerValue = float(LaserPowerValue)
		LaserLightpathTemperatureValue = float(LaserLightpathTemperatureValue)
		LaserLaserTemperatureValue = float(LaserLaserTemperatureValue)

		if checkmd5.md5([MACAddress, '%d-%d-%d' % (_d, _min, LaserPowerValue)]) == md5Key:
			computer = Computer.objects.get(mac_address=MACAddress)
			worksection = Worksection.objects.get(computer=computer)

			o1 = Laserdata(work_section=worksection,
			               acquisition_time=LaserTime,
			               laser_power=LaserPowerValue,
			               laser_lightpath_temperature=LaserLightpathTemperatureValue,
			               laser_laser_temperature=LaserLaserTemperatureValue)
			o1.save()
			re = 'Save Success!'
		else:
			re = 'md5 Key Error! %s, %s, %s, %s, %s\n' % (
				MACAddress, LaserTime, LaserPowerValue, LaserLightpathTemperatureValue, LaserLaserTemperatureValue)
	except:
		re = 'Save Failed! %s, %s, %s, %s, %s\n' % (
			MACAddress, LaserTime, LaserPowerValue, LaserLightpathTemperatureValue, LaserLaserTemperatureValue)
	return HttpResponse(re)


def PostLAMProcessData_CNCdata(request):
	def getCutImg(image, regionCoordinate):
		if not regionCoordinate:
			return None, None
		cutimageCoordinate = regionCoordinate
		IdentifyRegion_Image = image[cutimageCoordinate[1]:cutimageCoordinate[3],
		                       cutimageCoordinate[0]:cutimageCoordinate[2]]
		grayImage = cv2.cvtColor(IdentifyRegion_Image, cv2.COLOR_BGR2GRAY)
		ret2, thresh = cv2.threshold(grayImage, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
		del IdentifyRegion_Image
		del grayImage
		del cutimageCoordinate
		# gc.collect()
		return ret2, thresh

	def getCutImgCode(image, regionCoordinate):
		ret2, thresh = getCutImg(image, regionCoordinate)
		re = dHash_ndarray(thresh)
		del thresh
		# gc.collect()
		return re
	def matchDeviceCode(device):
		return device["DeviceCode"].upper() == DeviceCode.upper()
	def checkImage(image):
		if not Device:
			pass
		if_auto_exec_intr = False
		if_exec_intr = False
		if_interrupt_intr = False  # 与if_exec_intr互斥
		'''判断是否为自动界面'''
		if getCutImgCode(image, Device["IdentifyAutoRegion"]) == Device["IdentifyAutoCode"]:
			if_auto_exec_intr = True
			'''判断是否执行程序中断'''
			if getCutImgCode(image, Device["IdentifyInterruptRegion"]) == Device["IdentifyInterruptCode"]:
				if_interrupt_intr=True
			'''判断是否在执行程序'''
			if getCutImgCode(image, Device["IdentifyExecuteRegion"]) == Device["IdentifyExecuteCode"]:
				if_exec_intr = True
		return if_auto_exec_intr, if_exec_intr, if_interrupt_intr

	if request.method == 'POST':
		# 清理缓存
		lastcleanuptime = CacheOperator('CleanUpTime', True, ())
		if lastcleanuptime == None or time.time()-lastcleanuptime>600:
			# 10min
			cleanup()
			CacheOperator('CleanUpTime',False,(),time.time())

		# print(request.POST.get('macaddress', None))
		# print(request.DATA.get('data', None))
		file = request.FILES.get('file', None)
		# print(file)
		if file:
			if file.size != 0:
				# _mac_add = request.POST.get('macaddress', None)
				'''# 此处应改为现场电脑时间'''
				_acqu_time = datetime.datetime.now()
				# print('5')

				# print(request.POST.get('macaddress', None))
				# computer = Computer.objects.get(mac_address=_mac_add)
				# worksection = Worksection.objects.get(cnc_computer=computer)
				worksection = getWorksectionByCNCMacAddress(request.POST.get('macaddress', None))
				DeviceCode = worksection.code
				Device = filter(matchDeviceCode, ImageSectionInfo_dict).__next__()

				image1 = np.asarray(bytearray(file.read()), dtype='uint8')
				if image1 is None:
					logger.error('Image is None Type')
				image = cv2.imdecode(image1, cv2.IMREAD_COLOR)
				if_auto_exec_intr, if_exec_intr, if_interrupt_intr = checkImage(image)
				# image = cv2.imread(path)
				# RecognitionImage(image, DeviceCode, 'eng')
				# print('6')
				file.name = '%s %s.png' % (worksection.code, str(_acqu_time).replace(':', '')[:20])
				_timestamp = int(time.mktime(_acqu_time.timetuple()))
				_status = CNCProcessStatus(work_section=worksection,
				                           acquisition_time=_acqu_time,
			                               acquisition_timestamp = _timestamp,
				                           # screen_image = file,
				                           if_auto_exec_intr = if_auto_exec_intr,
				                           if_exec_intr = if_exec_intr,
				                           if_interrupt_intr = if_interrupt_intr,
				                           if_checked = not if_exec_intr)
				if if_exec_intr:
					# 若截图为执行状态，则保留文件，否则跳过
					_status.screen_image = file

					# 识别典型参数ZValue
					try:
						Page = filter(
							lambda page: getCutImgCode(image, page["IdentifyPageRegion"]) == page["IdentifyPageCode"],
							Device["PageInfo"]).__next__()
					except:
						# Error_Flag = True
						raise ValueError
					ret2, Img_ZValue = getCutImg(image, Page["ZValueRegion"])
					re_img = []
					_psm, _img = MakeStandardizedLineImage(Img_ZValue, re_img, Page["XYZValueType"])
					ZValue = pytesseract.image_to_string(_img, lang='eng',
					                                                    config='-c -psm %d %s' % (_psm, 'digits')).replace(' ','')
					try:
						_status.ZValue=float(ZValue)
						# 更新近期实时记录
						RealtimeRecord.Realtime_Records.addRecords(worksection.id, 'cncstatus', _timestamp, float(ZValue))

					except:
						pass
					del _img
				_status.save()
				# updateProcessDataIndexingInfo(worksection, dateint, datatype, data_id):
				updateProcessDataIndexingInfo(worksection,
				                              int(_acqu_time.strftime('%Y%m%d')),
				                              'cncstatus',
				                              _status.id)
				'''保存至实时截图路径'''
				filepath = '.' + settings.REAL_TIME_SCREEN_URL + '/' + str(worksection.code) + '.png'
				# print(filepath)
				_file = open(filepath, 'wb+')
				for chunk in file.chunks():
					_file.write(chunk)
				_file.close()
				# logger.info('Save Success!')
				# WriteLog('info','Save Success!')
				return HttpResponse('Save Success!')

		settings.logger.error('Save Failed!')
		return HttpResponse('Save Failed!')
	else:
		logger.error('NO Post Data!')
		return HttpResponse('NO Post Data!')


def PostLAMProcessData_CNCdataScreenRecognition(request):
	def refreshGlobalTempList():
		'''更新临时辅助参数,保存至数据表'''
		if item_CNCProcessStatus.id not in settings.GLOBAL_CNCProcessStatus_SendImage_Waitfor_Recive_IDlist:
			logger.debug(
				'item_.id not in Waitfor_Recive_IDlist:%d' % item_CNCProcessStatus.id)
		else:
			logger.debug(
				'remove from Waitfor_Recive_IDlist:%d' % item_CNCProcessStatus.id)
		while item_CNCProcessStatus.id in settings.GLOBAL_CNCProcessStatus_SendImage_Waitfor_Recive_IDlist:
			settings.GLOBAL_CNCProcessStatus_SendImage_Waitfor_Recive_IDlist.remove(item_CNCProcessStatus.id)
		settings.GLOBAL_CNCProcessStatus_NotRecoge_Min_ID = min(
			settings.GLOBAL_CNCProcessStatus_SendImage_Waitfor_Recive_IDlist)
		_temp = TemporaryParameter_ID.objects.get(id=2)
		_temp.item_id = settings.GLOBAL_CNCProcessStatus_NotRecoge_Min_ID
		_temp.save()
		pass

	def deleteImg(image_file_path):
		# 删除截图
		if os.path.exists(image_file_path):
			os.remove(image_file_path)
			logger.debug('Remove ScreenImg %s'%image_file_path)

	def moveImg(image_file_path, newpath):
		if os.path.exists(image_file_path):
			shutil.copy(image_file_path, newpath)

	if request.method == 'POST':
		try:
			# print(request.POST)
			item_CNCProcessStatus = CNCProcessStatus.objects.get(id=request.POST.get('CNCProcessStatus_id'))

			item_CNCProcessStatus.if_auto_exec_intr = request.POST.get('if_auto_exec_intr')
			item_CNCProcessStatus.if_exec_intr = request.POST.get('if_exec_intr')
			item_CNCProcessStatus.if_interrupt_intr = request.POST.get('if_interrupt_intr')
			try:
				item_CNCProcessStatus.program_name = request.POST.get('program_name')
			except:
				pass
			# item_CNCProcessStatus.save()

			if request.POST.get('if_exec_intr') == 'True':
				# print(request.POST.get('if_exec_intr'))
				# print(type(request.POST.get('if_exec_intr')))
				# 自动界面且在运行程序中
				if request.POST.get('XValue') is None and request.POST.get('YValue') is None and request.POST.get(
						'ZValue') is None:
					# print(request.POST)
					image_file_path = '.' + settings.MEDIA_URL + str(item_CNCProcessStatus.screen_image)
					deleteImg(image_file_path)
					refreshGlobalTempList()
					logger.error('Post Value Error!id:%d'%item_CNCProcessStatus.id)
					raise ValueError
				# print('0')
				item_CNCProcessAutoData = CNCProcessAutoData.objects.create(
					program_name=request.POST.get('ProgramName'),
					X_value=request.POST.get('XValue'),
					Y_value=request.POST.get('YValue'),
					Z_value=request.POST.get('ZValue'),
					ScanningRate_value=request.POST.get('ScanningRate'),
					SReal_value=request.POST.get('Sreal'),
					FeedRate_value=request.POST.get('FeedRate'),
					GState_value=request.POST.get('GState'),
					MState_value=request.POST.get('MState'),
				)

				item_CNCProcessAutoData.save()
				# 更新精细数据表
				RT_FineData.Realtime_FineData.add_processRecord(item_CNCProcessStatus.acquisition_timestamp,
				                                                item_CNCProcessStatus.worksection.id,
				                                                {'X_value': request.POST.get('XValue'),
				                                                 'Y_value': request.POST.get('Y_value'),
				                                                 'Z_value': request.POST.get('Z_value'),
				                                                 'ScanningRate_value': request.POST.get('ScanningRate'),
				                                                 'FeedRate_value': request.POST.get('FeedRate'),
				                                                 'program_name': request.POST.get('ProgramName')})

				item_CNCProcessStatus.autodata = item_CNCProcessAutoData
				item_CNCProcessStatus.program_name = request.POST.get('ProgramName')
				item_CNCProcessStatus.Z_value = request.POST.get('ZValue')
				item_CNCProcessStatus.check_datetime = datetime.datetime.now()

			item_CNCProcessStatus.if_checked = True
			item_CNCProcessStatus.save()

			# 更新临时辅助参数,保存至数据表
			refreshGlobalTempList()

			image_file_path = '.' + settings.MEDIA_URL + str(item_CNCProcessStatus.screen_image)
			# 移动问题截屏
			try:
				if float(request.POST.get('FeedRate')) < 100 and float(request.POST.get('Sreal')) > 100:
					moveImg(image_file_path, '.' + settings.MEDIA_BACKUP_URL)
			except:
				pass

			# 删除截图
			deleteImg(image_file_path)

			print('Save Success!')
			# print(request.POST.get('SReal'))
			return HttpResponse('Save Success!')
		except:
			print('Save Failed!')
			print(request.POST)
			return HttpResponse('Save Failed!')
	else:
		return HttpResponse('NO Post Data!')


def PostLAMProcessData_Oxygen(request):
	if request.method == 'POST':
		# 此处时间应更改为现场电脑时间
		_acqu_time = datetime.datetime.now()
		try:
			worksection = getWorksectionByDesktopMacAddress(request.POST.get('macaddress', None))
			_timestamp = int(time.mktime(_acqu_time.timetuple()))
			_oxydata = Oxygendata(work_section=worksection,
			                      acquisition_time=_acqu_time,
			                      acquisition_timestamp = _timestamp,
			                      oxygen_value=float(request.POST.get('oxygen_value', None)),
			                      oxygen_sensor_value=float(request.POST.get('oxygen_sensor_value', None)),
			                      internal_pressure_value=float(request.POST.get('internal_pressure_value', None))
			                      )
			_oxydata.save()

			# 更新近期实时记录 绘制现场操作实时曲线
			RealtimeRecord.Realtime_Records.addRecords(worksection.id, 'oxygen', _timestamp, float(request.POST.get('oxygen_value', None)))

			# updateProcessDataIndexingInfo(worksection, dateint, datetype, data_id):
			updateProcessDataIndexingInfo(worksection,
			                              int(_acqu_time.strftime('%Y%m%d')),
			                              'oxygen',
			                              _oxydata.id)

			# 更新精细数据表
			RT_FineData.Realtime_FineData.add_processRecord(_timestamp, worksection.id, {'oxygen_value':float(request.POST.get('oxygen_value', None))})
			return HttpResponse('Save Success!')
		except:
			print('Oxygen Save Failed!')
			print(request.POST)
			return HttpResponse('Save Failed!')
	else:
		return HttpResponse('NO Post Data!')




# def PostLAMProcessData_Laser(request):
# 	# def deleteLogfile(file_path):
# 	# 	# 删除激光日志
# 	# 	if os.path.exists(file_path):
# 	# 		os.remove(file_path)
#
# 	def InsertOneLaserData(record, worksection):
# 		_r = record.strip()
# 		_r = _r[2:len(_r) - 3]
# 		# matchObj = re.match(
# 		# 	r'([0-9]+)\.([0-9]+)\.([0-9]+) ([0-9]+):([0-9]+):([0-9\.]+)[ ]+([0-9\.]+)[ ]+([0-9\.]+)[ ]+([0-9\.]+)[ ]+([0-9\.]+)',
# 		# 	_r, re.M | re.I)
# 		matchObj = re.match(
# 			r'([0-9]+)\.([0-9]+)\.([0-9]+) ([0-9]+):([0-9]+):([0-9]+).([0-9]+)[ ]+([0-9\.]+)[ ]+([0-9\.]+)[ ]+([0-9\.]+)',
# 			_r, re.M | re.I)
# 		try:
# 			if matchObj:
# 				'''筛去功率为0的记录'''
# 				if float(matchObj.group(8))==0.0:
# 					return 'blank'
# 				# 14.10.17 18:28:03.265    7478    30.0    21.4     4.3
# 				_time = "%d-%d-%d %d:%d:%d.%d" % (
# 					int('20' + matchObj.group(3)), int(matchObj.group(2)), int(matchObj.group(1)),
# 					int(matchObj.group(4)),
# 					int(matchObj.group(5)), int(matchObj.group(6)),float(matchObj.group(7)))
# 				# print _time,matchObj.group(7),matchObj.group(8),matchObj.group(9)
# 				# LogText += 'LaserData:%s %s %f %f %f\n'%(worksection,_time,float(matchObj.group(7)),float(matchObj.group(8)),float(matchObj.group(9)))
# 				# WriteLog(LogText)
# 				_laserdata = Laserdata(work_section=worksection,
# 				                       acquisition_time=_time,
# 				                       acquisition_timestamp = int(time.mktime(time.strptime(_time, "%Y-%m-%d %H:%M:%S.%f"))),
# 				                       laser_power=float(matchObj.group(8)),
# 				                       laser_lightpath_temperature=float(matchObj.group(9)),
# 				                       laser_laser_temperature=float(matchObj.group(10)))
# 				_laserdata.save()
# 				# updateProcessDataIndexingInfo(worksection, dateint, datetype, data_id):
# 				updateProcessDataIndexingInfo(worksection,
# 				                              int(_time.split(' ')[0].replace('-','')),
# 				                              'laser',
# 				                              _laserdata.id)
# 				# Process_Laserdata_Date_Worksection_indexing
# 			return 'success'
# 		except:
# 			# WriteLog('debug','\tError In InsertOneLaserData : %s' % record)
# 			logger.error('Error In InsertOneLaserData : %s' % record)
# 			return 'failed'
#
# 	if request.method == 'POST':
# 		macaddress = request.POST.get('macaddress', None)
# 		try:
# 			worksection = getWorksectionByDesktopMacAddress(request.POST.get('macaddress', None))
#
# 			file = request.FILES.get('file', None)
# 			# print(file)
# 			t0=time.time()
# 			logger.info('Start Process LaserLogFile : %s %s' % (worksection.code, file.name))
# 			if file:
# 				if file.size != 0:
# 					# worksection = getWorksectionByCNCMacAddress(request.POST.get('macaddress', None))
# 					# WriteLog('debug','Read LaserLogFile : %s %s' % (worksection.code, file.name))
# 					logger.info('Read LaserLogFile : %s %s' % (worksection.code, file.name))
# 					file.open()
# 					RecordsList = file.readlines()
# 					file.close()
#
# 					for record in RecordsList:
# 						try:
# 							# laserdata = {}
# 							# WriteLog('debug','Read Record:%s' % record)
# 							re = InsertOneLaserData(str(record), worksection)
# 							if re not in ('success', 'blank'):
# 								return HttpResponse('Save Failed!')
# 							# print('Save Success!')
# 						except:
# 							print('LaserData Save Failed!')
# 							# WriteLog('debug','LaserData Save Failed!')
# 							# WriteLog('Read Record Error : %s' % record)
# 							logger.error('Read Record Error : %s' % record)
# 							pass
#
# 			logger.info('Finish Process LaserLogFile : %s %s Costs %d' % (worksection.code, file.name,time.time()-t0))
# 			return HttpResponse('Save Success!')
# 		except:
# 			print('LaserData Save Failed!')
# 			# WriteLog('debug','LaserData Save Failed!')
# 			logger.error('LaserData Posted from %s Save Failed!'%macaddress)
# 			# print(request.POST)
# 			# print(request.FILES.get('file', None))
# 			return HttpResponse('Save Failed!')
# 	else:
# 		return HttpResponse('NO Post Data!')


def PostLAMProcessData_Laser(request):
	# def deleteLogfile(file_path):
	# 	# 删除激光日志
	# 	if os.path.exists(file_path):
	# 		os.remove(file_path)

	def InsertOneLaserData(record, worksection):
		_r = record.strip()
		# print(_r)
		_r = _r[2:len(_r) - 3]
		_rlist = _r.split(' ')
		while '' in _rlist:
			_rlist.remove('')
		logger.debug(_rlist)
		# matchObj = re.match(
		# 	r'([0-9]+)\.([0-9]+)\.([0-9]+) ([0-9]+):([0-9]+):([0-9\.]+)[ ]+([0-9\.]+)[ ]+([0-9\.]+)[ ]+([0-9\.]+)[ ]+([0-9\.]+)',
		# 	_r, re.M | re.I)
		# matchObj = re.match(
		# 	r'([0-9]+)\.([0-9]+)\.([0-9]+) ([0-9]+):([0-9]+):([0-9]+).([0-9]+)[ ]+([0-9\.]+)[ ]+([0-9\.]+)[ ]+([0-9\.]+)',
		# 	_r, re.M | re.I)
		try:
			# logger.info(matchObj)
			# if matchObj:
			if len(_rlist)>=5:
				islaserdata=True
				try:
					temp_data=float(_rlist[2])
					temp_data=float(_rlist[3])
					temp_data=float(_rlist[4])
				except:
					islaserdata=False
				logger.debug(islaserdata)
				if not islaserdata:
					return 'blank'
				# print(matchObj)
				'''筛去功率为0的记录'''
				# if float(matchObj.group(8))<20.0:
				# 	return 'blank'
				# # 14.10.17 18:28:03.265    7478    30.0    21.4     4.3
				# _time = "%d-%d-%d %d:%d:%d.%d" % (
				# 	int('20' + matchObj.group(3)), int(matchObj.group(2)), int(matchObj.group(1)),
				# 	int(matchObj.group(4)),
				# 	int(matchObj.group(5)), int(matchObj.group(6)'''
				if float(_rlist[2])<20.0:
					return 'blank'
				# 14.10.17 18:28:03.265    7478    30.0    21.4     4.3
				# _rlist=['06.12.19', '08:39:56.746', '0', '29.9', '21.9']
				_day, _month, _year=map(lambda x:int(x), _rlist[0].split('.'))
				# _hour, _minute, _second = map(lambda x:float(x) if '.' in x else int(x), _rlist[1].split(':'))
				_time = "20%d-%d-%d %s" % (_year, _month, _day, _rlist[1])
				logger.debug(_time)
				_timestamp=int(time.mktime(time.strptime(_time, "%Y-%m-%d %H:%M:%S.%f")))
				_laserdata = Laserdata(work_section=worksection,
				                       acquisition_time=_time,
				                       acquisition_timestamp = _timestamp,
				                       laser_power=float(_rlist[2]),
				                       laser_lightpath_temperature=float(_rlist[3]),
				                       laser_laser_temperature=float(_rlist[4]))
				_laserdata.save()

				# 更新近期实时记录
				RealtimeRecord.Realtime_Records.addRecords(worksection.id, 'laser', _timestamp, float(_rlist[2]))

				# 更新精细数据表
				RT_FineData.Realtime_FineData.add_processRecord(_timestamp, worksection.id, {'laser_power': float(_rlist[2])})

				# logger.debug('laser_id:%d' % _laserdata.id)
				# logger.debug('timeint:%d' % int(_time.split(' ')[0].replace('-','')))
				# updateProcessDataIndexingInfo(worksection, dateint, datetype, data_id):
				updateProcessDataIndexingInfo(worksection,
				                              datetime.datetime(int('20%d'%_year), _month, _day).strftime('%Y%m%d'),
				                              # int(_time.splsit(' ')[0].replace('-','')),
				                              'laser',
				                              _laserdata.id)
				# Process_Laserdata_Date_Worksection_indexing
				# print('laser success')
			return 'success'
		except:
			# WriteLog('debug','\tError In InsertOneLaserData : %s' % record)
			logger.error('Error In InsertOneLaserData : %s' % record)
			return 'failed'

	if request.method == 'POST':
		macaddress = request.POST.get('macaddress', None)
		try:
			worksection = getWorksectionByDesktopMacAddress(request.POST.get('macaddress', None))
			file = request.FILES.get('file', None)
			# print(file)
			t0=time.time()
			logger.debug('Start Process LaserLogFile : %s %s' % (worksection.code, file.name))
			if file:
				if file.size != 0:
					# worksection = getWorksectionByCNCMacAddress(request.POST.get('macaddress', None))
					# WriteLog('debug','Read LaserLogFile : %s %s' % (worksection.code, file.name))
					logger.debug('Read LaserLogFile : %s %s' % (worksection.code, file.name))
					file.open()
					RecordsList = file.readlines()
					file.close()

					for record in RecordsList:
						try:
							re = InsertOneLaserData(str(record), worksection)
							if re not in ('success', 'blank'):
								return HttpResponse('Save Failed!')
							# print('Save Success!')
						except:
							print('LaserData Save Failed!')
							# WriteLog('debug','LaserData Save Failed!')
							# WriteLog('Read Record Error : %s' % record)
							logger.error('Read Record Error : %s' % record)
							pass

			logger.debug('Finish Process LaserLogFile : %s %s Costs %d' % (worksection.code, file.name,time.time()-t0))
			return HttpResponse('Save Success!')
		except:
			print('LaserData Save Failed!')
			# WriteLog('debug','LaserData Save Failed!')
			logger.error('LaserData Posted from %s Save Failed!'%macaddress)
			# print(request.POST)
			# print(request.FILES.get('file', None))
			return HttpResponse('Save Failed!')
	else:
		return HttpResponse('NO Post Data!')



def lamprocessmission_CutRecords_by_Time(request):
	t1=time.time()
	# 如果不是POST方法访问
	save_success = None
	if request.method != 'POST':
		# 创建一个空表单在页面显示
		_form_inst = LAMProcessMission_TimeCutRecordsForm()
	else:
		# 否则为POST方式
		# request.POST方法，将会获取到表单中我们输入的数据
		# --首先判断是否已存在该项timecut
		mission_id = int(request.POST['process_mission'])
		mission = LAMProcessMission.objects.get(id=mission_id)

		_PostData = request.POST.copy()
		start_datetime = datetime.datetime.strptime(_PostData['process_start_time'], "%Y-%m-%dT%H:%M:%S")
		finish_datetime = datetime.datetime.strptime(_PostData['process_finish_time'], "%Y-%m-%dT%H:%M:%S")
		# _form_inst.data['process_start_time'] = datetime.datetime.strptime(_PostData['process_start_time'], "%Y-%m-%dT%H:%M:%S")
		# _form_inst.data['process_finish_time'] = datetime.datetime.strptime(_PostData['process_finish_time'], "%Y-%m-%dT%H:%M:%S")

		start_DT_str = _PostData['process_start_time'].replace('T', ' ')
		finish_DT_str = _PostData['process_finish_time'].replace('T', ' ')
		# _form_inst.data['process_start_time'] = _PostData['process_start_time'].replace('T', ' ')
		# _form_inst.data['process_finish_time'] = _PostData['process_finish_time'].replace('T', ' ')

		# 检测日期是否合法
		try:
			start_timestamp = int(time.mktime(start_datetime.timetuple()))
			finish_timestamp = int(time.mktime(finish_datetime.timetuple()))


			worksection = mission.work_section
			# 获取各项数据的最大最小数据id
			with connection.cursor() as cursor:
				# cursor.execute("UPDATE bar SET foo = 1 WHERE baz = %s", [self.baz])
				cursor.execute(
					"SELECT max(id),min(id) FROM lamdataserver.lamprocessdata_oxygendata where work_section_id = %d and acquisition_timestamp >= %d and acquisition_timestamp <= %d;" % (
					worksection.id, start_timestamp, finish_timestamp))
				row = cursor.fetchall()
				oxygen_maxid = row[0][0]
				oxygen_minid = row[0][1]
				t2 = time.time()
				cursor.execute(
					"SELECT max(id),min(id) FROM lamdataserver.lamprocessdata_laserdata where work_section_id = %d and acquisition_timestamp >= %d and acquisition_timestamp <= %d;" % (
					worksection.id, start_timestamp, finish_timestamp))
				row = cursor.fetchall()
				laser_maxid = row[0][0]
				laser_minid = row[0][1]
				t3=time.time()
				cursor.execute(
					"SELECT max(id),min(id) FROM lamdataserver.lamprocessdata_cncprocessstatus where work_section_id = %d and acquisition_timestamp >= %d and acquisition_timestamp <= %d;" % (
						worksection.id, start_timestamp, finish_timestamp))
				row = cursor.fetchall()
				cnc_maxid = row[0][0]
				cnc_minid = row[0][1]
				print(t2-t1, t3-t2, time.time()-t3)
				# 4.492816925048828 11.877208232879639 24.164589881896973
				# 3.5282106399536133 9.010584831237793 23.99515962600708
				# print(oxygen_minid, oxygen_maxid, laser_minid, laser_maxid, cnc_minid, cnc_maxid)
				'''更新Process_Mission_timecut'''
				if_mission_exists = False
				try:
					# ----若已存在，则更改
					_model_inst = Process_Mission_timecut.objects.get(process_mission=mission)
					if_mission_exists = True
				except:
					# ----若不存在，则新建
					_model_inst = Process_Mission_timecut(process_mission=mission,
					                                      process_start_time=start_DT_str,
					                                      process_finish_time = finish_DT_str,
					                                      laserdata_start_recordid = oxygen_minid,
					                                      laserdata_finish_recordid = oxygen_maxid,
					                                      oxygendata_start_recordid = laser_minid,
					                                      oxygendata_finish_recordid = laser_maxid,
					                                      cncstatusdata_start_recordid = cnc_minid,
					                                      cncstatusdata_finish_recordid = cnc_maxid
					                                      )
					_model_inst.save()
				if if_mission_exists:
					# _model_inst.process_start_time = start_DT_str
					_model_inst.process_start_time = start_datetime
					# _model_inst.process_finish_time = finish_DT_str
					_model_inst.process_finish_time = finish_datetime
					_model_inst.laserdata_start_recordid = oxygen_minid
					_model_inst.laserdata_finish_recordid = oxygen_maxid
					_model_inst.oxygendata_start_recordid = laser_minid
					_model_inst.oxygendata_finish_recordid = laser_maxid
					_model_inst.cncstatusdata_start_recordid = cnc_minid
					_model_inst.cncstatusdata_finish_recordid = cnc_maxid
					_model_inst.save()

			'''更新任务基本表LAMProcessMission'''
			mission.completion_date = datetime.date.today()
			mission.save()
			save_success = 'True'
		except:
			save_success = 'False'

		_form_inst = LAMProcessMission_TimeCutRecordsForm(request.POST)
			# _model_inst.save()
			# _form_inst = LAMProcessMission_TimeCutRecordsForm(request.POST.copy())
			# https://www.cnblogs.com/SunQi-Tony/p/9985616.html
	# 保存成功，使用redirect()跳转到指定页面
	# return redirect('/LAMProcessData/EditBasicInfomation/Workshop/')
	# return HttpResponseRedirect(reverse('/LAMProcessData/EditBasicInfomation/Workshop/', args=[111, 222]))
	# return HttpResponseRedirect(reverse('/LAMProcessData/EditBasicInfomation/Workshop/', kwargs={'success': 'True'}))
	# return render(request, 'EditForm_Workshop.html', {'form': form})
	# print(save_success)
	# print(time.time()-t1)
	templateFileName = 'LAMProcessMission_CutRecords_by_Time.html'
	color = {
		'oxygen_markLine_color': "#8A0808",
		'laser_markLine_color': "#5882FA",
	}
	return render(request, templateFileName,
	              {'form': _form_inst,
	               'operate': '激光成形采集数据划分',
	               'save_success': save_success,
	               'Common_URL': Common_URL,
	               'color':ECharts_Color,
	               'Back_URL':'.'})

# 成形工段现场操作
# 设定任务起止
# 观察成形参数状态记录情况
def lamprocess_worksection_operate(request, WorksectionID):
	def getForm():
		_form_inst = LAMProcess_Worksection_OperateForm()
		_form_inst.setMissionQueryset(_worksection.id)
		if_onwork = _form_inst.refresh_by_currentmission(_worksection.id)
		if if_onwork:
			submit_text = '终止当前任务'
		else:
			if if_onwork==False:
				submit_text = '开始一个任务'
			else:
				submit_text = '当前无任务'
		return _form_inst,submit_text
	def selectRecordID_Start(type, WorksectionID, _start_timestamp):
		if type=='oxygen':
			tablename = 'lamdataserver.lamprocessdata_oxygendata'
		elif type == 'laser':
			tablename = 'lamdataserver.lamprocessdata_laserdata'
		elif type == 'cncstatus':
			tablename = 'lamdataserver.lamprocessdata_cncprocessstatus'

		with connection.cursor() as cursor:
			cursor.execute(
				"SELECT min(id) FROM %s where work_section_id = %d and acquisition_timestamp >= %d;" % (
					tablename, WorksectionID, _start_timestamp))
			row = cursor.fetchall()
			_start_recordid = row[0][0]
			if not _start_recordid:
				cursor.execute(
					"SELECT max(id) FROM %s where work_section_id = %d and acquisition_timestamp <= %d;" % (
						tablename, WorksectionID, _start_timestamp))
				row = cursor.fetchall()
				_start_recordid = row[0][0]
		return _start_recordid

	def selectRecordID_Finish(type, WorksectionID, _start_record_id, _finish_timestamp):
		if type=='oxygen':
			tablename = 'lamdataserver.lamprocessdata_oxygendata'
		elif type == 'laser':
			tablename = 'lamdataserver.lamprocessdata_laserdata'
		elif type == 'cncstatus':
			tablename = 'lamdataserver.lamprocessdata_cncprocessstatus'

		with connection.cursor() as cursor:
			cursor.execute(
				"SELECT max(id) FROM %s where work_section_id = %d and id >= %d and acquisition_timestamp <= %d;" % (
					tablename, WorksectionID, _start_record_id, _finish_timestamp))
			row = cursor.fetchall()
			_finish_recordid = row[0][0]
		return _finish_recordid

	save_success = None
	WorksectionID = int(WorksectionID)
	_worksection = Worksection.objects.get(id = WorksectionID)

	recordLastTime = {}
	recordLastTime['laser'] = CacheOperator('recordLastTime',True,(_worksection.id, 'laser'))
	recordLastTime['oxygen'] = CacheOperator('recordLastTime', True, (_worksection.id, 'oxygen'))
	recordLastTime['cncstatus'] = CacheOperator('recordLastTime', True, (_worksection.id, 'cncstatus'))

	if request.method != 'POST':
		# 创建一个空表单在页面显示
		# _form_inst = LAMProcess_Worksection_OperateForm(_worksection.id)
		# _form_inst = LAMProcess_Worksection_OperateForm(worksection = _worksection)



		# _form_inst = LAMProcess_Worksection_OperateForm()
		# _form_inst.setMissionQueryset(_worksection.id)
		# if_onwork = _form_inst.refresh_by_currentmission(_worksection.id)
		# if if_onwork:
		# 	submit_text='终止当前任务'
		# else:
		# 	submit_text='开始一个任务'
		save_success = None
		_form_inst, submit_text = getForm()
	else:
		# 否则为POST方式
		# 如果是post,instance=article当前数据填充表单，并用data=request.POST获取到表单里的内容
		crtmission_obj = Worksection_Current_LAMProcessMission.objects.get(work_section=WorksectionID)
		if crtmission_obj.if_onwork:
			try:
				# 原本正在执行，则Post后终止执行，记录当前时间
				crtmission_obj.if_onwork = False
				crtmission_obj.save()
				_mission_obj = crtmission_obj.process_mission
				_mission_attr_obj = Process_Mission_timecut.objects.get(process_mission=crtmission_obj.process_mission)
				# 任务结束的时间及其时间戳
				_finish_time = datetime.datetime.now()
				_finish_timestamp=int(time.mktime(_finish_time.timetuple()))
				# 查询任务开始的各项参数id
				_oxygendata_start_recordid=_mission_attr_obj.oxygendata_start_recordid
				_laserdata_start_recordid=_mission_attr_obj.laserdata_start_recordid
				_cncstatusdata_start_recordid=_mission_attr_obj.cncstatusdata_start_recordid
				if not _oxygendata_start_recordid:
					_oxygendata_start_recordid = 1
				if not _laserdata_start_recordid:
					_laserdata_start_recordid = 1
				if not _cncstatusdata_start_recordid:
					_cncstatusdata_start_recordid = 1
				# 找到各项过程记录终止的id
				_oxygendata_finish_recordid = selectRecordID_Finish('oxygen', WorksectionID, _oxygendata_start_recordid, _finish_timestamp)
				_laserdata_finish_recordid = selectRecordID_Finish('laser', WorksectionID, _laserdata_start_recordid, _finish_timestamp)
				_cncstatusdata_finish_recordid = selectRecordID_Finish('cncstatus', WorksectionID, _cncstatusdata_start_recordid, _finish_timestamp)

				# 任务实例属性
				# 设置结束时间
				_mission_attr_obj.process_finish_time = _finish_time
				# 记录各项过程参数的终止id
				_mission_attr_obj.laserdata_finish_recordid = _laserdata_finish_recordid
				_mission_attr_obj.oxygendata_finish_recordid = _oxygendata_finish_recordid
				_mission_attr_obj.cncstatusdata_finish_recordid = _cncstatusdata_finish_recordid
				_mission_attr_obj.save()

				# 任务实例设置完成日期，
				_mission_obj.completion_date = datetime.date.today()
				_mission_obj.save()
				save_success = True
			except:
				save_success = False

		else:
			try:
				# 记录中未进行任务，post后开启此任务
				_mission_id = request.POST['process_mission']
				crtmission_obj.process_mission = LAMProcessMission.objects.get(id=_mission_id)
				crtmission_obj.if_onwork = True
				crtmission_obj.save()

				# 任务结束的时间及其时间戳
				_start_time = datetime.datetime.now()
				_start_timestamp = int(time.mktime(_start_time.timetuple()))

				# 在Process_Mission_timecut中更新
				_mission_attr_obj = Process_Mission_timecut.objects.get(process_mission=crtmission_obj.process_mission)

				# 找到各项过程记录起始的id
				_oxygendata_start_recordid = selectRecordID_Start('oxygen', WorksectionID, _start_timestamp)
				_laserdata_start_recordid = selectRecordID_Start('laser', WorksectionID, _start_timestamp)
				_cncstatusdata_start_recordid = selectRecordID_Start('cncstatus', WorksectionID, _start_timestamp)

				# 设置开始时间
				_mission_attr_obj.process_start_time = _start_time
				# 记录各项过程参数的终止id
				_mission_attr_obj.laserdata_start_recordid = _laserdata_start_recordid
				_mission_attr_obj.oxygendata_start_recordid = _oxygendata_start_recordid
				_mission_attr_obj.cncstatusdata_start_recordid = _cncstatusdata_start_recordid
				_mission_attr_obj.save()

				save_success=True
			except:
				save_success=False
			pass
		_form_inst, submit_text = getForm()

	templateFileName = 'LAMProcess_Worksection_Operate.html'

	return render(request, templateFileName,
	              {'form': _form_inst,
	               'operate': '激光成形工段%s现场操作'%_worksection.code,
	               'worksection_id': WorksectionID,
	               'save_success': save_success,
	               'Common_URL': Common_URL,
	               'Back_URL': '.',
	               'recordLastTime':recordLastTime,
	               'color':ECharts_Color,
	               'submit_text':submit_text})


# 操作页面
@login_required
def OperateData_lamprocessparameters(request):
	def initTableData(Model, form_display_fields=None):
		try:
			all_entries = Model.objects.filter((Q(available=True)))
			_modelfilednames = [f.attname for f in Model._meta.fields]
			# attlist = [f.attname for f in Model._meta.fields]

			all_entries_list = []
			for i in all_entries:
				_dict = {}
				for att in form_display_fields:
					_dict[att] = str(i.__getattribute__(att.replace('_id', '')))
					# if att in _modelfilednames:
					# 	# 替换_id, 从而获得外键实例的名称
					# 	_dict[att] = str(i.__getattribute__(att.replace('_id', '')))
					# else:
					# 	_dict[att] = list(map(str, list(i.__getattribute__(att).all())))
				all_entries_list.append(_dict)
			# print(all_entries_list)
			return all_entries_list
		except:
			pass
	_form_inst = LAMProcessParameters_Browse()
	all_entries_list = initTableData(LAMProcessParameters, ['id','name', 'comment'])
	all_serial_entries_list = initTableData(LAM_TechInst_Serial, ['id',
	                                                              'technique_instruction',
	                                                              'serial_number',
	                                                              'serial_worktype',
	                                                              'serial_note',
	                                                              'process_parameter'])
	# try:
	# 	all_entries = LAMProcessParameters.objects.filter((Q(available=True)))
	# 	_modelfilednames = [f.attname for f in LAMProcessParameters._meta.fields]
	# 	attlist = [f.attname for f in LAMProcessParameters._meta.fields]
	#
	# 	all_serial_entries = LAM_TechInst_Serial.objects.filter((Q(available=True)))
	# 	_modelfilednames_serial = [f.attname for f in LAM_TechInst_Serial._meta.fields]
	# 	attlist_serial = [f.attname for f in LAM_TechInst_Serial._meta.fields]
	# except:
	# 	pass
	#
	# all_entries_list = []
	# for i in all_entries:
	# 	_dict = {}
	# 	for att in attlist:
	# 		if att == 'available' and 'available' not in list(_form_inst.fields):
	# 			continue
	# 		# _dict[att] = list(map(str, list(i.__getattribute__(att).all())))
	# 		if att in _modelfilednames:
	# 			# 替换_id, 从而获得外键实例的名称
	# 			_dict[att] = str(i.__getattribute__(att.replace('_id', '')))
	# 		else:
	# 			_dict[att] = list(map(str, list(i.__getattribute__(att).all())))
	# 	all_entries_list.append(_dict)
	#
	# all_serial_entries_list = []
	# for i in all_serial_entries:
	# 	_dict = {}
	# 	for att in attlist_serial:
	# 		# 不显示available字段
	# 		if att == 'available':
	# 			continue
	# 		# _dict[att] = list(map(str, list(i.__getattribute__(att).all())))
	# 		if att in _modelfilednames_serial:
	# 			# 替换_id, 从而获得外键实例的名称
	# 			_dict[att] = str(i.__getattribute__(att.replace('_id', '')))
	# 		else:
	# 			_dict[att] = list(map(str, list(i.__getattribute__(att).all())))
	# 	all_serial_entries_list.append(_dict)

	# print(all_serial_entries_list)
	return render(request, 'OperateData_LAMProcessParameters.html',
	              {'form': _form_inst,
	               'operate': '',
	               'all_entries': all_entries_list,
	               'all_entries_serial':all_serial_entries_list,
	               # 'save_success': save_success,
	               'Common_URL': Common_URL,
	               'Back_URL': Common_URL['Back_URL_lamprocessparameters']})

def del_lamprocessparameters(request):
	return BasicInformation_Delete(request, Model=LAMProcessParameters, modelname='lamprocessparameters')

# 新建参数包 弹出子窗
@login_required
def new_lamprocessparameters(request):
	save_success = None
	if request.method != 'POST':
		# 创建一个空表单在页面显示
		_form_inst = LAMProcessParameters_Edit()
	else:
		# 否则为POST方式
		# request.POST方法，将会获取到表单中我们输入的数据
		_form_inst = LAMProcessParameters_Edit(request.POST)
		# 验证其合法性，使用is_valid()方法
		_isValid = _form_inst.is_valid()
		if _isValid:
			# func(_form_inst, MissionItemID)
			_form_inst.save()
			save_success = 'True'
			_form_inst = LAMProcessParameters_Edit(request.POST)
		else:
			save_success = 'False'

	return render(request, "SubWindow_SimpleForm.html",
	              {'form': _form_inst,
	               'operate': 'new',
	               'save_success': save_success,
	               'Common_URL': Common_URL,
	               })


# 编辑模板 弹出子窗
@login_required
def edit_Template_SubWindow(request, Model, ModelForm, item_id, back_url, Tabletype='simple'):
	save_success = None
	# 查询到指定的数据
	try:
		_model_inst = Model.objects.get(id=item_id)
	except:
		messages.success(request, "未找到此条记录！")
		return redirect(back_url)

	if request.method != 'POST':
		# 如果不是post,创建一个表单，并用instance=article当前数据填充表单
		_form_inst = ModelForm(instance=_model_inst)
		_form_inst.itemid = item_id
	else:
		# 如果是post,instance=article当前数据填充表单，并用data=request.POST获取到表单里的内容
		_form_inst = ModelForm(instance=_model_inst, data=request.POST)
		try:
			try:
				_isValid = _form_inst.is_valid_custom()
			except:
				_isValid = _form_inst.is_valid()
			if _isValid:  # 验证
				_form_inst.save()  # 保存
				_form_inst.itemid = item_id
				save_success = 'True'
			else:
				# _form_inst.error_messages = _form_inst.errors.get_json_data()
				save_success = 'False'
		except:
			save_success = 'False'
			# _form_inst.error_messages = _form_inst.errors.get_json_data()
	if Tabletype=='simple':
		templateFileName= "SubWindow_SimpleForm.html"
	elif Tabletype=='withlabel':
		templateFileName = "SubWindow_SimpleForm_with_label.html"

	return render(request, templateFileName,
	              {'form': _form_inst,
	               'operate': 'edit',
	               'save_success': save_success,
	               'Common_URL': Common_URL,
	               })

# 编辑参数包 弹出子窗
@login_required
def edit_lamprocessparameters(request, ProcessParameterItemID):

	return edit_Template_SubWindow(request,
	                               LAMProcessParameters,
	                               LAMProcessParameters_Edit,
	                               ProcessParameterItemID,
	                               Common_URL['Back_URL_lamprocessparameters'],
	                               'simple')

	# item_id = ProcessParameterItemID
	# save_success = None
	# # 查询到指定的数据
	# try:
	# 	_model_inst = LAMProcessParameters.objects.get(id=item_id)
	# except:
	# 	messages.success(request, "未找到此条记录！")
	# 	return redirect(Common_URL['Back_URL_lamprocessparameters'])
	# if request.method != 'POST':
	# 	# 如果不是post,创建一个表单，并用instance=article当前数据填充表单
	# 	_form_inst = LAMProcessParameters_Edit(instance=_model_inst)
	# 	_form_inst.itemid = item_id
	# else:
	# 	# 如果是post,instance=article当前数据填充表单，并用data=request.POST获取到表单里的内容
	# 	_form_inst = LAMProcessParameters_Edit(instance=_model_inst, data=request.POST)
	# 	try:
	# 		_form_inst.save()  # 保存
	#
	# 		_form_inst.itemid = item_id
	#
	# 		_isValid = _form_inst.is_valid()
	# 		if _isValid:  # 验证
	# 			save_success = 'True'
	# 		else:
	# 			_form_inst.error_messages = _form_inst.errors.get_json_data()
	# 			save_success = 'False'
	# 	except:
	# 		save_success = 'False'
	# 		_form_inst.error_messages = _form_inst.errors.get_json_data()
	#
	#
	# return render(request, "SubWindow_SimpleForm.html",
	#               {'form': _form_inst,
	#                'operate': 'edit',
	#                'save_success': save_success,
	#                'Common_URL': Common_URL,
	#                })

# 新建条件单元 弹出子窗
@login_required
def new_lamprocessparameterConditionalCell(request, ProcessParameterItemID):
	# print(ProcessParameterItemID)
	save_success = None
	if request.method != 'POST':
		# 创建一个空表单在页面显示
		_form_inst = LAMProcessConditionalCell_Edit(ProcessParameterID=ProcessParameterItemID)
		# _form_inst = LAMProcessConditionalCell_Edit()
	else:
		# 否则为POST方式
		# request.POST方法，将会获取到表单中我们输入的数据
		_form_inst = LAMProcessConditionalCell_Edit(request.POST,ProcessParameterID=ProcessParameterItemID)
		# 验证其合法性，使用is_valid()方法
		_isValid = _form_inst.is_valid_custom()
		if _isValid:
			_conditional_cell = LAMProcessParameterConditionalCell.objects.create(
				level=_form_inst.cleaned_data['level'],
				precondition=_form_inst.cleaned_data['precondition'],
				expression=_form_inst.cleaned_data['expression'],
				comment=_form_inst.cleaned_data['comment']
			)
			_conditional_cell.save()
			_ProcessParameter = LAMProcessParameters.objects.get(id=ProcessParameterItemID)
			_ProcessParameter.conditional_cell.add(_conditional_cell)
			save_success = 'True'
			_form_inst = LAMProcessConditionalCell_Edit(request.POST,ProcessParameterID=ProcessParameterItemID)
		else:
			save_success = 'False'

	return render(request, "SubWindow_SimpleForm_with_label.html",
	              {'form': _form_inst,
	               'operate': 'new',
	               'save_success': save_success,
	               'Common_URL': Common_URL,
	               })

# 编辑条件单元 弹出子窗
@login_required
def edit_lamprocessparameterConditionalCell(request, ConditionalCellItemID):
	return edit_Template_SubWindow(request,
	                               LAMProcessParameterConditionalCell,
	                               LAMProcessConditionalCell_Edit,
	                               ConditionalCellItemID,
	                               Common_URL['Back_URL_lamprocessparameters'],
	                               'withlabel')

# 保存适用的工序
@login_required
def save_lamprocessparameterTechInstSerial(request):
	# 此处有问题
	ProcessParameterID = int(request.POST.get('id'))
	Post_TechInst_Serial_List = request.POST.get('techinst_serial_list').split(',')
	if '' in Post_TechInst_Serial_List:
		Post_TechInst_Serial_List.remove('')
	Post_TechInst_Serial_List = list(set(map(int, Post_TechInst_Serial_List)))
	print(Post_TechInst_Serial_List)
	qset = (
			Q(available=True) &
			Q(process_parameter=ProcessParameterID)
	)
	target_ProcessParameter = LAMProcessParameters.objects.get(id=ProcessParameterID)
	Old_TechInst_Serial_inst_List = LAM_TechInst_Serial.objects.filter(qset)
	Old_TechInst_Serial_list = [i.id for i in Old_TechInst_Serial_inst_List]
	# 新增的工序ID列表
	select_on_id_list = [i for i in Post_TechInst_Serial_List if i not in Old_TechInst_Serial_list]
	# 取消选择的工序ID列表
	select_off_id_list = [i for i in Old_TechInst_Serial_list if i not in Post_TechInst_Serial_List]

	try:
		for id in select_on_id_list:
			_serial = LAM_TechInst_Serial.objects.get(id=id)
			_serial.process_parameter = target_ProcessParameter
			_serial.save()
		for id in select_off_id_list:
			_serial = LAM_TechInst_Serial.objects.get(id=id)
			_serial.process_parameter = None
			_serial.save()
		save_success = 'True'
	except:
		save_success = 'False'

	re_dict = {
		'save_success':save_success,
	}
	# print('end save_lamprocessparameterTechInstSerial')
	html = json.dumps(re_dict, ensure_ascii=False)
	return HttpResponse(html, content_type='application/json')


# 接收1条记录时，更新index表
def UpdateIndexing_OneRecord_Oxygen(date_int, record_id):



	pass
# 更新数据库内空的时间戳  CNCProcessStatus  Laserdata  Oxygendata
def UpdateRecordTimeStamp(request):
	t1 = time.time()
	# d = datetime.datetime(2019, 11, 9)
	# x = int(d.strftime('%Y%m%d')) - d0

	# timeArray = time.strptime("2019-11-29 20:35:00", "%Y-%m-%d %H:%M:%S")
	# timestamp = int(time.mktime(timeArray))

	qset = (
			Q(acquisition_timestamp__isnull=True)
	)
	num_per_page = 2000

	print('start Oxygendata')
	# Oxygendata
	# oxygendata_list = Oxygendata.objects.filter(qset).distinct()
	# Length_statuslist = oxygendata_list.count()
	# Sum_i = int((Length_statuslist/num_per_page)+1)
	# for Current_i in range(Sum_i):
	# 	print('Oxygendata: %d / %d'%(Current_i, Sum_i))
	# 	_list = oxygendata_list[Current_i*num_per_page:(Current_i+1)*num_per_page]
	# 	for oxy in _list:
	# 		acq_time = oxy.acquisition_time
	# 		# print(time.mktime(acq_time.timetuple()))
	# 		oxy.acquisition_timestamp = int(time.mktime(acq_time.timetuple()))
	# 		oxy.save()
	MaxID = Oxygendata.objects.all().count()
	Sum_i = int((MaxID / num_per_page) + 1)
	for Current_i in range(Sum_i):
		t2 = time.time()
		print('Oxygendata: %d / %d' % (Current_i, Sum_i))
		qset = (
				Q(id__gte=Current_i * num_per_page) &
				Q(id__lt=(Current_i + 1) * num_per_page) &
				Q(acquisition_timestamp__isnull=True)
		)
		_list = Oxygendata.objects.filter(qset).distinct()
		for status in _list:
			acq_time = status.acquisition_time
			status.acquisition_timestamp = int(time.mktime(acq_time.timetuple()))
			status.save()
		print(time.time() - t2)

	#
	print('start Laserdata')
	# Laserdata
	# Laserdata_list = Laserdata.objects.filter(qset).distinct()
	# Length_statuslist = Laserdata_list.count()
	# Sum_i = int((Length_statuslist/num_per_page)+1)
	# for Current_i in range(Sum_i):
	# 	print('Laserdata: %d / %d'%(Current_i, Sum_i))
	# 	_list = Laserdata_list[Current_i*num_per_page:(Current_i+1)*num_per_page]
	# 	for laser in _list:
	# 		acq_time = laser.acquisition_time
	# 		laser.acquisition_timestamp = int(time.mktime(acq_time.timetuple()))
	# 		laser.save()
	MaxID = Laserdata.objects.all().count()
	Sum_i = int((MaxID / num_per_page) + 1)
	for Current_i in range(Sum_i):
		t2 = time.time()
		print('Laserdata: %d / %d' % (Current_i, Sum_i))
		qset = (
				Q(id__gte=Current_i * num_per_page) &
				Q(id__lt=(Current_i + 1) * num_per_page) &
				Q(acquisition_timestamp__isnull=True)
		)
		_list = Laserdata.objects.filter(qset).distinct()
		for status in _list:
			acq_time = status.acquisition_time
			status.acquisition_timestamp = int(time.mktime(acq_time.timetuple()))
			status.save()
		print(time.time() - t2)

	print('start CNCProcessStatus')
	# CNCProcessStatus
	MaxID = CNCProcessStatus.objects.all().count()
	Sum_i = int((MaxID / num_per_page) + 1)
	for Current_i in range(Sum_i):
		t2 = time.time()
		print('CNCProcessStatus: %d / %d' % (Current_i, Sum_i))
		qset = (
			Q(id__gte=Current_i * num_per_page) &
			Q(id__lt=(Current_i + 1) * num_per_page) &
			Q(acquisition_timestamp__isnull=True)
		)
		_list = CNCProcessStatus.objects.filter(qset).distinct()
		for status in _list:
			acq_time = status.acquisition_time
			status.acquisition_timestamp = int(time.mktime(acq_time.timetuple()))
			status.save()
		print(time.time() - t2)


	html = "<html><body>UpdateRecordTimeStamp Cost Time %f.</body></html>" % (time.time() - t1)
	return HttpResponse(html)


# 更新数据库CNCProcessStatus表中的Z_Value、ProgramName信息
def UpdateRecordCNCProcessStatus(request):
	t1 = time.time()
	# qset = (
	# 	Q(autodata__isnull=False)&
	# 	Q(Z_value__isnull=True)
	# )
	print('start CNCProcessStatus')

	MaxID = CNCProcessStatus.objects.all().count()
	num_per_page = 2000
	Sum_i = int((MaxID / num_per_page) + 1)

	# CNCstatus_list = CNCProcessStatus.objects.filter(qset).distinct()
	# Length_statuslist = CNCstatus_list.count()	#
	# Sum_i = int((Length_statuslist/num_per_page)+1)

	for Current_i in range(Sum_i):
		print('UpdateRecordCNCProcessStatus: %d / %d'%(Current_i, Sum_i))
		qset = (
				Q(id__gte=Current_i * num_per_page) &
				Q(id__lt=(Current_i + 1) * num_per_page) &
				Q(autodata__isnull=False) &
				Q(Z_value__isnull=True)
		)
		_list = CNCProcessStatus.objects.filter(qset).distinct()
		# _list = CNCstatus_list[Current_i*num_per_page:(Current_i+1)*num_per_page]

		for status in _list:
			try:
				auto_data_obj = status.autodata
				status.program_name = auto_data_obj.program_name
				status.Z_value = auto_data_obj.Z_value
				status.save()
			except:
				print('Error in UpdateRecordCNCProcessStatus,id=%d'%status.id)

	html = "<html><body>UpdateRecordCNCProcessStatus Cost Time %f.</body></html>" % (time.time() - t1)
	return HttpResponse(html)

# 更新数据库Process_Oxygendata_Date_Worksection_indexing
# @lock("global")
def UpdateOxygendata_Date_Worksection_indexing(request):
	global GLOBAL_UPDATE_INDEXINGTABLE_FLAG_OXYGEN
	if settings.GLOBAL_UPDATE_INDEXINGTABLE_FLAG_OXYGEN:
		return HttpResponse("<html><body>已有运行，自动退出</body></html>")
	else:
		settings.GLOBAL_UPDATE_INDEXINGTABLE_FLAG_OXYGEN=True
	t1 = time.time()
	start_Oxygendata_id = TemporaryParameter_ID.objects.get(id=3).item_id

	# Key: worksection_id     Value: list of index_date_int
	# exist_Oxygen_index_date_Dict = {}
	# Key: worksection_id-dateint    Value:  [oxygendata_start_id, oxygendata_finish_id, id]
	exist_Oxygen_index_date_with_RecID_Dict = {}
	num_per_page = 200

	# 整理出Process_Oxygendata_Date_Worksection_indexing表中已有的索引
	_ws_exist_indexing = Process_Oxygendata_Date_Worksection_indexing.objects.filter()
	length_list = _ws_exist_indexing.count()
	Sum_i = int((length_list / num_per_page) + 1)
	for Current_i in range(Sum_i):
		_list = _ws_exist_indexing[Current_i * num_per_page:(Current_i + 1) * num_per_page]
		for _date in _list:
			exist_Oxygen_index_date_with_RecID_Dict['%d-%d' % (_date.work_section.id, _date.index_date_int)] = [_date.data_start_id, _date.data_finish_id, _date.id]

	# 对未整理的记录建立索引
	qset = (
		Q(id__gte=start_Oxygendata_id)
	)
	oxygendata_list = Oxygendata.objects.filter(qset).distinct()
	length_list = oxygendata_list.count()
	Sum_i = int((length_list / num_per_page) + 1)
	for Current_i in range(Sum_i):
		print('UpdateOxygendata_Date_Worksection_indexing: %d / %d'%(Current_i, Sum_i))
		_list = oxygendata_list[Current_i * num_per_page:(Current_i + 1) * num_per_page]
		for _oxydata in _list:
			_record_wc_id = _oxydata.work_section.id
			_record_date_int = int(_oxydata.acquisition_time.strftime('%Y%m%d'))
			_key = '%d-%d' % (_record_wc_id, _record_date_int)
			# if _record_date_int not in exist_Oxygen_index_date_Dict[_record_wc_id]:
			if _key not in exist_Oxygen_index_date_with_RecID_Dict:
				# 增加日期索引
				_index = Process_Oxygendata_Date_Worksection_indexing(work_section=Worksection.objects.get(id=_record_wc_id),
				                                                      index_date=_oxydata.acquisition_time.strftime('%Y-%m-%d'),
				                                                      index_date_int=_record_date_int,
				                                                      data_start_id=_oxydata.id,
				                                                      data_finish_id=_oxydata.id)
				_index.save()

				# exist_Oxygen_index_date_Dict[_record_wc_id].append(_record_date_int)
				exist_Oxygen_index_date_with_RecID_Dict[_key] = [_oxydata.id,_oxydata.id, _index.id]
			else:
				# _index = Process_Oxygendata_Date_Worksection_indexing.objects.get(id = exist_Oxygen_index_date_with_RecID_Dict[_key][2])
				if _oxydata.id < exist_Oxygen_index_date_with_RecID_Dict[_key][0]:
					exist_Oxygen_index_date_with_RecID_Dict[_key][0] = _oxydata.id
				elif _oxydata.id > exist_Oxygen_index_date_with_RecID_Dict[_key][1]:
					exist_Oxygen_index_date_with_RecID_Dict[_key][1] = _oxydata.id
			start_Oxygendata_id += 1

		# print(exist_Oxygen_index_date_with_RecID_Dict)
		# 每页保存1次数据
		for _key in exist_Oxygen_index_date_with_RecID_Dict:
			_index_id = exist_Oxygen_index_date_with_RecID_Dict[_key][2]
			_temp = Process_Oxygendata_Date_Worksection_indexing.objects.get(id = _index_id)
			_temp.data_start_id = exist_Oxygen_index_date_with_RecID_Dict[_key][0]
			_temp.data_finish_id = exist_Oxygen_index_date_with_RecID_Dict[_key][1]
			_temp.save()
		_temp = TemporaryParameter_ID.objects.get(id=3)
		_temp.item_id = start_Oxygendata_id
		_temp.save()
	settings.GLOBAL_UPDATE_INDEXINGTABLE_FLAG_OXYGEN = False
	html = "<html><body>UpdateOxygendata_Date_Worksection_indexing Cost Time %f.</body></html>" % (time.time() - t1)
	return HttpResponse(html)

# 更新数据库Process_Laserdata_Date_Worksection_indexing
# @lock("global")
def UpdateLaserdata_Date_Worksection_indexing(request):
	global GLOBAL_UPDATE_INDEXINGTABLE_FLAG_LASER
	if settings.GLOBAL_UPDATE_INDEXINGTABLE_FLAG_LASER:
		return HttpResponse("<html><body>已有运行，自动退出</body></html>")
	else:
		settings.GLOBAL_UPDATE_INDEXINGTABLE_FLAG_LASER=True
	t1 = time.time()
	start_Laserdata_id = TemporaryParameter_ID.objects.get(id=4).item_id

	# Key: worksection_id     Value: list of index_date_int
	# exist_Oxygen_index_date_Dict = {}
	# Key: worksection_id-dateint    Value:  [oxygendata_start_id, oxygendata_finish_id, id]
	exist_Laser_index_date_with_RecID_Dict = {}
	num_per_page = 200

	# 整理出Process_Oxygendata_Date_Worksection_indexing表中已有的索引
	_ws_exist_indexing = Process_Laserdata_Date_Worksection_indexing.objects.filter()
	length_list = _ws_exist_indexing.count()
	Sum_i = int((length_list / num_per_page) + 1)
	for Current_i in range(Sum_i):
		_list = _ws_exist_indexing[Current_i * num_per_page:(Current_i + 1) * num_per_page]
		for _date in _list:
			exist_Laser_index_date_with_RecID_Dict['%d-%d' % (_date.work_section.id, _date.index_date_int)] = [_date.data_start_id, _date.data_finish_id, _date.id]


	# 对未整理的记录建立索引
	qset = (
		Q(id__gte=start_Laserdata_id)
	)
	laserdata_list = Laserdata.objects.filter(qset).distinct()
	length_list = laserdata_list.count()
	Sum_i = int((length_list / num_per_page) + 1)
	for Current_i in range(Sum_i):
		print('UpdateLaserdata_Date_Worksection_indexing: %d / %d'%(Current_i, Sum_i))
		_list = laserdata_list[Current_i * num_per_page:(Current_i + 1) * num_per_page]
		for _laserdata in _list:
			_record_wc_id = _laserdata.work_section.id
			_record_date_int = int(_laserdata.acquisition_time.strftime('%Y%m%d'))
			_key = '%d-%d' % (_record_wc_id, _record_date_int)
			# if _record_date_int not in exist_Oxygen_index_date_Dict[_record_wc_id]:
			if _key not in exist_Laser_index_date_with_RecID_Dict:
				# 增加日期索引
				_index = Process_Laserdata_Date_Worksection_indexing(work_section=Worksection.objects.get(id=_record_wc_id),
				                                                index_date=_laserdata.acquisition_time.strftime('%Y-%m-%d'),
				                                                index_date_int=_record_date_int,
				                                                data_start_id=_laserdata.id,
				                                                data_finish_id=_laserdata.id)
				_index.save()

				# exist_Oxygen_index_date_Dict[_record_wc_id].append(_record_date_int)
				exist_Laser_index_date_with_RecID_Dict[_key] = [_laserdata.id,_laserdata.id, _index.id]
			else:
				# _index = Process_Oxygendata_Date_Worksection_indexing.objects.get(id = exist_Oxygen_index_date_with_RecID_Dict[_key][2])
				if _laserdata.id < exist_Laser_index_date_with_RecID_Dict[_key][0]:
					exist_Laser_index_date_with_RecID_Dict[_key][0] = _laserdata.id
				elif _laserdata.id > exist_Laser_index_date_with_RecID_Dict[_key][1]:
					exist_Laser_index_date_with_RecID_Dict[_key][1] = _laserdata.id
			start_Laserdata_id += 1

		# print(exist_Laser_index_date_with_RecID_Dict)
		# 每页保存1次数据
		for _key in exist_Laser_index_date_with_RecID_Dict:
			_index_id = exist_Laser_index_date_with_RecID_Dict[_key][2]
			_temp = Process_Laserdata_Date_Worksection_indexing.objects.get(id = _index_id)
			_temp.data_start_id = exist_Laser_index_date_with_RecID_Dict[_key][0]
			_temp.data_finish_id = exist_Laser_index_date_with_RecID_Dict[_key][1]
			_temp.save()
		_temp = TemporaryParameter_ID.objects.get(id=4)
		_temp.item_id = start_Laserdata_id
		_temp.save()
	settings.GLOBAL_UPDATE_INDEXINGTABLE_FLAG_LASER = False
	html = "<html><body>UpdateLaserdata_Date_Worksection_indexing Cost Time %f.</body></html>" % (time.time() - t1)
	return HttpResponse(html)

# 更新数据库Process_CNCStatusdata_Date_Worksection_indexing
# @lock("global")
def UpdateCNCStatusdata_Date_Worksection_indexing(request):
	global GLOBAL_UPDATE_INDEXINGTABLE_FLAG_CNCSTATUS
	if settings.GLOBAL_UPDATE_INDEXINGTABLE_FLAG_CNCSTATUS:
		return HttpResponse("<html><body>已有运行，自动退出</body></html>")
	else:
		settings.GLOBAL_UPDATE_INDEXINGTABLE_FLAG_CNCSTATUS=True
	t1 = time.time()
	start_CNCStatusdata_id = TemporaryParameter_ID.objects.get(id=5).item_id

	# Key: worksection_id     Value: list of index_date_int
	# exist_Oxygen_index_date_Dict = {}
	# Key: worksection_id-dateint    Value:  [oxygendata_start_id, oxygendata_finish_id, id]
	exist_CNCStatus_index_date_with_RecID_Dict = {}
	num_per_page = 200

	# 整理出Process_Oxygendata_Date_Worksection_indexing表中已有的索引
	_ws_exist_indexing = Process_CNCStatusdata_Date_Worksection_indexing.objects.filter()
	length_list = _ws_exist_indexing.count()
	Sum_i = int((length_list / num_per_page) + 1)
	for Current_i in range(Sum_i):
		_list = _ws_exist_indexing[Current_i * num_per_page:(Current_i + 1) * num_per_page]
		for _date in _list:
			exist_CNCStatus_index_date_with_RecID_Dict['%d-%d' % (_date.work_section.id, _date.index_date_int)] = [_date.data_start_id, _date.data_finish_id, _date.id]


	# 对未整理的记录建立索引
	qset = (
		Q(id__gte=start_CNCStatusdata_id)
	)
	CNCdata_list = CNCProcessStatus.objects.filter(qset).distinct()
	length_list = CNCdata_list.count()
	Sum_i = int((length_list / num_per_page) + 1)
	for Current_i in range(Sum_i):
		print('UpdateCNCStatusdata_Date_Worksection_indexing: %d / %d'%(Current_i, Sum_i))
		_list = CNCdata_list[Current_i * num_per_page:(Current_i + 1) * num_per_page]
		for _CNCdata in _list:
			_record_wc_id = _CNCdata.work_section.id
			_record_date_int = int(_CNCdata.acquisition_time.strftime('%Y%m%d'))
			_key = '%d-%d' % (_record_wc_id, _record_date_int)
			# if _record_date_int not in exist_Oxygen_index_date_Dict[_record_wc_id]:
			if _key not in exist_CNCStatus_index_date_with_RecID_Dict:
				# 增加日期索引
				_index = Process_CNCStatusdata_Date_Worksection_indexing(work_section=Worksection.objects.get(id=_record_wc_id),
				                                                index_date=_CNCdata.acquisition_time.strftime('%Y-%m-%d'),
				                                                index_date_int=_record_date_int,
				                                                data_start_id=_CNCdata.id,
				                                                data_finish_id=_CNCdata.id)
				_index.save()
				# print('New Process_CNCStatusdata_Date_Worksection_indexing: _key=%s'%_key)
				# exist_Oxygen_index_date_Dict[_record_wc_id].append(_record_date_int)
				exist_CNCStatus_index_date_with_RecID_Dict[_key] = [_CNCdata.id,_CNCdata.id, _index.id]
			else:
				# _index = Process_Oxygendata_Date_Worksection_indexing.objects.get(id = exist_Oxygen_index_date_with_RecID_Dict[_key][2])
				if _CNCdata.id < exist_CNCStatus_index_date_with_RecID_Dict[_key][0]:
					exist_CNCStatus_index_date_with_RecID_Dict[_key][0] = _CNCdata.id
				elif _CNCdata.id > exist_CNCStatus_index_date_with_RecID_Dict[_key][1]:
					exist_CNCStatus_index_date_with_RecID_Dict[_key][1] = _CNCdata.id

			start_CNCStatusdata_id += 1

		# print(exist_CNCStatus_index_date_with_RecID_Dict)
		# 每页保存1次数据
		for _key in exist_CNCStatus_index_date_with_RecID_Dict:
			_index_id = exist_CNCStatus_index_date_with_RecID_Dict[_key][2]
			_temp = Process_CNCStatusdata_Date_Worksection_indexing.objects.get(id = _index_id)
			_temp.data_start_id = exist_CNCStatus_index_date_with_RecID_Dict[_key][0]
			_temp.data_finish_id = exist_CNCStatus_index_date_with_RecID_Dict[_key][1]
			_temp.save()
		_temp = TemporaryParameter_ID.objects.get(id=5)
		_temp.item_id = start_CNCStatusdata_id
		_temp.save()
	settings.GLOBAL_UPDATE_INDEXINGTABLE_FLAG_CNCSTATUS = False
	html = "<html><body>UpdateCNCStatusdata_Date_Worksection_indexing Cost Time %f.</body></html>" % (time.time() - t1)
	return HttpResponse(html)

# @cache_page(60 * 15)
def DrawData_Oxygen(request):
	class BADRecord():
		BADRecordList = []

		# def __init__(self,startdate,enddate,errortype):
		#     self.startdate = startdate
		#     self.enddate = enddate
		#     self.errortype = errortype
		@staticmethod
		def AddErrorRecord(startdate, enddate, errortype):
			if len(BADRecord.BADRecordList) == 0:
				BADRecord.BADRecordList.append([startdate, enddate, errortype])
			elif BADRecord.BADRecordList[-1][2] == errortype and BADRecord.BADRecordList[-1][1] == startdate:
				BADRecord.BADRecordList[-1][1] = enddate
			else:
				BADRecord.BADRecordList.append([startdate, enddate, errortype])

	worksection_list = Worksection.objects.all()
	query_worksection_code = request.GET.get('work_section_code', '')
	query_startDate = request.GET.get('startDate',
	                                  (datetime.datetime.now() - datetime.timedelta(days=7)).strftime('%Y-%m-%dT23:59'))
	query_endDate = request.GET.get('endDate', time.strftime('%Y-%m-%dT23:59', time.localtime()))
	query_startDate = [query_startDate, '1949-10-01T00:00'][query_startDate == '']
	query_endDate = [query_endDate, time.strftime('%Y-%m-%dT23:59', time.localtime())][query_endDate == '']
	query_secondsdelta = int(request.GET.get('seconds_delta', 60))
	query_setValue = int(request.GET.get('oxy_set_value', 80))
	# print query_setValue
	# print query_worksection_code
	# badOxyList = []
	dict_content = {'RecordDateList': [],
	                'RecordOxyvalueList': [],
	                'PanelTitle': '激光增材制造过程实测参数记录',
	                'txtFigTitle': '氧含量记录曲线',
	                'txtDataName': '氧含量(PPM)',
	                'worksectionList': worksection_list,
	                'worksectionCode': query_worksection_code,
	                'startDate': query_startDate,
	                'endDate': query_endDate,
	                'seconds_delta': query_secondsdelta,
	                'oxy_set_value': query_setValue,
	                'badOxyList': BADRecord.BADRecordList
	                }

	if query_worksection_code:
		qset = (
				Q(work_section=Worksection.objects.get(code=query_worksection_code)) &
				Q(acquisition_time__gte=query_startDate) &
				Q(acquisition_time__lte=query_endDate)
		)
		# oxygendata_list = Oxygendata.objects.all()
		oxygendata_list = Oxygendata.objects.filter(qset).distinct()

		# oxygendata_list = Oxygendata.objects.filter(mac_address = query_mac and )

		# RecordDateList = map(lambda oxy:str(oxy.acquisition_time),oxygendata_list)
		# RecordOxyvalueList = map(lambda oxy:int(oxy.oxygen_value),oxygendata_list)
		# lambda record1,record2:int((datetime.datetime.strptime(record2,"%Y-%m-%d %H:%M:%S")-datetime.datetime.strptime(record1,"%Y-%m-%d %H:%M:%S")).total_seconds())

		class tempoxy():
			def __init__(self, t, v):
				self.acquisition_time = t
				self.oxygen_value = v

		_predate = None
		_newOxyList = []

		for oxy in oxygendata_list:
			_nowdate = oxy.acquisition_time
			if _predate != None:
				if int((_nowdate - _predate).total_seconds()) > query_secondsdelta:
					_newOxyList.append(tempoxy(_predate + datetime.timedelta(seconds=1), '-'))
					_newOxyList.append(tempoxy(_nowdate - datetime.timedelta(seconds=1), '-'))
					BADRecord.AddErrorRecord(_predate, _nowdate, '数据丢失')
				# if len(badOxyList)==0:
				#     badOxyList.append([_predate,_nowdate,1])
				# elif badOxyList[-1][2]==1 and badOxyList[-1][1] == _predate:
				#     badOxyList[-1][1] = _nowdate

				elif oxy.oxygen_value > query_setValue:
					# badOxyList.append([_predate, _nowdate, 2])
					BADRecord.AddErrorRecord(_predate, _nowdate, '氧含量超出限定值')
			_predate = _nowdate
			_newOxyList.append(oxy)

		# RecordDateList = map(lambda oxy: str(oxy.acquisition_time), oxygendata_list)
		# RecordOxyvalueList = map(lambda oxy: int(oxy.oxygen_value), oxygendata_list)
		RecordDateList = map(lambda oxy: str(oxy.acquisition_time), _newOxyList)
		RecordOxyvalueList = map(
			lambda oxy: int(oxy.oxygen_value) if type(oxy.oxygen_value) == type(float) else str(oxy.oxygen_value),
			_newOxyList)

		dict_content['RecordDateList'] = RecordDateList
		dict_content['RecordOxyvalueList'] = RecordOxyvalueList
		dict_content['txtFigTitle'] = dict_content['txtFigTitle'] + str(query_worksection_code)
		dict_content['badOxyList'] = BADRecord.BADRecordList

	# print RecordDateList,RecordOxyvalueList

	# print dict_content
	# return render_to_response('OxygenData.html', dict_content)
	return render(request, 'OxygenData.html', dict_content)


# 将已存在的数据复制到FineData表中
def Update_ExistingData_to_FineData(request):
	print('start Update_ExistingData_to_FineData...')
	t1=time.time()

	# 遍历氧含量数据
	# all_data_list = Oxygendata.objects.all()
	# count_i=0
	# count_sum = all_data_list.count()
	# for _data in all_data_list:
	# 	count_i += 1
	# 	if count_i % 1000 == 0:
	# 		print('Oxygen Data : %d/%d=%.3f' % (count_i, count_sum, count_i / count_sum))
	# 	# 更新精细数据表
	# 	RT_FineData.Realtime_FineData.add_processRecord(int(time.mktime(_data.acquisition_time.timetuple())), _data.work_section.id,
	# 	                                                {'oxygen_value': _data.oxygen_value})

	# 遍历激光数据
	all_data_list = Laserdata.objects.all()
	count_i=0
	count_sum = all_data_list.count()
	for _data in all_data_list:
		count_i+=1
		if count_i%1000==0:
			print('Laser Data : %d/%d=%.3f'%(count_i, count_sum, count_i/count_sum))
		if count_i<106000:
			continue
		# 更新精细数据表
		RT_FineData.Realtime_FineData.add_processRecord(int(time.mktime(_data.acquisition_time.timetuple())),
		                                                _data.work_section.id,
		                                                {'laser_power': _data.laser_power})

	# 遍历机床运动数据
	all_data_list = CNCProcessStatus.objects.all()
	count_i = 0
	count_sum = all_data_list.count()
	for _data in all_data_list:
		count_i += 1
		if count_i % 1000 == 0:
			print('CNCProcessStatus Data : %d/%d=%.3f' % (count_i, count_sum, count_i / count_sum))
		# 更新精细数据表
		try:
			_autodata = _data.autodata
			RT_FineData.Realtime_FineData.add_processRecord(int(time.mktime(_data.acquisition_time.timetuple())),
			                                                _data.work_section.id,
			                                                {'X_value': _autodata.X_value,
			                                                 'Y_value': _autodata.Y_value,
			                                                 'Z_value': _autodata.Z_value,
			                                                 'ScanningRate_value': _autodata.ScanningRate_value,
			                                                 'FeedRate_value': _autodata.FeedRate_value,
			                                                 'program_name': _autodata.program_name,
			                                                 })
		except:
			pass


	print('end Update_ExistingData_to_FineData...')
	html = "<html><body>Update_ExistingData_to_FineData Cost Time %f.</body></html>" % (time.time() - t1)
	return HttpResponse(html)

# 将FineData表中datetime字段根据timestamp计算
def Update_ExistingFineData_datetime(request):
	'''可在mysql workbench中以SQL更新

		UPDATE lamdataserver.lamprocessdata_process_realtime_finedata_by_worksectionid_1
		SET acquisition_datetime=FROM_UNIXTIME(acquisition_timestamp,'%Y-%m-%d %H:%i:%s')
		where id>4669200;

	'''
	def update_Finedate(_model):
		t1 = time.time()
		for _finedata in Process_Realtime_FineData_By_WorkSectionID_1.objects.all().iterator():
			_finedata.acquisition_datetime =datetime.datetime.fromtimestamp(_finedata.acquisition_timestamp)
			_finedata.save()
		print('%s:%.2f'%(_model, time.time()-t1))
	print('start Update_ExistingFineData_datetime...')

	update_Finedate(Process_Realtime_FineData_By_WorkSectionID_1)
	update_Finedate(Process_Realtime_FineData_By_WorkSectionID_2)
	update_Finedate(Process_Realtime_FineData_By_WorkSectionID_3)
	update_Finedate(Process_Realtime_FineData_By_WorkSectionID_4)
	update_Finedate(Process_Realtime_FineData_By_WorkSectionID_5)
	update_Finedate(Process_Realtime_FineData_By_WorkSectionID_6)

	# all_data_list = Laserdata.objects.all()
	# all_data_list = Laserdata.objects.get(id=1)
	# all_data_list = Process_Realtime_FineData_By_WorkSectionID_1.objects.filter(id=1).update(acquisition_datetime=datetime.datetime.fromtimestamp(int(F('acquisition_timestamp'))))
	# all_data_list = Process_Realtime_FineData_By_WorkSectionID_1.objects.filter(id=1).update(acquisition_datetime=datetime.datetime.fromtimestamp(int(F('acquisition_timestamp'))))
	# all_data_list = Process_Realtime_FineData_By_WorkSectionID_1.objects.all().update(acquisition_datetime=datetime.datetime.fromtimestamp(F('acquisition_timestamp')))
	# from django.db.models import date_format
	# Process_Realtime_FineData_By_WorkSectionID_1.objects.update(acquisition_datetime=date_format(F('acquisition_timestamp'),'%Y-%m-%d %H:%i:%s'))
	print('end Update_ExistingFineData_datetime...')
	html = "<html><body>Update_ExistingFineData_datetime Cost Time %f.</body></html>" % (time.time() - t1)
	return HttpResponse(html)

'''清空缓存'''
cache.clear()

'''启动定时任务'''
'''pip install apscheduler==2.1.2'''
sched = Scheduler()
# 每天执行1次
# @sched.interval_schedule(days=1,start_date=datetime.datetime.fromtimestamp(float(time.time())+20))
@sched.interval_schedule(days=1, start_date=datetime.datetime.fromtimestamp(float(time.time())+10))
def regulartime_task():
	RT_FineData.Realtime_FineData.init_Tomorrow_rows()

logger = logging.getLogger()
# @sched.interval_schedule(days=1, start_date=datetime.datetime.now())
@sched.cron_schedule(hour=0)
def OpenLog():
	global logger
	logger = logging.getLogger()
	logger.setLevel(logging.DEBUG)
	time_handler = logging.handlers.TimedRotatingFileHandler('.' + MEDIA_LOGFLE_URL + 'LAMDataServer%s.log'%datetime.date.today().strftime('%Y-%m-%d'),
	                                                         when='midnight', interval=1, backupCount=0)
	fmt = '%(asctime)s - %(funcName)s - %(lineno)s - %(levelname)s - %(message)s'
	formatter = logging.Formatter(fmt)
	time_handler.setFormatter(formatter)
	logger.addHandler(time_handler)

OpenLog()
# sched.add_job(RT_FineData.Realtime_FineData.init_Tomorrow_rows, 'interval', days=1)
# sched.add_job(RT_FineData.Realtime_FineData.init_Tomorrow_rows, 'cron', hour=0)
# print('before add_job')
# sched.add_job(RT_FineData.Realtime_FineData.init_Tomorrow_rows, 'interval', days=1, start_date=datetime.datetime.fromtimestamp(float(time.time())+10))
# print('after add_job')
sched.start()
# print('after start')
# print('end views.py')