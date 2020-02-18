# -*- coding: gbk -*-
# print('start process_realtime_finedata')
from django.conf import settings
from LAMProcessData.models import *
from LAMProcessData.forms import *
import time
import datetime
import threading
from django.core.cache import cache
from django.db.models import Q
import os

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
	'''暂时未使用
	:param operateType:
		'WS_CrtMissionId' 未用
		'ProgressBarValue_CompleteInspect_MissionId'    对某任务的过程记录进行检查 可能为None, x, 100三种状态
	:param ifget:
	:param ParamSet:    (worksectionid,datatype)
		datatype:laser, oxygen, cncstatus
	:param data:
	:return:
	'''
	revalue = None

	if operateType == 'WS_CrtMissionId':
		# 当工段正在工作时，得到当前任务id
		worksectionid = ParamSet[0]
		datatype = ParamSet[1]
		key = 'CrtMissionId_WS%s'%(worksectionid)
		# _ws_crt_mission = Worksection_Current_LAMProcessMission.objects.get(
		# 	work_section=Worksection.objects.get(id=worksectionid))

		if not ifget:
			# set cache
			_ws_crt_mission = Worksection_Current_LAMProcessMission.objects.get(
				work_section=Worksection.objects.get(id=worksectionid))
			if _ws_crt_mission.if_onwork:
				# worksection is on work
				cache.set(key,_ws_crt_mission.process_mission.id)
			else:
				# cache.delete(key)
				cache.set(key, None)
				return 'NotOnWork'
		else:
			# get cache
			revalue = cache.get(key)
			if revalue==None:
				re = CacheOperator(operateType, False, ParamSet, data)
				if re=='NotOnWork':
				# 	非工作
					revalue=None
				else:
					revalue = cache.get(key)
	elif operateType == 'ProgressBarValue_CompleteInspect_MissionId':
		missionid = ParamSet
		key = 'PBR_Insp_MsID%s' % (missionid)
		if not ifget:
			# print('set:',data)
			cache.set(key, data)
		else:
			revalue = cache.get(key)

	return revalue



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


