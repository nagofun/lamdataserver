# -*- coding: gbk -*-
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse

from django.db.models import Q
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

from django.template import loader, RequestContext
from django.template import Context, Template
from django.conf import settings
from django_lock import lock

from LAMProcessData.models import *
from LAMProcessData.forms import *
import LAMProcessData.realtime_records as RealtimeRecord
# from LAMProcessData.permission import check_permission

from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page
from django.core.cache import cache

import json
import random
from xml.etree.ElementTree import Element, SubElement, tostring
import datetime
import logging
import time
import sys
# from lamdataserver.settings import logger
# from lamdataserver.LAMProcessData.views import CacheOperator
from LAMProcessData.views import CacheOperator, logger, time_data1, time_data2
import LAMProcessData.process_realtime_finedata as RT_FineData
# import settings.MEDIA_URL as MEDIA_URL


GLOBAL_CNCScreenInfo_IDList = []

try:
	settings.GLOBAL_CNCProcessStatus_SendImage_MAX_ID = TemporaryParameter_ID.objects.get(id=1).item_id
	settings.GLOBAL_CNCProcessStatus_NotRecoge_Min_ID = TemporaryParameter_ID.objects.get(id=2).item_id
	settings.GLOBAL_CNCProcessStatus_SendImageBefore_Not_Recive_ITEMlist = list(CNCProcessStatus.objects.filter(
		Q(id__gte=settings.GLOBAL_CNCProcessStatus_NotRecoge_Min_ID) & Q(
			id__lte=settings.GLOBAL_CNCProcessStatus_SendImage_MAX_ID) & Q(if_checked=False)))
	settings.GLOBAL_CNCProcessStatus_SendImage_Waitfor_Recive_IDlist = list(map(lambda item:item.id,settings.GLOBAL_CNCProcessStatus_SendImageBefore_Not_Recive_ITEMlist))
	logger.debug('SendBefore_NotRecive : %s'%str(settings.GLOBAL_CNCProcessStatus_SendImageBefore_Not_Recive_ITEMlist))
	logger.debug('Waitfor_Recive : %s'%str(settings.GLOBAL_CNCProcessStatus_SendImage_Waitfor_Recive_IDlist))
except:
	logger.error('INIT ERROR')
	pass

# logger = logging.getLogger(__name__)
# logger.debug(settings.GLOBAL_CNCProcessStatus_SendImage_MAX_ID)
# logger.debug(settings.GLOBAL_CNCProcessStatus_NotRecoge_Min_ID)
# logger.debug(settings.GLOBAL_CNCProcessStatus_SendImageBefore_Not_Recive_ITEMlist)

# GLOBAL_

def dict_to_xml(tag, d):
	'''
	Turn a simple dict of key/value pairs into XML
	'''
	_element = Element(tag)
	for id, info in d.items():  # 此处若用python2，则改为iteritems()
		_subelement = SubElement(_element, 'subElement')
		# print(info)
		for key, val in info.items():
			# print(key, val)
			SubElement(_subelement, key).text = val
	# print(SubElement(_subelement, key))
	# print(_element.TechInst)
	return _element


@login_required
@csrf_exempt
def queryData_LAMTechInst_Preview(request, TechInstID):
	all_datadict = LAM_TechInst_Serial.objects.filter(available=True, technique_instruction=TechInstID).order_by(
		'serial_number')
	TechInst_dict = {
		'id_%d' % data.id:
			{'serial_number': data.serial_number,
			 'serial_worktype': str(data.serial_worktype),
			 'serial_note': data.serial_note if data.serial_note else ' '}
		for data in all_datadict
	}
	# print(TechInst_dict)
	html = json.dumps(TechInst_dict, ensure_ascii=False)
	# html = dict_to_xml('TechInst', TechInst_dict)
	# print(html)
	# response.setContentType("text/html;charset=utf-8”);
	# return HttpResponse(TechInst_dict, content_type='application/json')
	return HttpResponse(html, content_type='application/json')

@login_required
@csrf_exempt
def queryData_LAMProcessParameterConditionalCell(request, ProcessParameterID):
	# 根据ParameterID传回包含的ConditionalCell内容并列成表格
	_ProcessParameter = LAMProcessParameters.objects.get(id=ProcessParameterID)
	all_datadict = _ProcessParameter.conditional_cell.all()
	_dict = {
		'id_%d' % data.id:
			{'id': str(data.id),
			 'level': str(data.level),
			 'precondition': data.precondition,
			 'expression': data.expression,
			 'comment':data.comment,
			 'instead_Cond_Cell':str(data.instead_Cond_Cell)}
		for data in all_datadict
	}
	# print(_dict)
	html = json.dumps(_dict, ensure_ascii=False)
	return HttpResponse(html, content_type='application/json')

@login_required
@csrf_exempt
def queryData_LAMProcessParameterAccumulateCell(request, ProcessParameterID):
	# 根据ParameterID传回包含的AccumulateCell内容并列成表格
	_ProcessParameter = LAMProcessParameters.objects.get(id=ProcessParameterID)
	_accumulate = _ProcessParameter.accumulate_cell
	if _accumulate ==None:
		_dict = {}
	else:
		_dict = {
			'id_%d' % data.id:
				{
				 'active': data.active,
				 'M1': data.M1,
				 'M2': data.M2,
				 'l':data.l,
				 'tm':data.tm,
				 'alarm_value':data.alarm_value}
			for data in [_accumulate]
		}
	# print(_dict)
	html = json.dumps(_dict, ensure_ascii=False)
	return HttpResponse(html, content_type='application/json')

