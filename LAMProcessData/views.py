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
from django.http import HttpResponse, Http404, FileResponse
from django_lock import lock
from django.template import loader, RequestContext
from django.template import Context, Template
# from django.template.defaulttags import register
from django.views.decorators.cache import cache_page
from django.core.cache import cache
import numpy as np
import cv2
import gc
from LAMProcessData.models import *
from LAMProcessData.forms import *
# from models import *
# from forms import *
# from LAMProcessData.permission import check_permission
from ImageRecognition import ImageRecognition
from PracticalTools import SShapeBreak, ReadPDF
from django.views.generic import View
import os
from tempfile import TemporaryFile, NamedTemporaryFile
import shutil
import datetime
import time
import re
# from lamdataserver.settings import logger
import logging
from logging.handlers import TimedRotatingFileHandler
from lamdataserver.settings import ImageSectionInfo_dict, MEDIA_LOGFLE_URL, APP_PATH
# from ImageRecognition.ImageRecognition import cleanup, MakeStandardizedLineImage
import tempfile
import pytesseract
import LAMProcessData.realtime_records as RealtimeRecord
import LAMProcessData.process_realtime_finedata as RT_FineData
from apscheduler.scheduler import Scheduler
import json
import xlrd
# import LAMProcessData.checkmd5
# import sys
# import lamdataserver.settings.DEBUG as DEBUG
# import LAMProcessData.realtime_records

# sys.path.append("..")
# import ImageRecognition.ImageRecognition as IMR

# logger = logging.getLogger(__name__)



# print('START views.py')

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
		'ProgressBarValue_PracticalTools_SShapeBreak_By_GUID'    由SShapeBreak中的CacheOperator进行赋值
		'ProgressBarValue_PracticalTools_BreakBlockResumption_By_GUID'    由views.PracticalTools_BreakBlockResumption进行赋值
		'ProgressBarValue_New_LAMTechInstSerial_UploadPDFFile_By_TechInstID'    由views.***进行赋值
		'ProgressBarValue_Update_ExistingData_to_FineData'                      由view.Update_ExistingData_to_FineData进行赋值
		'ProgressBarValue_Update_ExistingData_to_FineData_text'                      由view.Update_ExistingData_to_FineData进行赋值
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
	elif operateType == 'ProgressBarValue_PracticalTools_SShapeBreak_By_GUID':
		GUID = ParamSet
		key = 'PBR_Tools_SSBK_GUID%s' % (GUID)
		if not ifget:
			cache.set(key, data)
		else:
			revalue = cache.get(key)
	elif operateType == 'ProgressBarValue_PracticalTools_BreakBlockResumption_By_GUID':
		GUID = ParamSet
		key = 'PBR_Tools_BrkBlkRUM_GUID%s' % (GUID)
		if not ifget:
			cache.set(key, data)
		else:
			revalue = cache.get(key)
	elif operateType == 'ProgressBarValue_New_LAMTechInstSerial_UploadPDFFile_By_TechInstID':
		TechInstID = ParamSet
		key = 'PBR_NewTechInstByPDF_TechInstID%s' % (TechInstID)
		if not ifget:
			cache.set(key, data)
		else:
			revalue = cache.get(key)
	elif operateType == 'ProgressBarValue_Update_ExistingData_to_FineData':
		datatype = ParamSet
		key = 'PBR_UpDate_FineData_%s' % (datatype)
		if not ifget:
			cache.set(key, data)
		else:
			revalue = cache.get(key)
	elif operateType == 'ProgressBarValue_Update_ExistingData_to_FineData_text':
		datatype = ParamSet
		key = 'PBR_UpDate_FineData_Text_%s' % (datatype)
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
	gc.collect()
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
	user = request.user
	print(user.get_all_permissions())
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

# 系统操作
Common_URL['UpdateRecordToFineData'] = Common_URL['ProcessPath'] + 'LAMProcessData/UpdateRecordToFineData/'
# Common_URL['UpdateRecordToFineData'] = Common_URL['ProcessPath'] + 'QueryData/ProgressBarValue/Update_ExistingData_to_FineData'
Common_URL['Query_UpdateRecordToFineData'] = Common_URL['ProcessPath'] +  'QueryData/ProgressBarValue/Update_ExistingData_to_FineData/'
Common_URL['Query_DefectPicture'] = Common_URL['ProcessPath'] +  'QueryData/NonDestructiveTest/DefectPicture_by_Defect/'
Common_URL['Query_DingDingRecordPicture'] = Common_URL['ProcessPath'] +  'QueryData/AnalyseLAMProcess/DingDingRecordPictures_by_ID/'

# 基本信息
Common_URL['EditBasicInfomation'] = Common_URL['ProcessPath'] + 'EditBasicInfomation/'

# 生产记录
Common_URL['ProcessRecords'] = Common_URL['ProcessPath'] + 'ProcessRecords/'
# 检验记录
Common_URL['InspectionRecords'] = Common_URL['ProcessPath'] + 'InspectionRecords/'
# 过程分析
Common_URL['AnalyseLAMProcess'] = Common_URL['ProcessPath'] + 'AnalyseLAMProcess/'
# 编程小工具
Common_URL['PracticalTools'] = Common_URL['ProcessPath'] + 'PracticalTools/'
# 新窗口浏览图片
Common_URL['NewWindow_URL_UTDefectPicturesViewer'] = Common_URL['ProcessPath'] + 'PicturesViewer/NonDestructiveTest/UTDefect/'
Common_URL['NewWindow_URL_RTDefectPicturesViewer'] = Common_URL['ProcessPath'] + 'PicturesViewer/NonDestructiveTest/RTDefect/'
Common_URL['NewWindow_URL_PTDefectPicturesViewer'] = Common_URL['ProcessPath'] + 'PicturesViewer/NonDestructiveTest/PTDefect/'
Common_URL['NewWindow_URL_MTDefectPicturesViewer'] = Common_URL['ProcessPath'] + 'PicturesViewer/NonDestructiveTest/MTDefect/'
Common_URL['NewWindow_URL_AllUTDefectPicturesViewer'] = Common_URL['ProcessPath'] + 'PicturesViewer/NonDestructiveTest/AllUTDefect/'
Common_URL['NewWindow_URL_AllRTDefectPicturesViewer'] = Common_URL['ProcessPath'] + 'PicturesViewer/NonDestructiveTest/AllRTDefect/'
Common_URL['NewWindow_URL_AllPTDefectPicturesViewer'] = Common_URL['ProcessPath'] + 'PicturesViewer/NonDestructiveTest/AllPTDefect/'
Common_URL['NewWindow_URL_AllMTDefectPicturesViewer'] = Common_URL['ProcessPath'] + 'PicturesViewer/NonDestructiveTest/AllMTDefect/'

# 基本信息--分支
Common_URL['Back_URL_workshop'] = Common_URL['EditBasicInfomation'] + 'Workshop/'
Common_URL['Back_URL_worksection'] = Common_URL['EditBasicInfomation'] + 'Worksection/'
Common_URL['Back_URL_computer'] = Common_URL['EditBasicInfomation'] + 'Computer/'
Common_URL['Back_URL_cncstatuscategory'] = Common_URL['EditBasicInfomation'] + 'CNCStatusCategory/'

Common_URL['Back_URL_productcategory'] = Common_URL['EditBasicInfomation'] + 'ProductCategory/'
Common_URL['Back_URL_lamproductsubarea'] = Common_URL['EditBasicInfomation'] + 'LAMProductSubarea/'
Common_URL['Back_URL_lammaterial'] = Common_URL['EditBasicInfomation'] + 'LAMMaterial/'
Common_URL['Back_URL_rawstockcategory'] = Common_URL['EditBasicInfomation'] + 'RawStockCategory/'
Common_URL['Back_URL_lamproductionworktype'] = Common_URL['EditBasicInfomation'] + 'LAMProductionWorkType/'
Common_URL['Back_URL_lamtechniqueinstruction'] = Common_URL['EditBasicInfomation'] + 'LAMTechniqueInstruction/'
Common_URL['Back_URL_lamprocessparameters'] = Common_URL['EditBasicInfomation'] + 'LAMProcessParameters/'

Common_URL['Back_URL_lamtechinstserial'] = Common_URL['EditBasicInfomation'] + 'LAMTechInstSerial/'
Common_URL['Back_URL_lamtechinstserial_pdf'] = Common_URL['EditBasicInfomation'] + 'New_LAMTechInstSerial_By_PDF/'
Common_URL['Back_URL_lamtechinstserial_uploadpdf'] = Common_URL['Back_URL_lamtechinstserial_pdf'] + 'UploadFile/'
Common_URL['Back_URL_lamtechinstserial_savepdf'] = Common_URL['Back_URL_lamtechinstserial_pdf'] + 'SavePDF/'
Common_URL['Back_URL_chicharacters'] = Common_URL['EditBasicInfomation'] + 'Chi_Characters/'
# Common_URL['Back_URL_lamprodcate_techinst'] = Common_URL['EditBasicInfomation'] + 'LAMProdCate_TechInst/'
Common_URL['Back_URL_samplingposition'] = Common_URL['EditBasicInfomation'] + 'SamplingPosition/'
Common_URL['Back_URL_samplingdirection'] = Common_URL['EditBasicInfomation'] + 'SamplingDirection/'
Common_URL['Back_URL_heattreatmentstate'] = Common_URL['EditBasicInfomation'] + 'HeatTreatmentState/'
Common_URL['Back_URL_machiningstate'] = Common_URL['EditBasicInfomation'] + 'MachiningState/'
Common_URL['Back_URL_physicochemicaltest_mission_Product'] = Common_URL['InspectionRecords'] + 'PhysicochemicalTest/Product/'
Common_URL['Back_URL_physicochemicaltest_mission_RawStock'] = Common_URL['InspectionRecords'] + 'PhysicochemicalTest/RawStock/'
Common_URL['Back_URL_nondestructivetest_mission_Product'] = Common_URL['InspectionRecords'] + 'NonDestructiveTest/Product/'
Common_URL['Back_URL_nondestructivetest_mission_RawStock'] = Common_URL['InspectionRecords'] + 'NonDestructiveTest/RawStock/'

# 子窗
Common_URL['SubWindow_URL_LAMProcessParameters_Add'] = Common_URL['Back_URL_lamprocessparameters'] + 'AddLAMParameter/'
Common_URL['SubWindow_URL_LAMProcessParameters_Edit'] = Common_URL['Back_URL_lamprocessparameters'] + 'EditLAMParameter/'
Common_URL['SubWindow_URL_LAMProcessParametersConditionalCell_Add'] = Common_URL['Back_URL_lamprocessparameters'] + 'AddConditionalCell/'
Common_URL['SubWindow_URL_LAMProcessParametersConditionalCell_Edit'] = Common_URL['Back_URL_lamprocessparameters'] + 'EditConditionalCell/'
Common_URL['SubWindow_URL_LAMProcessParametersAccumulateCell_Edit'] = Common_URL['Back_URL_lamprocessparameters'] + 'EditAccumulateCell/'

Common_URL['SubWindow_URL_LAMProcessParametersTechInstSerial_Edit'] = Common_URL['Back_URL_lamprocessparameters'] + 'EditTechInstSerial/'

# 提交数据
Common_URL['Update_URL_LAMProcessParametersTechInstSerial_Save'] = Common_URL['Back_URL_lamprocessparameters'] + 'SaveTechInstSerial/'



# 过程记录--分支
Common_URL['Back_URL_lamproduct'] = Common_URL['ProcessRecords'] + 'LAMProduct/'
Common_URL['Back_URL_rawstock'] = Common_URL['ProcessRecords'] + 'RawStock/'
Common_URL['Back_URL_rawstockflow'] = Common_URL['ProcessRecords'] + 'RawStockFlow/'
Common_URL['Back_URL_rawstockflow_statistic'] = Common_URL['ProcessRecords'] + 'RawStockFlowStatistic/'
Common_URL['Back_URL_lamprocessmission'] = Common_URL['ProcessRecords'] + 'LAMProcessMission/'

Common_URL['SubWindow_URL_RawStockFlow_SendAddition_Add'] = Common_URL[
																	'ProcessRecords'] + 'RawStockFlow/AddSendAddition/'
Common_URL['SubWindow_URL_RawStockFlow_SendAddition_Edit'] = Common_URL[
																	 'ProcessRecords'] + 'RawStockFlow/EditSendAddition/'

# 检验记录--分支
Common_URL['Back_URL_InspectionRecords_ProductPhyChemTest'] = Common_URL[
																  'InspectionRecords'] + 'PhysicochemicalTest/Product/'
Common_URL['Back_URL_InspectionRecords_RawStockPhyChemTest'] = Common_URL[
																   'InspectionRecords'] + 'PhysicochemicalTest/RawStock/'
Common_URL['Back_URL_InspectionRecords_ProductNonDestructiveTest'] = Common_URL[
																  'InspectionRecords'] + 'NonDestructiveTest/Product/'
Common_URL['Back_URL_InspectionRecords_RawStockNonDestructiveTest'] = Common_URL[
																  'InspectionRecords'] + 'NonDestructiveTest/RawStock/'
# 理化检测
Common_URL['SubWindow_URL_InspectionRecords_TensileTest_Add'] = Common_URL[
																	'InspectionRecords'] + 'PhysicochemicalTest/AddTensile/'
Common_URL['SubWindow_URL_InspectionRecords_TensileTest_Edit'] = Common_URL[
																	 'InspectionRecords'] + 'PhysicochemicalTest/EditTensile/'
Common_URL['SubWindow_URL_InspectionRecords_ToughnessTest_Add'] = Common_URL[
																	  'InspectionRecords'] + 'PhysicochemicalTest/AddToughness/'
Common_URL['SubWindow_URL_InspectionRecords_ToughnessTest_Edit'] = Common_URL[
																	   'InspectionRecords'] + 'PhysicochemicalTest/EditToughness/'
Common_URL['SubWindow_URL_InspectionRecords_FracturetoughnessTest_Add'] = Common_URL[
																	  'InspectionRecords'] + 'PhysicochemicalTest/AddFracturetoughness/'
Common_URL['SubWindow_URL_InspectionRecords_FracturetoughnessTest_Edit'] = Common_URL[
																	   'InspectionRecords'] + 'PhysicochemicalTest/EditFracturetoughness/'
Common_URL['SubWindow_URL_InspectionRecords_ChemicalElement_Add'] = Common_URL[
																		'InspectionRecords'] + 'PhysicochemicalTest/AddChemicalElement/'
Common_URL['SubWindow_URL_InspectionRecords_ChemicalElement_Edit'] = Common_URL[
																		 'InspectionRecords'] + 'PhysicochemicalTest/EditChemicalElement/'

# 无损检测
Common_URL['SubWindow_URL_InspectionRecords_UTdefect_Add'] = Common_URL[
																	'InspectionRecords'] + 'NonDestructiveTest/AddUTDefect/'
Common_URL['SubWindow_URL_InspectionRecords_UTdefect_Edit'] = Common_URL[
																	 'InspectionRecords'] + 'NonDestructiveTest/EditUTDefect/'
Common_URL['SubWindow_URL_InspectionRecords_RTdefect_Add'] = Common_URL[
																	'InspectionRecords'] + 'NonDestructiveTest/AddRTDefect/'
Common_URL['SubWindow_URL_InspectionRecords_RTdefect_Edit'] = Common_URL[
																	 'InspectionRecords'] + 'NonDestructiveTest/EditRTDefect/'
Common_URL['SubWindow_URL_InspectionRecords_PTdefect_Add'] = Common_URL[
																	'InspectionRecords'] + 'NonDestructiveTest/AddPTDefect/'
Common_URL['SubWindow_URL_InspectionRecords_PTdefect_Edit'] = Common_URL[
																	 'InspectionRecords'] + 'NonDestructiveTest/EditPTDefect/'
Common_URL['SubWindow_URL_InspectionRecords_MTdefect_Add'] = Common_URL[
																	'InspectionRecords'] + 'NonDestructiveTest/AddMTDefect/'
Common_URL['SubWindow_URL_InspectionRecords_MTdefect_Edit'] = Common_URL[
																	 'InspectionRecords'] + 'NonDestructiveTest/EditMTDefect/'
Common_URL['SubWindow_URL_InspectionRecords_UTdefect_Add'] = Common_URL[
																	'InspectionRecords'] + 'NonDestructiveTest/AddUTDefect/'


# 过程记录过检
# 激光成形过程
Common_URL['Back_URL_InspectionRecords_ProcessMissionInspection_LAMProcess'] = Common_URL[
																  'InspectionRecords'] + 'ProcessMissionInspection/LAMProcess/'
Common_URL['SubWindow_URL_InspectionRecords_ProcessMissionInspection_LAMProcess'] = Common_URL[
				'Back_URL_InspectionRecords_ProcessMissionInspection_LAMProcess'] + 'ByMissionID/'
# 激光成形制造过程分析
Common_URL['SubWindow_URL_AnalyseLAMProcess_MissionFilter'] = Common_URL['AnalyseLAMProcess'] + 'MissionFilter/'
Common_URL['SubWindow_URL_AnalyseLAMProcess_MissionFilter_ZValue'] = Common_URL['SubWindow_URL_AnalyseLAMProcess_MissionFilter'] + 'ZValue/'
Common_URL['SubWindow_URL_AnalyseLAMProcess_MissionFilter_AccumulateData'] = Common_URL['SubWindow_URL_AnalyseLAMProcess_MissionFilter'] + 'AccumulateData/'
Common_URL['SubWindow_URL_AnalyseLAMProcess_MissionFilter_LayerData'] = Common_URL['SubWindow_URL_AnalyseLAMProcess_MissionFilter'] + 'LayerData/'
Common_URL['SubWindow_URL_AnalyseLAMProcess_MissionFilter_ScanningRate3D'] = Common_URL['SubWindow_URL_AnalyseLAMProcess_MissionFilter'] + 'ScanningRate3D/'

Common_URL['Back_URL_AnalyseLAMProcess_ZValue'] = Common_URL['AnalyseLAMProcess'] + 'ZValue/'
Common_URL['Back_URL_AnalyseLAMProcess_AccumulateData'] = Common_URL['AnalyseLAMProcess'] + 'AccumulateData/'
Common_URL['Back_URL_AnalyseLAMProcess_LayerData'] = Common_URL['AnalyseLAMProcess'] + 'LayerData/'
Common_URL['Back_URL_AnalyseLAMProcess_ScanningRate3D'] = Common_URL['AnalyseLAMProcess'] + 'ScanningRate3D/'

Common_URL['Back_URL_AnalyseLAMProcess_DingDingRecords_Upload'] = Common_URL['AnalyseLAMProcess'] + 'DingDingRecords/Upload/'
Common_URL['Back_URL_AnalyseLAMProcess_DingDingRecords_Browse'] = Common_URL['AnalyseLAMProcess'] + 'DingDingRecords/Browse/'
Common_URL['Query_DingDingRecords_info'] = Common_URL['ProcessPath'] + 'QueryData/AnalyseLAMProcess/DingDingRecords_by_ID/'

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


# 编程小工具
Common_URL['Back_URL_BreakBlockResumption'] = Common_URL['PracticalTools'] + 'BreakBlockResumption/'
Common_URL['Back_URL_SShapeBreak'] = Common_URL['PracticalTools'] + 'SShapeBreak/'
Common_URL['Back_URL_MakeMainProgramFile_8070'] = Common_URL['PracticalTools'] + 'MakeMainProgramFile_8070/'

# 查询
Common_URL['Query_LAMTechInst_Preview'] = Common_URL['ProcessPath'] + 'QueryData/PreviewTable/LAMTechniqueInstruction/'
Common_URL['Query_LAMTechInstSerialDetails_Preview'] = Common_URL['ProcessPath'] + 'QueryData/PreviewTable/LAMTechniqueInstruction_SerialDetails/'
Common_URL['Query_LAMProductMission_Preview'] = Common_URL['ProcessPath'] + 'QueryData/PreviewTable/LAMProductMission/'
Common_URL['Query_ProductPhyChemTestMission_Preview'] = Common_URL['ProcessPath'] + 'QueryData/PreviewTable/ProductPhyChemTestMission/'
Common_URL['Query_RawStockPhyChemTestMission_Preview'] = Common_URL['ProcessPath'] + 'QueryData/PreviewTable/RawStockPhyChemTestMission/'
Common_URL['Query_ProductNonDestructiveTestMission_Preview'] = Common_URL['ProcessPath'] + 'QueryData/PreviewTable/ProductNonDestructiveTestMission/'
Common_URL['Query_RawStockNonDestructiveTestMission_Preview'] = Common_URL['ProcessPath'] + 'QueryData/PreviewTable/RawStockNonDestructiveTestMission/'

# Common_URL['Query_LAMTechInst_By_ProductCategory'] = Common_URL['ProcessPath'] + 'QueryData/LAMTechniqueInstruction_By_ProductCategory/'