class Realtime_FineData():
	__lock = threading.Lock()
	__Tomorrow_rows_initializing = False
	__Oneday_rows_initializing_list = []
	__Last_initialize_tomorrow_rows_timestamp = TemporaryParameter_ID.objects.get(id=6).item_id

	__Models_ByWorkSectionID_Dict={
		'1': Process_Realtime_FineData_By_WorkSectionID_1,
		'2': Process_Realtime_FineData_By_WorkSectionID_2,
		'3': Process_Realtime_FineData_By_WorkSectionID_3,
		'4': Process_Realtime_FineData_By_WorkSectionID_4,
		'5': Process_Realtime_FineData_By_WorkSectionID_5,
		'6': Process_Realtime_FineData_By_WorkSectionID_6,
	}
	def __init__(self):
		pass

	@classmethod
	def getFineDataModel_ByWSID(cls, WSID):
		return Realtime_FineData.__Models_ByWorkSectionID_Dict[WSID]

	@classmethod
	def getFineDataList_ByWSID(cls, WSID, starttimestamp, endtimestamp):
		# def patchEmptyData(datalist):
		# 	for i, _value in enumerate(datalist):
		# 		if i == 0 or i == (len(datalist) - 1): continue
		#
		# 		if _value is None and not (datalist[i - 1] is None) and not (datalist[i + 1] is None):
		# 			datalist[i] = (datalist[i - 1] + datalist[i + 1]) / 2
		# 			datalist[i] = float('%.3f' % datalist[i])
		#
		# 	return datalist

		_model = cls.getFineDataModel_ByWSID(str(WSID))
		qset = (
				Q(acquisition_timestamp__gte=starttimestamp) &
				Q(acquisition_timestamp__lte=endtimestamp)
		)
		_finedata_list = _model.objects.filter(qset).order_by('acquisition_timestamp')

		return _finedata_list

	@classmethod
	def init_Tomorrow_rows(cls):
		tomorrow_starttime_str = (datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d 00:00:00')
		tomorrow_starttime_struct = time.strptime(tomorrow_starttime_str, "%Y-%m-%d %H:%M:%S")
		tomorrow_starttime_stamp = int(time.mktime(tomorrow_starttime_struct))
		# 若已经将明天的条目初始化，则退出
		if (tomorrow_starttime_stamp - cls.__Last_initialize_tomorrow_rows_timestamp < 24 * 60 * 60):
			return

		# 加锁
		cls.__lock.acquire()
		if not cls.__Tomorrow_rows_initializing:
			cls.__Tomorrow_rows_initializing = True

			try:
				hour_starttime_stamp = tomorrow_starttime_stamp
				for _hour in range(24):
					_hour_stamp_list = [hour_starttime_stamp + _hour*3600 + i for i in range(3600)]

					for _wsid,_model in Realtime_FineData.__Models_ByWorkSectionID_Dict.items():
						# print('start %s' % _wsid)
						insert_data_list = [_model(acquisition_timestamp=i, acquisition_datetime=datetime.datetime.fromtimestamp(i)) for i in _hour_stamp_list]
						_model.objects.bulk_create(insert_data_list)
						# print('finish %s'%_wsid)
				cls.__Last_initialize_tomorrow_rows_timestamp = time.mktime(datetime.datetime.now().timetuple())

				_temp = TemporaryParameter_ID.objects.get(id=6)
				_temp.item_id = cls.__Last_initialize_tomorrow_rows_timestamp
				_temp.save()
			finally:
				cls.__Tomorrow_rows_initializing=False

		# 修改完成，释放锁
		cls.__lock.release()

	@classmethod
	def init_OneDay_rows(cls, _timestamp):
		# tomorrow_starttime_str = (datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d 00:00:00')
		# day_starttime_struct = time.strptime(day_starttime_str+' 00:00:00', "%Y-%m-%d %H:%M:%S")
		# day_starttime_stamp = int(time.mktime(day_starttime_struct))
		# 若已经将明天的条目初始化，则退出
		# if (day_starttime_stamp - cls.__Last_initialize_tomorrow_rows_timestamp < 24 * 60 * 60):
		# 	return

		# 加锁
		cls.__lock.acquire()
		_timeArray = time.localtime(_timestamp)
		day_starttime_stamp=int(time.mktime(time.strptime(time.strftime("%Y-%m-%d 00:00:00", _timeArray), "%Y-%m-%d %H:%M:%S")))
		if day_starttime_stamp not in cls.__Oneday_rows_initializing_list:
			try:
				hour_starttime_stamp = day_starttime_stamp
				# 遍历24小时
				for _hour in range(24):
					_hour_stamp_list = [hour_starttime_stamp + _hour * 3600 + i for i in range(3600)]
					# 遍历每个worksection表
					for _wsid, _model in Realtime_FineData.__Models_ByWorkSectionID_Dict.items():
						try:
							insert_data_list = [_model(acquisition_timestamp=i, acquisition_datetime=datetime.datetime.fromtimestamp(i)) for i in _hour_stamp_list]
							_model.objects.bulk_create(insert_data_list)
						except:
							pass

				cls.__Oneday_rows_initializing_list.append(day_starttime_stamp)
			except:
				pass

		# 修改完成，释放锁
		cls.__lock.release()

	@classmethod
	def add_processRecord(cls, timestamp, WSID, RecordValueDict):
		# print(timestamp)
		# print('RecordValueDict:', RecordValueDict)
		_model = Realtime_FineData.getFineDataModel_ByWSID(str(WSID))
		_record = _model.objects.filter(acquisition_timestamp=timestamp)
		if not _record:
			cls.init_OneDay_rows(timestamp)
			_record = _model.objects.filter(acquisition_timestamp=timestamp)
		_record.update(**RecordValueDict)
		# _record.save()
		# print(_record.oxygen_value)

		# https: // blog.csdn.net / qq_43567641 / article / details / 94740704
		# Staff.objects.filter(id=get_id).update(action_flag=0, username=Concat(F('username'), Value("_lizhi")))

		# if RecordType=='laser':
		# 	# _laser_power = RecordValueDict['laser_power']
		# 	_model.objects.filter(acquisition_timestamp=timestamp).update(**RecordValueDict)
		# elif RecordType=='oxygen':
		# 	pass
		# elif RecordType=='cncstatus':
		# 	pass



	@classmethod
	def inspect_complete_processRecord(cls, MissionID, Last_HeatTreatment_Timestamp = None):


		def inspect_Sigma_formula(formula, finedatalist, CertainTimestamp):
			pass
		def inspect_one_ConditionalCell_formula(formula, finedata):
			'''
			在指定时间点CertainTimestamp，计算finedata的符合性
			判断一条FineData是否符合formula, formula可以是precondition，也可以是expression
			:param formula: 公式
			:param finedata: 一条过程记录实例
			:return:
			('and','且'),
			('or','或'),
			('not','非'),
			('{P_laser}','激光功率(W)'),
			('{P_oxy}','气氛氧含量(ppm)'),
			('{P_x}','工件坐标X(mm)'),
			('{P_y}','工件坐标Y(mm)'),
			('{P_z}','工件坐标Z(mm)'),
			('{P_feed}','机床进给率(%)'),
			('{P_scanspd}','移动扫描速率(mm/min)'),
			('{P_TimeStamp}','数据点时间戳(second)'),
			('{Sigma} A {WHILE} B {/Sigma}','当B为真时，求A的叠加值'),
			('{NOW_TimeStamp}','当前时间戳(second)'),
			('{Last_PowerOFF_TimeStamp}','数据点以前最近一次激光停光时间戳(second)'),
			('{DeltaTime_To_Now}','数据点距今时间(second)'),
			('{Last_HeatTreatment_TimeStamp}','数据点以前最近一次无应力状态时间戳(second)')
			'''
			lmd_getDigitParam = lambda p: float(p) if p is not None else 'None'
			_label_data_dict = {
				'{P_programname}': '\'%s\''%finedata.program_name,
				'{P_laser}': lmd_getDigitParam(finedata.laser_power),
				'{P_oxy}': lmd_getDigitParam(finedata.oxygen_value),
				'{P_x}': lmd_getDigitParam(finedata.X_value),
				'{P_y}': lmd_getDigitParam(finedata.Y_value),
				'{P_z}': lmd_getDigitParam(finedata.Z_value),
				'{P_feed}': lmd_getDigitParam(finedata.FeedRate_value),
				'{P_scanspd}': lmd_getDigitParam(finedata.ScanningRate_value),
				'{P_TimeStamp}': int(finedata.acquisition_timestamp),
				'{Last_PowerOFF_TimeStamp}': Last_PowerOFF_TimeStamp if Last_PowerOFF_TimeStamp is not None else int(
					finedata.acquisition_timestamp),
				'{Last_HeatTreatment_TimeStamp}': Last_HeatTreatment_Timestamp,
				# 对后期截止到某时间点（CertainTimestamp）计算有效，如无指定，则以finedata时间作为CertainTimestamp
				# '{NOW_TimeStamp}': int(CertainTimestamp) if CertainTimestamp is not None else int(finedata.acquisition_timestamp),
				# '{DeltaTime_To_Now}': (int(CertainTimestamp)  if CertainTimestamp is not None else int(finedata.acquisition_timestamp))
				#                       -int(finedata.acquisition_timestamp),

				# '{Sigma} A {Until CertainTime WHILE} B {/Sigma}': '', #待处理 CertainTime由程序自动赋值
			}
			_new_formula = formula
			for _key, _value in _label_data_dict.items():
				_new_formula=_new_formula.replace(_key, str(_value))
			if '{Sigma}' not in _new_formula:
				return eval(_new_formula)



			''' End inspect_one_ConditionalCell_formula '''

		def inspect_one_processRecord(finedata):
			'''判断一条FineData是否符合参数包'''
			# 首先得到列表：本条finedata都符合哪些条件单元
			_final_conditional_cell_list = []
			for _cond_cell in _conditional_cell_list:
				if inspect_one_ConditionalCell_formula(_cond_cell.precondition, finedata):
					_final_conditional_cell_list.append(_cond_cell)
					if _cond_cell.instead_Cond_Cell and _cond_cell.instead_Cond_Cell in _final_conditional_cell_list:
						_final_conditional_cell_list.remove(_cond_cell.instead_Cond_Cell)
			# 然后再逐条判断表达式expression是否符合，如有不符合，则返回False
			_discordant_cell_list = []
			for _cond_cell in _final_conditional_cell_list:
				if not inspect_one_ConditionalCell_formula(_cond_cell.expression, finedata):
					_discordant_cell_list.append(_cond_cell)
			if _discordant_cell_list==[]:
				return True, _discordant_cell_list
			else:
				return False, _discordant_cell_list

			''' End inspect_one_processRecord '''

		''' start inspect_complete_processRecord '''
		print('start inspect_complete_processRecord')
		# 若系统上正在运行本mission的检查，则直接退出，返回等待查询flag
		_current_progressBar_Rate = CacheOperator('ProgressBarValue_CompleteInspect_MissionId', True, MissionID, None)
		if _current_progressBar_Rate==1.0:
			# 查询数据库，直接返回结果
			pass
		elif type(_current_progressBar_Rate) in (float,int) and _current_progressBar_Rate<1.0:
			return 'Wait_And_Following'
		elif _current_progressBar_Rate==None:
			# 查询数据库，如有则直接返回结果，如没有则进行后续计算
			pass


		# print("%s is running" % os.getpid())
		t1 = time.time()
		# 上次停光的时间，初始为None，由出光转为停光后赋值当前时间
		Last_PowerOFF_TimeStamp = None
		# 前一时刻是否开光
		PreTime_If_Laser_PowerOn = False
		# 数据点以前最近一次无应力状态时间戳(second)，若无初始设置，则以任务开始时间赋值，见后
		# 事后对整个过程记录进行检查
		_mission = LAMProcessMission.objects.get(id = MissionID)

		'''得到Finedata'''
		_worksection = _mission.work_section

		'''得到起止时间戳'''
		_mission_timecut = Process_Mission_timecut.objects.get(process_mission = _mission)
		process_start_time = _mission_timecut.process_start_time
		process_finish_time = _mission_timecut.process_finish_time
		_start_timestamp = time_data1(process_start_time)

		Last_HeatTreatment_Timestamp = _start_timestamp if Last_HeatTreatment_Timestamp is None else Last_HeatTreatment_Timestamp
		try:
			_finish_timestamp = time_data1(process_finish_time)
		except:
			_finish_timestamp = int(time.time())

		'''得到参数包'''
		_process_parameter = _mission.LAM_techinst_serial.process_parameter
		_conditional_cell_list = list(_process_parameter.conditional_cell.all().order_by('level'))

		_finedata_list = Realtime_FineData.getFineDataList_ByWSID(_worksection.id, _start_timestamp, _finish_timestamp)

		t2 = time.time()
		print(t2-t1)
		expression_result_list = []

		data_length=len(_finedata_list)
		for num,i in enumerate(_finedata_list):
			expression_result_list.append((i, inspect_one_processRecord(i)))
			# 更新进度条
			CacheOperator('ProgressBarValue_CompleteInspect_MissionId', False, MissionID, num/data_length)
		# 进度条数据更新至100%
		CacheOperator('ProgressBarValue_CompleteInspect_MissionId', False, MissionID, 1.0)

		expression_False_list = filter(lambda i: not i[1][0], expression_result_list)
		t3 = time.time()
		print(t3 - t2)

		'''将不符合的列表按类别聚集、时间连续后输出'''
		''''[[minID, maxID, starttime, finishtime, condition_cell]]'''
		expression_False_gather_list = []
		false_item = {'minID': None,
		              'maxID': None,
		              'start_timestamp': None,
		              'finish_timestamp': None,
		              'condition_cell': None}
		for i in list(expression_False_list):
			if false_item['condition_cell'] is None:
				false_item['minID'] = i[0].id
				false_item['start_timestamp'] = i[0].acquisition_timestamp
				false_item['condition_cell'] = i[1][1]
			elif false_item['condition_cell'] == i[1][1]:
				false_item['maxID'] = i[0].id
				false_item['finish_timestamp'] = i[0].acquisition_timestamp
			else:
				if false_item['maxID'] is None:
					false_item['maxID'] = i[0].id
					false_item['finish_timestamp'] = i[0].acquisition_timestamp
				expression_False_gather_list.append(false_item)
				false_item = {'minID': i[0].id,
				              'maxID': None,
				              'start_timestamp': i[0].acquisition_timestamp,
				              'finish_timestamp': None,
				              'condition_cell': str(map(lambda _l:str(_l.comment),i[1][1]))}
		return expression_False_gather_list