@login_required
@csrf_exempt
def queryData_LAMProcessParameterTechInstSerial(request, ProcessParameterID):
	check_datalist = LAM_TechInst_Serial.objects.filter(available=True, process_parameter=ProcessParameterID)
	check_IDlist = [i.id for i in check_datalist]
	html = json.dumps({'techinst_serial_idlist':check_IDlist}, ensure_ascii=False)
	return HttpResponse(html, content_type='application/json')

@login_required
@csrf_exempt
def queryData_LAMProcessParameterTechInstSerial_Refresh(request):
	# 待增加内容，根据ParameterID传回包含的ConditionalCell内容并列成表格
	_TechInstSerial = LAM_TechInst_Serial.objects.filter((Q(available=True)))
	# all_datadict = _ProcessParameter.conditional_cell.all()
	_dict = {
		'id_%d' % data.id:
			{'id': str(data.id),
			 'technique_instruction': str(data.technique_instruction),
			 'serial_number': data.serial_number,
			 'serial_worktype': str(data.serial_worktype),
			 'serial_note': data.serial_note,
			 'process_parameter': str(data.process_parameter)}
		for data in _TechInstSerial
	}
	# print(_dict)
	html = json.dumps(_dict, ensure_ascii=False)
	return HttpResponse(html, content_type='application/json')
	# def initTableData(Model, form_display_fields=None):
	# 	try:
	# 		all_entries = Model.objects.filter((Q(available=True)))
	#
	# 		all_entries_list = []
	# 		for i in all_entries:
	# 			_dict = {}
	# 			for att in form_display_fields:
	# 				_dict[att] = str(i.__getattribute__(att.replace('_id', '')))
	# 			all_entries_list.append(_dict)
	# 		return all_entries_list
	# 	except:
	# 		pass
	#
	# all_serial_entries_list = initTableData(LAM_TechInst_Serial, ['id',
	#                                                               'technique_instruction',
	#                                                               'serial_number',
	#                                                               'serial_worktype',
	#                                                               'serial_note',
	#                                                               'process_parameter'])
	# html = json.dumps({'all_entries_serial': all_serial_entries_list}, ensure_ascii=False)
	# return HttpResponse(html, content_type='application/json')


@login_required
@csrf_exempt
def queryData_LAMProductMission_Preview(request, ProductID):
	all_datadict = LAMProcessMission.objects.filter(available=True, LAM_product=ProductID).order_by('arrangement_date')
	Mission_dict = {
		'id_%d' % data.id:
			{'LAM_techinst_serial': str(data.LAM_techinst_serial),
			 'arrangement_date': str(data.arrangement_date),
			 'completion_date': str(data.completion_date) if str(data.completion_date) else ' '}
		for data in all_datadict
	}
	# print(TechInst_dict)
	html = json.dumps(Mission_dict, ensure_ascii=False)
	# html = dict_to_xml('TechInst', TechInst_dict)
	# print(html)
	# response.setContentType("text/html;charset=utf-8”);
	# return HttpResponse(TechInst_dict, content_type='application/json')
	return HttpResponse(html, content_type='application/json')


# 根据产品类型查询该产品涉及的所有工艺文件
# 此函数失效 at 20190804
# @login_required
# @csrf_exempt
# def queryData_LAMTechInst_By_ProdCate(request, ProductCategoryID):
# 	# print(ProductCategoryID)
# 	all_datadict = LAMProdCate_TechInst.objects.filter(available=True, lamproductcategory=ProductCategoryID).order_by(
# 		'lamtechniqueinstruction')
# 	TechInst_dict = {
# 		'id_%d' % data.id:
# 			{
# 				'id': data.id,
# 				'lamtechniqueinstruction': str(data.lamtechniqueinstruction)
# 			}
# 		for data in all_datadict
# 	}
# 	html = json.dumps(TechInst_dict, ensure_ascii=False)
# 	return HttpResponse(html, content_type='application/json')

# 根据零件编号查询可用的工艺文件
@login_required
@csrf_exempt
def queryData_LAMTechInst_By_ProductCode(request, ProductCode):
	filtecondition_Product = LAMProduct.objects.get(product_code=ProductCode)
	filtecondition_ProdCate = filtecondition_Product.product_category

	all_datadict = LAMTechniqueInstruction.objects.filter(
		(Q(product_category=filtecondition_ProdCate) | Q(product=filtecondition_Product)) & Q(available=True) & Q(
			filed=False)).order_by(
		'instruction_code')
	TechInst_dict = {
		'id_%d' % data.id:
			{
				'id': data.id,
				'lamtechniqueinstruction': str(data)
			}
		for data in all_datadict
	}
	html = json.dumps(TechInst_dict, ensure_ascii=False)
	return HttpResponse(html, content_type='application/json')