Common_URL['Query_LAMTechniqueInstruction_By_ProductCode'] = Common_URL['ProcessPath'] + 'QueryData/LAMTechniqueInstruction_By_ProductCode/'
Common_URL['Query_LAMTechInstSerial_LAM_By_ProductCodeList'] = Common_URL['ProcessPath'] + 'QueryData/LAMTechInstSerial_LAM_By_ProductCodeList/'
Common_URL['Query_LAMTechInstSerial_Test_By_ProductCodeList'] = Common_URL['ProcessPath'] + 'QueryData/LAMTechInstSerial_Test_By_ProductCodeList/'
Common_URL['Query_WorkType_By_LAMTechInst'] = Common_URL['ProcessPath'] + 'QueryData/WorkType_By_LAMTechInst/'
Common_URL['Query_WorkType_By_LAMTechInst_filter_LAM'] = Common_URL['ProcessPath'] + 'QueryData/WorkType_By_LAMTechInst_filter_LAM/'
Common_URL['Query_WorkType_By_LAMTechInst_filter_PhyChemTest'] = Common_URL['ProcessPath'] + 'QueryData/WorkType_By_LAMTechInst_filter_PhyChemTest/'
Common_URL['Query_WorkType_By_LAMTechInst_filter_RawStockSendRetrieve'] = Common_URL['ProcessPath'] + 'QueryData/WorkType_By_LAMTechInst_filter_RawStockSendRetrieve/'
Common_URL['Query_Product_By_ProductCategory'] = Common_URL['ProcessPath'] + 'QueryData/Product_By_ProductCategory/'
Common_URL['Query_ProductID_By_ProductCode'] = Common_URL['ProcessPath'] + 'QueryData/ProductID_By_ProductCode/'
Common_URL['Query_RawStockID_By_RawStockBatchNumber'] = Common_URL['ProcessPath'] + 'QueryData/RawStockID_By_RawStockBatchNumber/'
Common_URL['Query_WorksectionId_By_MissionID'] = Common_URL['ProcessPath'] + 'QueryData/WorksectionId_By_MissionID/'
Common_URL['Query_StartFinishTime_By_MissionID'] = Common_URL['ProcessPath'] + 'QueryData/StartFinishTime_By_MissionID/'
Common_URL['Query_StartFinishTime_IfExists_By_MissionID'] = Common_URL['ProcessPath'] + 'QueryData/StartFinishTime_IfExists_By_MissionID/'
Common_URL['Query_StartFinishTime_IfExists_By_MissionIDList'] = Common_URL['ProcessPath'] + 'QueryData/StartFinishTime_IfExists_By_MissionIDList/'
Common_URL['Query_ArrangementDate_By_MissionID'] = Common_URL['ProcessPath'] + 'QueryData/ArrangementDate_By_MissionID/'
Common_URL['Query_Oxydata_By_WorkSectionDatetime'] = Common_URL['ProcessPath'] + 'QueryData/Oxydata_By_WorkSectionDatetime/'
Common_URL['Query_Oxydata_By_MissionDatetime'] = Common_URL['ProcessPath'] + 'QueryData/Oxydata_By_MissionDatetime/'
Common_URL['Query_Data_By_WorkSectionDatetime'] = Common_URL['ProcessPath'] + 'QueryData/Data_By_WorkSectionDatetime/'
Common_URL['Query_Mission_By_ProductCode'] = Common_URL['ProcessPath'] + 'QueryData/Mission_By_ProductCode/'
Common_URL['Query_RecordLastTime_By_WorksectionID'] = Common_URL['ProcessPath'] + 'QueryData/RecordLastTime_by_WorksectionID/'
Common_URL['Query_RealTimeRecord_By_WorksectionID'] = Common_URL['ProcessPath'] + 'QueryData/RealTimeRecord_by_WorksectionID/'
Common_URL['Query_ConditionalCell_By_ProcessParameterID'] = Common_URL['ProcessPath'] + 'QueryData/LAMProcessParameterConditionalCell_By_ProcessParameterID/'
Common_URL['Query_AccumulateCell_By_ProcessParameterID'] = Common_URL['ProcessPath'] + 'QueryData/LAMProcessParameterAccumulateCell_By_ProcessParameterID/'
Common_URL['Query_ProcessParameterTechInstSerial_By_ProcessParameterID'] = Common_URL['ProcessPath'] + 'QueryData/LAMProcessParameter_TechInstSerial_By_ProcessParameterID/'
Common_URL['Query_ProcessParameterTechInstSerial'] = Common_URL['ProcessPath'] + 'QueryData/LAMProcessParameter_TechInstSerial/'
Common_URL['Query_ProcessFineData_By_MissionID'] = Common_URL['ProcessPath'] + 'QueryData/FineData_By_MissionID/'
Common_URL['Query_ProcessFineData_By_MissionID_Datetime'] = Common_URL['ProcessPath'] + 'QueryData/FineData_By_MissionID_Datetime/'

Common_URL['Query_ProgressBarValue'] = Common_URL['ProcessPath'] +'QueryData/ProgressBarValue/'
Common_URL['Query_ProgressBarValue_InspectionLAMRecords_By_MissionID'] = Common_URL['Query_ProgressBarValue'] + 'InspectionLAMRecords_By_MissionID/'
Common_URL['Query_ProgressBarValue_PracticalTools_BreakBlockResumption_By_GUID'] = Common_URL['Query_ProgressBarValue'] + 'PracticalTools_BreakBlockResumption_By_GUID/'
Common_URL['Query_ProgressBarValue_PracticalTools_SShapeBreak_By_GUID'] = Common_URL['Query_ProgressBarValue'] + 'PracticalTools_SShapeBreak_By_GUID/'
Common_URL['Query_ProgressBarValue_New_LAMTechInstSerial_UploadPDFFile_By_TechInstID'] = Common_URL['Query_ProgressBarValue'] + 'New_LAMTechInstSerial_UploadPDFFile_By_TechInstID/'
Common_URL['Query_ProgressBarValue_Analyse_ZValue_By_MissionIDList'] = Common_URL['Query_ProgressBarValue'] + 'Analyse_ZValue_By_MissionIDList/'
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

@permission_required('LAMProcessData.SystemInformation', login_url=Common_URL['403'])
def SystemOperation(request):
	return render(request, 'SystemOperation.html', {'Common_URL': Common_URL,
	                                                'moveDataToFinedataTypeList':{'oxygen':r'将已有的氧含量数据导入finedata表中',
	                                                                              'laser':r'将已有的激光功率数据导入finedata表中',
	                                                                              'cncstatus':r'将已有的运动数据导入finedata表中'}})
	


@login_required
def userprofile(request):
	current_user_set = request.user
	current_group_set = Group.objects.filter(user=current_user_set)
	current_group_permissions = []
	# for _group in current_group_set:
	# 	current_group_permissions.extend(_group.get_group_permissions())
	# [ for _group in current_group_set]
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
	elif TableType == 'TechInst_Excel':
		_form_inst.setNewMode()
		templateFileName = 'EditForm_TechInst_Excel.html'
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
	elif TableType == 'TechInst_Excel':
		templateFileName = 'EditForm_TechInst_Excel.html'
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
def BasicInformation_OperateData(request, Model, ModelForm, TableType='common', ImageField=None, attlist=None, qset=(Q(available=True))):
	# Check_Is_authenticated(request)
	# all_entries = Model.objects.all()
	try:
		if qset is None:
			all_entries = Model.objects.all()
		else:
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
	if all_entries is not None:
		for i in all_entries:
			_dict = {}
			for att in attlist:
				if att in _modelfilednames:
					# 替换_id, 从而获得外键实例的名称
					_dict[att] = str(i.__getattribute__(att.replace('_id', '')))
				else:
					_dict[att] = list(map(str, list(i.__getattribute__(att).all())))
			if TableType=='common':
				_dict['displayname'] = str(i)
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
	                                          'ImageField':ImageField,
											  'all_entries': all_entries_dict,
	                                          # 'BASE_DIR':BASE_URL,
											  'Common_URL': Common_URL})

@permission_required('LAMProcessData.SystemInformation', login_url=Common_URL['403'])
def OperateData_workshop(request):
	return BasicInformation_OperateData(request, Model=Workshop, ModelForm=WorkshopForm)


@permission_required('LAMProcessData.SystemInformation', login_url=Common_URL['403'])
def new_workshop(request):
	return BasicInformation_New(request, ModelForm=WorkshopForm, modelname='workshop')


@permission_required('LAMProcessData.SystemInformation', login_url=Common_URL['403'])
def edit_workshop(request):
	return BasicInformation_Edit(request, Model=Workshop, ModelForm=WorkshopForm, modelname='workshop')


@permission_required('LAMProcessData.SystemInformation', login_url=Common_URL['403'])
def del_workshop(request):
	return BasicInformation_Delete(request, Model=Workshop, modelname='workshop')


'''============================================================================'''

@permission_required('LAMProcessData.SystemInformation', login_url=Common_URL['403'])
def OperateData_computer(request):
	return BasicInformation_OperateData(request, Model=Computer, ModelForm=ComputerForm)


@permission_required('LAMProcessData.SystemInformation', login_url=Common_URL['403'])
def new_computer(request):
	return BasicInformation_New(request, ModelForm=ComputerForm, modelname='computer')


@permission_required('LAMProcessData.SystemInformation', login_url=Common_URL['403'])
def edit_computer(request):
	return BasicInformation_Edit(request, Model=Computer, ModelForm=ComputerForm, modelname='computer')


@permission_required('LAMProcessData.SystemInformation', login_url=Common_URL['403'])
def del_computer(request):
	return BasicInformation_Delete(request, Model=Computer, modelname='computer')


'''============================================================================'''

@permission_required('LAMProcessData.SystemInformation', login_url=Common_URL['403'])
def OperateData_worksection(request):
	return BasicInformation_OperateData(request, Model=Worksection, ModelForm=WorksectionForm)


@permission_required('LAMProcessData.SystemInformation', login_url=Common_URL['403'])
def new_worksection(request):
	def insertworksection_current_mission(_form_inst):
		_worksection_crtmission_obj = Worksection_Current_LAMProcessMission(work_section = _form_inst.instance)
		_worksection_crtmission_obj.save()
		pass
	return BasicInformation_New(request, ModelForm=WorksectionForm, modelname='worksection',customfunction=insertworksection_current_mission)


@permission_required('LAMProcessData.SystemInformation', login_url=Common_URL['403'])
def edit_worksection(request):
	return BasicInformation_Edit(request, Model=Worksection, ModelForm=WorksectionForm, modelname='worksection')


@permission_required('LAMProcessData.SystemInformation', login_url=Common_URL['403'])
def del_worksection(request):
	return BasicInformation_Delete(request, Model=Worksection, modelname='worksection')


'''============================================================================'''

@permission_required('LAMProcessData.SystemInformation', login_url=Common_URL['403'])
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


@permission_required('LAMProcessData.SystemInformation', login_url=Common_URL['403'])
def new_lammaterial(request):
	return BasicInformation_New(request, ModelForm=LAMMaterialForm, modelname='lammaterial')


@permission_required('LAMProcessData.SystemInformation', login_url=Common_URL['403'])
def edit_lammaterial(request):
	return BasicInformation_Edit(request, Model=LAMMaterial, ModelForm=LAMMaterialForm, modelname='lammaterial')


@permission_required('LAMProcessData.SystemInformation', login_url=Common_URL['403'])
def del_lammaterial(request):
	return BasicInformation_Delete(request, Model=LAMMaterial, modelname='lammaterial')

'''============================================================================'''

@permission_required('LAMProcessData.SystemInformation', login_url=Common_URL['403'])
def OperateData_rawstockcategory(request):
	return BasicInformation_OperateData(request, Model=RawStockCategory, ModelForm=RawStockCategoryForm)

@permission_required('LAMProcessData.SystemInformation', login_url=Common_URL['403'])
def new_rawstockcategory(request):
	return BasicInformation_New(request, ModelForm=RawStockCategoryForm, modelname='rawstockcategory')

@permission_required('LAMProcessData.SystemInformation', login_url=Common_URL['403'])
def edit_rawstockcategory(request):
	return BasicInformation_Edit(request, Model=RawStockCategory, ModelForm=RawStockCategoryForm,
								 modelname='rawstockcategory')

@permission_required('LAMProcessData.SystemInformation', login_url=Common_URL['403'])
def del_rawstockcategory(request):
	return BasicInformation_Delete(request, Model=RawStockCategory, modelname='rawstockcategory')

'''============================================================================'''

@permission_required('LAMProcessData.SystemInformation', login_url=Common_URL['403'])
def OperateData_cncstatuscategory(request):
	return BasicInformation_OperateData(request, Model=CNCStatusCategory, ModelForm=CNCStatusCategoryForm)

@permission_required('LAMProcessData.SystemInformation', login_url=Common_URL['403'])
def new_cncstatuscategory(request):
	return BasicInformation_New(request, ModelForm=CNCStatusCategoryForm, modelname='cncstatuscategory')

@permission_required('LAMProcessData.SystemInformation', login_url=Common_URL['403'])
def edit_cncstatuscategory(request):
	return BasicInformation_Edit(request, Model=CNCStatusCategory, ModelForm=CNCStatusCategoryForm,
								 modelname='cncstatuscategory')

@permission_required('LAMProcessData.SystemInformation', login_url=Common_URL['403'])
def del_cncstatuscategory(request):
	return BasicInformation_Delete(request, Model=CNCStatusCategory, modelname='cncstatuscategory')

'''============================================================================'''


# 取样部位
@permission_required('LAMProcessData.SystemInformation', login_url=Common_URL['403'])
def OperateData_samplingposition(request):
	return BasicInformation_OperateData(request, Model=SamplingPosition, ModelForm=SamplingPositionForm)


@permission_required('LAMProcessData.SystemInformation', login_url=Common_URL['403'])
def new_samplingposition(request):
	return BasicInformation_New(request, ModelForm=SamplingPositionForm, modelname='samplingposition')


@permission_required('LAMProcessData.SystemInformation', login_url=Common_URL['403'])
def edit_samplingposition(request):
	return BasicInformation_Edit(request, Model=SamplingPosition, ModelForm=SamplingPositionForm,
								 modelname='samplingposition')


@permission_required('LAMProcessData.SystemInformation', login_url=Common_URL['403'])
def del_samplingposition(request):
	return BasicInformation_Delete(request, Model=SamplingPosition, modelname='samplingposition')


'''============================================================================'''


# 取样方向
@permission_required('LAMProcessData.SystemInformation', login_url=Common_URL['403'])
def OperateData_samplingdirection(request):
	return BasicInformation_OperateData(request, Model=SamplingDirection, ModelForm=SamplingDirectionForm)


@permission_required('LAMProcessData.SystemInformation', login_url=Common_URL['403'])
def new_samplingdirection(request):
	return BasicInformation_New(request, ModelForm=SamplingDirectionForm, modelname='samplingdirection')


@permission_required('LAMProcessData.SystemInformation', login_url=Common_URL['403'])
def edit_samplingdirection(request):
	return BasicInformation_Edit(request, Model=SamplingDirection, ModelForm=SamplingDirectionForm,
								 modelname='samplingdirection')


@permission_required('LAMProcessData.SystemInformation', login_url=Common_URL['403'])
def del_samplingdirection(request):
	return BasicInformation_Delete(request, Model=SamplingDirection, modelname='samplingdirection')


'''============================================================================'''


# 热处理状态
@permission_required('LAMProcessData.SystemInformation', login_url=Common_URL['403'])
def OperateData_heattreatmentstate(request):
	return BasicInformation_OperateData(request, Model=HeatTreatmentState, ModelForm=HeatTreatmentStateForm)


@permission_required('LAMProcessData.SystemInformation', login_url=Common_URL['403'])
def new_heattreatmentstate(request):
	return BasicInformation_New(request, ModelForm=HeatTreatmentStateForm, modelname='heattreatmentstate')


@permission_required('LAMProcessData.SystemInformation', login_url=Common_URL['403'])
def edit_heattreatmentstate(request):
	return BasicInformation_Edit(request, Model=HeatTreatmentState, ModelForm=HeatTreatmentStateForm,
								 modelname='heattreatmentstate')


@permission_required('LAMProcessData.SystemInformation', login_url=Common_URL['403'])
def del_heattreatmentstate(request):
	return BasicInformation_Delete(request, Model=HeatTreatmentState, modelname='heattreatmentstate')


'''============================================================================'''


# 机械加工状态
@permission_required('LAMProcessData.SystemInformation', login_url=Common_URL['403'])
def OperateData_machiningstate(request):
	return BasicInformation_OperateData(request, Model=MachiningState, ModelForm=MachiningStateForm)


@permission_required('LAMProcessData.SystemInformation', login_url=Common_URL['403'])
def new_machiningstate(request):
	return BasicInformation_New(request, ModelForm=MachiningStateForm, modelname='machiningstate')


@permission_required('LAMProcessData.SystemInformation', login_url=Common_URL['403'])
def edit_machiningstate(request):
	return BasicInformation_Edit(request, Model=MachiningState, ModelForm=MachiningStateForm,
								 modelname='machiningstate')


@permission_required('LAMProcessData.SystemInformation', login_url=Common_URL['403'])
def del_machiningstate(request):
	return BasicInformation_Delete(request, Model=MachiningState, modelname='machiningstate')


'''============================================================================'''

@permission_required('LAMProcessData.Technique', login_url=Common_URL['403'])
def OperateData_lamproductionworktype(request):
	return BasicInformation_OperateData(request, Model=LAMProductionWorkType, ModelForm=LAMProductionWorkTypeForm)

@permission_required('LAMProcessData.Technique', login_url=Common_URL['403'])
def new_lamproductionworktype(request):
	return BasicInformation_New(request, ModelForm=LAMProductionWorkTypeForm, modelname='lamproductionworktype')

@permission_required('LAMProcessData.Technique', login_url=Common_URL['403'])
def edit_lamproductionworktype(request):
	return BasicInformation_Edit(request, Model=LAMProductionWorkType, ModelForm=LAMProductionWorkTypeForm,
								 modelname='lamproductionworktype')

@permission_required('LAMProcessData.Technique', login_url=Common_URL['403'])
def del_lamproductionworktype(request):
	return BasicInformation_Delete(request, Model=LAMProductionWorkType, modelname='lamproductionworktype')


'''============================================================================'''


# 工序在工艺文件中实例化
@permission_required('LAMProcessData.Technique', login_url=Common_URL['403'])
def OperateData_lamtechinstserial(request):
	return BasicInformation_OperateData(request, Model=LAM_TechInst_Serial, ModelForm=LAMTechInstSerialForm_Browse,
										TableType='advanced')

@permission_required('LAMProcessData.Technique', login_url=Common_URL['403'])
def new_lamtechinstserial(request):
	return BasicInformation_New(request, ModelForm=LAMTechInstSerialForm, modelname='lamtechinstserial',
								TableType='advanced', isvalidType='custom')

@permission_required('LAMProcessData.Technique', login_url=Common_URL['403'])
def edit_lamtechinstserial(request):
	return BasicInformation_Edit(request, Model=LAM_TechInst_Serial, ModelForm=LAMTechInstSerialForm_Edit,
								 modelname='lamtechinstserial')

@permission_required('LAMProcessData.Technique', login_url=Common_URL['403'])
def del_lamtechinstserial(request):
	return BasicInformation_Delete(request, Model=LAM_TechInst_Serial, modelname='lamtechinstserial')


