import requests
import uuid
import os

def get_mac_address():
	node = uuid.getnode()
	mac = uuid.UUID(int = node).hex[-12:]
	return mac



if __name__ == '__main__':
	url = 'http://127.0.0.1:8080/LAMProcessData/CNCData/Update/'
	mac = {'macaddress': get_mac_address()}
	rootdir = r'E:\1.chenbo\1-program\14-PrintScreen\DATA CT04'
	# DeviceCode = "sc-ct-01"
	list = os.listdir(rootdir)
	for i in range(0, len(list)):
		path = os.path.join(rootdir, list[i])
		if os.path.isfile(path):
			if list[i].startswith('CT01'):
				DeviceCode = "sc-ct-01"
			elif list[i].startswith('CT02'):
				DeviceCode = "sc-ct-02"
			elif list[i].startswith('CT04'):
				DeviceCode = "sc-ct-04"
			elif list[i].startswith('CT06'):
				DeviceCode = "sc-ct-06"
		files = {"file":open(path,"rb")}
		r = requests.post(url, data=mac, files=files)
		if 'Success' not in r.text:
		# if r.text == 'A server error occurred.  Please contact the administrator.':
			print(path)
			pass
		# print(r.text)




# files = {"file":open(r"E:\1.chenbo\1-program\14-PrintScreen\DATA CT04\20180919 083459.png","rb")}
# r = requests.post(url, data=mac, files=files)