# 根据工艺文件id查询该工艺文件所有工序
@login_required
@csrf_exempt
def queryData_WorkType_By_LAMTechInst(request, LAMTechInstID):
	# print(ProductCategoryID)
	all_datadict = LAM_TechInst_Serial.objects.filter(available=True, technique_instruction=LAMTechInstID).order_by(
		'serial_number')
	TechInst_dict = {
		'id_%d' % data.id:
			{
				'id': data.id,
				'worktype': '%d-%s[%s]' % (data.serial_number, data.serial_worktype, data.serial_note)
			}
		for data in all_datadict
	}
	html = json.dumps(TechInst_dict, ensure_ascii=False)
	return HttpResponse(html, content_type='application/json')


# 根据产品类型id查询所有产品实例
@login_required
@csrf_exempt
def queryData_Product_By_ProductCategory(request, ProductCategoryID):
	# print(ProductCategoryID)
	all_datadict = LAMProduct.objects.filter(available=True, product_category=ProductCategoryID).order_by(
		'product_code')
	TechInst_dict = {
		'id_%d' % data.id:
			{
				'id': data.id,
				'product_code': data.product_code
			}
		for data in all_datadict
	}
	html = json.dumps(TechInst_dict, ensure_ascii=False)
	return HttpResponse(html, content_type='application/json')


# 根据产品编号查询产品实例id
@login_required
@csrf_exempt
def queryData_ProductID_By_ProductCode(request, ProductCode):
	# print(ProductCategoryID)
	try:
		productid = LAMProduct.objects.get(available=True, product_code=ProductCode).id
	except:
		productid = -1
	# print('queryData_ProductID_By_ProductCode:'+str(productid))
	_dict = {
		'productid': productid,
	}
	html = json.dumps(_dict, ensure_ascii=False)
	return HttpResponse(html, content_type='application/json')

# 根据任务编号查询所在工段id号
@login_required
@csrf_exempt
def queryData_WorksectionId_By_MissionID(request, MissionID):
	try:
		mission = LAMProcessMission.objects.get(id=MissionID)
		worksectionid = mission.work_section.id
	except:
		worksectionid = -1
	_dict = {
		'worksectionid': worksectionid,
	}
	html = json.dumps(_dict, ensure_ascii=False)
	return HttpResponse(html, content_type='application/json')