@permission_required('LAMProcessData.Technique', login_url=Common_URL['403'])
# @cache_page(60 * 30)
def new_lamtechinstserial_by_pdf(request):
	# 上传PDF实例化工序
	'''主函数开始'''
	qset = (Q(available=True))
	all_techinst = LAMTechniqueInstruction.objects.filter(qset)
	worktype_list = LAMProductionWorkType.objects.filter(qset)
	# step = ('ready', 'uploadPDF', 'save')
	if request.method != 'POST':
		_form_inst = LAMTechInstSerial_PDF_Form()
		
		
		step = 'ready'
		return render(request, "OperateForm_LAMTechInstSerial_ByPDF.html",
		              {
			              'form': _form_inst,
			              'all_techinst': all_techinst,
						  'worktype_list':worktype_list,
			              'Common_URL': Common_URL,
			              'step': step,
		              })
	else:
		# 选中的工艺文件ID
		tech_inst_id = request.POST['Technique_Instruction_ID']
		# 选中的工艺文件名称
		tech_inst_name = request.POST['Technique_Instruction']
		# 选中的工艺文件实例
		tech_inst = LAMTechniqueInstruction.objects.get(id=int(tech_inst_id))
		# 选中的工艺文件 数据库中现有工序
		tech_inst_serial_list = LAM_TechInst_Serial.objects.filter(Q(technique_instruction=tech_inst_id))
		if 'jqery_post' in request.POST:
			'''模拟post提交，保存'''
			success = True
			errors = []
			infomations = []
			
			# GUID = request.POST['GUID']
			# select_tech_inst_id = request.POST['Technique_Instruction_ID']
			# select_tech_inst_name = request.POST['Technique_Instruction']
			tableInfo_list = eval(request.POST['tableInfo'])
			with open(request.POST['TempfileName']) as _tempfile:
				PDF_dict_str = _tempfile.read()
				PDF_dict = json.loads(PDF_dict_str)
				
				'''将上传修正的数据以工序为单位汇总，稍后与之前自主识别的信息拼合到tableInfo_list_Merge中'''
				_struct = {'number': -1, 'name': '', 'note': [], 'DD_CanSee': False, 'JGCX_CanSee': False,
				           'RCL_CanSee': False, 'JY_CanSee': False, 'KF_CanSee': False, 'CZ_CanSee': False}
				tableInfo_list_Merge = []
				for _info in tableInfo_list:
					if _info[1] != '':
						if _struct['number'] != -1:
							tableInfo_list_Merge.append(_struct)
							_struct = {'number': -1, 'name': '', 'note': [], 'DD_CanSee': False, 'JGCX_CanSee': False,
							           'RCL_CanSee': False, 'JY_CanSee': False, 'KF_CanSee': False, 'CZ_CanSee': False}
						_struct['number'] = int(_info[1])
						_struct['name'] = _info[2]
						_struct['DD_CanSee'] = eval(_info[4])
						_struct['JGCX_CanSee'] = eval(_info[5])
						_struct['RCL_CanSee'] = eval(_info[6])
						_struct['JY_CanSee'] = eval(_info[7])
						_struct['KF_CanSee'] = eval(_info[8])
						_struct['CZ_CanSee'] = eval(_info[9])
					else:
						_struct['note'].append(_info[3])
				tableInfo_list_Merge.append(_struct)
				
				def getMergeInfoItem(number):
					return list(filter(lambda i: i['number'] == number, tableInfo_list_Merge))[0]
				
				for item in PDF_dict['Serial_Item_List']:
					# _Merge_info = getMergeInfoItem(int(item['number']))
					# _Merge_info['imgcodelist'] = item['imgcodelist']
					# _Merge_info['originalimg'] = np.array(PDF_dict['NameImgList'][PDF_dict['NumberStrList'].index(item['number'])])
					# getMergeInfoItem(int(item['number']))['imgcodelist'] = item['imgcodelist']
					try:
						_Merge_info = getMergeInfoItem(int(item['number']))
					except:
						pass
					_Merge_info['imgcodelist'] = item['imgcodelist']
					_Merge_info['originalimg'] = np.array(PDF_dict['NameImgList'][item['name_lineid']])
					_Merge_info['noteimglist']=[]
					for note_lineid in item['note_lineid_list']:
						_Merge_info['noteimglist'].append(np.array(PDF_dict['NameImgList'][note_lineid]))
					
					
				
				'''保存数据库'''
				'''|--保存/更新 PDFImageCode'''
				for item in tableInfo_list_Merge:
					try:
						ReadPDF.Save_ImgCode(item['name'], item['imgcodelist'][0][0], item['imgcodelist'][0][1], item['originalimg'])
						for _id, notename in enumerate(item['note']):
							ReadPDF.Save_ImgCode(notename, item['imgcodelist'][_id + 1][0], item['imgcodelist'][_id + 1][1],item['noteimglist'][_id])
					except:
						errors.append('保存工序%s的图像识别码失败。\n'%(item['name']))
						success = False
				'''|--保存/更新 LAM_TechInst_Serial'''
				'''|    |--先检查是否有与数据库中已有内容冲突的工序号（不生效）'''
				'''|    |--先检查提交的工序号列表中有无重复'''
				# qset = (
				# 		Q(technique_instruction=tech_inst_id)
				# )
				# existing_TechInst_Serial_list = LAM_TechInst_Serial.objects.filter(qset)
				existing_serial_num_dict = {serial.serial_number:serial.id for serial in tech_inst_serial_list}
				updateing_serial_num_list = [int(serial['number']) for serial in tableInfo_list_Merge]
				
				# 对数据库进行更新、新增，若不存在则新增，若存在则修改，若新增的工序有重号，则报错
				
				# if len(set(existing_serial_num_list+updateing_serial_num_list)) < len(existing_serial_num_list) + len(updateing_serial_num_list):
				# 	errors.append('技术文件（%s）中已有工序%s与新增工序%s有重叠，请重新检查。\n'%(tech_inst_name,str(existing_serial_num_list),str(updateing_serial_num_list)))
				# 	success = False
				if len(set(updateing_serial_num_list)) < len(updateing_serial_num_list):
					errors.append('新增工序%s中工序号有重复，请检查后重新保存。\n'%(str(updateing_serial_num_list)))
					success = False
				else:
					'''|    |--再进行保存'''
					'''可以进行保存操作'''
					for item in tableInfo_list_Merge:
						try:
							_worktype = LAMProductionWorkType.objects.get(worktype_name=item['name'])
							if int(item['number']) in existing_serial_num_dict.keys():
								# 	已存在，则更新
								existing_serial = LAM_TechInst_Serial.objects.get(
									id=existing_serial_num_dict[int(item['number'])])
								_successText = '工序%d-%s成功更新。'%(int(item['number']), item['name']) if (
										existing_serial.serial_worktype != _worktype or
										existing_serial.serial_note != ','.join(item['note']) or
										existing_serial.selectable_Scheduling != item['DD_CanSee'] or
										existing_serial.selectable_LAM != item['JGCX_CanSee'] or
										existing_serial.selectable_HeatTreatment != item['RCL_CanSee'] or
										existing_serial.selectable_PhyChemNonDestructiveTest != item['JY_CanSee'] or
										existing_serial.selectable_RawStockSendRetrieve != item['KF_CanSee'] or
										existing_serial.selectable_Weighing != item['CZ_CanSee']) else None
								
								existing_serial.serial_worktype = _worktype
								existing_serial.serial_note = ','.join(item['note'])
								existing_serial.selectable_Scheduling = item['DD_CanSee']
								existing_serial.selectable_LAM = item['JGCX_CanSee']
								existing_serial.selectable_HeatTreatment = item['RCL_CanSee']
								existing_serial.selectable_PhyChemNonDestructiveTest = item['JY_CanSee']
								existing_serial.selectable_RawStockSendRetrieve = item['KF_CanSee']
								existing_serial.selectable_Weighing = item['CZ_CanSee']
								existing_serial.save()
								if _successText:
									infomations.append(_successText)
								pass
							else:
								
								new_serial = LAM_TechInst_Serial.objects.create(
									technique_instruction= LAMTechniqueInstruction.objects.get(id=tech_inst_id),
									serial_number= int(item['number']),
									serial_worktype = _worktype,
									serial_note = ','.join(item['note']),
									serial_content = '',
									available = True,
									process_parameter = None,
									selectable_Scheduling=item['DD_CanSee'],
									selectable_LAM=item['JGCX_CanSee'],
									selectable_HeatTreatment=item['RCL_CanSee'],
									selectable_PhyChemNonDestructiveTest=item['JY_CanSee'],
									selectable_RawStockSendRetrieve =item['KF_CanSee'],
									selectable_Weighing = item['CZ_CanSee'],
								)
								new_serial.save()
								infomations.append('工序%d-%s成功新增。' % (int(item['number']), item['name']))
						except:
							errors.append('工序%d-%s保存失败。\n'%(int(item['number']), item['name']))
							success = False
						# edit at 20200326 23:58
							# 选中的工艺文件 数据库中现有工序
				tech_inst_serial_list = LAM_TechInst_Serial.objects.filter(Q(technique_instruction=tech_inst_id))
			
			html = json.dumps(
				{
					'success': success,
					'errors': errors,
			        'infomations':infomations,
			        'Existing_TechInst_Serials': [[
				         _serial.id,
							_serial.serial_number,
					     str(_serial.serial_worktype),
					     _serial.serial_note,
					     _serial.serial_content,
					     _serial.selectable_Scheduling,
					     _serial.selectable_LAM,
					     _serial.selectable_HeatTreatment,
					     _serial.selectable_PhyChemNonDestructiveTest,
					     _serial.selectable_RawStockSendRetrieve,
					     _serial.selectable_Weighing] for _serial in tech_inst_serial_list if _serial.available],
			    }, ensure_ascii=False)
			
			return HttpResponse(html, content_type='application/json')
			
		else:
			# 20200325：此处应传回GUID
			'''form表单提交，分析pdf'''
			step = 'uploadPDF'
			# GUID = request.POST['GUID']
			# tech_inst_id = request.POST['Technique_Instruction_ID']
			# tech_inst_name = request.POST['Technique_Instruction']
			# tech_inst = LAMTechniqueInstruction.objects.get(id = int(tech_inst_id))
			# tech_inst_serial_list = LAM_TechInst_Serial.objects.filter(Q(technique_instruction=tech_inst_id))
			
			file = request.FILES.get('File', None)
			if file:
				if file.size != 0:
					# _tempfile = os.path.join (tempfile.mkdtemp()+'.pdf')
					# with open(_tempfile, 'wb') as fp:
					# 	for part in file.chunks():
					# 		fp.write(part)
					# pdfInfo_dict = ReadPDF.pyMuPDF_fitz(pdfPath = _tempfile)
					# os.remove(_tempfile)
					file.open()
					contents = file.read()
					file.close()
					pdfInfo_dict = ReadPDF.pyMuPDF_fitz(stream=contents, filetype='stream', ifTemporaryFile=tech_inst.temporary, TechInstID=tech_inst_id)
					'''
					data = {"embeddings": knownEmbeddings.tolist(), "names": knownNames} ,
					you can retrieve the data to ndarray using np.asarray(data["embeddings"])
					– Shijith Jul 30 '19 at 10:50
					
					从str到bytes:调用方法encode().
					从bytes到str:调用方法decode().
					'''
					SerialItemList_for_JSON = {
						'Technique_Instruction_ID': tech_inst_id,
						'Serial_Item_List': pdfInfo_dict['Serial_Item_List'],
						'NameStrList': pdfInfo_dict['NameStrList'],
						'NumberStrList': pdfInfo_dict['NumberStrList'],
						'NameCodeIMGList': pdfInfo_dict['NameCodeIMGList'],
						'NameImgList': [img_array.tolist() for img_array in pdfInfo_dict['NameImgList']],
					}
					_tempfile = tempfile.NamedTemporaryFile(prefix='LAMServer', delete=False)
					_tempfile.write(json.dumps(SerialItemList_for_JSON, ensure_ascii=True).encode(encoding="utf8",errors="strict"))
					_tempfile.close()
					tempfile_name = _tempfile.name
					print(tempfile_name)
					'''start 合并单元格'''
					# 工序号、工种、概述
					pdfInfo_list = []
					# 哪些单元格合并
					pdfInfo_Merge_list = []
					_currentNumber = 0
					_current_rowNumber = 0
					_current_merge = [0, 0, 0]
					for i in range(len(pdfInfo_dict['NumberStrList'])):
						if len(str(pdfInfo_dict['NumberStrList'][i]))==0 and len(str(pdfInfo_dict['NameStrList'][i]))==0:
							continue
						_current_rowNumber += 1
						if len(str(pdfInfo_dict['NumberStrList'][i]))>0:
							# 结束上一次的merge，存入列表
							if _current_merge[0] != 0 and _current_merge[1] ==0:
								_current_merge[1] = _current_rowNumber
								if _current_merge[0] != _current_merge[1]-1:
									_current_merge[2] = _current_merge[1] - _current_merge[0]
									pdfInfo_Merge_list.append(_current_merge)
								_current_merge = [0, 0, 0]
							# 开始新的merge
							_current_merge[0] = _current_rowNumber
							_currentNumber = pdfInfo_dict['NumberStrList'][i]
							
						pdfInfo_list.append(
							[
								# pdfInfo_dict['NumberStrList'][i] if len(str(pdfInfo_dict['NumberStrList'][i]))>0 else _currentNumber,
								pdfInfo_dict['NumberStrList'][i],
								pdfInfo_dict['NameStrList'][i] if len(str(pdfInfo_dict['NumberStrList'][i])) != 0 else '',
								'' if len(str(pdfInfo_dict['NumberStrList'][i])) != 0 else pdfInfo_dict['NameStrList'][i],
							]
						)
					# 最后一行
					_current_merge[1] = _current_rowNumber
					if _current_merge[0] != _current_merge[1]:
						_current_merge[2] = _current_merge[1] - _current_merge[0]+1
						pdfInfo_Merge_list.append(_current_merge)
					'''end 合并单元格'''
					
					
					# 增加只读单元格的Y坐标，X=1时与X=2时
					pdfInfo_readonly_Y_list = [ id for (id, i) in enumerate(pdfInfo_list) if len(i[0])>0]
					print(pdfInfo_list)
					print(pdfInfo_Merge_list)
					print(pdfInfo_readonly_Y_list)
					# pdfInfo_list = [
					# 	[
					# 		pdfInfo_dict['NumberStrList'][i],
					# 		pdfInfo_dict['NameStrList'][i] if len(str(pdfInfo_dict['NumberStrList'][i])) != 0 else '',
					# 		'' if len(str(pdfInfo_dict['NumberStrList'][i])) != 0 else pdfInfo_dict['NameStrList'][i],
					#     ] for i in range(len(pdfInfo_dict['NumberStrList'])) if len(str(pdfInfo_dict['NumberStrList'][i]))>0 or len(str(pdfInfo_dict['NameStrList'][i]))>0  ]
					return render(request, "OperateForm_LAMTechInstSerial_ByPDF.html",
						{
							'Common_URL': Common_URL,
							'step': step,
							# 'GUID': GUID,
							'Technique_Instruction': tech_inst_name,
							'Technique_Instruction_ID': tech_inst_id,
							'Existing_TechInst_Serials': [[_serial.id,
							                               _serial.serial_number,
							                               str(_serial.serial_worktype),
							                               _serial.serial_note,
							                               _serial.serial_content,
							                               _serial.selectable_Scheduling,
							                               _serial.selectable_LAM,
							                               _serial.selectable_HeatTreatment,
							                               _serial.selectable_PhyChemNonDestructiveTest,
							                               _serial.selectable_RawStockSendRetrieve,
							                               _serial.selectable_Weighing] for _serial in tech_inst_serial_list if _serial.available],
							'select_product_code': list(map(lambda p: p.product_code, tech_inst.product.all())),
							'tech_inst_name': tech_inst_name,
							'pdfInfo_list': pdfInfo_list,
							'pdfInfo_Merge_list': pdfInfo_Merge_list,
							'pdfInfo_readonly_Y_list':pdfInfo_readonly_Y_list,
							'worktype_list':worktype_list,
				            'all_techinst': all_techinst,
							'tempfile_name': tempfile_name.replace('\\','\\\\'),
					    })
			else:
				save_success = 'False'
			
		
	
	
	

@permission_required('LAMProcessData.Technique', login_url=Common_URL['403'])
def new_lamtechinstserial_upload_pdf(request):
	
	tech_inst = request.POST['tech_inst_id']
	file = request.FILES.get('File', None)

	
	print(request.POST)
	if file:
		if file.size != 0:
			# args = [
			# 	file.name,
			# 	file,
			# 	# PowderOnOrder,
			# 	# PowderOffOrder,
			# 	TurningFunction,
			# 	SwitchBlockFunction,
			# 	IfPrintTurningFunction,
			# 	IfPrintSwitchBlockFunction,
			# 	GUID,
			# ]
			# # newText = SShapeBreak.MakeSShapeBreakGCode(file.name, file)
			# # ProgressBarValue_PracticalTools_SShapeBreak_By_GUID
			# newText = SShapeBreak.MakeSShapeBreakGCode(*args)
			# _tempfile = tempfile.NamedTemporaryFile(prefix='LAMServer', delete=False)
			# _tempfile.writelines(newText)
			# _tempfile.close()
			# tempfile_name = _tempfile.name
			# # tempfile_name = NCFileInsert(file, [ParamCurrentPPOSX, ParamCurrentPPOSY, ParamCurrentPPOSZ, ParamCounter])
			save_success = 'True'
	else:
		save_success = 'False'
	
	# _dict = RealtimeRecord.Realtime_Records.getRecords(WorksectionID)
	# # print(reDict['2019-11-19 11:35:00'])
	# html = json.dumps(_dict, ensure_ascii=False)
	# # print(html)
	# return HttpResponse(html, content_type='application/json')
	pass

@permission_required('LAMProcessData.Technique', login_url=Common_URL['403'])
def new_lamtechinstserial_save_pdf():
	pass

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

@permission_required('LAMProcessData.Technique', login_url=Common_URL['403'])
def OperateData_lamproductcategory(request):
	return BasicInformation_OperateData(request, Model=LAMProductCategory, ModelForm=LAMProductCategoryForm)

@permission_required('LAMProcessData.Technique', login_url=Common_URL['403'])
def new_lamproductcategory(request):
	return BasicInformation_New(request, ModelForm=LAMProductCategoryForm, modelname='productcategory')

@permission_required('LAMProcessData.Technique', login_url=Common_URL['403'])
def edit_lamproductcategory(request):
	return BasicInformation_Edit(request, Model=LAMProductCategory, ModelForm=LAMProductCategoryForm,
								 modelname='productcategory')

@permission_required('LAMProcessData.Technique', login_url=Common_URL['403'])
def del_lamproductcategory(request):
	return BasicInformation_Delete(request, Model=LAMProductCategory, modelname='productcategory')

'''============================================================================'''

@permission_required('LAMProcessData.Technique', login_url=Common_URL['403'])
def OperateData_lamproductsubarea(request):
	return BasicInformation_OperateData(request, Model=LAMProductSubarea, ModelForm=LAMProductSubareaForm)

@permission_required('LAMProcessData.Technique', login_url=Common_URL['403'])
def new_lamproductsubarea(request):
	return BasicInformation_New(request, ModelForm=LAMProductSubareaForm, modelname='lamproductsubarea')

@permission_required('LAMProcessData.Technique', login_url=Common_URL['403'])
def edit_lamproductsubarea(request):
	return BasicInformation_Edit(request, Model=LAMProductSubarea, ModelForm=LAMProductSubareaForm,
								 modelname='lamproductsubarea')

@permission_required('LAMProcessData.Technique', login_url=Common_URL['403'])
def del_lamproductsubarea(request):
	return BasicInformation_Delete(request, Model=LAMProductSubarea, modelname='lamproductsubarea')


'''============================================================================'''
@permission_required('LAMProcessData.Technique', login_url=Common_URL['403'])
def OperateData_chicharacters(request):
	attlist = [
		'id',
		'text',
		'OriginalImage',
	]
	ImageField = 'OriginalImage'
	return BasicInformation_OperateData(request, Model=PDFImageCode, ModelForm=PDFImageCodeForm,
	                                    TableType='advanced', ImageField=ImageField, attlist=attlist,  qset=None)

@permission_required('LAMProcessData.Technique', login_url=Common_URL['403'])
def edit_chicharacters(request):
	return BasicInformation_Edit(request, Model=PDFImageCode, ModelForm=PDFImageCodeForm,
								 modelname='chicharacters')

def test1(request):
	return BasicInformation_OperateData(request, Model=LAMTechniqueInstruction, ModelForm=LAMTechniqueInstructionForm,
										TableType='test')

@permission_required('LAMProcessData.Technique', login_url=Common_URL['403'])
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
	# return BasicInformation_OperateData(request, Model=LAMTechniqueInstruction, ModelForm=LAMTechniqueInstructionForm,
	# 									TableType='advanced', attlist=attlist)
	return BasicInformation_OperateData(request, Model=LAMTechniqueInstruction, ModelForm=LAMTechniqueInstruction_OperateForm,
										TableType='advanced', attlist=attlist)

@permission_required('LAMProcessData.Technique', login_url=Common_URL['403'])
def new_lamtechniqueinstruction(request):
	def saveTechInstSerial(form):
		serial_list = json.loads(request.POST['TechInst_SerialTable'])
		techinst_obj = LAMTechniqueInstruction.objects.get(id=form.save().id)
		for _serial_info in serial_list:
			new_serial = LAM_TechInst_Serial.objects.create(
				technique_instruction=techinst_obj,
				serial_number=int(_serial_info[1]),
				serial_worktype=LAMProductionWorkType.objects.get(id=_serial_info[2].split('-')[0]),
				serial_note=_serial_info[3],
				serial_content='',
				available=True,
				process_parameter=LAMProcessParameters.objects.get(id=_serial_info[4].split('-')[0]),
			)
			new_serial.save()
		# 20200718 night edit here
		pass
	return BasicInformation_New(request, ModelForm=LAMTechniqueInstructionForm, modelname='lamtechniqueinstruction', TableType='TechInst_Excel', customfunction=saveTechInstSerial)

@permission_required('LAMProcessData.Technique', login_url=Common_URL['403'])
def edit_lamtechniqueinstruction(request):
	return BasicInformation_Edit(request, Model=LAMTechniqueInstruction, ModelForm=LAMTechniqueInstructionForm,
								 modelname='lamtechniqueinstruction', TableType='TechInst_Excel', SaveMethod = 'custom')

@permission_required('LAMProcessData.Technique', login_url=Common_URL['403'])
def del_lamtechniqueinstruction(request):
	return BasicInformation_Delete(request, Model=LAMTechniqueInstruction, modelname='lamtechniqueinstruction')


'''============================================================================'''

@permission_required('LAMProcessData.Technique', login_url=Common_URL['403'])
def OperateData_lamprodcate_techinst(request):
	return BasicInformation_OperateData(request, Model=LAMProdCate_TechInst, ModelForm=LAMProdCate_TechInstForm)

@permission_required('LAMProcessData.Technique', login_url=Common_URL['403'])
def new_lamprodcate_techinst(request):
	return BasicInformation_New(request, ModelForm=LAMProdCate_TechInstForm, modelname='lamprodcate_techinst')

@permission_required('LAMProcessData.Technique', login_url=Common_URL['403'])
def edit_lamprodcate_techinst(request):
	return BasicInformation_Edit(request, Model=LAMProdCate_TechInst, ModelForm=LAMProdCate_TechInstForm,
								 modelname='lamprodcate_techinst')

@permission_required('LAMProcessData.Technique', login_url=Common_URL['403'])
def del_lamprodcate_techinst(request):
	return BasicInformation_Delete(request, Model=LAMProdCate_TechInst, modelname='lamprodcate_techinst')


'''============================================================================'''

@permission_required('LAMProcessData.Manufacture', login_url=Common_URL['403'])
def OperateData_lamproduct(request):
	return BasicInformation_OperateData(request, Model=LAMProduct, ModelForm=LAMProductForm)

@permission_required('LAMProcessData.Manufacture', login_url=Common_URL['403'])
def new_lamproduct(request):
	return BasicInformation_New(request, ModelForm=LAMProductForm, modelname='lamproduct')

@permission_required('LAMProcessData.Manufacture', login_url=Common_URL['403'])
def edit_lamproduct(request):
	return BasicInformation_Edit(request, Model=LAMProduct, ModelForm=LAMProductForm,
								 modelname='lamproduct')

@permission_required('LAMProcessData.Manufacture', login_url=Common_URL['403'])
def del_lamproduct(request):
	return BasicInformation_Delete(request, Model=LAMProduct, modelname='lamproduct')



'''============================================================================'''



@permission_required('LAMProcessData.Operator_STOREROOM', login_url=Common_URL['403'])
def OperateData_rawstock(request):
	return BasicInformation_OperateData(request, Model=RawStock, ModelForm=RawStockForm,
										TableType='advanced')

@permission_required('LAMProcessData.Operator_STOREROOM', login_url=Common_URL['403'])
def new_rawstock(request):
	return BasicInformation_New(request, ModelForm=RawStockForm, modelname='rawstock')

@permission_required('LAMProcessData.Operator_STOREROOM', login_url=Common_URL['403'])
def edit_rawstock(request):
	return BasicInformation_Edit(request, Model=RawStock, ModelForm=RawStockForm_Edit,
								 modelname='rawstock')


'''============================================================================'''

@permission_required('LAMProcessData.Operator_STOREROOM', login_url=Common_URL['403'])
def rawstockflow(request):
	# 注意'id'项，注意外键增加'_id'
	attlist = [
		'id',
		'send_time',
		'LAM_mission_id',
		'raw_stock_id',
		'raw_stock_sent_amount',
		'send_addition',
		'retrieve_time',
		'raw_stock_unused_amount',
		'raw_stock_primaryretrieve_amount',
		'raw_stock_secondaryretrieve_amount',
		'available',
	]
	return BasicInformation_OperateData(request,
	                                    Model=RawStockSendRetrieve,
	                                    ModelForm=RawStockSendRetrieveForm,
	                                    attlist=attlist,
										TableType='advanced')

@permission_required('LAMProcessData.Operator_STOREROOM', login_url=Common_URL['403'])
def del_rawstock(request):
	return BasicInformation_Delete(request, Model=RawStock, modelname='rawstockflow')

@permission_required('LAMProcessData.Operator_STOREROOM', login_url=Common_URL['403'])
def rawstockflow_statistic(request):
	_form_inst = RawStockFlow_Statistic_Form()
	return render(request, 'Statisitic_RawStockFlow.html', {'form': _form_inst,
	                                          'operate': '编辑',
	                                          'Common_URL': Common_URL,
	                                          'Back_URL': Common_URL['Back_URL_rawstockflow_statistic']})

@permission_required('LAMProcessData.Operator_STOREROOM', login_url=Common_URL['403'])
def send_rawstockflow(request):
	return BasicInformation_New(request, ModelForm=RawStockSendForm, modelname='rawstockflow')

@permission_required('LAMProcessData.Operator_STOREROOM', login_url=Common_URL['403'])
def edit_sendaddition_rawstockflow(request, RawStockSendAdditionItemID):
	return PhyChemTest_EditSingleTestData(request, RawStockSendAdditionItemID, RawStockSendAdditionForm, RawStockSendAddition)

