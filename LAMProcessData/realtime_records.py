# -*- coding: gbk -*-
import datetime
import time
import threading
import LAMProcessData.process_realtime_finedata as RT_FineData

RecordTypes = ('laser', 'oxygen', 'cncstatus')
BlankValue = ''
class Realtime_Records():
	lock = threading.Lock()
	# ����������
	records_count = 60*60
	WS_RT_RC_Dict = {}
	# ����ò���
	CleanupParam_crt = 0
	CleanupParam_Max = 10

	# ��¼�������θ��ּ�¼����������ʱ��stamp,�˴β�ͬ��View��CacheOperator���������ص����������ϴ�ʱ�������ݲ���
	lastrecord_time = {}
	# ��¼�������θ��ּ�¼�������ʱ��stamp����ʱ�䲻ͬ��lastrecord_time����ʹû�������ϴ����˲����Բ�ͣ����
	lastcheck_time = {}
	# WS_RT_Time_list= []

	def __init__(self):
		# Realtime_Records.WS_RT_Time_list = [(datetime.datetime.now() - datetime.timedelta(seconds=(Realtime_Records.records_count - i))).strftime('%Y-%m-%d %H:%M:%S')
		#                                     for i in range(Realtime_Records.records_count)]

		pass

	@classmethod
	def getlastrecord_time(cls, worksection_ID, recordType):
		# print('getlastrecord_time')
		# print(cls.lastrecord_time)
		# print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(cls.lastrecord_time['%s-%s'%(worksection_ID, recordType)])))
		# return cls.lastrecord_time['%s-%s'%(worksection_ID, recordType)]
		return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(cls.lastrecord_time['%s-%s'%(worksection_ID, recordType)]))

	@classmethod
	def addWorksection(cls, worksection_ID):

		cls.WS_RT_RC_Dict[worksection_ID] = {tp:[] for tp in RecordTypes}
		# cls.WS_RT_RC_Dict[worksection_ID] = {
		# 	'laser':[],
		#     'oxygen':[],
		# 	'cncstatus':[]}
		now_timestamp = time.mktime(datetime.datetime.now().timetuple())
		# print('now_timestamp', now_timestamp)
		for tp in RecordTypes:
			cls.lastrecord_time['%s-%s' % (worksection_ID, tp)] = int(now_timestamp)
			cls.lastcheck_time['%s-%s' % (worksection_ID, tp)] = int(now_timestamp)


		finedata_list = list(RT_FineData.Realtime_FineData.getFineDataList_ByWSID(worksection_ID, now_timestamp-cls.records_count, now_timestamp))

		RecordType_to_FineDataField = {'laser':'laser_power','oxygen':'oxygen_value','cncstatus':'Z_value'}
		for tp in ['laser', 'oxygen']:
			cls.WS_RT_RC_Dict[worksection_ID][tp] = [(_finedata.acquisition_timestamp, _finedata.__getattribute__(RecordType_to_FineDataField[tp]) if (_finedata.__getattribute__(RecordType_to_FineDataField[tp]) is not None and _finedata.__getattribute__(RecordType_to_FineDataField[tp]) > 0) else '') for _finedata in finedata_list]

		cls.WS_RT_RC_Dict[worksection_ID]['cncstatus'] = [
			(_finedata.acquisition_timestamp, _finedata.__getattribute__(RecordType_to_FineDataField['cncstatus'])) for _finedata
			in finedata_list]

	# cls.lastrecord_time['%s-%s' % (worksection_ID, 'laser')] = int(now_timestamp)
		# cls.lastrecord_time['%s-%s' % (worksection_ID, 'oxygen')] = int(now_timestamp)
		# cls.lastrecord_time['%s-%s' % (worksection_ID, 'cncstatus')] = int(now_timestamp)
		# print(datetime.datetime.now().timetuple())
		# print(cls.lastrecord_time)
		# print('addWorksection')
	# @classmethod
	# def setLastCheckTime(cls, worksection_ID, recordType,timestamp):
	# 	cls.lastcheck_time['%s-%s' % (worksection_ID, recordType)] = timestamp
	#
	#
	# @classmethod
	# def getLastCheckTime(cls, worksection_ID, recordType):
	# 	return cls.lastcheck_time['%s-%s'%(worksection_ID, recordType)]



	@classmethod
	def addRecords(cls, worksection_ID, recordType, recordtime, recordValue):
		# print('addRecords', worksection_ID, recordType, recordtime, recordValue)
		'''
		:param worksection_ID:
		:param recordType: 'laser', 'oxygen', 'cncstatus'
		:param recordtime: timestamp(int)
		:param recordValue:
		:return:
		'''
		# cls.updateNow(worksection_ID)
		# ����
		cls.lock.acquire()
		try:
			# �������ʱ����벢�ÿ�

			# print('in addRecords', cls.lastcheck_time)
			if recordType=='laser':
				# logger.debug(cls.WS_RT_RC_Dict[str(worksection_ID)][recordType])
				# print(cls.WS_RT_RC_Dict[str(worksection_ID)][recordType])
				pass
			lastrecord_Timestamp = cls.lastcheck_time['%s-%s'%(worksection_ID, recordType)]
			# lastrecord_Timestamp = cls.getLastCheckTime(worksection_ID, recordType)
			if recordtime > lastrecord_Timestamp:
				# ��ǰ��������������ϴ�����¼��ʱ�䣬���м�������¿հ�
				for i in range(1, int(recordtime-lastrecord_Timestamp)):
					cls.WS_RT_RC_Dict[str(worksection_ID)][recordType].append((lastrecord_Timestamp+i, BlankValue))
				# ���뱾����
				cls.WS_RT_RC_Dict[str(worksection_ID)][recordType].append((recordtime, recordValue))
				# ����
				cls.lastcheck_time['%s-%s' % (worksection_ID, recordType)] = recordtime
				cls.lastrecord_time['%s-%s' % (worksection_ID, recordType)] = recordtime
				# print('addRecords')
				if recordType == 'laser':
					print(cls.lastcheck_time['%s-%s' % (worksection_ID, recordType)])

			elif recordtime > lastrecord_Timestamp-cls.records_count:
				# ��ǰ��������������ϴμ�¼��ʱ�䣬�����ڸ�������ʱ�䣬����ļ�¼
				for i in range(len(cls.WS_RT_RC_Dict[str(worksection_ID)][recordType]),0,-1):
					if cls.WS_RT_RC_Dict[str(worksection_ID)][recordType][i-1][0] == recordtime:
						cls.WS_RT_RC_Dict[str(worksection_ID)][recordType][i-1] = (recordtime, recordValue)
						# cls.WS_RT_RC_Dict[str(worksection_ID)][recordType][i-1][1] = recordValue
						pass

						break
			# print(cls.WS_RT_RC_Dict)
		finally:
			# �޸���ɣ��ͷ���
			cls.CleanupParam_crt += 1
			cls.lock.release()

			if cls.CleanupParam_crt >= cls.CleanupParam_Max:
				cls.CleanupParam_crt = 0
				cls.cleanRecords()


	@classmethod
	def cleanRecords(cls):
		# print('cleanRecords')
		# ����
		cls.lock.acquire()
		now_timestamp = int(time.mktime(datetime.datetime.now().timetuple()))
		cleanout_timestamp = now_timestamp - cls.records_count
		def checkByTimestamp(tp):
			return tp[0] >= cleanout_timestamp
		try:
			for worksection_ID in cls.WS_RT_RC_Dict:
				for recordType in RecordTypes:
					cls.WS_RT_RC_Dict[worksection_ID][recordType] = list(filter(checkByTimestamp, cls.WS_RT_RC_Dict[worksection_ID][recordType]))
		finally:
			# �޸���ɣ��ͷ���
			cls.lock.release()

	@classmethod
	def updateNow(cls, worksection_ID):
		# print('updateNow')
		'''
		�Ե�ǰʱ�䲹��
		:param worksection_ID:
		:return:
		'''
		# ����
		cls.lock.acquire()
		# print(cls.lastcheck_time)
		now_timestamp = time.mktime(datetime.datetime.now().timetuple())
		try:
			for recordType in RecordTypes:
				_key = '%s-%s' % (worksection_ID, recordType)
				if now_timestamp - cls.lastcheck_time[_key]>1:
					# ��ǰ��������������ϴ�����¼��ʱ�䣬���м�������¿հ�
					cls.WS_RT_RC_Dict[str(worksection_ID)][recordType].extend([(cls.lastcheck_time[_key] + i, BlankValue) for i in range(1, 1+int(now_timestamp - cls.lastcheck_time[_key]))])
					# for i in range( int(now_timestamp - cls.lastcheck_time[_key])):
					# 	cls.WS_RT_RC_Dict[str(worksection_ID)][recordType].append((cls.lastcheck_time[_key] + i, BlankValue))
					cls.lastcheck_time[_key] = now_timestamp
					# print('updateNow')
		finally:
			# �޸���ɣ��ͷ���
			# print(len(cls.WS_RT_RC_Dict[str(worksection_ID)]['laser']))
			# print(cls.WS_RT_RC_Dict[str(worksection_ID)]['laser'])
			cls.lock.release()
			if len(cls.WS_RT_RC_Dict[str(worksection_ID)]['laser']) > cls.CleanupParam_Max:
				cls.cleanRecords()


	@classmethod
	def getRecords(cls, worksection_ID):
		# print('getRecords')
		'''

		:param worksection_ID:
		:return:
		'''
		# ����ʱ��
		cls.updateNow(worksection_ID)
		try:
			# ����
			cls.lock.acquire()
			now_timestamp = int(time.mktime(datetime.datetime.now().timetuple()))
			cleanout_timestamp = now_timestamp - cls.records_count
			def checkByTimestamp(tp):
				return tp[0] >= cleanout_timestamp and tp[0] < (now_timestamp-2)
			_dict = {}
			for recordType in RecordTypes:
				filter_by_Timestamp = filter(checkByTimestamp, cls.WS_RT_RC_Dict[str(worksection_ID)][recordType])
				filter_value = [i[1] for i in filter_by_Timestamp]
				_dict[recordType] = filter_value
				filter_by_Timestamp = filter(checkByTimestamp, cls.WS_RT_RC_Dict[str(worksection_ID)][recordType])
				filter_time = [time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(i[0])) for i in filter_by_Timestamp]
				_dict['datetime'] = filter_time
			# _dict['datetime'] = [(datetime.datetime.now() - datetime.timedelta(seconds=(Realtime_Records.records_count - i))).strftime('%Y-%m-%d %H:%M:%S')
			#                                     for i in range(Realtime_Records.records_count)]
		finally:
			# print('now_timestamp:',now_timestamp)
			# for i in _dict:
			# 	print(len(_dict[i]))
			# 	try:
			# 		print(i, cls.WS_RT_RC_Dict[str(worksection_ID)][i][0],cls.WS_RT_RC_Dict[str(worksection_ID)][i][-1])
			# 	except:
			# 		pass
			cls.lock.release()

		return _dict