# 根据任务编号查询开始结束时间（若存在）
@login_required
@csrf_exempt
def queryData_StartFinishTime_By_MissionID(request, MissionID):
	try:
		mission = LAMProcessMission.objects.get(id=MissionID)
		mission_cut = Process_Mission_timecut.objects.get(process_mission = mission)
		start_datetime = mission_cut.process_start_time.strftime("%Y-%m-%dT%H:%M:%S")
		finish_datetime = mission_cut.process_finish_time.strftime("%Y-%m-%dT%H:%M:%S")
	except:
		start_datetime = (datetime.date.today()-datetime.timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S")
		finish_datetime = datetime.date.today().strftime("%Y-%m-%dT%H:%M:%S")
	_dict = {
		'start_datetime': start_datetime,
		'finish_datetime': finish_datetime,
	}
	# print(_dict)
	html = json.dumps(_dict, ensure_ascii=False)
	return HttpResponse(html, content_type='application/json')

# 根据任务编号查询所在工段id号
@login_required
@csrf_exempt
def queryData_ArrangementDate_By_MissionID(request, MissionID):
	try:
		mission = LAMProcessMission.objects.get(id=MissionID)
		arrangementdate = str(mission.arrangement_date)
	except:
		arrangementdate = ''
	_dict = {
		'arrangementdate': arrangementdate,
	}
	html = json.dumps(_dict, ensure_ascii=False)
	return HttpResponse(html, content_type='application/json')


# 根据产品编号查询任务列表
@login_required
@csrf_exempt
def queryData_Mission_By_ProductCode(request, ProductCode):
	# print(ProductCategoryID)
	try:
		product = LAMProduct.objects.get(available=True, product_code=ProductCode)
		mission_list = list(LAMProcessMission.objects.filter(LAM_product=product).order_by('arrangement_date'))
		mission_list_rest = list(LAMProcessMission.objects.filter(~Q(LAM_product=product)).order_by('arrangement_date'))
		mission_list.extend(mission_list_rest)
		_list = [{'id':_m.id, 'mission':str(_m)} for _m in mission_list]
	except:
		_list = []
	# print('queryData_ProductID_By_ProductCode:'+str(productid))
	# _dict = {
	# 	'mission_list': mission_list,
	# }
	html = json.dumps(_list, ensure_ascii=False)
	return HttpResponse(html, content_type='application/json')

# 以任务id、起止时间、时间间隔查询氧含量数据
@login_required
@csrf_exempt
def queryData_Oxydata_By_MissionDatetime(request, MissionID, StartDateTime, FinishDateTime, Interval):
	try:
		mission = LAMProcessMission.objects.get(id=MissionID)
		worksectionid = mission.work_section.id
		html = queryData_Oxydata_By_WorkSectionDatetime(request, worksectionid, StartDateTime, FinishDateTime, Interval)
		return HttpResponse(html, content_type='application/json')
	except:
		worksectionid = -1
		html = json.dumps('', ensure_ascii=False)
		return HttpResponse(html, content_type='application/json')

# 以工段id、起止时间、时间间隔查询氧含量、激光功率、CNC-Z数据
@login_required
@csrf_exempt
# @cache_page(60 * 15)
def queryData_data_By_WorkSectionDatetime(request, ifForceRefresh, WorksectionID, StartDateTime, FinishDateTime, Interval):
	def getcache(worksection, dateint, indexmodel, datatype):
		key = 'DATA_WS%s_D%d_TP%s' % (worksection.id, dateint, datatype)
		cachevalue = cache.get(key)
		if not cachevalue:
			qset = (
					Q(work_section=worksection) &
					Q(index_date_int=dateint)
			)
			# if datatype == 'oxygen':
			# 	indexmodel = Process_Oxygendata_Date_Worksection_indexing
			# elif datatype == 'laser':
			# 	indexmodel = Process_Laserdata_Date_Worksection_indexing
			# elif datatype == 'cncstatus':
			# 	indexmodel = Process_CNCStatusdata_Date_Worksection_indexing
			try:
				_dataindex = indexmodel.objects.filter(qset)[0]
				cachevalue = _dataindex.data_string
			except:
				logger.debug('getcache error, qset:%s, datatype:%s'%(str(qset),datatype))
				pass
			cache.set(key, cachevalue)
		return cache.get(key)
	def setcache(worksection, dateint, indexmodel, datatype, data):
		setkey = 'DATA_WS%s_D%d_TP%s' % (worksection.id, dateint, datatype)
		qset = (
				Q(work_section=worksection) &
				Q(index_date_int=dateint)
		)
		# if datatype == 'oxygen':
		# 	indexmodelname = Process_Oxygendata_Date_Worksection_indexing
		# elif datatype == 'laser':
		# 	indexmodelname = Process_Laserdata_Date_Worksection_indexing
		# elif datatype == 'cncstatus':
		# 	indexmodelname = Process_CNCStatusdata_Date_Worksection_indexing
		try:
			_dataindex = indexmodel.objects.filter(qset)[0]
			_dataindex.data_string = data
			_dataindex.save()
		except:
			logger.debug('setcache error, qset:%s, datatype:%s' % (str(qset),datatype))
		cache.set(setkey, data)
	def make_minute_data(datatype, indexmodelname, datamodelname, dateint, thisdatetime):
		'''获得以分钟索引的数据字典'''
		num_per_page = 1000
		try:
			qset = (
					Q(work_section=worksection) &
					Q(index_date_int=dateint)
			)
			indexing_datalist = indexmodelname.objects.filter(qset)[0]
			data_startid = indexing_datalist.data_start_id
		except:
			data_startid = 1
		try:
			qset = (
					Q(work_section=worksection) &
					Q(index_date_int=dateint)
			)
			indexing_datalist = indexmodelname.objects.filter(qset)[0]
			data_finishid = indexing_datalist.data_finish_id
		except:
			data_finishid = datamodelname.objects.last().id

		# 根据此日的数据起始终止id 时间int值筛选
		Sum_i = int(((data_finishid - data_startid) / num_per_page) + 1)
		IntervalDict = {}
		_flagvalue = -1
		_tempValue = _flagvalue
		# 初始化为当天的00:00:00所对应的时间戳
		_lastdatatime = int(time.mktime(thisdatetime.timetuple()))
		# 时间戳最小值为当天00:00:00所对应的时间戳
		MinStamp=int(time.mktime(thisdatetime.timetuple()))
		# 时间戳最大值为第二天00:00:00所对应的时间戳
		MaxStamp=int(time.mktime((thisdatetime+datetime.timedelta(days=1)).timetuple()))
		for Current_i in range(Sum_i):
			_start_id = data_startid + Current_i * num_per_page
			_end_id = min(data_startid + (Current_i + 1) * num_per_page, data_finishid)
			qset = (
					Q(id__gte=_start_id) &
					Q(id__lte=_end_id) &
					Q(acquisition_timestamp__gte=MinStamp) &
					Q(acquisition_timestamp__lt=MaxStamp) &
					Q(work_section=worksection)
			)
			_list = datamodelname.objects.filter(qset).order_by('acquisition_timestamp')
			for _d in _list:
				try:
					if datatype == 'oxygen':
						_tempValue = max(_tempValue, _d.oxygen_value)
					elif datatype == 'laser':
						_tempValue = max(_tempValue, _d.laser_power)
					elif datatype == 'cncstatus':
						_tempValue = max(_tempValue, _d.Z_value)

					if _d.acquisition_timestamp is None:
						_d.acquisition_timestamp = int(time.mktime(_d.acquisition_time.timetuple()))
						_d.save()
					if _d.acquisition_timestamp - _lastdatatime > Interval:
						_timekey = _d.acquisition_time.strftime('%Y-%m-%d %H:%M:00')
						IntervalDict[_timekey] = (_tempValue if _tempValue != -1 else '')
						_tempValue = -1
						_lastdatatime = _d.acquisition_timestamp
				except:
					pass
		return IntervalDict

	def make_day_data(datatype, indexmodelname, datamodelname, dateint,reDict):
		_date_dt = datetime.datetime.strptime(str(dateint), '%Y%m%d')
		cachevalue = getcache(worksection, _dateint, indexmodelname, datatype)
		# [str(_date + datetime.timedelta(seconds=i * 60)) for i in range(24 * 60)]
		# [str(_date_dt + datetime.timedelta(seconds=i * 60)) for i in range(24 * 60)]
		'''以Interval=60计(1分钟)'''
		# _thisday_datetimelist = [str(_date_dt + datetime.timedelta(seconds=i * 60)) for i in range(24 * 60)]
		_thisday_datetimelist = [str(_date_dt + datetime.timedelta(seconds=i * Interval)) for i in
		                         range(int(24 * 60 * 60 * 1.0 / Interval) + 1)]
		_thisday_allDataDict = {}
		if int(ifForceRefresh) == 0 and cachevalue:
			_thisday_valuelist = cachevalue.split(',')
			'''处理缓存中的数据'''
			for i in zip(_thisday_datetimelist, _thisday_valuelist):
				_thisday_allDataDict[i[0]] = i[1]
		else:
			'''计算当天_date_dt(datetime)的数据,若数据库中无某一时刻的数据，则返回的Dict缺少该项'''
			# make_minute_data(datatype, indexmodelname, datamodelname, dateint, thisdatetime):
			_thisday_existedDataDict = make_minute_data(datatype, indexmodelname,
			                                            datamodelname, _dateint, _date_dt)
			'''更新至包含当天所有分钟的字典'''
			_thisday_allDataDict = {i: '' for i in _thisday_datetimelist}
			_thisday_allDataDict.update(_thisday_existedDataDict)
			'''按时间排序，输出数据，存入cache'''
			itemlist = sorted(_thisday_allDataDict.items(), key=lambda e: e[0])
			_thisday_valuelist = []
			for item in itemlist:
				_thisday_valuelist.append(str(item[1]))
			setcache(worksection, _dateint, indexmodelname, datatype, ','.join(_thisday_valuelist))
		reDict.update(_thisday_allDataDict)
		# print(reDict)
		pass

	'''函数正文'''
	t1=time.time()
	# print(t1)
	try:
		datetime_Start = datetime.datetime.strptime(StartDateTime, '%Y-%m-%d%H:%M')
		datetime_Finish = datetime.datetime.strptime(FinishDateTime, '%Y-%m-%d%H:%M')
	except:
		datetime_Start = datetime.datetime.strptime(StartDateTime, '%Y-%m-%d%H:%M:%S')
		datetime_Finish = datetime.datetime.strptime(FinishDateTime, '%Y-%m-%d%H:%M:%S')
	# datetimelist = []
	Interval=int(Interval)
	deltaT = datetime.timedelta(seconds=Interval)
	deltaTime = datetime_Finish-datetime_Start
	deltaSeconds = deltaTime.days*24*60*60+deltaTime.seconds
	datetimelist=[str(datetime_Start+deltaT*i) for i in range(int(deltaSeconds*1.0/Interval)+1)]

	worksection = Worksection.objects.get(id=WorksectionID)

	t2 = time.time()
	try:
		date_start = datetime_Start.date()
		date_finish = datetime_Finish.date()
		delta_days = (date_finish-date_start).days
		reDict_Oxygen = {i: '' for i in datetimelist}
		reDict_Laser = {i: '' for i in datetimelist}
		reDict_CNCZ = {i: '' for i in datetimelist}

		# 检查每天的记录是否在缓存内
		for i in range(delta_days+1):
			_date= date_start + datetime.timedelta(days=i)
			_dateint = int(_date.strftime('%Y%m%d'))
			make_day_data('oxygen', Process_Oxygendata_Date_Worksection_indexing, Oxygendata, _dateint,reDict_Oxygen)
			make_day_data('laser', Process_Laserdata_Date_Worksection_indexing, Laserdata, _dateint, reDict_Laser)
			make_day_data('cncstatus', Process_CNCStatusdata_Date_Worksection_indexing, CNCProcessStatus, _dateint, reDict_CNCZ)
	except:
		reDict_Oxygen = {}
		reDict_Laser = {}
		reDict_CNCZ = {}
	_dict = {
		'oxydata': list(reDict_Oxygen.values()),
		'laserdata':list(reDict_Laser.values()),
		'cnczdata':list(reDict_CNCZ.values()),
		'datetime': datetimelist,
	}
	# print(reDict['2019-11-19 11:35:00'])
	html = json.dumps(_dict, ensure_ascii=False)
	# print(html)
	print(time.time()-t1)
	return HttpResponse(html, content_type='application/json')

# 以工段id、起止时间、时间间隔查询氧含量数据
@login_required
@csrf_exempt
def queryData_Oxydata_By_WorkSectionDatetime(request, WorksectionID, StartDateTime, FinishDateTime, Interval):
	try:
		datetime_Start = datetime.datetime.strptime(StartDateTime, '%Y-%m-%d%H:%M')
		datetime_Finish = datetime.datetime.strptime(FinishDateTime, '%Y-%m-%d%H:%M')
	except:
		datetime_Start = datetime.datetime.strptime(StartDateTime, '%Y-%m-%d%H:%M:%S')
		datetime_Finish = datetime.datetime.strptime(FinishDateTime, '%Y-%m-%d%H:%M:%S')
	# datetimelist = []

	# 计算日期列表
	Interval=int(Interval)
	deltaT = datetime.timedelta(seconds=Interval)
	deltaTime = datetime_Finish-datetime_Start
	deltaSeconds = deltaTime.days*24*60*60+deltaTime.seconds

	datetimelist=[str(datetime_Start+deltaT*i) for i in range(int(deltaSeconds*1.0/Interval)+1)]

	# 获得氧含量的起始终止id
	worksection = Worksection.objects.get(id=WorksectionID)
	qset = (
			Q(work_section=worksection) &
			Q(index_date_int=int(datetime_Start.strftime('%Y%m%d')))
	)
	oxygen_indexing = Process_Oxygendata_Date_Worksection_indexing.objects.get(qset)
	oxygen_data_startid = oxygen_indexing.oxygendata_start_id
	oxygen_data_finishid = oxygen_indexing.oxygendata_finish_id

	qset = (
			Q(id__gte=oxygen_data_startid) &
			Q(id__lte=oxygen_data_finishid) &
			Q(acquisition_timestamp__gte=int(time.mktime(datetime_Start.timetuple()))) &
			Q(acquisition_timestamp__lte=int(time.mktime(datetime_Finish.timetuple())))
	)
	queryDataSet = Oxygendata.objects.filter(qset).order_by('acquisition_timestamp')
	IntervalDict = {}
	_tempOxyValue = -1
	_lastdatatime = datetime_Start
	for _d in queryDataSet:
		_deltaTime = _d.acquisition_time-datetime_Start
		# _deltaSeconds = _deltaTime.days*24*60*60+_deltaTime.seconds
		_tempOxyValue = max(_tempOxyValue, _d.oxygen_value)
		# if _deltaSeconds%Interval == 0:
		if _d.acquisition_time-_lastdatatime > datetime.timedelta(seconds=Interval):
			# if _d.acquisition_time.strftime('%Y-%m-%d %H:%M:%S')=='2019-11-19 11:35:00':
			# 	pass
			IntervalDict[_d.acquisition_time.strftime('%Y-%m-%d %H:%M:00')] = _tempOxyValue
			_tempOxyValue = -1
			_lastdatatime = _d.acquisition_time
	logger.debug(IntervalDict)
	# print(len(IntervalDict))
	reDict = {i:-1 for i in datetimelist}
	reDict.update(IntervalDict)
	# queryDataSet = map(lambda Q:Q.oxygen_value,queryDataSet)
	_dict = {
		'oxydata': list(reDict.values()),
		'datetime': datetimelist,
	}
	# print(reDict['2019-11-19 11:35:00'])
	html = json.dumps(_dict, ensure_ascii=False)
	# print(html)
	return HttpResponse(html, content_type='application/json')
	# pass

# 以工段id、起止时间、时间间隔查询激光功率数据
@login_required
@csrf_exempt
def queryData_Laserdata_By_WorkSectionDatetime(request, WorksectionID, StartDateTime, FinishDateTime, Interval):
	pass

def queryData_finedata_By_MissionID_with_certain_timestamp(MissionItemID, starttimestamp, finishstamp):
	def patchEmptyData(datalist):
		# for i,_value in enumerate(datalist):
		# 	if i==0 or i==(len(datalist)-1):continue
		#
		# 	if _value is None and not (datalist[i-1] is None) and not (datalist[i+1] is None):
		# 		datalist[i]=(datalist[i-1]+datalist[i+1])/2
		# 		datalist[i]=float('%.3f'%datalist[i])

		return datalist

	_mission = LAMProcessMission.objects.get(id=MissionItemID)
	# _mission_timecut = Process_Mission_timecut.objects.get(process_mission=_mission)
	_worksection_id = _mission.work_section.id
	_finedata_list = RT_FineData.Realtime_FineData.getFineDataList_ByWSID(_worksection_id, starttimestamp, finishstamp)

	_timelist = map(lambda d: d.acquisition_datetime.strftime('%Y-%m-%d %H:%M:%S'), _finedata_list)
	_oxygen_value_list = map(lambda d: d.oxygen_value, _finedata_list)
	_laser_value_list = map(lambda d: d.laser_power, _finedata_list)
	_Z_value_list = map(lambda d: d.Z_value, _finedata_list)
	_feedrate_list = map(lambda d: d.FeedRate_value, _finedata_list)
	_scanningrate_list = map(lambda d: d.ScanningRate_value, _finedata_list)
	# print(len(_timelist))
	_dict = {
		'datetime': list(_timelist),
		'oxydata': patchEmptyData(list(_oxygen_value_list)),
		'laserdata': list(_laser_value_list),
		'cnczdata': patchEmptyData(list(_Z_value_list)),
		'cncfeedratedata': patchEmptyData(list(_feedrate_list)),
		'cncscanningratedata': patchEmptyData(list(_scanningrate_list)),
	}
	return _dict


@login_required
@csrf_exempt
def queryData_finedata_By_MissionID(request, MissionItemID,DateStr,HourStr):
	print('queryData_finedata_By_MissionID start')
	t1=time.time()
	_start_datetime_str = '%s %s:00:00'%(DateStr, HourStr)
	_end_datetime_str = (datetime.datetime.strptime(_start_datetime_str, '%Y-%m-%d %H:%M:%S')+datetime.timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S')
	_dict = queryData_finedata_By_MissionID_with_certain_timestamp(MissionItemID, time_data1(_start_datetime_str), time_data1(_end_datetime_str))

	print(time.time()-t1)
	print('queryData_finedata_By_MissionID return')
	html = json.dumps(_dict, ensure_ascii=False)
	return HttpResponse(html, content_type='application/json')


@login_required
@csrf_exempt
def queryData_finedata_By_MissionID_timestamp(request, MissionItemID,startTimestamp,finishTimestamp):
	'''对指定时间范围进行查询，返回数据'''
	_dict = queryData_finedata_By_MissionID_with_certain_timestamp(MissionItemID, int(startTimestamp), int(finishTimestamp))
	html = json.dumps(_dict, ensure_ascii=False)
	return HttpResponse(html, content_type='application/json')

@login_required
@csrf_exempt
def queryData_Inspect_Complete_MissionLAMProcessRecords(request, MissionItemID):
	inspect_flag = RT_FineData.Realtime_FineData.inspect_complete_processRecord(MissionItemID)
	if inspect_flag == 'Wait_And_Following':
		print('Wait_And_Following')
		return HttpResponse(json.dumps(['Wait_And_Following'], ensure_ascii=False), content_type='application/json')
	elif inspect_flag == 'Query_Database':
		print('Query_Database')
		qset = (
			Q(process_mission=LAMProcessMission.objects.get(id=MissionItemID))
		)
		_discordant_records = Process_Inspect_FineData_DiscordantRecords.objects.filter(qset)
		_dict = {
			'%d'%i.id:
				{
					'id':i.id,
					'start_timestamp':i.start_timestamp,
					'finish_timestamp':i.finish_timestamp,
					'start_time':time_data2(i.start_timestamp),
					'finish_time': time_data2(i.finish_timestamp),
					'condition_cell':str(i.parameter_conditionalcell),
				} for i in _discordant_records
		}
		html = json.dumps(_dict, ensure_ascii=False)
		return HttpResponse(html, content_type='application/json')

	# _dict = {
	# 		'timestampid:%d-%d'%(data['minID'],data['maxID']):
	# 			{'timestamp': '%d~%d' % (data['minID'],data['maxID']),
	# 			 'start_time': time_data2(data['start_timestamp']),
	# 			 'finish_time': time_data2(data['finish_timestamp']),
	# 			 'condition_cell': str(list(map(lambda cell:cell.comment, data['condition_cell']))).replace('[','').replace(']','').replace('\'','')}
	# 		for data in expression_False_gather_list
	# }
	# html = json.dumps(_dict, ensure_ascii=False)
	# # print(html)
	# print('-------')
	# return HttpResponse(html, content_type='application/json')

with lock("global"):
	pass


@csrf_exempt
@lock("global")
def DownloadCNCScreenInfo(request):
	# 获取一条待处理的记录
	global GLOBAL_CNCScreenInfo_IDList
	try:
		while True:
			# logger.debug('GLOBAL_CNCProcessStatus_SendImageBefore_Not_Recive_ITEMlist Length: %d' % len(settings.GLOBAL_CNCProcessStatus_SendImageBefore_Not_Recive_ITEMlist))
			if len(settings.GLOBAL_CNCProcessStatus_SendImageBefore_Not_Recive_ITEMlist) == 0:
				# 发送GLOBAL_CNCProcessStatus_SendImage_MAX_ID+1
				# 更新GLOBAL_CNCProcessStatus_SendImage_Waitfor_Recive_IDlist
				# 	_maxid = CNCProcessStatus.objects.
				settings.GLOBAL_CNCProcessStatus_SendImage_MAX_ID += 1
				item_CNCProcessStatus = CNCProcessStatus.objects.get(id=settings.GLOBAL_CNCProcessStatus_SendImage_MAX_ID)

				'''更新临时辅助参数,保存至数据表'''
				_temp = TemporaryParameter_ID.objects.get(id=1)
				_temp.item_id = settings.GLOBAL_CNCProcessStatus_SendImage_MAX_ID
				_temp.save()
				# logger.debug('GLOBAL_CNCProcessStatus_SendImage_MAX_ID: %d'%settings.GLOBAL_CNCProcessStatus_SendImage_MAX_ID)
			else:
				# 发送GLOBAL_CNCProcessStatus_SendImageBefore_Not_Recive_IDlist列表中数据
				# 更新GLOBAL_CNCProcessStatus_SendImage_Waitfor_Recive_IDlist
				item_CNCProcessStatus = settings.GLOBAL_CNCProcessStatus_SendImageBefore_Not_Recive_ITEMlist.pop(0)
				logger.debug(
					'Not_Recive_ITEMlist: %s' % str(settings.GLOBAL_CNCProcessStatus_SendImageBefore_Not_Recive_ITEMlist))
			if item_CNCProcessStatus.if_exec_intr is None or item_CNCProcessStatus.if_exec_intr == True:
				break

		settings.GLOBAL_CNCProcessStatus_SendImage_Waitfor_Recive_IDlist.append(item_CNCProcessStatus.id)
		logger.debug('Waitfor_Recive_IDlist: %s'%str(settings.GLOBAL_CNCProcessStatus_SendImage_Waitfor_Recive_IDlist))

		# if len(GLOBAL_CNCScreenInfo_IDList)==0:
		# 	t1=time.time()
		# 	pretime = datetime.datetime.now() - datetime.timedelta(hours=0, minutes=3, seconds=0)
		# 	GLOBAL_CNCScreenInfo_IDList = list(CNCProcessStatus.objects.filter(
		# 	Q(if_checked=False) & (Q(check_datetime__isnull=True) | Q(check_datetime__lt=pretime)))[:5000])
		# 	print('--------------------------------------Cost Time:%.2f'%(time.time()-t1))
		# # print(len(GLOBAL_CNCScreenInfo_IDList))
		# item_CNCProcessStatus = GLOBAL_CNCScreenInfo_IDList.pop()

		# print(item_CNCProcessStatus)
		# pretime = datetime.datetime.now() - datetime.timedelta(hours=0, minutes=3, seconds=0)
		# # print(len(CNCProcessStatus.objects.filter(Q(if_checked=False) & (Q(check_datetime__isnull=True)|Q(check_datetime__lt= yesterday)))))
		# # print(int(random.random()*20))
		# item_CNCProcessStatus = CNCProcessStatus.objects.filter(
		# 	Q(if_checked=False) & (Q(check_datetime__isnull=True) | Q(check_datetime__lt=pretime)))[
		# 	int(random.random() * 50)]
		# # item_CNCProcessStatus = CNCProcessStatus.objects.filter(
		# # 	Q(if_checked=False) & (Q(check_datetime__isnull=True) | Q(check_datetime__lt=pretime)))[0]

		CNCProcessStatusid = item_CNCProcessStatus.id
		Worksection_code = item_CNCProcessStatus.work_section.code
		item_CNCProcessStatus.check_datetime = datetime.datetime.now()
		item_CNCProcessStatus.save()
	# print(CNCProcessStatusid)
	except:
		item_CNCProcessStatus = None
		CNCProcessStatusid = -1
		Worksection_code = None
	_dict = {
		'CNCProcessStatus_id': CNCProcessStatusid,
		'Worksection_code': Worksection_code,
	}
	logger.info('Send CNCProcessStatus_id:%d' % CNCProcessStatusid)
	html = json.dumps(_dict, ensure_ascii=False)
	# print(html)
	return HttpResponse(html, content_type='application/json')


@csrf_exempt
def DownloadCNCScreenImage_by_id(requests, cncstatus_id):
	# 对选中的一条记录下载截图
	try:
		# print(0)
		item_CNCProcessStatus = CNCProcessStatus.objects.get(id=cncstatus_id)
		# print(1)
		# print(settings.MEDIA_URL)
		# print(item_CNCProcessStatus.screen_image)
		# image_path = settings.MEDIA_URL + str(item_CNCProcessStatus.screen_image)
		# print(2)
		# with open(image_path, 'rb') as f:
		# 	image_data = f.read()
		# 	print(3)
		# print(4)
		# print(image_data)
		return HttpResponse(item_CNCProcessStatus.screen_image.file, content_type='image/png')
	except:
		image_data = None
		# print(image_data)
		item_CNCProcessStatus = CNCProcessStatus.objects.get(id=cncstatus_id)
		item_CNCProcessStatus.if_checked = True
		item_CNCProcessStatus.save()
		print('Image Not Found!')
		return HttpResponse(None, content_type='image/png')
# return HttpResponse(image_data, content_type='image/png')

@login_required
@csrf_exempt
def queryData_RecordLastTime_by_WorksectionID(requests, WorksectionID):
	recordLastTime = {}
	recordLastTime['laser'] = str(CacheOperator('recordLastTime', True, (WorksectionID, 'laser')))
	recordLastTime['oxygen'] = str(CacheOperator('recordLastTime', True, (WorksectionID, 'oxygen')))
	recordLastTime['cncstatus'] = str(CacheOperator('recordLastTime', True, (WorksectionID, 'cncstatus')))

	html = json.dumps(recordLastTime, ensure_ascii=False)
	return HttpResponse(html, content_type='application/json')

@login_required
@csrf_exempt
def queryData_RealTimeRecord_by_WorksectionID(requests, WorksectionID):
	_dict = RealtimeRecord.Realtime_Records.getRecords(WorksectionID)
	# print(reDict['2019-11-19 11:35:00'])
	html = json.dumps(_dict, ensure_ascii=False)
	# print(html)
	return HttpResponse(html, content_type='application/json')

# print('query_view.py end')


@login_required
@csrf_exempt
def queryData_ProgressBarValue_InspectionLAMRecords_By_MissionID(request, MissionID):

	cache_value = CacheOperator('ProgressBarValue_CompleteInspect_MissionId', True, MissionID, None)
	# print('get:',cache_value)
	if cache_value == None:
		cache_value = 0.0

		pass
	_dict = {
		'progress_rate':'%.5f%%'%(100*cache_value),
	}
	html = json.dumps(_dict, ensure_ascii=False)
	return HttpResponse(html, content_type='application/json')