@permission_required('LAMProcessData.Operator_STOREROOM', login_url=Common_URL['403'])
def new_sendaddition_rawstockflow(request, RawStockFlowItemID):
	def func(_form_inst, RawStockFlowItemID):
		send_addition = RawStockSendAddition.objects.create(
			send_time=_form_inst.cleaned_data['send_time'],
			raw_stock=_form_inst.cleaned_data['raw_stock'],
			raw_stock_sent_amount=_form_inst.cleaned_data['raw_stock_sent_amount'],
		)
		rawstockflow = RawStockSendRetrieve.objects.get(id=RawStockFlowItemID)
		rawstockflow.send_addition.add(send_addition.id)
		rawstockflow.save()

	return PhyChemTest_AddSingleTestData(request, RawStockFlowItemID, RawStockSendAdditionForm, func)
	# # Check_Is_authenticated(request)
	# item_id = request.GET.get('item_id')
	# save_success = None
	# # 查询到指定的数据
	# try:
	# 	_model_inst = RawStockSendRetrieve.objects.get(id=item_id)
	# 	RawStockSendRetrieve_String = str(_model_inst)
	# except:
	# 	messages.success(request, "未找到此条记录！")
	# 	return redirect(Common_URL['Back_URL_rawstockflow'])
	#
	# # 如果不是POST方法访问
	# save_success = None
	# if request.method != 'POST':
	# 	# 创建一个空表单在页面显示
	# 	# _form_inst = RawStockSendAdditionForm(item_id)
	# 	_form_inst = RawStockSendAdditionForm()
	# 	# _form_inst = RawStockSendAdditionForm({'RawStockSendRetrieve':item_id})
	# else:
	# 	# 否则为POST方式
	# 	# request.POST方法，将会获取到表单中我们输入的数据
	# 	_form_inst = RawStockSendAdditionForm(request.POST)
	# 	# 验证其合法性，使用is_valid()方法
	# 	_isValid = True
	# 	_isValid = _form_inst.is_valid()
	#
	# 	if _isValid:
	# 		# 验证通过，使用save()方法保存数据
	# 		_form_inst.save()
	# 		# 若有自定义函数，则执行
	# 		# if customfunction:
	# 		# 	customfunction(_form_inst)
	# 		# _temp = int(_form_inst.data['technique_instruction'])
	# 		# print(_temp)
	# 		save_success = 'True'
	# 		_form_inst = RawStockSendAdditionForm(request.POST)
	# 	else:
	# 		save_success = 'False'
	# # 保存成功，使用redirect()跳转到指定页面
	# # return redirect('/LAMProcessData/EditBasicInfomation/Workshop/')
	# # return HttpResponseRedirect(reverse('/LAMProcessData/EditBasicInfomation/Workshop/', args=[111, 222]))
	# # return HttpResponseRedirect(reverse('/LAMProcessData/EditBasicInfomation/Workshop/', kwargs={'success': 'True'}))
	# # return render(request, 'EditForm_Workshop.html', {'form': form})
	# # print(save_success)
	#
	# templateFileName = 'EditForm_BasicInformation.html'
	# # _form_inst.title = '原材料追加发放记录:%s'%RawStockSendRetrieve_String
	# # _form_inst.fields['RawStockSendRetrieve']=item_id
	# # _form_inst.data['RawStockSendRetrieve'].value = item_id
	# _form_inst.fields['RawStockSendRetrieve'].widget.attrs.update(
	# 	{'value': '%s'%item_id, 'title':RawStockSendRetrieve_String})
	# return render(request, templateFileName,
	#               {'form': _form_inst,
	#                'operate': '新建',
	#                # 'operate': RawStockSendRetrieve_String,
	#                'RawStockSendRetrieve_String':RawStockSendRetrieve_String,
	#                'save_success': save_success,
	#                'Common_URL': Common_URL,
	#                'Back_URL': Common_URL['Back_URL_rawstockflow']})
	
	# if request.method != 'POST':
	# 	# 创建一个空表单在页面显示
	# 	_form_inst = RawStockSendAdditionForm(item_id)
	# 	templateFileName = 'EditForm_BasicInformation.html'
	# 	return render(request, templateFileName,
	# 	              {'form': _form_inst,
	# 	               'operate': '新建',
	# 	               'save_success': save_success,
	# 	               'Common_URL': Common_URL,
	# 	               # 'Back_URL': Common_URL['Back_URL_rawstockflow'],
	# 	               })
	# else:
	#
	# 	def insertaddition_of_RawStockSendRetrieve(_form_inst):
	# 		# _worksection_crtmission_obj = RawStockSendRetrieve(work_section = _form_inst.instance)
	# 		# _worksection_crtmission_obj.save()
	# 		pass
	#
	# 	return BasicInformation_New(request, ModelForm=RawStockSendAdditionForm, modelname='rawstockflow',customfunction = insertaddition_of_RawStockSendRetrieve)


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
@permission_required('LAMProcessData.Operator_STOREROOM', login_url=Common_URL['403'])
def retrieve_rawstockflow(request):
	# return BasicInformation_New(request, ModelForm=RawStockRetrieveForm, modelname='rawstockflow')
	return BasicInformation_Edit(request, Model=RawStockSendRetrieve, ModelForm=RawStockRetrieveForm,
								 modelname='rawstockflow')

@permission_required('LAMProcessData.Operator_STOREROOM', login_url=Common_URL['403'])
def edit_rawstockflow(request):
	item_id = request.GET.get('item_id')
	save_success = None
	# 查询到指定的数据
	try:
		_model_inst = RawStockSendRetrieve.objects.get(id=item_id)
	except:
		messages.success(request, "未找到此条记录！")
		return redirect(Common_URL['Back_URL_rawstockflow'])

	# 该发放记录中内的追加发放数据
	all_entries = _model_inst.send_addition.order_by('send_time')
	sendaddition_datalist = getTestDataList(all_entries, RawStockSendAddition, [])
	

	if request.method != 'POST':
		# 如果不是post,创建一个表单，并用instance=article当前数据填充表单
		_form_inst = RawStockSendForm(instance=_model_inst)
		# _form_Tensile = MechanicalTest_TensileForm()
		_form_inst.itemid = item_id
	else:
		# 如果是post,instance=article当前数据填充表单，并用data=request.POST获取到表单里的内容
		_form_inst = RawStockSendForm(instance=_model_inst, data=request.POST)

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
	
	BackURL = Common_URL['Back_URL_rawstockflow']
	return render(request, "EditForm_RawStockFlow.html",
				  {'form': _form_inst,
				   'sendaddition_datalist': sendaddition_datalist,
				   'operate': 'edit',
				   'save_success': save_success,
				   'Common_URL': Common_URL,
				   'Back_URL': BackURL})
	# return BasicInformation_Edit(request, Model=RawStockSendRetrieve, ModelForm=RawStockSendForm,
	# 							 modelname='rawstockflow')

@permission_required('LAMProcessData.Operator_STOREROOM', login_url=Common_URL['403'])
def del_rawstockflow(request):
	return BasicInformation_Delete(request, Model=RawStockSendRetrieve, modelname='rawstockflow')


'''============================================================================'''


# 生产任务
@permission_required('LAMProcessData.Manufacture', login_url=Common_URL['403'])
def OperateData_lamprocessmission(request):
	attlist = [
		'id',
		'LAM_product', #多对多不加_id后缀
		'LAM_techinst_serial_id', # 外键加_id 后缀
		'work_section_id',
		'arrangement_date',
		'completion_date',
		'available',
	]
	return BasicInformation_OperateData(request, Model=LAMProcessMission, ModelForm=LAMProcessMissionForm_Browse,attlist=attlist,
										TableType='advanced')

@permission_required('LAMProcessData.Manufacture', login_url=Common_URL['403'])
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

@permission_required('LAMProcessData.Manufacture', login_url=Common_URL['403'])
def finish_lamprocessmission(request):
	# if request.method == 'POST':
	# 	pass
	return BasicInformation_Edit(request, Model=LAMProcessMission,
								 ModelForm=LAMProcessMissionForm_Finish,
								 modelname='lamprocessmission', SaveMethod='custom')

@permission_required('LAMProcessData.Manufacture', login_url=Common_URL['403'])
def del_lamprocessmission(request):
	return BasicInformation_Delete(request, Model=LAMProcessMission, modelname='lamprocessmission')


'''============================================================================'''
'''======☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆======'''
'''======                             检验记录                              ======'''
'''======☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆======'''

@permission_required('LAMProcessData.Operator_INSP', login_url=Common_URL['403'])
def OperateData_ProductPhyChemTest(request):
	# 注意'id'项，注意外键增加'_id'
	attlist = [
		'id',
		'LAM_product',
		'LAM_techinst_serial_id',
		'commission_date',
		'heat_treatment_state_id',
		'mechanicaltest_tensile',
		'mechanicaltest_toughness',
		'mechanicaltest_fracturetoughness',
		'chemicaltest']
	return BasicInformation_OperateData(request, Model=PhysicochemicalTest_Mission,
										ModelForm=ProductPhyChemTestForm_Browse,
										TableType='advanced',
										attlist=attlist,
										qset=(Q(available=True) & Q(RawStock_id=None))
										)

@permission_required('LAMProcessData.Operator_INSP', login_url=Common_URL['403'])
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
		'mechanicaltest_fracturetoughness',
		'chemicaltest']
	return BasicInformation_OperateData(request, Model=PhysicochemicalTest_Mission,
										ModelForm=RawStockPhyChemTestForm_Browse,
										TableType='advanced',
										attlist=attlist,
										qset=(Q(available=True) & ~Q(RawStock_id=None))
										)

@permission_required('LAMProcessData.Operator_INSP', login_url=Common_URL['403'])
def OperateData_ProductNonDestructiveTest(request):
	# 注意'id'项，注意外键增加'_id'
	attlist = [
		'id',
		'LAM_product_id',
		'LAM_techinst_serial_id',
		'machining_state_id',
		'heat_treatment_state_id',
		'arrangement_date',
		'completion_date',
		# 'NDT_type',
		'UT_defect',
		'RT_defect',
		'PT_defect',
		'MT_defect',
		'rewelding_number',
		'quality_reviewsheet_id',
	]
	return BasicInformation_OperateData(request, Model=NonDestructiveTest_Mission,
										ModelForm=ProductNonDestructiveTestForm_Browse,
										TableType='advanced',
										attlist=attlist,
										qset=(Q(available=True) & ~Q(LAM_product_id=None))
										)

@permission_required('LAMProcessData.Operator_INSP', login_url=Common_URL['403'])
def OperateData_RawStockNonDestructiveTest(request):
	# 注意'id'项，注意外键增加'_id'
	attlist = [
		'id',
		'RawStock_id',
		'LAM_techinst_serial_id',
		'machining_state_id',
		'heat_treatment_state_id',
		'arrangement_date',
		'completion_date',
		# 'NDT_type',
		'UT_defect',
		'RT_defect',
		'PT_defect',
		'MT_defect',
		'rewelding_number',
		'quality_reviewsheet_id',
	]
	return BasicInformation_OperateData(request, Model=NonDestructiveTest_Mission,
										ModelForm=RawStockNonDestructiveTestForm_Browse,
										TableType='advanced',
										attlist=attlist,
										qset=(Q(available=True) & Q(LAM_product_id=None))
										)


@permission_required('LAMProcessData.Operator_INSP', login_url=Common_URL['403'])
def BrowseData_MissionLAMProcessInspection(request):
	# return BasicInformation_OperateData(request, Model=LAMProcessMission, ModelForm=LAMProcessMissionForm_Browse,
	#                                     TableType='advanced')
	all_mission = LAMProcessMission.objects.filter((Q(available=True)))
	# for i in list(all_mission):
	# 	print(i)
	
	
	attlist = None
	qset = (Q(available=True))
	Model = LAMProcessMission
	ModelForm = LAMProcessMissionForm_Browse
	try:
		all_entries = Model.objects.filter(qset)
		_modelfilednames = [f.attname for f in Model._meta.fields]
		# if not attlist:
		# 	attlist = [f.attname for f in Model._meta.fields]
		# 	attlist.append('LAM_product')
	except:
		pass
	attlist = ['id', 'LAM_product', 'LAM_techinst_serial_id', 'work_section_id', 'arrangement_date', 'completion_date', 'available']
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

@permission_required('LAMProcessData.Operator_INSP', login_url=Common_URL['403'])
def Inspect_MissionLAMProcessInspection(request, MissionItemID):
	_mission = LAMProcessMission.objects.get(id = MissionItemID)
	_mission_timecut = Process_Mission_timecut.objects.get(process_mission = _mission)
	_start_datetime = _mission_timecut.process_start_time
	_finish_datetime = _mission_timecut.process_finish_time

	_datetime_list = [(_start_datetime+datetime.timedelta(days=i)).strftime('%Y-%m-%d') for i in range((_finish_datetime - _start_datetime).days)]
	if _finish_datetime.strftime('%Y-%m-%d') not in _datetime_list:
		_datetime_list.append(_finish_datetime.strftime('%Y-%m-%d'))

	# 以2h切分一天24h，分为12块
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
					  'smalltitle': '%s/%s/%s[%s-%s]'%(','.join(map(lambda p:p.product_code, _mission.LAM_product.all())),
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

# 任务选择页面，选择后分析成形制造过程
@permission_required('LAMProcessData.Technique', login_url=Common_URL['403'])
def AnalyseLAMProcess_MissionFilter(request, AnalyseType):
	'''
	AnalyseType: ZValue, AccumulateData, LayerData
	'''
	_mission_all_dict = LAMProcessMission.objects.filter(available=True)
	attlist = None
	# ifmultiple_dict = {
	# 	'ZValue': True,
	# 	'AccumulateData': True,
	# 	'LayerData': False,
	# }
	try:
		all_entries = LAMProcessMission.objects.filter(available=True)
		_modelfilednames = [f.attname for f in LAMProcessMission._meta.fields]
		if not attlist:
			attlist = [f.attname for f in LAMProcessMission._meta.fields]
		attlist = ['id', 'LAM_product', 'LAM_techinst_serial_id', 'work_section_id', 'arrangement_date',
		           'completion_date', 'available']
	
	except:
		pass
	all_entries_dict = []
	for i in all_entries:
		_dict = {}
		for att in attlist:
			if att in _modelfilednames:
				# 替换_id, 从而获得外键实例的名称
				if att == 'available':continue
				_dict[att] = str(i.__getattribute__(att.replace('_id', '')))
				if att=='LAM_product_id':
					_dict[att] = i.__getattribute__(att.replace('_id', '')).product_code
			else:
				_dict[att] = list(map(str, list(i.__getattribute__(att).all())))

		all_entries_dict.append(_dict)

	return render(request, 'SubWindow_MissionFilter.html',
				  {
					  'all_mission': all_entries_dict,
					  'form':LAMProcessMissionForm_Browse,
					  'displayFieldLabel':['零件','任务工序','工段','下达','完成'],
					  'title': '选择任务',
					  'operate': AnalyseType,
					  # 'ifMultipleSelect': ifmultiple_dict[AnalyseType],
					  'Target_URL': Common_URL['Back_URL_AnalyseLAMProcess_'+AnalyseType],
					  'Common_URL': Common_URL})
	pass

# 数据分析视图模板
@permission_required('LAMProcessData.Technique', login_url=Common_URL['403'])
def AnalyseLAMProcess(request, templateFileName):
	if request.method == 'POST':
		_missionId_list_str = request.POST.get('MissionID_list')
		_missionId_list = _missionId_list_str.split(',')
		_product_code_list = [
			'%s (id:%s)'%(
				','.join(map(lambda p:p.product_code, LAMProcessMission.objects.get(id=int(id)).LAM_product.all())),
				id
			) for id in _missionId_list
		]

		return render(request, templateFileName,
					  {'Common_URL': Common_URL,
					   'MissionID_list':_missionId_list_str,
					   'MissionID_list_for_InitColorlist':_missionId_list,
					   'Product_code_list':_product_code_list})
	return render(request, templateFileName,
				  {'Common_URL': Common_URL})


# 成形高度随时间变化分析
@permission_required('LAMProcessData.Technique', login_url=Common_URL['403'])
def AnalyseLAMProcess_ZValue(request):
	return AnalyseLAMProcess(request, 'SubWindow_Analyse_ZValue.html')


# 累计数据随时间变化分析
@permission_required('LAMProcessData.Technique', login_url=Common_URL['403'])
def AnalyseLAMProcess_AccumulateData(request):
	return AnalyseLAMProcess(request, 'Analyse_AccumulateData.html')


# 成形过程层内分析
@permission_required('LAMProcessData.Technique', login_url=Common_URL['403'])
def AnalyseLAMProcess_LayerData(request):
	return AnalyseLAMProcess(request, 'Analyse_LayerData.html')


# 扫描速率空间分布分析
@permission_required('LAMProcessData.Technique', login_url=Common_URL['403'])
def AnalyseLAMProcess_ScanningRate3D(request):
	return AnalyseLAMProcess(request, 'Analyse_ScanningRate3D.html')


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
			try:
				_dict[att] = eval('i.get_%s_display()' % att)
			except:
				# _dict[att] = str(i.__getattribute__(att.replace('_id', '')))
				_dict[att] = str(eval('i.%s'%att.replace('_id', '')))
			if att in manytomanykey:
				_dict[att] = list(map(str, list(i.__getattribute__(att).all())))
			# else:
			# 	_dict[att] = str(i.__getattribute__(att.replace('_id', '')))
		datalist.append(_dict)
	return datalist

@permission_required('LAMProcessData.Operator_INSP', login_url=Common_URL['403'])
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
	# 该检测任务内的断裂韧度数据
	all_entries = _model_inst.mechanicaltest_fracturetoughness.order_by('sample_number')
	fracturetoughness_datalist = getTestDataList(all_entries, MechanicalTest_FractureToughness, [])

	# 该检测任务内的化学成分测试数据
	# |--首先获得应检测的化学成分项目
	# 元素
	# element_items = _model_inst.LAM_product.product_category.material.chemicalelements.all().order_by('id')
	if bool(IfProductTest):
		element_items = _model_inst.LAM_product.all()[0].product_category.material.chemicalelements.all().order_by('id')
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
				   'fracturetoughness_datalist': fracturetoughness_datalist,
				   'chemical_datalist': chemical_datalist,
				   'chemical_items': chemical_items,
				   'operate': 'edit',
				   'save_success': save_success,
				   'Common_URL': Common_URL,
				   'Back_URL': BackURL,
				   'If_Product_Test': IfProductTest})


@permission_required('LAMProcessData.Operator_INSP', login_url=Common_URL['403'])
def edit_TemplateNonDestructiveTest(request, IfProductTest, EditForm):
	item_id = request.GET.get('item_id')
	save_success = None
	# 查询到指定的数据
	try:
		_model_inst = NonDestructiveTest_Mission.objects.get(id=item_id)
	except:
		messages.success(request, "未找到此条记录！")
		return redirect(Common_URL['Back_URL_InspectionRecords_ProductNonDestructiveTest'])

	# _form_tensile_data = _model_inst.mechanicaltest_tensile
	# Defect_datalist = []
	# if _model_inst.NDT_type == 'UT':
		# 该检测任务内的超声测试结果
	all_UT_entries = _model_inst.UT_defect.order_by('defect_number')
	UTDefect_datalist = getTestDataList(all_UT_entries, UTDefectInformation, [])
	# elif _model_inst.NDT_type == 'RT':
		# 该检测任务内的X射线测试结果
	all_RT_entries = _model_inst.RT_defect.order_by('defect_number')
	RTDefect_datalist = getTestDataList(all_RT_entries, RTDefectInformation, [])
	# elif _model_inst.NDT_type == 'PT':
		# 该检测任务内的渗透测试结果
	all_PT_entries = _model_inst.PT_defect.order_by('defect_number')
	PTDefect_datalist = getTestDataList(all_PT_entries, PTDefectInformation, [])
	# elif _model_inst.NDT_type == 'MT':
		# 该检测任务内的磁粉测试结果
	all_MT_entries = _model_inst.MT_defect.order_by('defect_number')
	MTDefect_datalist = getTestDataList(all_MT_entries, MTDefectInformation, [])

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
		BackURL = Common_URL['Back_URL_InspectionRecords_ProductNonDestructiveTest']
	else:
		BackURL = Common_URL['Back_URL_InspectionRecords_RawStockNonDestructiveTest']
	
	return render(request, "EditForm_NonDestructiveTest.html",
				  {'form': _form_inst,
				   'UTDefect_datalist': UTDefect_datalist,
				   'RTDefect_datalist': RTDefect_datalist,
				   'PTDefect_datalist': PTDefect_datalist,
				   'MTDefect_datalist': MTDefect_datalist,
				   'operate': 'edit',
				   'save_success': save_success,
				   'Common_URL': Common_URL,
				   'Back_URL': BackURL,
				   'If_Product_Test': IfProductTest})


# 产品理化检测 新建
@permission_required('LAMProcessData.Operator_INSP', login_url=Common_URL['403'])
def new_ProductPhyChemTest(request):
	# save_success = None
	# if request.method != 'POST':
	# 	# 创建一个空表单在页面显示
	# 	_form_inst = ProductPhyChemTestForm_New()
	# else:
	# 	# 否则为POST方式
	# 	# request.POST方法，将会获取到表单中我们输入的数据
	# 	_form_inst = ProductPhyChemTestForm_New(request.POST)
	# 	# 验证其合法性，使用is_valid()方法
	# 	_isValid = True
	# 	_isValid = _form_inst.is_valid()
	#
	# 	if _isValid:
	# 		# 验证通过，使用save()方法保存数据
	# 		_form_inst.save()
	# 		# _temp = int(_form_inst.data['technique_instruction'])
	# 		# print(_temp)
	# 		save_success = 'True'
	# 		_form_inst = ProductPhyChemTestForm_New(request.POST)
	# 	else:
	# 		save_success = 'False'
	#
	# return render(request, "EditForm_PhyChemTest.html",
	#               {'form': _form_inst,
	#                'operate': 'new',
	#                'save_success': save_success,
	#                'Common_URL': Common_URL,
	#                'Back_URL': Common_URL['Back_URL_InspectionRecords_ProductPhyChemTest']})
	# def insertprocessmission_timecutrecords(_form_inst):
	# 	_timecut_obj = Process_Mission_timecut(process_mission = _form_inst.instance)
	# 	_timecut_obj.save()
	# 	pass
	return BasicInformation_New(request,
								ModelForm=ProductPhyChemTestForm_New,
								modelname='physicochemicaltest_mission_Product',
								TableType='advanced',
								isvalidType='custom',
								)

@permission_required('LAMProcessData.Operator_INSP', login_url=Common_URL['403'])
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
@permission_required('LAMProcessData.Operator_INSP', login_url=Common_URL['403'])
def new_RawStockPhyChemTest(request):
	# save_success = None
	# if request.method != 'POST':
	# 	# 创建一个空表单在页面显示
	# 	_form_inst = RawStockPhyChemTestForm_New()
	# else:
	# 	# 否则为POST方式
	# 	# request.POST方法，将会获取到表单中我们输入的数据
	# 	_form_inst = RawStockPhyChemTestForm_New(request.POST)
	# 	# 验证其合法性，使用is_valid()方法
	# 	_isValid = _form_inst.is_valid()
	#
	# 	if _isValid:
	# 		# 验证通过，使用save()方法保存数据
	# 		_form_inst.save()
	# 		save_success = 'True'
	# 		_form_inst = RawStockPhyChemTestForm_New(request.POST)
	# 	else:
	# 		save_success = 'False'
	#
	# return render(request, "EditForm_PhyChemTest.html",
	#               {'form': _form_inst,
	#                'operate': 'new',
	#                'save_success': save_success,
	#                'Common_URL': Common_URL,
	#                'Back_URL': Common_URL['Back_URL_InspectionRecords_RawStockPhyChemTest']})
	return BasicInformation_New(request,
								ModelForm=RawStockPhyChemTestForm_New,
								modelname='physicochemicaltest_mission_RawStock',
								TableType='advanced',
								isvalidType='custom',
								)

@permission_required('LAMProcessData.Operator_INSP', login_url=Common_URL['403'])
def edit_RawStockPhyChemTest(request):
	return edit_TemplatePhyChemTest(request, 0, RawStockPhyChemTestForm_Edit)



