# -*- coding: gbk -*-
import cv2
import json

#差值感知算法 adarray数组
def dHash_ndarray(array):
    hash_str=''
    shape = array.shape
    newarray= array.reshape(1,shape[0]*shape[1])[0]
    for i in newarray:
        hash_str = hash_str + '1' if i > 125 else hash_str + '0'
    return hash_str

if __name__ == '__main__':
    with open("./IMAGE Templates/ImageSectionInfo.json",'r') as load_f:
        load_dict = json.load(load_f)
        print(load_dict)

    for Device in load_dict:
        # print(Device["DeviceCode"])
        image = cv2.imread(Device["TemplateFilePath"])

        '''自动界面'''
        cutimageCoordinate = Device["IdentifyAutoRegion"]
        IdentifyRegion_Image = image[cutimageCoordinate[1]:cutimageCoordinate[3],
                                   cutimageCoordinate[0]:cutimageCoordinate[2]]
        grayImage = cv2.cvtColor(IdentifyRegion_Image, cv2.COLOR_BGR2GRAY)
        ret2, thresh = cv2.threshold(grayImage, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        Device["IdentifyAutoCode"] = dHash_ndarray(thresh)
        # cv2.imshow('自动', thresh)
        # cv2.waitKey(0)

        '''运行状态'''
        cutimageCoordinate = Device["IdentifyExecuteRegion"]
        IdentifyRegion_Image = image[cutimageCoordinate[1]:cutimageCoordinate[3],
                                   cutimageCoordinate[0]:cutimageCoordinate[2]]
        grayImage = cv2.cvtColor(IdentifyRegion_Image, cv2.COLOR_BGR2GRAY)
        ret2, thresh = cv2.threshold(grayImage, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        Device["IdentifyExecuteCode"] = dHash_ndarray(thresh)

        cutimageCoordinate = Device["IdentifyInterruptRegion"]
        IdentifyRegion_Image = image[cutimageCoordinate[1]:cutimageCoordinate[3],
                               cutimageCoordinate[0]:cutimageCoordinate[2]]
        grayImage = cv2.cvtColor(IdentifyRegion_Image, cv2.COLOR_BGR2GRAY)
        ret2, thresh = cv2.threshold(grayImage, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        Device["IdentifyInterruptCode"] = dHash_ndarray(thresh)

        # cv2.imshow('运行', thresh)
        # cv2.waitKey(0)

        '''分页状态'''
        for Page in Device["PageInfo"]:
            image = cv2.imread(Page["PageTemplateFilePath"])
            cutimageCoordinate = Page["IdentifyPageRegion"]
            IdentifyRegion_Image = image[cutimageCoordinate[1]:cutimageCoordinate[3],
                                       cutimageCoordinate[0]:cutimageCoordinate[2]]
            grayImage = cv2.cvtColor(IdentifyRegion_Image, cv2.COLOR_BGR2GRAY)
            ret2, thresh = cv2.threshold(grayImage, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            Page["IdentifyPageCode"] = dHash_ndarray(thresh)
            # print(Page["PageNumber"])
            # cv2.imshow('分页', thresh)
            # cv2.waitKey(0)

    with open("./IMAGE Templates/ImageSectionInfo_code.json",'w') as f:
        json.dump(load_dict, f)
    pass
