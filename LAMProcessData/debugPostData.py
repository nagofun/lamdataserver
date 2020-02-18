# coding=utf-8
import requests
import random
import time, datetime
import math



starttime = time.mktime(datetime.datetime.now().timetuple())
# starttime = datetime.datetime.now()

def postData():
	while True:
		t_start = time.time()
		try:
			data = {
				'macaddress':'98eecb499fb3',
				'oxygen_value':50+100*math.sin((time.mktime(datetime.datetime.now().timetuple())-starttime)*0.01),
				'oxygen_sensor_value':20*random.random(),
				'internal_pressure_value':random.random(),
			}
			r = requests.post('http://127.0.0.1:8080/LAMProcessData/LAMProcessData/UpdateOxygenData/', data)
			print(r)

			# data = {
			# 	'macaddress': '98eecb499fb3',
			# 	'oxygen_value': 50 + 100 * math.cos((time.mktime(datetime.datetime.now().timetuple()) - starttime) * 0.01),
			# 	'oxygen_sensor_value': 20 * random.random(),
			# 	'internal_pressure_value': random.random(),
			# }
			# r = requests.post('http://127.0.0.1:8080/LAMProcessData/LAMProcessData/UpdateOxygenData/', data)
			# print(r)
		except:
			pass

		# time.sleep(t_start+1-time.time())
		print(time.time()-t_start)
		time.sleep(0.8)
if __name__ == '__main__':
	postData()