# 产品无损检测 新建
@permission_required('LAMProcessData.Operator_INSP', login_url=Common_URL['403'])
def new_ProductNonDestructiveTest(request):
	return BasicInformation_New(request,
								ModelForm=ProductNonDestructiveTestForm_New,
								modelname='nondestructivetest_mission_Product',
								TableType='advanced',
								isvalidType='custom',
								)

@permission_required('LAMProcessData.Operator_INSP', login_url=Common_URL['403'])
def edit_ProductNonDestructiveTest(request):
	# return edit_TemplatePhyChemTest(request, 1, ProductNonDestructiveTestForm_Edit)
	return edit_TemplateNonDestructiveTest(request, 1, ProductNonDestructiveTestForm_Edit)

# 原材料无损检测 新建
@permission_required('LAMProcessData.Operator_INSP', login_url=Common_URL['403'])
def new_RawStockNonDestructiveTest(request):
	return BasicInformation_New(request,
								ModelForm=RawStockNonDestructiveTestForm_New,
								modelname='nondestructivetest_mission_RawStock',
								TableType='advanced',
								isvalidType='custom',
								)

@permission_required('LAMProcessData.Operator_INSP', login_url=Common_URL['403'])
def edit_RawStockNonDestructiveTest(request):
	return edit_TemplateNonDestructiveTest(request, 0, RawStockNonDestructiveTestForm_Edit)

'''============================================================================'''


# 弹出增加数据的子窗口
@permission_required('LAMProcessData.Operator_INSP', login_url=Common_URL['403'])
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
@permission_required('LAMProcessData.Operator_INSP', login_url=Common_URL['403'])
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
@permission_required('LAMProcessData.Operator_INSP', login_url=Common_URL['403'])
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
@permission_required('LAMProcessData.Operator_INSP', login_url=Common_URL['403'])
def PhyChemTest_EditTensile(request, TensileID):
	return PhyChemTest_EditSingleTestData(request, TensileID, MechanicalTest_TensileForm, MechanicalTest_Tensile)


# 新建冲击数据
@permission_required('LAMProcessData.Operator_INSP', login_url=Common_URL['403'])
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
@permission_required('LAMProcessData.Operator_INSP', login_url=Common_URL['403'])
def PhyChemTest_EditToughness(request, ToughnessID):
	return PhyChemTest_EditSingleTestData(request, ToughnessID, MechanicalTest_ToughnessForm, MechanicalTest_Toughness)


# 新建断裂韧性数据
@permission_required('LAMProcessData.Operator_INSP', login_url=Common_URL['403'])
def PhyChemTest_AddFracturetoughness(request, MissionItemID):
	def func(_form_inst, MissionItemID):
		test_fracturetoughness = MechanicalTest_FractureToughness.objects.create(
			sample_number=_form_inst.cleaned_data['sample_number'],
			sampling_position=_form_inst.cleaned_data['sampling_position'],
			sampling_direction=_form_inst.cleaned_data['sampling_direction'],
			test_temperature=_form_inst.cleaned_data['test_temperature'],
			fracturetoughness_KIC=_form_inst.cleaned_data['fracturetoughness_KIC'],
			fracturetoughness_KQ=_form_inst.cleaned_data['fracturetoughness_KQ'],
			Effectiveness=_form_inst.cleaned_data['Effectiveness'],
			available=_form_inst.cleaned_data['available']
		)
		test_mission = PhysicochemicalTest_Mission.objects.get(id=MissionItemID)
		test_mission.mechanicaltest_fracturetoughness.add(test_fracturetoughness.id)
		test_mission.save()

	return PhyChemTest_AddSingleTestData(request, MissionItemID, MechanicalTest_FracturetoughnessForm, func)

# 编辑断裂韧性数据
@permission_required('LAMProcessData.Operator_INSP', login_url=Common_URL['403'])
def PhyChemTest_EditFracturetoughness(request, FracturetoughnessID):
	return PhyChemTest_EditSingleTestData(request, FracturetoughnessID, MechanicalTest_FracturetoughnessForm, MechanicalTest_FractureToughness)

# 新建化学元素数据
@permission_required('LAMProcessData.Operator_INSP', login_url=Common_URL['403'])
def PhyChemTest_AddChemicalElement(request, MissionItemID, IfProductTest):
	save_success = None
	_model_inst = PhysicochemicalTest_Mission.objects.get(id=MissionItemID)
	if bool(int(IfProductTest)):
		chemical_items = _model_inst.LAM_product.all()[0].product_category.material.chemicalelements.all().order_by('id')
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

@permission_required('LAMProcessData.Operator_INSP', login_url=Common_URL['403'])
def PhyChemTest_EditChemicalElement(request, MissionItemID, ChemicalItemID, IfProductTest):
	save_success = None
	# 理化测试任务实例
	_model_inst = PhysicochemicalTest_Mission.objects.get(id=MissionItemID)
	# 化学测试任务实例
	chemicaltest_inst = ChemicalTest.objects.get(id=ChemicalItemID)
	# 化学成分测试项
	if bool(int(IfProductTest)):
		chemical_items = _model_inst.LAM_product.all()[0].product_category.material.chemicalelements.all().order_by('id')
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



# 弹出增加数据的子窗口
@permission_required('LAMProcessData.Operator_INSP', login_url=Common_URL['403'])
def NonDestructiveTest_AddDefectData(request, MissionItemID, ModelForm, func):
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
			func(_form_inst, request, MissionItemID)
			save_success = 'True'
			_form_inst = ModelForm(request.POST)
		else:
			save_success = 'False'
	_form_inst.set_Subarea_QuerySet(DefectInformationObj=None, MissionObj=NonDestructiveTest_Mission.objects.get(id = MissionItemID))
	return render(request, "SubWindow_SimpleForm_with_photos.html",
				  {'form': _form_inst,
				   'operate': 'new',
				   'save_success': save_success,
				   'Common_URL': Common_URL,
				   })


# 弹出增加数据的子窗口
@permission_required('LAMProcessData.Operator_INSP', login_url=Common_URL['403'])
def NonDestructiveTest_EditDefectData(request, MissionItemID, ModelForm, Model, func):
	save_success = None
	_existing_pictures = []
	SingleTest_obj = Model.objects.get(id=MissionItemID)
	if request.method != 'POST':
		# 创建一个表单在页面显示
		_form_inst = ModelForm(instance=SingleTest_obj)
		
	else:
		# 否则为POST方式
		# request.POST方法，将会获取到表单中我们输入的数据
		
		_form_inst = ModelForm(instance=SingleTest_obj, data=request.POST)
		# 验证其合法性，使用is_valid()方法
		_isValid = _form_inst.is_valid()

		if _isValid:
			# 验证通过，使用save()方法保存数据
			_form_inst.save()
			func(request, MissionItemID)
			save_success = 'True'
			_form_inst = ModelForm(request.POST)
		else:
			save_success = 'False'
	_form_inst.set_Subarea_QuerySet(SingleTest_obj, None)
	_existing_pictures = list(Model.objects.get(id=MissionItemID).photos.all())
	return render(request, "SubWindow_SimpleForm_with_photos.html",
				  {'form': _form_inst,
				   'existing_pictures': _existing_pictures,
				   'operate': 'edit',
				   'save_success': save_success,
				   'Common_URL': Common_URL,
				   })

# 新建超声缺陷记录
@permission_required('LAMProcessData.Operator_INSP', login_url=Common_URL['403'])
def NonDestructiveTest_AddUTDefect(request, MissionItemID):
	def func(_form_inst, request, MissionItemID):
		UTDefect = UTDefectInformation.objects.create(
			defect_number=_form_inst.cleaned_data['defect_number'],
			defect_type=_form_inst.cleaned_data['defect_type'],
			equivalent_hole_diameter=_form_inst.cleaned_data['equivalent_hole_diameter'],
			radiation_equivalent=_form_inst.cleaned_data['radiation_equivalent'],
			product_subarea=_form_inst.cleaned_data['product_subarea'],
			X_coordinate=_form_inst.cleaned_data['X_coordinate'],
			Y_coordinate=_form_inst.cleaned_data['Y_coordinate'],
			Z_coordinate=_form_inst.cleaned_data['Z_coordinate'],
			# photos=_form_inst.cleaned_data['photos']
		)
		for img in request.FILES.getlist('file[]'):
			_def_pic = DefectPicture.objects.create(
				picture = img
			)
			UTDefect.photos.add(_def_pic)
		UTDefect.save()
		test_mission = NonDestructiveTest_Mission.objects.get(id=MissionItemID)
		test_mission.UT_defect.add(UTDefect.id)
		test_mission.save()

	return NonDestructiveTest_AddDefectData(request, MissionItemID, NonDestructiveTest_UTDefectForm, func)


# 编辑超声缺陷记录
@permission_required('LAMProcessData.Operator_INSP', login_url=Common_URL['403'])
def NonDestructiveTest_EditUTDefect(request, UTDefectID):
	def func(request, UTDefectID):
		UTDefect = UTDefectInformation.objects.get(id=UTDefectID)
		# 之前上传的图片
		_existing_pictures = list(UTDefect.photos.all())
		# 删除图片
		if 'jfiler-items-exclude-file-0' in request.POST:
			for img_name in json.loads(request.POST['jfiler-items-exclude-file-0']):
				_defectID = int(img_name.split('-')[0].split(':')[1])
				DefectPicture.objects.get(id = _defectID).delete()
			
		# UTDefect.photos.clear()
		# 保存新上传图片
		for img in request.FILES.getlist('file[]'):
			_def_pic = DefectPicture.objects.create(
				picture=img
			)
			UTDefect.photos.add(_def_pic)
		UTDefect.save()
		
	return NonDestructiveTest_EditDefectData(request, UTDefectID, NonDestructiveTest_UTDefectForm, UTDefectInformation, func)

# 新建X射线缺陷记录
@permission_required('LAMProcessData.Operator_INSP', login_url=Common_URL['403'])
def NonDestructiveTest_AddRTDefect(request, MissionItemID):
	def func(_form_inst, request, MissionItemID):
		RTDefect = RTDefectInformation.objects.create(
			defect_number=_form_inst.cleaned_data['defect_number'],
			defect_type=_form_inst.cleaned_data['defect_type'],
			size=_form_inst.cleaned_data['size'],
			product_subarea=_form_inst.cleaned_data['product_subarea'],
			X_coordinate=_form_inst.cleaned_data['X_coordinate'],
			Y_coordinate=_form_inst.cleaned_data['Y_coordinate'],
			Z_coordinate=_form_inst.cleaned_data['Z_coordinate'],
		)
		for img in request.FILES.getlist('file[]'):
			_def_pic = DefectPicture.objects.create(
				picture = img
			)
			RTDefect.photos.add(_def_pic)
		RTDefect.save()
		test_mission = NonDestructiveTest_Mission.objects.get(id=MissionItemID)
		test_mission.RT_defect.add(RTDefect.id)
		test_mission.save()

	return NonDestructiveTest_AddDefectData(request, MissionItemID, NonDestructiveTest_RTDefectForm, func)


# 编辑X射线缺陷记录
@permission_required('LAMProcessData.Operator_INSP', login_url=Common_URL['403'])
def NonDestructiveTest_EditRTDefect(request, RTDefectID):
	def func(request, RTDefectID):
		RTDefect = RTDefectInformation.objects.get(id=RTDefectID)
		# 之前上传的图片
		_existing_pictures = list(RTDefect.photos.all())
		# 删除图片
		if 'jfiler-items-exclude-file-0' in request.POST:
			for img_name in json.loads(request.POST['jfiler-items-exclude-file-0']):
				_defectID = int(img_name.split('-')[0].split(':')[1])
				DefectPicture.objects.get(id=_defectID).delete()
		
		# UTDefect.photos.clear()
		# 保存新上传图片
		for img in request.FILES.getlist('file[]'):
			_def_pic = DefectPicture.objects.create(
				picture=img
			)
			RTDefect.photos.add(_def_pic)
		RTDefect.save()
	
	return NonDestructiveTest_EditDefectData(request, RTDefectID, NonDestructiveTest_RTDefectForm, RTDefectInformation, func)


# 新建荧光缺陷记录
@permission_required('LAMProcessData.Operator_INSP', login_url=Common_URL['403'])
def NonDestructiveTest_AddPTDefect(request, MissionItemID):
	def func(_form_inst, request, MissionItemID):
		PTDefect = PTDefectInformation.objects.create(
			defect_number=_form_inst.cleaned_data['defect_number'],
			defect_type=_form_inst.cleaned_data['defect_type'],
			product_subarea=_form_inst.cleaned_data['product_subarea'],
			X_coordinate=_form_inst.cleaned_data['X_coordinate'],
			Y_coordinate=_form_inst.cleaned_data['Y_coordinate'],
			Z_coordinate=_form_inst.cleaned_data['Z_coordinate'],
		)
		for img in request.FILES.getlist('file[]'):
			_def_pic = DefectPicture.objects.create(
				picture=img
			)
			PTDefect.photos.add(_def_pic)
		PTDefect.save()
		test_mission = NonDestructiveTest_Mission.objects.get(id=MissionItemID)
		test_mission.PT_defect.add(PTDefect.id)
		test_mission.save()
	
	return NonDestructiveTest_AddDefectData(request, MissionItemID, NonDestructiveTest_PTDefectForm, func)


# 编辑荧光缺陷记录
@permission_required('LAMProcessData.Operator_INSP', login_url=Common_URL['403'])
def NonDestructiveTest_EditPTDefect(request, PTDefectID):
	def func(request, PTDefectID):
		PTDefect = RTDefectInformation.objects.get(id=PTDefectID)
		# 之前上传的图片
		_existing_pictures = list(PTDefect.photos.all())
		# 删除图片
		if 'jfiler-items-exclude-file-0' in request.POST:
			for img_name in json.loads(request.POST['jfiler-items-exclude-file-0']):
				_defectID = int(img_name.split('-')[0].split(':')[1])
				DefectPicture.objects.get(id=_defectID).delete()
		
		# 保存新上传图片
		for img in request.FILES.getlist('file[]'):
			_def_pic = DefectPicture.objects.create(
				picture=img
			)
			PTDefect.photos.add(_def_pic)
		PTDefect.save()
	
	return NonDestructiveTest_EditDefectData(request, PTDefectID, NonDestructiveTest_PTDefectForm, PTDefectInformation,
	                                         func)


# 新建磁粉缺陷记录
@permission_required('LAMProcessData.Operator_INSP', login_url=Common_URL['403'])
def NonDestructiveTest_AddMTDefect(request, MissionItemID):
	def func(_form_inst, request, MissionItemID):
		MTDefect = MTDefectInformation.objects.create(
			defect_number=_form_inst.cleaned_data['defect_number'],
			defect_type=_form_inst.cleaned_data['defect_type'],
			product_subarea=_form_inst.cleaned_data['product_subarea'],
			X_coordinate=_form_inst.cleaned_data['X_coordinate'],
			Y_coordinate=_form_inst.cleaned_data['Y_coordinate'],
			Z_coordinate=_form_inst.cleaned_data['Z_coordinate'],
		)
		for img in request.FILES.getlist('file[]'):
			_def_pic = DefectPicture.objects.create(
				picture=img
			)
			MTDefect.photos.add(_def_pic)
		MTDefect.save()
		test_mission = NonDestructiveTest_Mission.objects.get(id=MissionItemID)
		test_mission.MT_defect.add(MTDefect.id)
		test_mission.save()
	
	return NonDestructiveTest_AddDefectData(request, MissionItemID, NonDestructiveTest_MTDefectForm, func)


# 编辑磁粉缺陷记录
@permission_required('LAMProcessData.Operator_INSP', login_url=Common_URL['403'])
def NonDestructiveTest_EditMTDefect(request, MTDefectID):
	def func(request, PTDefectID):
		MTDefect = MTDefectInformation.objects.get(id=PTDefectID)
		# 之前上传的图片
		_existing_pictures = list(MTDefect.photos.all())
		# 删除图片
		if 'jfiler-items-exclude-file-0' in request.POST:
			for img_name in json.loads(request.POST['jfiler-items-exclude-file-0']):
				_defectID = int(img_name.split('-')[0].split(':')[1])
				DefectPicture.objects.get(id=_defectID).delete()
		
		# 保存新上传图片
		for img in request.FILES.getlist('file[]'):
			_def_pic = DefectPicture.objects.create(
				picture=img
			)
			MTDefect.photos.add(_def_pic)
		MTDefect.save()
	
	return NonDestructiveTest_EditDefectData(request, MTDefectID, NonDestructiveTest_MTDefectForm, MTDefectInformation,
	                                         func)


# 浏览图片-UT 超声缺陷
@permission_required('LAMProcessData.Operator_INSP', login_url=Common_URL['403'])
def ViewUTDefectPictures(request, UTDefectID):
	UTDefect_obj = UTDefectInformation.objects.get(id=UTDefectID)
	_pictures_list = list(UTDefect_obj.photos.all())

	return render(request, "SubWindow_ViewPhotos.html",
				  {'pictures': _pictures_list,
				   'Defect_obj': UTDefect_obj,
				   'heading': 'UT超声检测缺陷(ID=%s)'%UTDefectID,
				   'Common_URL': Common_URL,
				   })

# 浏览图片-RT 射线缺陷
@permission_required('LAMProcessData.Operator_INSP', login_url=Common_URL['403'])
def ViewRTDefectPictures(request, RTDefectID):
	RTDefect_obj = RTDefectInformation.objects.get(id=RTDefectID)
	_pictures_list = list(RTDefect_obj.photos.all())

	return render(request, "SubWindow_ViewPhotos.html",
				  {'pictures': _pictures_list,
				   'Defect_obj': RTDefect_obj,
				   'heading':  'RT射线检测缺陷(ID=%s)'%RTDefectID,
				   'Common_URL': Common_URL,
				   })

# 浏览图片-PT 荧光缺陷
@permission_required('LAMProcessData.Operator_INSP', login_url=Common_URL['403'])
def ViewPTDefectPictures(request, PTDefectID):
	PTDefect_obj = PTDefectInformation.objects.get(id=PTDefectID)
	_pictures_list = list(PTDefect_obj.photos.all())

	return render(request, "SubWindow_ViewPhotos.html",
				  {'pictures': _pictures_list,
				   'Defect_obj': PTDefect_obj,
				   'heading':  'PT荧光检测缺陷(ID=%s)'%PTDefectID,
				   'Common_URL': Common_URL,
				   })

# 浏览图片-MT 磁粉缺陷
@permission_required('LAMProcessData.Operator_INSP', login_url=Common_URL['403'])
def ViewMTDefectPictures(request, MTDefectID):
	MTDefect_obj = MTDefectInformation.objects.get(id=MTDefectID)
	_pictures_list = list(MTDefect_obj.photos.all())

	return render(request, "SubWindow_ViewPhotos.html",
				  {'pictures': _pictures_list,
				   'Defect_obj': MTDefect_obj,
				   'heading':  'MT磁粉检测缺陷(ID=%s)'%MTDefectID,
				   'Common_URL': Common_URL,
				   })


# 浏览图片-一次检测任务中所有UT超声缺陷照片
@permission_required('LAMProcessData.Operator_INSP', login_url=Common_URL['403'])
def ViewAllUTDefectPictures(request, MissionItemID):
	mission_obj = NonDestructiveTest_Mission.objects.get(id=MissionItemID)
	_pictures_list = []
	for ut_defect_obj in mission_obj.UT_defect.all():
		for photo_obj in ut_defect_obj.photos.all():
			_pictures_list.append(photo_obj)
	return render(request, "SubWindow_ViewPhotos.html",
				  {'pictures': _pictures_list,
				   'heading': '检测任务(ID=%s)中UT超声检测缺陷照片'%MissionItemID,
				   'Common_URL': Common_URL,
				   })

# 浏览图片-一次检测任务中所有RT射线缺陷照片
@permission_required('LAMProcessData.Operator_INSP', login_url=Common_URL['403'])
def ViewAllRTDefectPictures(request, MissionItemID):
	mission_obj = NonDestructiveTest_Mission.objects.get(id=MissionItemID)
	_pictures_list = []
	for rt_defect_obj in mission_obj.RT_defect.all():
		for photo_obj in rt_defect_obj.photos.all():
			_pictures_list.append(photo_obj)
	return render(request, "SubWindow_ViewPhotos.html",
				  {'pictures': _pictures_list,
				   'heading': '检测任务(ID=%s)中RT射线检测缺陷照片'%MissionItemID,
				   'Common_URL': Common_URL,
				   })

# 浏览图片-一次检测任务中所有PT荧光缺陷照片
@permission_required('LAMProcessData.Operator_INSP', login_url=Common_URL['403'])
def ViewAllPTDefectPictures(request, MissionItemID):
	mission_obj = NonDestructiveTest_Mission.objects.get(id=MissionItemID)
	_pictures_list = []
	for pt_defect_obj in mission_obj.PT_defect.all():
		for photo_obj in pt_defect_obj.photos.all():
			_pictures_list.append(photo_obj)
	return render(request, "SubWindow_ViewPhotos.html",
				  {'pictures': _pictures_list,
				   'heading': '检测任务(ID=%s)中PT荧光检测缺陷照片'%MissionItemID,
				   'Common_URL': Common_URL,
				   })

# 浏览图片-一次检测任务中所有MT磁粉缺陷照片
@permission_required('LAMProcessData.Operator_INSP', login_url=Common_URL['403'])
def ViewAllMTDefectPictures(request, MissionItemID):
	mission_obj = NonDestructiveTest_Mission.objects.get(id=MissionItemID)
	_pictures_list = []
	for mt_defect_obj in mission_obj.MT_defect.all():
		for photo_obj in mt_defect_obj.photos.all():
			_pictures_list.append(photo_obj)
	return render(request, "SubWindow_ViewPhotos.html",
				  {'pictures': _pictures_list,
				   'heading': '检测任务(ID=%s)中MT磁粉检测缺陷照片'%MissionItemID,
				   'Common_URL': Common_URL,
				   })

'''============================================================================'''
def download_template(request, tempfilepath):
	file = open(tempfilepath, 'rb')
	response = FileResponse(file)
	response['Content-Type'] = 'application/octet-stream'
	response['Content-Disposition'] = 'attachment'
	# response['Content-Disposition'] = 'attachment;filename="GCodeFile.nc"'
	return response

