# -*- coding: gbk -*-
from PIL import ImageGrab
import time
# import thread
import threading
import requests
import uuid
import os
from LoadSettings import SettingDict

def get_mac_address():
	node = uuid.getnode()
	mac = uuid.UUID(int = node).hex[-12:]
	return mac

def GET_TIME_STRING(format = 1,writetime = None):
    if format == 1:
        return time.strftime('%Y-%m-%d %H:%M:%S',(time.localtime(),writetime)[writetime!=None])
    elif format == 2:
        return str(datetime.datetime.now()).replace('-','').replace(':','').replace('.','')
    elif format == 3:
        '''得到当前日期，命名文件名'''
        return time.strftime('%Y%m%d %H%M%S', time.localtime())


def UpdateScreen(imgfilepathname):
    img = open(imgfilepathname, "rb")
    files = {"file": img}
    r = requests.post(url, data=mac, files=files)
    # print(url)
    # print(mac)
    # print(r.text)
    # print(imgfilepathname)
    img.close()
    os.remove(imgfilepathname)
    print(r.text)
    # if 'Success' in r.text:
    #     print('Success!')
    # else:
    #     print('Failed')

class GrabScreenThread(threading.Thread):  # The timer class is derived from the class threading.Thread
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):  # Overwrite run() method, put what you want the thread do here
        while True:
            im = ImageGrab.grab()
            imgfilepathname = '%s.png' % GET_TIME_STRING(format=3)
            im.save(imgfilepathname)
            im.close()
            # im = None
            try:
                UpdateScreen(imgfilepathname)
                time.sleep(WaitSeconds)
            except:
                print('Access Declined!')
                time.sleep(DecliendSeconds)
            # UpdateScreen(im)

    def stop(self):
        self.exit_thread()
        # time.sleep(0.5)
        # self.exit_thread()
if __name__ == '__main__':
    url = SettingDict['[UpdataURL]']
    WaitSeconds = int(SettingDict['[Seconds]'])
    DecliendSeconds = int(SettingDict['[DeclinedSeconds]'])
    mac = {'macaddress': get_mac_address()}

    GrabScreenThread = GrabScreenThread()
    GrabScreenThread.run()
# GrabScreenThread.start()