'''============================================================================'''
@permission_required('LAMProcessData.Technique', login_url=Common_URL['403'])
def AnalyseLAMProcess_DingDingRecords_Upload(request):
	# 上传钉钉日志
	def filter_emoji(desstr, restr=''):
		# 过滤表情
		try:
			res = re.compile(u'[\U00010000-\U0010ffff]')
		except re.error:
			res = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
		return res.sub(restr, desstr)
	
	if request.method != 'POST':
		return render(request, "AnalyseLAMProcess_DingDingRecords_Upload.html",
		              {'Common_URL': Common_URL,})
	else:
		# for img in request.FILES.getlist('image_file[]'):
		# 	_def_pic = DingDingPicture.objects.create(
		# 		picture=img
		# 	)
		# 	DingDingPicture.objects.create()
		try:
			uploadedFile = request.FILES.get('excel_file')
			tempFilePath = uploadedFile.temporary_file_path()
		# for excel in request.FILES.getlist('excel_file'):
			x1 = xlrd.open_workbook(tempFilePath)
			Sheet_obj = x1.sheets()[0]
			nrows = Sheet_obj.nrows  # 获取该sheet中的有效行数
			for i in range(1, nrows):
				row_value = Sheet_obj.row_values(i, start_colx=0, end_colx=None)  # 返回由该行中所有单元格的数据组成的列表
				if row_value[0] == '':
					continue
				try:
					_datetime = datetime.datetime.strptime(row_value[7], "%Y-%m-%d %H:%M")
				except:
					_datetime = datetime.datetime.strptime(row_value[3], "%Y年%m月%d日 %H:%M")
				if len(LAMProcess_DingDingRecord.objects.filter(acquisition_timestamp=int(time.mktime(_datetime.timetuple()))))>0:
					continue
					
				_image_url_list = row_value[12].split('\n')
				_image_name_list = list(map(lambda _url : os.path.basename(_url),  _image_url_list))
				_image_list = list(filter(lambda _temp_image: _temp_image.name in _image_name_list, request.FILES.getlist('image_file[]')))
				_record = LAMProcess_DingDingRecord.objects.create(
					acquisition_time = _datetime,
					acquisition_timestamp = int(time.mktime(_datetime.timetuple())),
					description = row_value[5],
					writer = row_value[1],
					reporter = row_value[10],
					worksection_code = row_value[8]+','+row_value[6],
					product_code = row_value[9],
					comment = filter_emoji(row_value[14]),
				)
				for _img in _image_list:
					_photo_obj = DingDingPicture.objects.create(
						picture=_img
					)
					_record.photos.add(_photo_obj)
				_record.save()
			success = True
		except:
			success = False
				
				
			
		return render(request, "AnalyseLAMProcess_DingDingRecords_Upload.html",
		              {'Common_URL': Common_URL,
		               'save_success':success})

@permission_required('LAMProcessData.Technique', login_url=Common_URL['403'])
def AnalyseLAMProcess_DingDingRecords_Browse(request):
	# 浏览钉钉日志
	Browse_fields = [
		['时间','150px'],
		['事件描述',''],
		['工段','100px'],
		['产品编号','100px'],
	]
	try:
		all_entries = LAMProcess_DingDingRecord.objects.all()
		_modelfilednames = [f.attname for f in LAMProcess_DingDingRecord._meta.fields]
		# attlist = [f.attname for f in LAMProcess_DingDingRecord._meta.fields]
		attlist = ['id','acquisition_time',
		          'description',
		          'worksection_code',
		          'product_code',]
	except:
		pass
	
	all_entries_dict = []
	if all_entries is not None:
		for i in all_entries:
			_dict = {}
			for att in attlist:
				if att in _modelfilednames:
					# 替换_id, 从而获得外键实例的名称
					_dict[att] = str(i.__getattribute__(att.replace('_id', '')))
				else:
					_dict[att] = list(map(str, list(i.__getattribute__(att).all())))
			
			# _dict['displayname'] = str(i)
			
			_dict['description'] = _dict['description'][:100]+'...' if len(_dict['description'])>100 else _dict['description']
			all_entries_dict.append(_dict)
	
	
	# all_entries = list(LAMProcess_DingDingRecord.objects.all().order_by('acquisition_timestamp'))
	_form_inst = DingDingRecordsForm_Browse()
	return render(request, "AnalyseLAMProcess_DingDingRecords_Browse.html",
	              {'Common_URL': Common_URL,
	               'Browse_fields':Browse_fields,
	               'all_entries':all_entries_dict,
	               'form':_form_inst,
	               })


@permission_required('LAMProcessData.Technique', login_url=Common_URL['403'])
def PracticalTools_BreakBlockResumption(request):
	# 复位后自上次已成形的分块继续成形

	def NCFileInsert(file, param):
		newText = []
		lines = file.readlines()
		# True 进入函数内  False 出函数
		new_function_flag = False
		block_num = 1
		_linecount = len(lines)
		_writeCacheCount = int(_linecount/20)
		for lineid, oneline in enumerate(lines):
			if lineid % _writeCacheCount == 0:
				CacheOperator('ProgressBarValue_PracticalTools_BreakBlockResumption_By_GUID', False, GUID, lineid / _linecount)

			oneline = str(oneline, encoding="utf8")
			block_in_flag = False
			block_out_flag = False

			if '%L' in oneline:
				new_function_flag = True
			if '#RET' in oneline:
				new_function_flag = False
				block_num = 1

			if new_function_flag:
				if '.igs))' in oneline or '-F)' in oneline or '-B)' in oneline:
					# 此处刚刚进入分块内，添加判断信息
					block_in_flag = True
				# block_num = int(oneline.split('-')[0][1:])

				if '#CALL 1121' in oneline:
					# 将要走出分块，需要添加结束信息
					block_out_flag = True
					block_num += 1
			newline = '\t' if (new_function_flag and not block_in_flag and '%L' not in oneline) else ''

			if block_in_flag:
				newline += '$IF [%s<=%d]\n\t' % (param[3], block_num)

			newline += oneline
			if block_out_flag:
				newline += '\t%s=%d\n' % (param[3], block_num)
				newline += '\t%s=V.A.PPOS.X\n' % (param[0])
				newline += '\t%s=V.A.PPOS.Y\n' % (param[1])
				newline += '\t%s=V.A.PPOS.Z\n' % (param[2])
				newline += '$ENDIF\n'
			newText.append(newline.encode())
		if newText !=[]:
			_tempfile = tempfile.NamedTemporaryFile(prefix='LAMServer', delete=False)
			_tempfile.writelines(newText)
			_tempfile.close()
			return _tempfile.name
		else:
			return None
		# with open(readfilename + ' %s.NC' % time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time())), 'w') as file:
		# 	file.write(newText)
		# print('finish')
	'''主函数开始'''
	print('start PracticalTools_BreakBlockResumption')
	tempfile_name = None
	if request.method != 'POST':
		# 创建一个空表单在页面显示
		_form_inst = BreakBlockResumptionForm()
		save_success=None
	else:
		# 否则为POST方式
		# request.POST方法，将会获取到表单中我们输入的数据
		_form_inst = BreakBlockResumptionForm(request.POST)
		# 验证其合法性，使用is_valid()方法
		GUID = request.POST['GUID']
		file = request.FILES.get('File', None)
		ParamCurrentPPOSX = request.POST['ParamCurrentPPOSX']
		ParamCurrentPPOSY = request.POST['ParamCurrentPPOSY']
		ParamCurrentPPOSZ = request.POST['ParamCurrentPPOSZ']
		ParamCounter = request.POST['ParamCounter']

		if file:
			if file.size != 0:
				tempfile_name = NCFileInsert(file, [ParamCurrentPPOSX, ParamCurrentPPOSY, ParamCurrentPPOSZ, ParamCounter])
				save_success = 'True'
		else:
			save_success = 'False'

	return render(request, "PracticalTools.html",
				  {'form': _form_inst,
				   'Common_URL': Common_URL,
				   'tempfile_name':tempfile_name,
				   'save_success':save_success,
				   })


@permission_required('LAMProcessData.Technique', login_url=Common_URL['403'])
def PracticalTools_SShapeBreak(request):
	# 连续弓字步拆分扫描

	'''主函数开始'''
	print('start PracticalTools_SShapeBreak')
	tempfile_name = None
	if request.method != 'POST':
		# 创建一个空表单在页面显示
		_form_inst = SShapeBreakForm()
		save_success = None
	else:
		# 否则为POST方式
		# request.POST方法，将会获取到表单中我们输入的数据
		_form_inst = SShapeBreakForm(request.POST)
		# 验证其合法性，使用is_valid()方法
		file = request.FILES.get('File', None)
		# PowderOnOrder = request.POST['PowderOnOrder']
		# PowderOffOrder = request.POST['PowderOffOrder']
		GUID = request.POST['GUID']
		TurningFunction = request.POST['TurningFunction']
		SwitchBlockFunction = request.POST['SwitchBlockFunction']
		IfPrintTurningFunction = request.POST['IfPrintTurningFunction'] if 'IfPrintTurningFunction' in request.POST else False
		IfPrintSwitchBlockFunction = request.POST['IfPrintSwitchBlockFunction'] if 'IfPrintSwitchBlockFunction' in request.POST else False

		print(request.POST)
		if file:
			if file.size != 0:
				args = [
					file.name,
					file,
					# PowderOnOrder,
					# PowderOffOrder,
					TurningFunction,
					SwitchBlockFunction,
					IfPrintTurningFunction,
					IfPrintSwitchBlockFunction,
					GUID,
				]
				# newText = SShapeBreak.MakeSShapeBreakGCode(file.name, file)
				# ProgressBarValue_PracticalTools_SShapeBreak_By_GUID
				newText = SShapeBreak.MakeSShapeBreakGCode(*args)
				_tempfile = tempfile.NamedTemporaryFile(prefix='LAMServer', delete=False)
				_tempfile.writelines(newText)
				_tempfile.close()
				tempfile_name = _tempfile.name
				# tempfile_name = NCFileInsert(file, [ParamCurrentPPOSX, ParamCurrentPPOSY, ParamCurrentPPOSZ, ParamCounter])
				save_success = 'True'
		else:
			save_success = 'False'

	return render(request, "PracticalTools.html",
				  {'form': _form_inst,
				   'Common_URL': Common_URL,
				   'tempfile_name':tempfile_name,
				   'save_success': save_success,
				   })



@permission_required('LAMProcessData.Technique', login_url=Common_URL['403'])
def PracticalTools_MakeMainProgramFile_8070(request):
	# 生成主程序段并提供下载

	'''主函数开始'''
	print('start PracticalTools_MakeMainProgramFile')
	tempfile_name = None
	if request.method != 'POST':
		# 创建一个空表单在页面显示
		_form_inst = MainProgramFileForm()
		save_success = None
		return render(request, "PracticalTools_MakeMainProgramFile.html",
		              {'form': _form_inst,
		               'Common_URL': Common_URL,
		               'tempfile_name': tempfile_name,
		               'save_success': save_success,
		               })

@permission_required('LAMProcessData.Technique', login_url=Common_URL['403'])
def PracticalTools_MakeMainProgramFile_8070_MakeCode(request):
	if request.method == 'POST':
		def makecode(_func):
			if _func['type_code'] in ['1', '2', '3', '4', '5', '6', '8']:
				# 是否定截面
				IfConstantLayer = True if _func['thickness'] >= _func['finish_z_value'] - _func['start_z_value'] else False
				TabText = '\t'
				gcode = '(%s)\n(%s)\n%%L %s\n\n' % (_func['type'], _func['note'], _func['name'])
				if _func['type_code'] == '1':
					# '8周期（弓字步正搭接填充）'
					
					if IfConstantLayer:
						# 定截面
						gcode += '\t$IF [P114>=%.3f] * [P114<%.3f]\n' % (_func['start_z_value'], _func['finish_z_value'])
						if _func['if_contour']:
							gcode += '\t\t$IF [P200==1] * [P110==1] * [P112==1]\n' \
							         '\t\t\t#CALL %d.NC\n' \
							         '\t\t$ELSEIF [P200==1] * [P110==2] * [P112==1]\n' \
							         '\t\t\t#CALL %d.NC\n' \
							         '\t\t$ENDIF\n' % (_func['first_function_number'] + 8, _func['first_function_number'] + 9)
						gcode += '\t\t$IF [P110==1] * [P111==1]\n' \
						         '\t\t\t#CALL %d.NC\n' \
						         '\t\t$ELSEIF [P110==2] * [P111==1]\n' \
						         '\t\t\t#CALL %d.NC\n' \
						         '\t\t$ELSEIF [P110==1] * [P111==2]\n' \
						         '\t\t\t#CALL %d.NC\n' \
						         '\t\t$ELSEIF [P110==2] * [P111==2]\n' \
						         '\t\t\t#CALL %d.NC\n' \
						         '\t\t$ELSEIF [P110==1] * [P111==3]\n' \
						         '\t\t\t#CALL %d.NC\n' \
						         '\t\t$ELSEIF [P110==2] * [P111==3]\n' \
						         '\t\t\t#CALL %d.NC\n' \
						         '\t\t$ELSEIF [P110==1] * [P111==4]\n' \
						         '\t\t\t#CALL %d.NC\n' \
						         '\t\t$ELSEIF [P110==2] * [P111==4]\n' \
						         '\t\t\t#CALL %d.NC\n' \
						         '\t\t$ENDIF\n' % tuple([_func['first_function_number'] + i for i in [0, 4, 1, 5, 2, 6, 3, 7]])
						if _func['if_contour']:
							gcode += '\t\t$IF [P200==1] * [P110==1] * [P112==0]\n' \
							         '\t\t\t#CALL %d.NC\n' \
							         '\t\t$ELSEIF [P200==1] * [P110==2] * [P112==0]\n' \
							         '\t\t\t#CALL %d.NC\n' \
							         '\t\t$ENDIF\n' % (_func['first_function_number'] + 8, _func['first_function_number'] + 9)
						gcode += '\t$ENDIF \n'
					
					else:
						# 变截面
						layers = int((_func['finish_z_value'] - _func['start_z_value']) / _func['thickness'])
						
						for i in range(layers):
							gcode += '\t%s [P114>=%.3f] * [P114<%.3f]\n' % (
										["$IF", "$ELSEIF"][i > 0],
										_func['start_z_value'] + i * _func['thickness'],
										_func['start_z_value'] + (i + 1) * _func['thickness'])
							if _func['if_contour']:
								gcode += '\t\t$IF [P200==1] * [P110==1] * [P112==1]\n' \
								         '\t\t\t#CALL %d.NC\n' \
								         '\t\t$ELSEIF [P200==1] * [P110==2] * [P112==1]\n' \
								         '\t\t\t#CALL %d.NC\n' \
								         '\t\t$ENDIF\n' %  tuple([_func['first_function_number'] + layers * j + i for j in range(8,10)])
							gcode += '\t\t$IF [P110==1] * [P111==1]\n' \
							         '\t\t\t#CALL %d.NC\n' \
							         '\t\t$ELSEIF [P110==2] * [P111==1]\n' \
							         '\t\t\t#CALL %d.NC\n' \
							         '\t\t$ELSEIF [P110==1] * [P111==2]\n' \
							         '\t\t\t#CALL %d.NC\n' \
							         '\t\t$ELSEIF [P110==2] * [P111==2]\n' \
							         '\t\t\t#CALL %d.NC\n' \
							         '\t\t$ELSEIF [P110==1] * [P111==3]\n' \
							         '\t\t\t#CALL %d.NC\n' \
							         '\t\t$ELSEIF [P110==2] * [P111==3]\n' \
							         '\t\t\t#CALL %d.NC\n' \
							         '\t\t$ELSEIF [P110==1] * [P111==4]\n' \
							         '\t\t\t#CALL %d.NC\n' \
							         '\t\t$ELSEIF [P110==2] * [P111==4]\n' \
							         '\t\t\t#CALL %d.NC\n' \
							         '\t\t$ENDIF\n' % tuple([_func['first_function_number'] + layers * j + i for j in [0,4,1,5,2,6,3,7]])
							if _func['if_contour']:
								gcode += '\t\t$IF [P200==1] * [P110==1] * [P112==0]\n' \
								         '\t\t\t#CALL %d.NC\n' \
								         '\t\t$ELSEIF [P200==1] * [P110==2] * [P112==0]\n' \
								         '\t\t\t#CALL %d.NC\n' \
								         '\t\t$ENDIF\n' % tuple([_func['first_function_number'] + layers * j + i for j in range(8,10)])
							
						gcode += '\t$ENDIF\n'
				
				elif _func['type_code'] == '2':
					# '4周期（弓字步负搭接填充/回填负搭接填充）'
					if IfConstantLayer:
						# 定截面
						gcode += '\t$IF [P114>=%.3f] * [P114<%.3f]\n' % (_func['start_z_value'], _func['finish_z_value'])
						if _func['if_contour']:
							gcode += '\t\t$IF [P200==1] * [P110==1] * [P112==1]\n' \
							         '\t\t\t#CALL %d.NC\n' \
							         '\t\t$ELSEIF [P200==1] * [P110==2] * [P112==1]\n' \
							         '\t\t\t#CALL %d.NC\n' \
							         '\t\t$ENDIF\n' % (
							         _func['first_function_number'] + 4, _func['first_function_number'] + 5)
						gcode += '\t\t$IF [P110==1] * [[P111 MOD 2]==1]\n' \
						         '\t\t\t#CALL %d.NC\n' \
						         '\t\t$ELSEIF [P110==2] * [[P111 MOD 2]==1]\n' \
						         '\t\t\t#CALL %d.NC\n' \
						         '\t\t$ELSEIF [P110==1] * [[P111 MOD 2]==0]\n' \
						         '\t\t\t#CALL %d.NC\n' \
						         '\t\t$ELSEIF [P110==2] * [[P111 MOD 2]==0]\n' \
						         '\t\t\t#CALL %d.NC\n' \
						         '\t\t$ENDIF\n' % tuple(
							[_func['first_function_number'] + i for i in [0, 2, 1, 3]])
						if _func['if_contour']:
							gcode += '\t\t$IF [P200==1] * [P110==1] * [P112==0]\n' \
							         '\t\t\t#CALL %d.NC\n' \
							         '\t\t$ELSEIF [P200==1] * [P110==2] * [P112==0]\n' \
							         '\t\t\t#CALL %d.NC\n' \
							         '\t\t$ENDIF\n' % (
							         _func['first_function_number'] + 4, _func['first_function_number'] + 5)
						gcode += '\t$ENDIF \n'
					else:
						# 变截面
						layers = int((_func['finish_z_value'] - _func['start_z_value']) / _func['thickness'])
						for i in range(layers):
							gcode += '\t%s [P114>=%.3f] * [P114<%.3f]\n' % (
								["$IF", "$ELSEIF"][i > 0],
								_func['start_z_value'] + i * _func['thickness'],
								_func['start_z_value'] + (i + 1) * _func['thickness'])
							if _func['if_contour']:
								gcode += '\t\t$IF [P200==1] * [P110==1] * [P112==1]\n' \
								         '\t\t\t#CALL %d.NC\n' \
								         '\t\t$ELSEIF [P200==1] * [P110==2] * [P112==1]\n' \
								         '\t\t\t#CALL %d.NC\n' \
								         '\t\t$ENDIF\n' % tuple(
									[_func['first_function_number'] + layers * j + i for j in range(4, 6)])
							gcode += '\t\t$IF [P110==1] * [[P111 MOD 2]==1]\n' \
							         '\t\t\t#CALL %d.NC\n' \
							         '\t\t$ELSEIF [P110==2] * [[P111 MOD 2]==1]\n' \
							         '\t\t\t#CALL %d.NC\n' \
							         '\t\t$ELSEIF [P110==1] * [[P111 MOD 2]==0]\n' \
							         '\t\t\t#CALL %d.NC\n' \
							         '\t\t$ELSEIF [P110==2] * [[P111 MOD 2]==0]\n' \
							         '\t\t\t#CALL %d.NC\n' \
							         '\t\t$ENDIF\n' % tuple(
								[_func['first_function_number'] + layers * j + i for j in [0, 2, 1, 3]])
							if _func['if_contour']:
								gcode += '\t\t$IF [P200==1] * [P110==1] * [P112==0]\n' \
								         '\t\t\t#CALL %d.NC\n' \
								         '\t\t$ELSEIF [P200==1] * [P110==2] * [P112==0]\n' \
								         '\t\t\t#CALL %d.NC\n' \
								         '\t\t$ENDIF\n' % tuple(
									[_func['first_function_number'] + layers * j + i for j in range(4, 6)])
						gcode += '\t$ENDIF\n'
				elif _func['type_code'] == '3':
					# '4周期（轮廓偏移填充）'
					if IfConstantLayer:
						# 定截面
						gcode += '\t$IF [P114>=%.3f] * [P114<%.3f]\n' % (_func['start_z_value'], _func['finish_z_value'])
						gcode += '\t\t$IF [P110==1] * [[P111 MOD 2]==1]\n' \
						         '\t\t\t#CALL %d.NC\n' \
						         '\t\t$ELSEIF [P110==2] * [[P111 MOD 2]==1]\n' \
						         '\t\t\t#CALL %d.NC\n' \
						         '\t\t$ELSEIF [P110==1] * [[P111 MOD 2]==0]\n' \
						         '\t\t\t#CALL %d.NC\n' \
						         '\t\t$ELSEIF [P110==2] * [[P111 MOD 2]==0]\n' \
						         '\t\t\t#CALL %d.NC\n' \
						         '\t\t$ENDIF\n' % tuple(
							[_func['first_function_number'] + i for i in [0, 2, 1, 3]])
						gcode += '\t$ENDIF \n'
					else:
						# 变截面
						layers = int((_func['finish_z_value'] - _func['start_z_value']) / _func['thickness'])
						for i in range(layers):
							gcode += '\t%s [P114>=%.3f] * [P114<%.3f]\n' % (
								["$IF", "$ELSEIF"][i > 0],
								_func['start_z_value'] + i * _func['thickness'],
								_func['start_z_value'] + (i + 1) * _func['thickness'])
							gcode += '\t\t$IF [P110==1] * [[P111 MOD 2]==1]\n' \
							         '\t\t\t#CALL %d.NC\n' \
							         '\t\t$ELSEIF [P110==2] * [[P111 MOD 2]==1]\n' \
							         '\t\t\t#CALL %d.NC\n' \
							         '\t\t$ELSEIF [P110==1] * [[P111 MOD 2]==0]\n' \
							         '\t\t\t#CALL %d.NC\n' \
							         '\t\t$ELSEIF [P110==2] * [[P111 MOD 2]==0]\n' \
							         '\t\t\t#CALL %d.NC\n' \
							         '\t\t$ENDIF\n' % tuple(
								[_func['first_function_number'] + layers * j + i for j in [0, 2, 1, 3]])
						gcode += '\t$ENDIF\n'
				elif _func['type_code'] == '4' or _func['type_code'] == '5':
					# '2周期（轮廓线扫描）'
					# '2周期（低功率扫坡口根部）'
					if IfConstantLayer:
						# 定截面
						gcode += '\t$IF [P114>=%.3f] * [P114<%.3f]\n' % (_func['start_z_value'], _func['finish_z_value'])
						gcode += '\t\t$IF [P110==1]\n' \
						         '\t\t\t#CALL %d.NC\n' \
						         '\t\t$ELSEIF [P110==2]\n' \
						         '\t\t\t#CALL %d.NC\n' \
						         '\t\t$ENDIF\n' % tuple(
							[_func['first_function_number'] + i for i in [0, 1]])
						gcode += '\t$ENDIF \n'
					else:
						# 变截面
						layers = int((_func['finish_z_value'] - _func['start_z_value']) / _func['thickness'])
						for i in range(layers):
							gcode += '\t%s [P114>=%.3f] * [P114<%.3f]\n' % (
								["$IF", "$ELSEIF"][i > 0],
								_func['start_z_value'] + i * _func['thickness'],
								_func['start_z_value'] + (i + 1) * _func['thickness'])
							gcode += '\t\t$IF [P110==1]\n' \
							         '\t\t\t#CALL %d.NC\n' \
							         '\t\t$ELSEIF [P110==2]\n' \
							         '\t\t\t#CALL %d.NC\n' \
							         '\t\t$ENDIF\n' % tuple(
								[_func['first_function_number'] + layers * j + i for j in [0, 1]])
						gcode += '\t$ENDIF\n'
				
				elif _func['type_code'] == '6':
					# 'N周期（定期补偿成形）'
					if IfConstantLayer:
						# 定截面
						gcode += '\t$IF [P114>=%.3f] * [P114<%.3f]\n' % (_func['start_z_value'], _func['finish_z_value'])
						gcode += '\t\t$IF [P213==1]\n' \
						         '\t\t\t#CALL %d.NC\n' \
						         '\t\t$ELSEIF [P213==2]\n' \
						         '\t\t\t#CALL %d.NC\n' \
						         '\t\t$ELSEIF [P213==3]\n' \
						         '\t\t\t#CALL %d.NC\n' \
						         '\t\t$ELSEIF [P213==4]\n' \
						         '\t\t\t#CALL %d.NC\n' \
						         '\t\t$ENDIF\n' % tuple(
							[_func['first_function_number'] + i for i in [0, 2, 1, 3]])
						gcode += '\t$ENDIF \n'
					else:
						# 变截面
						layers = int((_func['finish_z_value'] - _func['start_z_value']) / _func['thickness'])
						for i in range(layers):
							gcode += '\t%s [P114>=%.3f] * [P114<%.3f]\n' % (
								["$IF", "$ELSEIF"][i > 0],
								_func['start_z_value'] + i * _func['thickness'],
								_func['start_z_value'] + (i + 1) * _func['thickness'])
							gcode += '\t\t$IF [P213==1]\n' \
							         '\t\t\t#CALL %d.NC\n' \
							         '\t\t$ELSEIF [P213==2]\n' \
							         '\t\t\t#CALL %d.NC\n' \
							         '\t\t$ELSEIF [P213==3]\n' \
							         '\t\t\t#CALL %d.NC\n' \
							         '\t\t$ELSEIF [P213==4]\n' \
							         '\t\t\t#CALL %d.NC\n' \
							         '\t\t$ENDIF\n' % tuple(
								[_func['first_function_number'] + layers * j + i for j in [0, 2, 1, 3]])
						gcode += '\t$ENDIF\n'
						
				elif _func['type_code'] == '8':
					# '1周期（轮廓线扫描）'
					if IfConstantLayer:
						# 定截面
						gcode += '\t$IF [P114>=%.3f] * [P114<%.3f]\n' % (
						_func['start_z_value'], _func['finish_z_value'])
						gcode += '\t\t#CALL %d.NC\n'  % (_func['first_function_number'])
						gcode += '\t$ENDIF \n'
					else:
						# 变截面
						layers = int((_func['finish_z_value'] - _func['start_z_value']) / _func['thickness'])
						for i in range(layers):
							gcode += '\t%s [P114>=%.3f] * [P114<%.3f]\n' % (
								["$IF", "$ELSEIF"][i > 0],
								_func['start_z_value'] + i * _func['thickness'],
								_func['start_z_value'] + (i + 1) * _func['thickness'])
							gcode += '\t\t#CALL %d.NC\n'  % tuple(
								[_func['first_function_number'] + layers * j + i for j in [0]])
						gcode += '\t$ENDIF\n'
				gcode += '#RET\n'
			else:
				gcode = ''
			return gcode
		
		
		SubFunction_JsonData = json.loads(request.POST['SubFunction_Text'])
		Template_Content = request.POST
		FunctionList = []
		_startZValue, _finishZValue = None, None
		for key_id in SubFunction_JsonData:
			sub_func_infolist = SubFunction_JsonData[key_id]
			if not _startZValue or _startZValue > sub_func_infolist[4]:
				_startZValue = sub_func_infolist[4]
			if not _finishZValue or _finishZValue < sub_func_infolist[5]:
				_finishZValue = sub_func_infolist[5]
			_func = {
				'id': int(sub_func_infolist[0]),
				'type': sub_func_infolist[1],
				'name': sub_func_infolist[2],
				'note': sub_func_infolist[3],
				'start_z_value': float(sub_func_infolist[4]),
				'finish_z_value': float(sub_func_infolist[5]),
				'thickness': float(sub_func_infolist[6]) if sub_func_infolist[6] != '/' else None,
				'first_function_number': float(sub_func_infolist[7]) if sub_func_infolist[7] != '/' else None,
				'if_contour': True if sub_func_infolist[8] == 'true' else False,
				'delay_time':int(sub_func_infolist[9]) if sub_func_infolist[9] != '/' else None,
				'type_code': str(sub_func_infolist[10][0]),
				'powder_turn_On': [],
			}
			_func['gcode'] = makecode(_func)
			FunctionList.append(_func)
			pass
		if len(FunctionList)>0:
			START_Z_VALUE = min(map(lambda func: func['start_z_value'], FunctionList ))
			FINISH_Z_VALUE = max(map(lambda func: func['finish_z_value'], FunctionList ))
		else:
			START_Z_VALUE, FINISH_Z_VALUE=0, 0
			
		# Powder_On_Throughout  是否始终保持开粉状态
		# 若有暂停或者有空扫操作，则为False，否则为True
		if any([func['type_code']=='7' for func in FunctionList]) or any([func['type_code']=='5' for func in FunctionList]):
			Powder_On_Throughout = False
		else:
			Powder_On_Throughout = True
		# 根据不同函数的高度段切分高度范围
		StartZValue_list = [func['start_z_value'] for func in FunctionList]
		FinishZValue_list = [func['finish_z_value'] for func in FunctionList]
		ZValue_list = list(set(StartZValue_list + FinishZValue_list + [START_Z_VALUE, FINISH_Z_VALUE]))
		ZValue_list.sort()
		ZValue_range_list = list(zip(ZValue_list[:-1], ZValue_list[1:]))
		FunctionIfcontain_ZValueRange_list = [[ func['start_z_value']<= Zrange[0] and func['finish_z_value']>= Zrange[1]  for Zrange in ZValue_range_list] for func in FunctionList]
		# 针对每个高度段，若本函数需关粉而后面非None的函数需开粉，则本函数结束后应开粉
		FunctionIfNeedPowder_DivideBy_ZRange = [
			[None
			    if not j[zrange_id] else
			 FunctionList[func_id]['type_code'] in ['1', '2', '3', '4', '6', '8']
			 for func_id, j in enumerate(FunctionIfcontain_ZValueRange_list)]
			for zrange_id, Zrange in enumerate(ZValue_range_list)]
		for func_id, func in enumerate(FunctionList):
			if func['type_code'] in ['1', '2', '3', '4', '6', '8']:
				continue
			for zrange_id, zrange_by_func_list in enumerate(FunctionIfNeedPowder_DivideBy_ZRange):
				# 仅对关粉阶段进行识别，过滤zrange_by_func_list中标记为None的阶段
				if zrange_by_func_list[func_id] == False:
					rest_Not_None_list = list(filter(lambda x: x != None, zrange_by_func_list[func_id+1:]))
					if len(rest_Not_None_list) > 0:
						if rest_Not_None_list[0]:
							if len(func['powder_turn_On'])==0:
								func['powder_turn_On'].append(list(ZValue_range_list[zrange_id]))
							elif func['powder_turn_On'][-1][1] == ZValue_range_list[zrange_id][0]:
								# 将相邻的两个范围合并
								func['powder_turn_On'][-1][1] = ZValue_range_list[zrange_id][1]
							else:
								func['powder_turn_On'].append(list(ZValue_range_list[zrange_id]))
		
		
		return render(request, 'Template_Fagor8070.html',
		              {
			              'START_Z_VALUE':START_Z_VALUE,
			              'FINISH_Z_VALUE':FINISH_Z_VALUE,
			              'Program_FileCode':request.POST['Program_FileCode'],
			              'Program_DrawingCode':request.POST['Program_DrawingCode'],
			              'Program_TechInstCode':request.POST['Program_TechInstCode'],
			              'Program_WorksectionCode':request.POST['Program_WorksectionCode'],
			              'Program_Code':request.POST['Program_Code'],
			              'Program_SubFunctionPath':request.POST['Program_SubFunctionPath'],
			              'Program_Pace':request.POST['Program_Pace'],
			              'Powder_On_Order':request.POST['Powder_Order'].split('/')[0],
			              'Powder_Off_Order':request.POST['Powder_Order'].split('/')[1],
			              'FunctionList':FunctionList,
			              'Powder_On_Throughout':Powder_On_Throughout,
			              # 'Cooldown_Time':int(request.POST['Cooldown_Time']),
			              'DateTime':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
			              
			              
		              })

@permission_required('LAMProcessData.Technique', login_url=Common_URL['403'])
def PracticalTools_MakeMainProgramFile_8070_AddStructure(request, StructureCode):
# 	新增一个结构
# (
#     '连续函数',
#     (
#         (1, '8周期（弓字步正搭接填充）'),
#         (2, '4周期（弓字步负搭接填充/回填负搭接填充/轮廓偏移填充）'),
#         (3, '2周期（轮廓线扫描）'),
#         (4, '2周期（低功率扫坡口根部）'),
#         (5, 'N周期（定期补偿成形）'),
#     )
# ),
# (
#     '分段函数',
#     (
#         (11, '8周期（弓字步正搭接填充）'),
#         (12, '4周期（弓字步负搭接填充/回填负搭接填充/轮廓偏移填充）'),
#         (13, '2周期（轮廓线扫描）'),
#     )
# )
	
	# 创建一个空表单在页面显示
	_form_inst = MainProgram_8070_Function_Form()
	_form_inst.InitFields_By_StructureCode(StructureCode, operation='new')

	return render(request, "SubWindow_SimpleForm_with_table.html",
	              {'form': _form_inst,
	               'StructureCode':StructureCode,
	               'operate': 'new',
	               # 'save_success': save_success,
	               'Common_URL': Common_URL,
	               })

@permission_required('LAMProcessData.Technique', login_url=Common_URL['403'])
def PracticalTools_MakeMainProgramFile_8070_EditStructure(request, StructureCode, StructureID):
	# 创建一个空表单在页面显示
	
	# StructureCode = request.POST['StructureCode']
	_form_inst = MainProgram_8070_Function_Form()
	_form_inst.InitFields_By_StructureCode(StructureCode, operation='edit')
	
	return render(request, "SubWindow_SimpleForm_with_table.html",
	              {'form': _form_inst,
	               'StructureCode': StructureCode,
	               'StructureID': StructureID,
	               'operate': 'edit',
	               # 'save_success': save_success,
	               'Common_URL': Common_URL,
	               })

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
		try:
			grayImage = cv2.cvtColor(IdentifyRegion_Image, cv2.COLOR_BGR2GRAY)
		except:
			grayImage = IdentifyRegion_Image
		ret2, thresh = cv2.threshold(grayImage, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
		del IdentifyRegion_Image
		del grayImage
		del cutimageCoordinate
		gc.collect()
		return ret2, thresh

	def getCutImgCode(image, regionCoordinate):
		ret2, thresh = getCutImg(image, regionCoordinate)
		re = dHash_ndarray(thresh)
		del thresh
		# gc.collect()
		return re
	def matchDeviceCode(device):
		return device["DeviceCode"].upper() == DeviceCode.upper()
	
	def LoadScreen_from_Str(np_str):
		np_json = json.loads(np_str)
		re_img = np.array(np_json).astype('uint8')
		return re_img
	# def checkImage(image, Device):
	# 	if not Device:
	# 		pass
	# 	if_auto_exec_intr = False
	# 	if_exec_intr = False
	# 	if_interrupt_intr = False  # 与if_exec_intr互斥
	# 	'''判断是否为自动界面'''
	# 	if getCutImgCode(image, Device["IdentifyAutoRegion"]) == Device["IdentifyAutoCode"]:
	# 		if_auto_exec_intr = True
	# 		'''判断是否执行程序中断'''
	# 		if getCutImgCode(image, Device["IdentifyInterruptRegion"]) == Device["IdentifyInterruptCode"]:
	# 			if_interrupt_intr=True
	# 		'''判断是否在执行程序'''
	# 		if getCutImgCode(image, Device["IdentifyExecuteRegion"]) == Device["IdentifyExecuteCode"]:
	# 			if_exec_intr = True
	# 	return if_auto_exec_intr, if_exec_intr, if_interrupt_intr




	if request.method == 'POST':
		# 清理缓存
		lastcleanuptime = CacheOperator('CleanUpTime', True, ())

		if lastcleanuptime == None or time.time()-lastcleanuptime>600:
			# 10min
			cleanup()
			CacheOperator('CleanUpTime',False,(),time.time())

		# print(request.POST.get('macaddress', None))
		# print(request.DATA.get('data', None))
		try:
			file = request.FILES.get('file', None)
		except:
			file = None
		np_str = request.POST.get('np_str', None)
		
		# print(file)
		# if file:
		# 	if file.size != 0:
		
		if np_str:
			if len(np_str) != 0:
				# _mac_add = request.POST.get('macaddress', None)
				'''# 此处应改为现场电脑时间'''
				try:
					try:
						_acqu_time = datetime.datetime.strptime(request.POST.get('acqu_time', str(datetime.datetime.now())), '%Y-%m-%d %H:%M:%S.%f')
					except:
						_acqu_time = datetime.datetime.strptime(
							request.POST.get('acqu_time', str(datetime.datetime.now())), '%Y-%m-%d %H:%M:%S')
				except:
					logger.error('CNC PostData "acqu_time" Error:%s'%request.POST.get('acqu_time'))
					_acqu_time = datetime.datetime.now()
				_acqu_time = datetime.datetime.now()
				# print('5')

				# print(request.POST.get('macaddress', None))
				# computer = Computer.objects.get(mac_address=_mac_add)
				# worksection = Worksection.objects.get(cnc_computer=computer)
				worksection = getWorksectionByCNCMacAddress(request.POST.get('macaddress', None))
				DeviceCode = worksection.code
				# cv2.imshow('result.jpg', LoadScreen_from_Str(np_str))
				# cv2.waitKey(0)
				# cv2.destroyAllWindows()
				# cv2.waitKey(1)
				Device = filter(matchDeviceCode, ImageSectionInfo_dict).__next__()

				
				if file:
					# 以文件传递图片
					image1 = np.asarray(bytearray(file.read()), dtype='uint8')
					if image1 is None:
						logger.error('Image is None Type')
					image = cv2.imdecode(image1, cv2.IMREAD_COLOR)
				elif np_str:
					# 以json字符串格式传递图片
					image = LoadScreen_from_Str(np_str)
				if_auto_exec_intr, if_exec_intr, if_interrupt_intr = ImageRecognition.checkImage(image, Device)
				# image = cv2.imread(path)
				# RecognitionImage(image, DeviceCode, 'eng')
				# print('6')
				if file:
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
					'''此处应更改，记录手动界面'''
					# 若截图为执行状态，则保留文件，否则跳过
					if file:
						_status.screen_image = file
					realtime_recognition = ImageRecognition.realtimeRecognizeImage(image, DeviceCode)

					try:
						_status.ZValue = float(realtime_recognition['ZValue'])
						# print(realtime_recognition)
						# 更新近期实时记录
						RealtimeRecord.Realtime_Records.addRecords(worksection.id, 'cncstatus', _timestamp, float(_status.ZValue))
						# 更新精细数据表
						RT_FineData.Realtime_FineData.add_processRecord(_timestamp,
																		worksection.id,
																		{
																			'X_value': float(realtime_recognition['XValue']),
																			'Y_value': float(realtime_recognition['YValue']),
																			'Z_value': float(realtime_recognition['ZValue']),
																			'ScanningRate_value': float(realtime_recognition['ScanningRate']),
																			'FeedRate_value': float(realtime_recognition['FeedRate']),
																			'if_exec_intr': if_exec_intr,
																			'if_interrupt_intr': if_interrupt_intr})
					except:
						pass
				_status.save()
				# updateProcessDataIndexingInfo(worksection, dateint, datatype, data_id):
				'''停止更新Process_CNCStatusdata_Date_Worksection_indexing'''
				# updateProcessDataIndexingInfo(worksection,
				# 							  int(_acqu_time.strftime('%Y%m%d')),
				# 							  'cncstatus',
				# 							  _status.id)
				
				# '''保存至实时截图路径'''
				# filepath = '.' + settings.REAL_TIME_SCREEN_URL + '/' + str(worksection.code) + '.png'
				# # print(filepath)
				# _file = open(filepath, 'wb+')
				# for chunk in file.chunks():
				# 	_file.write(chunk)
				# _file.close()
				
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

				item_CNCProcessAutoData = item_CNCProcessStatus.autodata
				if item_CNCProcessAutoData is None:
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
					item_CNCProcessStatus.autodata = item_CNCProcessAutoData
				else:
					RecordValueDict = {
						'program_name': request.POST.get('ProgramName'),
						'X_value': request.POST.get('XValue'),
						'Y_value': request.POST.get('YValue'),
						'Z_value': request.POST.get('ZValue'),
						'ScanningRate_value': request.POST.get('ScanningRate'),
						'SReal_value': request.POST.get('Sreal'),
						'FeedRate_value': request.POST.get('FeedRate'),
						'GState_value': request.POST.get('GState'),
						'MState_value': request.POST.get('MState')}
					item_CNCProcessAutoData.update(**RecordValueDict)

				# 更新精细数据表
				RT_FineData.Realtime_FineData.add_processRecord(item_CNCProcessStatus.acquisition_timestamp,
																item_CNCProcessStatus.work_section.id,
																{'X_value': request.POST.get('XValue'),
																 'Y_value': request.POST.get('Y_value'),
																 'Z_value': request.POST.get('Z_value'),
																 'ScanningRate_value': request.POST.get('ScanningRate'),
																 'FeedRate_value': request.POST.get('FeedRate'),
																 'program_name': request.POST.get('ProgramName'),
																 'if_exec_intr':request.POST.get('if_exec_intr'),
																 'if_interrupt_intr':request.POST.get('if_interrupt_intr')})

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
			# _oxydata = Oxygendata(work_section=worksection,
			# 					  acquisition_time=_acqu_time,
			# 					  acquisition_timestamp = _timestamp,
			# 					  oxygen_value=float(request.POST.get('oxygen_value', None)),
			# 					  oxygen_sensor_value=float(request.POST.get('oxygen_sensor_value', None)),
			# 					  internal_pressure_value=float(request.POST.get('internal_pressure_value', None))
			# 					  )
			# _oxydata.save()

			# 更新近期实时记录 绘制现场操作实时曲线
			RealtimeRecord.Realtime_Records.addRecords(worksection.id, 'oxygen', _timestamp, float(request.POST.get('oxygen_value', None)))

			# updateProcessDataIndexingInfo(worksection, dateint, datetype, data_id):
			'''停止更新Process_Oxygendata_Date_Worksection_indexing'''
			# updateProcessDataIndexingInfo(worksection,
			# 							  int(_acqu_time.strftime('%Y%m%d')),
			# 							  'oxygen',
			# 							  _oxydata.id)

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
		# logger.debug(_rlist)
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
				# logger.debug(islaserdata)
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
				if float(_rlist[2])<20:
					_rlist[2]=0
					# return 'blank'
				# 14.10.17 18:28:03.265    7478    30.0    21.4     4.3
				# _rlist=['06.12.19', '08:39:56.746', '0', '29.9', '21.9']
				_day, _month, _year=map(lambda x:int(x), _rlist[0].split('.'))
				# _hour, _minute, _second = map(lambda x:float(x) if '.' in x else int(x), _rlist[1].split(':'))
				_time = "20%d-%d-%d %s" % (_year, _month, _day, _rlist[1])
				# logger.debug(_time)
				_timestamp=int(time.mktime(time.strptime(_time, "%Y-%m-%d %H:%M:%S.%f")))
				'''停止更新写入Laserdata'''
				# _laserdata = Laserdata(work_section=worksection,
				# 					   acquisition_time=_time,
				# 					   acquisition_timestamp = _timestamp,
				# 					   laser_power=float(_rlist[2]),
				# 					   laser_lightpath_temperature=float(_rlist[3]),
				# 					   laser_laser_temperature=float(_rlist[4]))
				# _laserdata.save()

				# 更新近期实时记录
				RealtimeRecord.Realtime_Records.addRecords(worksection.id, 'laser', _timestamp, float(_rlist[2]))
				# logger.debug(_timestamp)
				# logger.debug(RealtimeRecord.Realtime_Records.WS_RT_RC_Dict['3']['laser'])
				# 更新精细数据表
				RT_FineData.Realtime_FineData.add_processRecord(_timestamp, worksection.id, {'laser_power': float(_rlist[2])})

				# logger.debug('laser_id:%d' % _laserdata.id)
				# logger.debug('timeint:%d' % int(_time.split(' ')[0].replace('-','')))
				# updateProcessDataIndexingInfo(worksection, dateint, datetype, data_id):
				'''停止更新Process_Laserdata_Date_Worksection_indexing'''
				# updateProcessDataIndexingInfo(worksection,
				# 							  datetime.datetime(int('20%d'%_year), _month, _day).strftime('%Y%m%d'),
				# 							  # int(_time.splsit(' ')[0].replace('-','')),
				# 							  'laser',
				# 							  _laserdata.id)
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
		print(_PostData['process_start_time'])
		print(_PostData['process_finish_time'])
		if len(_PostData['process_start_time'])>=19:
			start_datetime = datetime.datetime.strptime(str(_PostData['process_start_time']), "%Y-%m-%dT%H:%M:%S")
		else:
			start_datetime = datetime.datetime.strptime(str(_PostData['process_start_time']), "%Y-%m-%dT%H:%M")
		if len(_PostData['process_finish_time'])>=19:
			finish_datetime = datetime.datetime.strptime(str(_PostData['process_finish_time']), "%Y-%m-%dT%H:%M:%S")
		else:
			finish_datetime = datetime.datetime.strptime(str(_PostData['process_finish_time']), "%Y-%m-%dT%H:%M")
		# try:
		# 	try:
		# 		start_datetime = datetime.datetime.strptime(str(_PostData['process_start_time']), "%Y-%m-%dT%H:%M")
		# 		finish_datetime = datetime.datetime.strptime(str(_PostData['process_finish_time']), "%Y-%m-%dT%H:%M")
		# 	except:
		# 		start_datetime = datetime.datetime.strptime(_PostData['process_start_time'], "%Y-%m-%dT%H:00")
		# 		finish_datetime = datetime.datetime.strptime(_PostData['process_finish_time'], "%Y-%m-%dT%H:00")
		# except:
		# 	start_datetime = datetime.datetime.strptime(str(_PostData['process_start_time']), "%Y-%m-%dT%H:%M:%S")
		# 	finish_datetime = datetime.datetime.strptime(str(_PostData['process_finish_time']), "%Y-%m-%dT%H:%M:%S")
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
			# 得到finedata开始、结束id
			finedata_model = RT_FineData.Realtime_FineData.getFineDataModel_ByWSID(str(worksection.id))
			finedata_obj = finedata_model.objects.get(acquisition_timestamp=start_timestamp)
			_finedata_start_recordid = finedata_obj.id
			finedata_obj = finedata_model.objects.get(acquisition_timestamp=finish_timestamp)
			_finedata_finish_recordid = finedata_obj.id
			
			# if_mission_exists = False
			try:
				# ----若已存在，则更改
				_model_inst = Process_Mission_timecut.objects.get(process_mission=mission)
				# if_mission_exists = True
				# _model_inst.process_start_time = start_DT_str
				_model_inst.process_start_time = start_datetime
				# _model_inst.process_finish_time = finish_DT_str
				_model_inst.process_finish_time = finish_datetime
				_model_inst.finedata_start_recordid = _finedata_start_recordid
				_model_inst.finedata_finish_recordid = _finedata_finish_recordid
				_model_inst.save()
			except:
				# ----若不存在，则新建
				_model_inst = Process_Mission_timecut(process_mission=mission,
				                                      # process_start_time=start_DT_str,
				                                      # process_finish_time=finish_DT_str,
				                                      process_start_time=start_datetime,
				                                      process_finish_time=finish_datetime,
				                                      finedata_start_recordid=_finedata_start_recordid,
				                                      finedata_finish_recordid=_finedata_finish_recordid
				                                      )
				_model_inst.save()
			
			# # 获取各项数据的最大最小数据id
			# with connection.cursor() as cursor:
			# 	# cursor.execute("UPDATE bar SET foo = 1 WHERE baz = %s", [self.baz])
			# 	cursor.execute(
			# 		"SELECT max(id),min(id) FROM lamdataserver.lamprocessdata_oxygendata where work_section_id = %d and acquisition_timestamp >= %d and acquisition_timestamp <= %d;" % (
			# 		worksection.id, start_timestamp, finish_timestamp))
			# 	row = cursor.fetchall()
			# 	oxygen_maxid = row[0][0]
			# 	oxygen_minid = row[0][1]
			# 	t2 = time.time()
			# 	cursor.execute(
			# 		"SELECT max(id),min(id) FROM lamdataserver.lamprocessdata_laserdata where work_section_id = %d and acquisition_timestamp >= %d and acquisition_timestamp <= %d;" % (
			# 		worksection.id, start_timestamp, finish_timestamp))
			# 	row = cursor.fetchall()
			# 	laser_maxid = row[0][0]
			# 	laser_minid = row[0][1]
			# 	t3=time.time()
			# 	cursor.execute(
			# 		"SELECT max(id),min(id) FROM lamdataserver.lamprocessdata_cncprocessstatus where work_section_id = %d and acquisition_timestamp >= %d and acquisition_timestamp <= %d;" % (
			# 			worksection.id, start_timestamp, finish_timestamp))
			# 	row = cursor.fetchall()
			# 	cnc_maxid = row[0][0]
			# 	cnc_minid = row[0][1]
			# 	print(t2-t1, t3-t2, time.time()-t3)
			# 	# 4.492816925048828 11.877208232879639 24.164589881896973
			# 	# 3.5282106399536133 9.010584831237793 23.99515962600708
			# 	# print(oxygen_minid, oxygen_maxid, laser_minid, laser_maxid, cnc_minid, cnc_maxid)
			# 	'''更新Process_Mission_timecut'''
			# 	if_mission_exists = False
			# 	try:
			# 		# ----若已存在，则更改
			# 		_model_inst = Process_Mission_timecut.objects.get(process_mission=mission)
			# 		if_mission_exists = True
			# 	except:
			# 		# ----若不存在，则新建
			# 		_model_inst = Process_Mission_timecut(process_mission=mission,
			# 											  process_start_time=start_DT_str,
			# 											  process_finish_time = finish_DT_str,
			# 											  laserdata_start_recordid = oxygen_minid,
			# 											  laserdata_finish_recordid = oxygen_maxid,
			# 											  oxygendata_start_recordid = laser_minid,
			# 											  oxygendata_finish_recordid = laser_maxid,
			# 											  cncstatusdata_start_recordid = cnc_minid,
			# 											  cncstatusdata_finish_recordid = cnc_maxid
			# 											  )
			# 		_model_inst.save()
			# 	if if_mission_exists:
			# 		# _model_inst.process_start_time = start_DT_str
			# 		_model_inst.process_start_time = start_datetime
			# 		# _model_inst.process_finish_time = finish_DT_str
			# 		_model_inst.process_finish_time = finish_datetime
			# 		_model_inst.laserdata_start_recordid = oxygen_minid
			# 		_model_inst.laserdata_finish_recordid = oxygen_maxid
			# 		_model_inst.oxygendata_start_recordid = laser_minid
			# 		_model_inst.oxygendata_finish_recordid = laser_maxid
			# 		_model_inst.cncstatusdata_start_recordid = cnc_minid
			# 		_model_inst.cncstatusdata_finish_recordid = cnc_maxid
			# 		_model_inst.save()

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
	# def selectRecordID_Start(type, WorksectionID, _start_timestamp):
	# 	if type=='oxygen':
	# 		tablename = 'lamdataserver.lamprocessdata_oxygendata'
	# 	elif type == 'laser':
	# 		tablename = 'lamdataserver.lamprocessdata_laserdata'
	# 	elif type == 'cncstatus':
	# 		tablename = 'lamdataserver.lamprocessdata_cncprocessstatus'
	#
	# 	with connection.cursor() as cursor:
	# 		cursor.execute(
	# 			"SELECT min(id) FROM %s where work_section_id = %d and acquisition_timestamp >= %d;" % (
	# 				tablename, WorksectionID, _start_timestamp))
	# 		row = cursor.fetchall()
	# 		_start_recordid = row[0][0]
	# 		if not _start_recordid:
	# 			cursor.execute(
	# 				"SELECT max(id) FROM %s where work_section_id = %d and acquisition_timestamp <= %d;" % (
	# 					tablename, WorksectionID, _start_timestamp))
	# 			row = cursor.fetchall()
	# 			_start_recordid = row[0][0]
	# 	return _start_recordid
	#
	# def selectRecordID_Finish(type, WorksectionID, _start_record_id, _finish_timestamp):
	# 	if type=='oxygen':
	# 		tablename = 'lamdataserver.lamprocessdata_oxygendata'
	# 	elif type == 'laser':
	# 		tablename = 'lamdataserver.lamprocessdata_laserdata'
	# 	elif type == 'cncstatus':
	# 		tablename = 'lamdataserver.lamprocessdata_cncprocessstatus'
	#
	# 	with connection.cursor() as cursor:
	# 		cursor.execute(
	# 			"SELECT max(id) FROM %s where work_section_id = %d and id >= %d and acquisition_timestamp <= %d;" % (
	# 				tablename, WorksectionID, _start_record_id, _finish_timestamp))
	# 		row = cursor.fetchall()
	# 		_finish_recordid = row[0][0]
	# 	return _finish_recordid

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
				# 得到finedata结束id
				finedata_model = RT_FineData.Realtime_FineData.getFineDataModel_ByWSID(str(WorksectionID))
				finedata_obj = finedata_model.objects.get(acquisition_timestamp = _finish_timestamp)
				_finedata_finish_recordid = finedata_obj.id
				# # 查询任务开始的各项参数id
				# _oxygendata_start_recordid=_mission_attr_obj.oxygendata_start_recordid
				# _laserdata_start_recordid=_mission_attr_obj.laserdata_start_recordid
				# _cncstatusdata_start_recordid=_mission_attr_obj.cncstatusdata_start_recordid
				# if not _oxygendata_start_recordid:
				# 	_oxygendata_start_recordid = 1
				# if not _laserdata_start_recordid:
				# 	_laserdata_start_recordid = 1
				# if not _cncstatusdata_start_recordid:
				# 	_cncstatusdata_start_recordid = 1
				# # 找到各项过程记录终止的id
				# _oxygendata_finish_recordid = selectRecordID_Finish('oxygen', WorksectionID, _oxygendata_start_recordid, _finish_timestamp)
				# _laserdata_finish_recordid = selectRecordID_Finish('laser', WorksectionID, _laserdata_start_recordid, _finish_timestamp)
				# _cncstatusdata_finish_recordid = selectRecordID_Finish('cncstatus', WorksectionID, _cncstatusdata_start_recordid, _finish_timestamp)

				# 任务实例属性
				# 设置结束时间
				_mission_attr_obj.process_finish_time = _finish_time
				# 记录各项过程参数的终止id
				# _mission_attr_obj.laserdata_finish_recordid = _laserdata_finish_recordid
				# _mission_attr_obj.oxygendata_finish_recordid = _oxygendata_finish_recordid
				# _mission_attr_obj.cncstatusdata_finish_recordid = _cncstatusdata_finish_recordid
				_mission_attr_obj.finedata_finish_recordid = _finedata_finish_recordid
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
				# _oxygendata_start_recordid = selectRecordID_Start('oxygen', WorksectionID, _start_timestamp)
				# _laserdata_start_recordid = selectRecordID_Start('laser', WorksectionID, _start_timestamp)
				# _cncstatusdata_start_recordid = selectRecordID_Start('cncstatus', WorksectionID, _start_timestamp)

				# 设置开始时间
				_mission_attr_obj.process_start_time = _start_time
				
				finedata_model = RT_FineData.Realtime_FineData.getFineDataModel_ByWSID(str(WorksectionID))
				finedata_obj = finedata_model.objects.get(acquisition_timestamp=_start_timestamp)
				_finedata_start_recordid = finedata_obj.id
				_mission_attr_obj.finedata_start_recordid = _finedata_start_recordid
				# 记录各项过程参数的终止id
				# _mission_attr_obj.laserdata_start_recordid = _laserdata_start_recordid
				# _mission_attr_obj.oxygendata_start_recordid = _oxygendata_start_recordid
				# _mission_attr_obj.cncstatusdata_start_recordid = _cncstatusdata_start_recordid
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
# 编辑累加单元 弹出子窗
@login_required
def edit_lamprocessparameterAccumulateCell(request, ProcessParameterItemID):
	_parameter = LAMProcessParameters.objects.get(id=ProcessParameterItemID)
	if _parameter.accumulate_cell is None:
		_accumulate_cell = LAMProcessParameterAccumulateCell.objects.create()
		_accumulate_cell.save()
		_parameter.accumulate_cell = _accumulate_cell
		_parameter.save()
	else:
		_accumulate_cell = _parameter.accumulate_cell



	return edit_Template_SubWindow(request,
								   LAMProcessParameterAccumulateCell,
								   LAMProcessAccumulateCell_Edit,
								   _accumulate_cell.id,
								   Common_URL['Back_URL_lamprocessparameters'],
								   )

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

def get3DTestData(request):
	# 读取数据
	with open(r'E:\1-program\11-LAMDataServer\lamdataserver\LAMProcessData\templates\moban1342\testdata.json', 'r') as f:
		data = json.load(f)
	# print('end save_lamprocessparameterTechInstSerial')
	html = json.dumps(data, ensure_ascii=False)
	return HttpResponse(html, content_type='application/json')

def get3DTestData2(request):
	# 读取数据
	with open(r'E:\1-program\11-LAMDataServer\lamdataserver\LAMProcessData\templates\moban1342\testdata2.json', 'r') as f:
		data = json.load(f)
	# print('end save_lamprocessparameterTechInstSerial')
	html = json.dumps(data, ensure_ascii=False)
	return HttpResponse(html, content_type='application/json')


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
def Update_ExistingData_to_FineData(request, datatype):
	
	cache_text = CacheOperator('ProgressBarValue_Update_ExistingData_to_FineData_text', True, datatype, None)
	if cache_text is not None:
		return
	print('start Update_ExistingData_to_FineData...')
	CacheOperator('ProgressBarValue_Update_ExistingData_to_FineData_text', False, datatype,
	              'ready to start')
	t1 = time.time()
	if datatype=='oxygen':
		# 遍历氧含量数据
		all_data_list = Oxygendata.objects.all()
		count_i=0
		count_sum = all_data_list.count()
		for _data in all_data_list:
			count_i += 1
			if count_i % 1000 == 0:
				CacheOperator('ProgressBarValue_Update_ExistingData_to_FineData', False, 'oxygen', count_i / count_sum)
				CacheOperator('ProgressBarValue_Update_ExistingData_to_FineData_text', False, 'oxygen', '%s/%s'%(count_i, count_sum))
			# 更新精细数据表
			RT_FineData.Realtime_FineData.add_processRecord(int(time.mktime(_data.acquisition_time.timetuple())), _data.work_section.id,
															{'oxygen_value': _data.oxygen_value})
	elif datatype=='laser':
		# 遍历激光数据
		all_data_list = Laserdata.objects.all()
		count_i=0
		count_sum = all_data_list.count()
		for _data in all_data_list:
			count_i+=1
			if count_i%1000==0:
				CacheOperator('ProgressBarValue_Update_ExistingData_to_FineData', False, 'laser', count_i / count_sum)
				CacheOperator('ProgressBarValue_Update_ExistingData_to_FineData_text', False, 'laser', '%s/%s'%(count_i, count_sum))
			# if count_i<106000:
			# 	continue
			# 更新精细数据表
			RT_FineData.Realtime_FineData.add_processRecord(int(time.mktime(_data.acquisition_time.timetuple())),
			                                                _data.work_section.id,
			                                                {'laser_power': _data.laser_power})
	elif datatype == 'cncstatus':
		# 遍历机床运动数据
		all_data_list = CNCProcessStatus.objects.all()
		count_i = 0
		count_sum = all_data_list.count()
		for _data in all_data_list:
			count_i += 1
			if count_i % 1000 == 0:
				CacheOperator('ProgressBarValue_Update_ExistingData_to_FineData', False, 'cncstatus', count_i / count_sum)
				CacheOperator('ProgressBarValue_Update_ExistingData_to_FineData_text', False, 'cncstatus',
				              '%s/%s' % (count_i, count_sum))
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
				                                                 'if_exec_intr':_data.if_exec_intr,
				                                                 'if_interrupt_intr':_data.if_interrupt_intr,
				                                                 })
			except:
				pass
	
	CacheOperator('ProgressBarValue_Update_ExistingData_to_FineData_text', False, datatype, '')
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
		for _finedata in _model.objects.all().iterator():
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


def Update_ExistingFinData_If_intr(request):
	t1 = time.time()
	print('start Update_ExistingFinData_If_intr...')

	num_per_page = 2000
	MaxID = CNCProcessStatus.objects.all().count()
	Sum_i = int((MaxID / num_per_page) + 1)
	for Current_i in range(Sum_i):
		print('If_intr: %d / %d' % (Current_i, Sum_i))
		# if Current_i<987:
		# 	continue
		qset = (
				Q(id__gte=Current_i * num_per_page) &
				Q(id__lt=(Current_i + 1) * num_per_page)
		)
		_list = CNCProcessStatus.objects.filter(qset).distinct()
		for _cncstatus in _list:
			_worksection = _cncstatus.work_section
			_model = RT_FineData.Realtime_FineData.getFineDataModel_ByWSID(str(_worksection.id))
			_finedata = _model.objects.get(acquisition_timestamp=_cncstatus.acquisition_timestamp)
			_finedata.if_exec_intr = _cncstatus.if_exec_intr
			_finedata.if_interrupt_intr = _cncstatus.if_interrupt_intr
			_finedata.save()
	print('end Update_ExistingFineData_PatchEmptyData...')
	html = "<html><body>Update_ExistingFineData_PatchEmptyData Cost Time %f.</body></html>" % (time.time() - t1)
	return HttpResponse(html)

def Update_ExistingFineData_PatchEmptyData(request):
	t1 = time.time()
	print('start Update_ExistingFineData_PatchEmptyData...')
	def update_Finedate(_model):
		t1 = time.time()
		preitem = [None,None]
		num_per_page = 2000
		MaxID = _model.objects.all().count()
		Sum_i = int((MaxID / num_per_page) + 1)
		t2 = time.time()
		for Current_i in range(Sum_i):
			if Current_i <0:
				continue

			print('PatchEmptyData: %d / %d Cost: %.3fs' % (Current_i, Sum_i,time.time()-t2))
			t2 = time.time()
			qset = (
					Q(id__gte=Current_i * num_per_page) &
					Q(id__lt=(Current_i + 1) * num_per_page)
			)
			_list = _model.objects.filter(qset).distinct()
			for _finedata in _list:
				if preitem[0] == None or preitem[1] == None:
					preitem[0] = preitem[1]
					preitem[1] = _finedata
					continue

				# 程序名
				if preitem[1].program_name is None and preitem[0].program_name is not None and _finedata.program_name == preitem[0].program_name:
					preitem[1].program_name = preitem[0].program_name

				# 是否执行界面
				if preitem[1].if_exec_intr is None and preitem[0].if_exec_intr is not None and _finedata.if_exec_intr == preitem[0].if_exec_intr:
					preitem[1].if_exec_intr = preitem[0].if_exec_intr

				# 是否执行中断界面
				if preitem[1].if_interrupt_intr is None and preitem[0].if_interrupt_intr is not None and _finedata.if_interrupt_intr == preitem[0].if_interrupt_intr:
					preitem[1].if_interrupt_intr = preitem[0].if_interrupt_intr

				# 氧含量
				if preitem[1].oxygen_value is None and preitem[0].oxygen_value is not None and _finedata.oxygen_value is not None:
					_value = (preitem[0].oxygen_value + _finedata.oxygen_value) / 2
					preitem[1].oxygen_value = float('%.3f' % _value)

				# CNC坐标
				if preitem[1].X_value is None and preitem[0].X_value is not None and _finedata.X_value is not None:
					_value = (preitem[0].X_value + _finedata.X_value) / 2
					preitem[1].X_value = float('%.3f' % _value)
				if preitem[1].Y_value is None and preitem[0].Y_value is not None and _finedata.Y_value is not None:
					_value = (preitem[0].Y_value + _finedata.Y_value) / 2
					preitem[1].Y_value = float('%.3f' % _value)
				if preitem[1].Z_value is None and preitem[0].Z_value is not None and _finedata.Z_value is not None:
					_value = (preitem[0].Z_value + _finedata.Z_value) / 2
					preitem[1].Z_value = float('%.3f' % _value)

				# 进给率
				if preitem[1].FeedRate_value is None and preitem[0].FeedRate_value is not None and _finedata.FeedRate_value is not None:
					_value = (preitem[0].FeedRate_value + _finedata.FeedRate_value) / 2
					preitem[1].FeedRate_value = float('%.3f' % _value)

				# 扫描速率
				if preitem[1].ScanningRate_value is None and preitem[0].ScanningRate_value is not None and _finedata.ScanningRate_value is not None:
					_value = (preitem[0].ScanningRate_value + _finedata.ScanningRate_value) / 2
					preitem[1].ScanningRate_value = float('%.3f' % _value)



				preitem[1].save()
				preitem[0] = preitem[1]
				preitem[1] = _finedata
				# _finedata.acquisition_datetime = datetime.datetime.fromtimestamp(_finedata.acquisition_timestamp)
				# _finedata.save()
		print('%s:%.2f' % (_model, time.time() - t1))

	update_Finedate(Process_Realtime_FineData_By_WorkSectionID_1)
	print('end Update_ExistingFineData_PatchEmptyData...')
	html = "<html><body>Update_ExistingFineData_PatchEmptyData Cost Time %f.</body></html>" % (time.time() - t1)
	return HttpResponse(html)

'''清空缓存'''
cache.clear()

'''启动定时任务'''
'''pip install apscheduler==2.1.2'''
sched = Scheduler()
# 20200817 本函数不需要执行，更换了存储数据表
# 每天执行1次
# @sched.interval_schedule(days=1,start_date=datetime.datetime.fromtimestamp(float(time.time())+20))
@sched.interval_schedule(days=1, start_date=datetime.datetime.fromtimestamp(float(time.time())+10))
def regulartime_task():
	RT_FineData.Realtime_FineData.init_Tomorrow_rows()

# @sched.interval_schedule(seconds=1, start_date=datetime.datetime.fromtimestamp(float(time.time())+10))
# # 	pass

# 每秒钟访问一次远程数据库，抓取成形过程数据
@sched.interval_schedule(seconds=1)
def getDataFromRemoteDataBase():
	# print(time.time())
	# RT_FineData.Realtime_FineData.add_processRecord()
	pass

# 清理缓存目录
 # 设置为每日凌晨03:00:00时执行一次调度程序
@sched.cron_schedule(day_of_week='*', hour='03', minute='00', second='00')
def cleanup():
	logger.info('start cleanup!')
	filelist = os.listdir(tempfile.gettempdir())
	# 3min
	Del_time = time.time()-10
	tempdir = tempfile.gettempdir()

	for filename in filelist:
		filepath = tempdir+'\\'+filename
		try:
			if filename.startswith('tess') and Del_time >= os.path.getatime(filepath):
				# delete
				os.unlink(filepath)
				os.remove(filepath)
				# logger.debug('remove file success:%s'%filepath)
			if filename.startswith('LAMServer') or filename.endswith('upload.nc'):
				# delete
				os.unlink(filepath)
				os.remove(filepath)
		except:
			pass
			# logger.debug('remove file error:%s' % filepath)
	for root, dirs, files in os.walk(tempdir):
		try:
			for dir in dirs:
				_path = root + '\\' + dir
				if dir.startswith('tmp') and Del_time >= os.path.getatime(_path):
					shutil.rmtree(_path, True)
					# logger.debug('remove dir success:%s' % _path)
		except:
			# logger.debug('remove dir error:')
			pass
	# import pytesseract
	logger.info('end cleanup!')


logger = logging.getLogger()
# @sched.interval_schedule(days=start cleanup!1, start_date=datetime.datetime.now())
@sched.cron_schedule(hour=0)
def OpenLog():
	global logger
	logger = logging.getLogger()
	logger.setLevel(logging.DEBUG)
	# time_handler = logging.handlers.TimedRotatingFileHandler('.' + MEDIA_LOGFLE_URL + 'LAMDataServer%s.log'%datetime.date.today().strftime('%Y-%m-%d'),
	# 														 when='midnight', interval=1, backupCount=0)
	time_handler = logging.handlers.TimedRotatingFileHandler(
		os.path.join(APP_PATH, '.'+MEDIA_LOGFLE_URL + 'LAMDataServer%s.log'%datetime.date.today().strftime('%Y-%m-%d')).replace('\\', '/'),
		# '.' + MEDIA_LOGFLE_URL + 'LAMDataServer%s.log'%datetime.date.today().strftime('%Y-%m-%d'),
		when='midnight',
		interval=1,
		backupCount=0)
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
