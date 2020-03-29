# coding:utf-8
from functools import reduce
from wand.image import Image
import pytesseract
import datetime
import time
import os
import fitz  # fitz就是pip install PyMuPDF
import cv2
import numpy as np
import difflib
import math
from LAMProcessData.models import *
from django.db.models import Q
from django.core.cache import cache
import tempfile
from lamdataserver.settings import PDFCode_OriginalImage_URL


def CacheOperator(operateType, ifget, ParamSet,data=None):
	'''
	:param operateType:
		'recordLastTime'
		'CleanUpTime'
		'ProgressBarValue_CompleteInspect_MissionId'    由process_realtime_finedata中的CacheOperator进行赋值
		'ProgressBarValue_PracticalTools_SShapeBreak_By_GUID'    由SShapeBreak中的CacheOperator进行赋值
		'ProgressBarValue_PracticalTools_BreakBlockResumption_By_GUID'    由views.PracticalTools_BreakBlockResumption进行赋值
		'ProgressBarValue_New_LAMTechInstSerial_UploadPDFFile_By_TechInstID'    由views.***进行赋值
	:param ifget:
	:param ParamSet:    (worksectionid,datatype)
		datatype:laser, oxygen, cncstatus
	:param data:
	:return:
	'''
	revalue = None

	if operateType == 'ProgressBarValue_New_LAMTechInstSerial_UploadPDFFile_By_TechInstID':
		TechInstID = ParamSet
		key = 'PBR_NewTechInstByPDF_TechInstID%s' % (TechInstID)
		if not ifget:
			cache.set(key, data)
		else:
			revalue = cache.get(key)
	return revalue

# 汉字识别包
language = 'chi_my'
# language = 'chi_sim'
_ImageSection = [
	[58, 284, 157, 318],
	[58, 321, 157, 354],
	[58, 357, 157, 390],
	[58, 393, 157, 426],
	[58, 429, 157, 463],
	[58, 466, 157, 499],
	[58, 502, 157, 535],
	[58, 538, 157, 572],
	[58, 575, 157, 608],
	[58, 611, 157, 644],
	[58, 647, 157, 680],
	[58, 683, 157, 717],
	[58, 720, 157, 753],
	[58, 756, 157, 789],
	[58, 792, 157, 826],
	[58, 829, 157, 862],
	[58, 865, 157, 898],
	[58, 901, 157, 934],
	[58, 937, 157, 971],
	[58, 974, 157, 1007]
]


difflib.SequenceMatcher(None, '1110','1100').ratio()

'''常用图像操作'''
kernel2_2 = np.ones((2, 2), np.uint8)
kernel5_5 = np.ones((5, 5), np.uint8)
# 加边框 黑底白字
MakeBorder = lambda img: cv2.copyMakeBorder(img, 5, 5, 5, 5, cv2.BORDER_CONSTANT, value=0)
# 膨胀
Dilate_2 = lambda img: cv2.dilate(img, kernel2_2, iterations=1)
Dilate_5 = lambda img: cv2.dilate(img, kernel5_5, iterations=1)
# 腐蚀
Erode_2 = lambda img: cv2.erode(img, kernel2_2, iterations=1)
Erode_5 = lambda img: cv2.erode(img, kernel5_5, iterations=1)
# 二值化
Threshold = lambda img: cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
# 锐化
kernel_Filter = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], np.float32)
Filter2D = lambda img: cv2.filter2D(img, -1, kernel=kernel_Filter)
# 高斯平滑
GaussianBlur = lambda img: cv2.GaussianBlur(img, (9, 9), 2)
# 放大
Resize_500H = lambda img: cv2.resize(img, (int(500 * img.shape[1]/img.shape[0]), int(500)), interpolation=cv2.INTER_CUBIC)
Resize_31H = lambda img: cv2.resize(img, (int(31 * img.shape[1]/img.shape[0]), int(31)), interpolation=cv2.INTER_CUBIC)
# 边框
MakeBorder_5 = lambda img: cv2.copyMakeBorder(img, 5, 5, 5, 5, cv2.BORDER_CONSTANT, value=255)
OperateDict = {
	'MakeBorder': MakeBorder,
	'Dilate_2': Dilate_2,
	'Dilate_5': Dilate_5,
	'Erode_2': Erode_2,
	'Erode_5': Erode_5,
	'Threshold': Threshold,
	'Filter2D': Filter2D,
	'GaussianBlur': GaussianBlur,
	'Resize_500H': Resize_500H,
	'Resize_31H': Resize_31H,
	'MakeBorder_5': MakeBorder_5,
}

def ImageListConcatenate(imglist):
	def concatenate2img(img1, img2):
		return np.concatenate((img1, img2))
	return reduce(concatenate2img, imglist)

def changeColorBlackBackWhiteFront(image):
	# 统一颜色 黑底白字
	height, width = image.shape[:2]
	max = image.max()
	if np.mean(image) > 127.5:
		for y in range(0, height):
			for x in range(0, width):
				image[y, x] = max - image[y, x]


def changeColorWhiteBackBlackFront(image):
	# 统一颜色 白底黑字
	height, width = image.shape[:2]
	max = image.max()
	if np.mean(image) <= 127.5:
		for y in range(0, height):
			for x in range(0, width):
				image[y, x] = max - image[y, x]
	return image


def splitImageIntoCharacter(WBimage):
	# 切割多行图像 先投影Y，再投影X
	if WBimage is None:
		return [None]
	# 投影在Y轴，得到h列表
	height, width = WBimage.shape[:2]
	# cv2.imshow("Image", image)
	# cv2.waitKey(0)
	
	BWimage = WBimage.copy()
	# image = changeColorBlackBackWhiteFront(image)
	changeColorBlackBackWhiteFront(BWimage)
	# 投影在Y轴，得到h列表
	h = [sum(BWimage[i]) for i in range(0, height)]
	
	# 获得行的Y轴坐标投影范围，得到linePixID_InHeight
	linePixID_InHeight = []
	startId = None
	for i in range(0, height):
		if h[i] == 0:
			if not startId is None:
				linePixID_InHeight.append([startId, i])
				startId = None
		else:
			if startId is None:
				startId = i
	if not startId is None:
		linePixID_InHeight.append([startId, i])
	
	# 得到若干行字符
	LineImage = [BWimage[start_i:end_i + 1, 0:width] for start_i, end_i in linePixID_InHeight]
	# LineImage = map(changeColorWhiteBackBlackFront, LineImage)
	# return LineImage
	# 将每行的字符集中在CharacterImage中
	CharacterImage = []
	for img_inLine in LineImage:
		# cv2.imshow("Image", img_inLine)
		# cv2.waitKey(0)
		# 投影在X轴，得到v列表
		_height, _width = img_inLine.shape[:2]
		v = [sum(img_inLine[0:_height, i]) for i in range(0, _width)]
		
		# 获得字符在X轴坐标投影范围，得到CharacterPixID_InWidth
		CharacterPixID_InWidth = []
		startId = None
		for i in range(0, _width):
			if i > 1 and v[i] == 0:
			# 两个空格
			# if i > 1 and v[i] == 0 and v[i - 1] == 0:
				if not startId is None:
					CharacterPixID_InWidth.append([startId, i])
					startId = None
			else:
				if startId is None:
					startId = i
		if not startId is None:
			CharacterPixID_InWidth.append([startId, i])
		# '''过滤掉高宽比<2的字符'''
		# _lineCharacterImage = [img_inLine[0:_height, start_i:end_i] for start_i, end_i in CharacterPixID_InWidth if
		#                        _height / (end_i - start_i) < 2]
		_lineCharacterImage = [img_inLine[0:_height, start_i:end_i] for start_i, end_i in CharacterPixID_InWidth]
		# for img in _lineCharacterImage:
		#     cv2.imshow("Image", img)
		#     cv2.waitKey(0)
		# _lineCharacterImage = map(changeColorWhiteBackBlackFront, _lineCharacterImage)
		CharacterImage.extend(_lineCharacterImage)
	list(map(changeColorWhiteBackBlackFront, CharacterImage))
	
	'''图像运算'''
	# kernel = np.ones((2, 2), np.uint8)
	# _size_w = 12
	# _size_h = _size_w * 6 / 5
	# Resize = lambda img: cv2.resize(img, (int(_size_w), int(_size_h)), interpolation=cv2.INTER_CUBIC)
	# MakeBorder = lambda img: cv2.copyMakeBorder(img, 2, 2, 2, 2, cv2.BORDER_CONSTANT, value=255)
	# # 膨胀
	# Dilate = lambda img: cv2.dilate(img, kernel, iterations=1)
	# Dilate2 = lambda img: cv2.dilate(img, kernel, iterations=2)
	# Dilate3 = lambda img: cv2.dilate(img, kernel, iterations=3)
	# Dilate4 = lambda img: cv2.dilate(img, kernel, iterations=4)
	# # 腐蚀
	# Erode = lambda img: cv2.erode(img, kernel, iterations=1)
	# # 锐化
	# kernel_Filter = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], np.float32)
	# # Filter2D = lambda img: cv2.filter2D(img, -1, kernel=kernel_Filter)
	# # 高斯平滑
	# GaussianBlur = lambda img: cv2.GaussianBlur(img, (9, 9), 2)
	# # 二值化
	# Threshold = lambda img: cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
	#
	# # CharacterImage = map(Resize, CharacterImage)
	# # # CharacterImage = map(Erode, CharacterImage)
	# # # CharacterImage = map(Erode, CharacterImage)
	# # # CharacterImage = map(Erode, CharacterImage)
	# # CharacterImage = map(GaussianBlur, CharacterImage)
	# # # CharacterImage = map(Resize, CharacterImage)
	# #
	# # CharacterImage = map(MakeBorder, CharacterImage)
	# CharacterImage = map(Resize, CharacterImage)
	# # CharacterImage = map(Threshold, CharacterImage)
	#
	return CharacterImage


def ImageOptimization(image, operatelist = None):
	if not operatelist is None:
		global OperateDict
		for _operate in operatelist:
			image = OperateDict[_operate](image)
		return image
	else:
		return image

def splitImageIntoCharacter_getFormCodeDigits(WBimage, forwardCutNum=2, backwardCutNum=-1, operatelist=None):
	'''
	forwardCutNum:  切除前几个字符
	backwardCutNum： 切除后几个字符
	operatelist：相邻字符应不粘连，且字迹尽量粗重，可通过此列表进行图形操作，Erode，Filter2D
	'''
	# 切割多行图像 先投影Y，再投影X
	if WBimage is None:
		return [None]
	# 将每行的字符集中在CharacterImage中
	CharacterImage = []
	# 投影在Y轴，得到h列表
	height, width = WBimage.shape[:2]
	# cv2.imshow("Image", image)
	# cv2.waitKey(0)
	
	BWimage = WBimage.copy()
	# image = changeColorBlackBackWhiteFront(image)
	changeColorBlackBackWhiteFront(BWimage)
	BWimage = cv2.copyMakeBorder(BWimage, 0, 0, 3, 3, cv2.BORDER_CONSTANT, value=0)
	
	# cv2.imwrite('PracticalTools\\RO HLJ23A.05.099\\getFormCodeDigits-before.bmp', BWimage)
	
	BWimage = ImageOptimization(BWimage, operatelist)
	# cv2.imwrite('PracticalTools\\RO HLJ23A.05.099\\getFormCodeDigits-after.bmp', BWimage)
	
	# 投影在X轴，得到v列表
	_height, _width = BWimage.shape[:2]
	v = [sum(BWimage[0:_height, i]) for i in range(0, _width)]
	
	'''跳过前两个字符，自0起数空白段，为2时开始剪切'''
	CharacterPixID_InWidth = []
	startId = None
	for i in range(_width):
		if v[i] == 0 and startId is None:
			# 空
			continue
		elif v[i] == 0 and not startId is None:
			# 结束一个字符
			CharacterPixID_InWidth.append([startId, i])
			startId = None
		elif v[i] > 0 and startId is None:
			# 开始一个字符
			startId = i
		elif v[i] > 0 and not startId is None:
			# 字符中
			continue
	Cuted_CharacterPixID_InWidth = CharacterPixID_InWidth[forwardCutNum:backwardCutNum]
	StrImg_startId_in_W = Cuted_CharacterPixID_InWidth[0][0]
	StrImg_finishId_in_W = Cuted_CharacterPixID_InWidth[-1][1]
	CutStrImg = BWimage[0:BWimage.shape[0], StrImg_startId_in_W:StrImg_finishId_in_W]
	return changeColorWhiteBackBlackFront(CutStrImg)
	# 	# if v[i] == 0:
	# 	# 	# 两个空格
	# 	# 	# if i > 1 and v[i] == 0 and v[i - 1] == 0:
	# 	# 	if not startId is None:
	# 	# 		CharacterPixID_InWidth.append([startId, i])
	# 	# 		startId = None
	# 	# else:
	# 	# 	if startId is None:
	# 	# 		startId = i
	# # if not startId is None:
	# # 	CharacterPixID_InWidth.append([startId, i])
	#
	#
	# if True:
	# 	''''''
	# 	img_inLine = BWimage
	# 	# cv2.imshow("Image", img_inLine)
	# 	# cv2.waitKey(0)
	# 	# 投影在X轴，得到v列表
	# 	_height, _width = img_inLine.shape[:2]
	# 	v = [sum(img_inLine[0:_height, i]) for i in range(0, _width)]
	#
	# 	# 获得字符在X轴坐标投影范围，得到CharacterPixID_InWidth
	# 	CharacterPixID_InWidth = []
	# 	startId = None
	# 	for i in range(0, _width):
	# 		if i > 1 and v[i] == 0:
	# 			# 两个空格
	# 			# if i > 1 and v[i] == 0 and v[i - 1] == 0:
	# 			if not startId is None:
	# 				CharacterPixID_InWidth.append([startId, i])
	# 				startId = None
	# 		else:
	# 			if startId is None:
	# 				startId = i
	# 	if not startId is None:
	# 		CharacterPixID_InWidth.append([startId, i])
	# 	# '''过滤掉高宽比<2的字符'''
	# 	# _lineCharacterImage = [img_inLine[0:_height, start_i:end_i] for start_i, end_i in CharacterPixID_InWidth if
	# 	#                        _height / (end_i - start_i) < 2]
	# 	_lineCharacterImage = [img_inLine[0:_height, start_i:end_i] for start_i, end_i in CharacterPixID_InWidth]
	# 	# for img in _lineCharacterImage:
	# 	#     cv2.imshow("Image", img)
	# 	#     cv2.waitKey(0)
	# 	# _lineCharacterImage = map(changeColorWhiteBackBlackFront, _lineCharacterImage)
	# 	CharacterImage.extend(_lineCharacterImage)
	# list(map(changeColorWhiteBackBlackFront, CharacterImage))
	#
	# '''图像运算'''
	# # kernel = np.ones((2, 2), np.uint8)
	# # _size_w = 12
	# # _size_h = _size_w * 6 / 5
	# # Resize = lambda img: cv2.resize(img, (int(_size_w), int(_size_h)), interpolation=cv2.INTER_CUBIC)
	# # MakeBorder = lambda img: cv2.copyMakeBorder(img, 2, 2, 2, 2, cv2.BORDER_CONSTANT, value=255)
	# # # 膨胀
	# # Dilate = lambda img: cv2.dilate(img, kernel, iterations=1)
	# # Dilate2 = lambda img: cv2.dilate(img, kernel, iterations=2)
	# # Dilate3 = lambda img: cv2.dilate(img, kernel, iterations=3)
	# # Dilate4 = lambda img: cv2.dilate(img, kernel, iterations=4)
	# # # 腐蚀
	# # Erode = lambda img: cv2.erode(img, kernel, iterations=1)
	# # # 锐化
	# # kernel_Filter = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], np.float32)
	# # # Filter2D = lambda img: cv2.filter2D(img, -1, kernel=kernel_Filter)
	# # # 高斯平滑
	# # GaussianBlur = lambda img: cv2.GaussianBlur(img, (9, 9), 2)
	# # # 二值化
	# # Threshold = lambda img: cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
	# #
	# # # CharacterImage = map(Resize, CharacterImage)
	# # # # CharacterImage = map(Erode, CharacterImage)
	# # # # CharacterImage = map(Erode, CharacterImage)
	# # # # CharacterImage = map(Erode, CharacterImage)
	# # # CharacterImage = map(GaussianBlur, CharacterImage)
	# # # # CharacterImage = map(Resize, CharacterImage)
	# # #
	# # # CharacterImage = map(MakeBorder, CharacterImage)
	# # CharacterImage = map(Resize, CharacterImage)
	# # # CharacterImage = map(Threshold, CharacterImage)
	# #
	# return CharacterImage


# 一个矩形识别区域
# 本例中尺寸根据按2.5倍数生成的图片切除页边距后测量而得
class PDFCutImageRectangle():
	def __init__(self, fatherImageShape):
		self.fatherImageShape = fatherImageShape
		self.regionCoordinate = None
		self.regionCoordinate_base_Shape = None
		self.BlodFlag = None
		# height, width = 1404, 1965
		# self.getRegionFun = lambda img, coor: img[
		#                                       int(fatherImageShape[0] * coor[1] / height): int(
		# 	                                      fatherImageShape[0] * coor[3] / height),
		#                                       int(fatherImageShape[1] * coor[0] / width): int(
		# 	                                      fatherImageShape[1] * coor[2] / width)]
		self.getRegionFun = lambda img, coor, base_Shape: img[
		                                      int(fatherImageShape[0] * coor[1] / base_Shape[0]): int(
			                                      fatherImageShape[0] * coor[3] / base_Shape[0]),
		                                      int(fatherImageShape[1] * coor[0] / base_Shape[1]): int(
			                                      fatherImageShape[1] * coor[2] / base_Shape[1])]
		self.img = None
	
	def getRegion(self, image):
		if self.regionCoordinate is None:
			return None
		self.img = self.getRegionFun(image, self.regionCoordinate, self.regionCoordinate_base_Shape)
		return self.img
	def setBlodFlag(self,ifblod):
		self.BlodFlag = ifblod


# 加粗标记区域识别
class PDFCutImageRectangle_BlodRegion(PDFCutImageRectangle):
	def __init__(self, fatherImageShape):
		super(PDFCutImageRectangle_BlodRegion, self).__init__(fatherImageShape)
		self.regionCoordinate = [16, 0, 50, 24]
		self.regionCoordinate_base_Shape = (1404, 1965)
	
	def getBlodRate(self, image):
		_img = self.getRegion(image)
		_img = getRealImage(_img)
		# 白底黑字
		height, width = _img.shape[:2]
		_sum = 0
		for h in range(height):
			for w in range(width):
				if _img[h][w] < 125:
					_sum +=1
		return _sum / (height*width)
		
		
	def getText(self, image):
		_img = self.getRegion(image)
		_img = getRealImage(_img)
		'''放大、加粗、平滑、缩小、边框'''
		# _imgH, _imgW = _img.shape[:2]
		# _rate_WH = _imgW / _imgH
		operatelist = ['Resize_500H', 'Erode_5', 'GaussianBlur', 'Resize_31H', 'MakeBorder_5']
		_img = ImageOptimization(_img, operatelist)
		cv2.imwrite('PracticalTools\\MPM-PTZJ-GC-002A\\BS.bmp', _img)
		code = pytesseract.image_to_string((_img), lang='eng', config="-psm 3 ")
		return code


# 表式区域识别
class PDFCutImageRectangle_FormCode(PDFCutImageRectangle):
	def __init__(self, fatherImageShape):
		super(PDFCutImageRectangle_FormCode, self).__init__(fatherImageShape)
		self.regionCoordinate = [0, 0, 110, 24]
		self.regionCoordinate_base_Shape = (1404, 1965)
	
	def getRegion(self, image):
		img = super(PDFCutImageRectangle_FormCode, self).getRegion(image)
		operatelist = ['Erode_2'] if self.BlodFlag else None
		_split_img_list = splitImageIntoCharacter_getFormCodeDigits(img, forwardCutNum=2, backwardCutNum=-1, operatelist=operatelist)
		
		self.img = cv2.copyMakeBorder(_split_img_list, 3, 3, 3, 3, cv2.BORDER_CONSTANT, value=255)
		return self.img

	def getText(self, image):
		_img = self.getRegion(image)
		_img = getRealImage(_img)
		'''放大、加粗、平滑、缩小、边框'''
		operatelist = ['Resize_500H', 'Erode_5', 'GaussianBlur', 'Resize_31H', 'MakeBorder_5']
		_img = ImageOptimization(_img, operatelist)
		# _imgH, _imgW = _img.shape[:2]
		# _rate_WH = _imgW / _imgH
		# kernel = np.ones((5, 5), np.uint8)
		# # 放大
		# _img = cv2.resize(_img, (int(500 * _rate_WH), int(500)), interpolation=cv2.INTER_CUBIC)
		# # 腐蚀加粗
		# _img = cv2.erode(_img, kernel, iterations=2)
		# # 高斯平滑
		# _img = cv2.GaussianBlur(_img, (9, 9), 2)
		# # 缩小
		# _img = cv2.resize(_img, (int(31 * _rate_WH), int(31)), interpolation=cv2.INTER_CUBIC)
		# # 加边框
		# _img = cv2.copyMakeBorder(_img, 5, 5, 5, 5, cv2.BORDER_CONSTANT, value=255)
		cv2.imwrite('PracticalTools\\MPM-PTZJ-GC-002A\\BS.bmp', _img)
		code = pytesseract.image_to_string((_img), lang='eng', config="-psm 3 ")
		return code


# TFO、RO首页技术文件编号
class PDFCutImageRectangle_Order_TechFileCode(PDFCutImageRectangle):
	def __init__(self, fatherImageShape):
		super(PDFCutImageRectangle_Order_TechFileCode, self).__init__(fatherImageShape)
		self.regionCoordinate = [127, 30, 370, 93]
		self.regionCoordinate_base_Shape = (1404, 1965)
	def getText(self, image):
		_img = self.getRegion(image)
		_img = getRealImage(_img)
		'''放大、加粗、平滑、缩小、边框'''
		if self.BlodFlag:
			operatelist = None
		else:
			operatelist = ['Resize_500H', 'Erode_5', 'Erode_5', 'GaussianBlur', 'Resize_31H','MakeBorder_5']
		_img = ImageOptimization(_img, operatelist)
		# _imgH, _imgW = _img.shape[:2]
		# _rate_WH = _imgW / _imgH
		# kernel = np.ones((5, 5), np.uint8)
		# # 放大
		# _img = cv2.resize(_img, (int(500 * _rate_WH), int(500)), interpolation=cv2.INTER_CUBIC)
		# # 腐蚀加粗
		# _img = cv2.erode(_img, kernel, iterations=2)
		# # 高斯平滑
		# _img = cv2.GaussianBlur(_img, (9, 9), 2)
		# # 缩小
		# _img = cv2.resize(_img, (int(31 * _rate_WH), int(31)), interpolation=cv2.INTER_CUBIC)
		# # 加边框
		# _img = cv2.copyMakeBorder(_img, 5, 5, 5, 5, cv2.BORDER_CONSTANT, value=255)
		cv2.imwrite('RO HLJ23A.05.099\\resizeByContent\\WJBH.bmp', _img)
		code = pytesseract.image_to_string((_img), lang='eng', config="-psm 7 ")
		return code


# TFO、RO首页零件编号
class PDFCutImageRectangle_Order_ProductCode(PDFCutImageRectangle):
	def __init__(self, fatherImageShape):
		super(PDFCutImageRectangle_Order_ProductCode, self).__init__(fatherImageShape)
		self.regionCoordinate = [156, 1088, 608, 1195]
		self.regionCoordinate_base_Shape = (1404, 1965)
	def getText(self, image):
		_img = self.getRegion(image)
		_img = getRealImage(_img)
		'''放大、加粗、平滑、缩小、边框'''
		if self.BlodFlag:
			operatelist = None
		else:
			operatelist = ['Resize_500H', 'Erode_5', 'Erode_5', 'GaussianBlur', 'Resize_31H', 'MakeBorder_5']
		_img = ImageOptimization(_img, operatelist)
		# _imgH, _imgW = _img.shape[:2]
		# _rate_WH = _imgW / _imgH
		# kernel = np.ones((5, 5), np.uint8)
		# # 放大
		# _img = cv2.resize(_img, (int(500 * _rate_WH), int(500)), interpolation=cv2.INTER_CUBIC)
		# # 腐蚀加粗
		# _img = cv2.erode(_img, kernel, iterations=2)
		# # 高斯平滑
		# _img = cv2.GaussianBlur(_img, (9, 9), 2)
		# # 缩小
		# _img = cv2.resize(_img, (int(31 * _rate_WH), int(31)), interpolation=cv2.INTER_CUBIC)
		# # 加边框
		# _img = cv2.copyMakeBorder(_img, 5, 5, 5, 5, cv2.BORDER_CONSTANT, value=255)
		cv2.imwrite('RO HLJ23A.05.099\\resizeByContent\\LJBH.bmp', _img)
		code = pytesseract.image_to_string((_img), lang='eng', config="-psm 3 ")
		return code


# TFO、RO 过程卡 工序名称
class PDFCutImageRectangle_Order_ProcessName(PDFCutImageRectangle):
	def __init__(self, fatherImageShape, lineid):
		super(PDFCutImageRectangle_Order_ProcessName, self).__init__(fatherImageShape)
		_regionCoordinate = {
			0: [4, 322, 125, 361],
			1: [4, 368, 125, 406],
			2: [4, 413, 125, 451],
			3: [4, 458, 125, 497],
			4: [4, 504, 125, 542],
			5: [4, 549, 125, 587],
			6: [4, 594, 125, 633],
			7: [4, 640, 125, 678],
			8: [4, 685, 125, 723],
			9: [4, 730, 125, 768],
			10: [4, 775, 125, 814],
			11: [4, 821, 125, 859],
			12: [4, 866, 125, 905],
			13: [4, 912, 125, 950],
			14: [4, 957, 125, 996],
			15: [4, 1003, 125, 1041],
			16: [4, 1048, 125, 1086],
			17: [4, 1093, 125, 1132],
			18: [4, 1139, 125, 1177],
			19: [4, 1184, 125, 1223],
		}
		self.regionCoordinate = _regionCoordinate[lineid]
		self.regionCoordinate_base_Shape = (1404, 1965)
	
	def getText(self, image):
		_img = self.getRegion(image)
		self.getCode_resizeByContent()
		if self.imgcode_8H is None:
			'''空白图片'''
			return ''
		# 从数据库查询相似的图形码，如没有则进行OCR识别
		code = Get_ImgText(self.imgcode_shape, self.imgcode_8H)
		if code is None:
			# global language
			# global ImageIndex_char
			
			# getCode_resizeByContent(_img)
			
			''' 拆分汉字单字 '''
			# charImage_list = splitImageIntoCharacter(_img)
			# _char_codelist = []
			# _char_codelist2 = []
			# for _charImg in charImage_list:
			# 	_char_codelist.append(pytesseract.image_to_string((_charImg), lang=language, config="-psm 10"))
			# 	_char_codelist2.append(pytesseract.image_to_string((_charImg), lang='chi_sim', config="-psm 10"))
			# 	cv2.imwrite('RO HLJ23A.05.099\\charimage\\%d.tif' % (ImageIndex_char), _charImg)
			# 	a = getImgCode(_charImg)
			# 	ImageIndex_char += 1
			if self.BlodFlag is True:
				operatelist = ['Resize_500H', ]
			else:
				operatelist = ['Resize_500H', 'Erode_5','Erode_5', 'GaussianBlur']
			# operatelist = ['Resize_500H', 'GaussianBlur']
			_img = ImageOptimization(_img, operatelist)
			'''整图识别'''
			# _imgH, _imgW = _img.shape[:2]
			# _rate_WH = _imgW / _imgH
			# kernel = np.ones((5, 5), np.uint8)
			# # 放大
			# _img = cv2.resize(_img, (int(500 * _rate_WH), int(500)), interpolation=cv2.INTER_CUBIC)
			# # 腐蚀加粗
			# _img = cv2.erode(_img, kernel, iterations=2)
			# # cv2.imwrite('RO HLJ23A.05.099\\resizeByContent\\erode-%s.bmp' % ImageIndex, _img)
			# # 高斯平滑
			# _img = cv2.GaussianBlur(_img, (9, 9), 2)
			# # 缩小
			# _img = cv2.resize(_img, (int(31 * _rate_WH), int(31)), interpolation=cv2.INTER_CUBIC)
			
			
			# cv2.imwrite('RO HLJ23A.05.099\\resizeByContent\\resize-%s.bmp' % ImageIndex, _img)
			# code = pytesseract.image_to_string((_img), lang=language, config="-psm 7 ")
			# cv2.imwrite('RO HLJ23A.05.099\\resizeByContent\\image_to_string-%s.bmp' % ImageIndex, _img)
			code = pytesseract.image_to_string((_img), lang='chi_sim', config="-psm 7 ")
		return code
	
	# 根据图片中字符真实尺寸缩放至8px高，高宽比不变
	def getCode_resizeByContent(self):
		# realimg = getRealImage(image)
		realimg = getRealImage(self.img.copy())
		if realimg is None:
			self.imgcode_8H=None
			self.imgcode_shape=None
			return None
		_imgH, _imgW = realimg.shape[:2]
		_rate_WH = math.ceil(_imgW / _imgH)
		_codeimg_H = 8
		_codeimg_W = int(8 * _rate_WH)
		kernel = np.ones((15, 15), np.uint8)
		
		
		# 放大到500高
		realimg = cv2.resize(realimg, (int(500 * _rate_WH), int(500)), interpolation=cv2.INTER_CUBIC)
		# 腐蚀
		realimg = cv2.erode(realimg, kernel, iterations=1)
		# cv2.imwrite('RO HLJ23A.05.099\\resizeByContent\\erode-%s.bmp' % ImageIndex, realimg)
		# # 二值化
		# ret2, realimg = cv2.threshold(realimg, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
		# 缩小到8高
		realimg = cv2.resize(realimg, (_codeimg_W, _codeimg_H), interpolation=cv2.INTER_CUBIC)
		# 二值化
		ret2, realimg = cv2.threshold(realimg, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
		# Resize = lambda img: cv2.resize(img, (int(_codeimg_H * _rate_WH), int(_codeimg_H)), interpolation=cv2.INTER_CUBIC)
		
		# cv2.imwrite('RO HLJ23A.05.099\\resizeByContent\\%s.bmp' % ImageIndex, realimg)
		self.imgcode_8H = getImgCode(realimg)
		self.imgcode_shape = (_codeimg_W, _codeimg_H)


# TFO、RO 过程卡 工序号
class PDFCutImageRectangle_Order_ProcessNumber(PDFCutImageRectangle):
	def __init__(self, fatherImageShape, lineid):
		super(PDFCutImageRectangle_Order_ProcessNumber, self).__init__(fatherImageShape)
		_regionCoordinate = {
			0: [131, 322, 214, 361],
			1: [131, 368, 214, 406],
			2: [131, 413, 214, 451],
			3: [131, 458, 214, 497],
			4: [131, 504, 214, 542],
			5: [131, 549, 214, 587],
			6: [131, 594, 214, 633],
			7: [131, 640, 214, 678],
			8: [131, 685, 214, 723],
			9: [131, 730, 214, 768],
			10: [131, 775, 214, 814],
			11: [131, 821, 214, 859],
			12: [131, 866, 214, 905],
			13: [131, 912, 214, 950],
			14: [131, 957, 214, 996],
			15: [131, 1003, 214, 1041],
			16: [131, 1048, 214, 1086],
			17: [131, 1093, 214, 1132],
			18: [131, 1139, 214, 1177],
			19: [131, 1184, 214, 1223],
		}
		self.regionCoordinate = _regionCoordinate[lineid]
		self.regionCoordinate_base_Shape = (1404, 1965)
	
	def getText(self, image):
		# global language
		# global ImageIndex_char
		_img = self.getRegion(image)
		if self.BlodFlag:
			operatelist = ['Resize_500H']
		else:
			operatelist = ['Resize_500H', 'Erode_5', 'Erode_5', 'GaussianBlur']
		_img = ImageOptimization(_img, operatelist)
		'''整图识别'''
		# _imgH, _imgW = _img.shape[:2]
		# _rate_WH = _imgW / _imgH
		# kernel = np.ones((5, 5), np.uint8)
		# # 放大
		# _img = cv2.resize(_img, (int(500 * _rate_WH), int(500)), interpolation=cv2.INTER_CUBIC)
		# # 腐蚀加粗
		# _img = cv2.erode(_img, kernel, iterations=2)
		# # 高斯平滑
		# _img = cv2.GaussianBlur(_img, (9, 9), 2)
		# # 缩小
		# _img = cv2.resize(_img, (int(31 * _rate_WH), int(31)), interpolation=cv2.INTER_CUBIC)
		# # 加边框
		# _img = cv2.copyMakeBorder(_img, 5, 5, 5, 5, cv2.BORDER_CONSTANT, value=255)
		code = pytesseract.image_to_string((_img), lang='eng', config="-psm 7 digits_ProcessNumber")
		if code == '1':
			pass
		# 筛除掉工步"10-1", "10-3"
		if not code.isnumeric():
		# if '-' in code:
			code = ''
		return code
		
		
# 工艺规程首页技术文件编号
class PDFCutImageRectangle_Regulation_TechFileCode(PDFCutImageRectangle):
	def __init__(self, fatherImageShape):
		super(PDFCutImageRectangle_Regulation_TechFileCode, self).__init__(fatherImageShape)
		self.regionCoordinate = [936, 85, 1396, 131]
		self.regionCoordinate_base_Shape = (1338, 1856)
	def getText(self, image):
		_img = self.getRegion(image)
		_img = getRealImage(_img)
		if self.BlodFlag:
			operatelist = None
		else:
			operatelist = ['Resize_500H', 'Erode_5', 'Erode_5', 'GaussianBlur', 'Resize_31H', 'MakeBorder_5']
		_img = ImageOptimization(_img, operatelist)
		'''放大、加粗、平滑、缩小、边框'''
		# _imgH, _imgW = _img.shape[:2]
		# _rate_WH = _imgW / _imgH
		# kernel = np.ones((5, 5), np.uint8)
		# # 放大
		# _img = cv2.resize(_img, (int(500 * _rate_WH), int(500)), interpolation=cv2.INTER_CUBIC)
		# # 腐蚀加粗
		# _img = cv2.erode(_img, kernel, iterations=2)
		# # 高斯平滑
		# _img = cv2.GaussianBlur(_img, (9, 9), 2)
		# # 缩小
		# _img = cv2.resize(_img, (int(31 * _rate_WH), int(31)), interpolation=cv2.INTER_CUBIC)
		# # 加边框
		# _img = cv2.copyMakeBorder(_img, 5, 5, 5, 5, cv2.BORDER_CONSTANT, value=255)
		# cv2.imwrite('RO HLJ23A.05.099\\resizeByContent\\WJBH.bmp', _img)
		code = pytesseract.image_to_string((_img), lang='eng', config="-psm 7 ")
		return code


# 工艺规程 过程卡 工序名称
class PDFCutImageRectangle_Regulation_ProcessName(PDFCutImageRectangle):
	def __init__(self, fatherImageShape, lineid):
		super(PDFCutImageRectangle_Regulation_ProcessName, self).__init__(fatherImageShape)
		_regionCoordinate = {
			0: [6, 305, 326, 371],
			1: [6, 380, 326, 446],
			2: [6, 454, 326, 521],
			3: [6, 529, 326, 596],
			4: [6, 604, 326, 671],
			5: [6, 679, 326, 746],
			6: [6, 754, 326, 821],
			7: [6, 829, 326, 896],
			8: [6, 904, 326, 970],
			9: [6, 979, 326, 1045],
			10: [6, 1053, 326, 1120],
			11: [6, 1128, 326, 1195],
			12: [6, 1203, 326, 1270],
			13: [6, 1278, 326, 1345],
			14: [6, 1353, 326, 1420],
			15: [6, 1428, 326, 1495],
			16: [6, 1503, 326, 1570],
			17: [6, 1578, 326, 1644],
			18: [6, 1652, 326, 1719],
			19: [6, 1727, 326, 1794],
		}
		self.regionCoordinate = _regionCoordinate[lineid]
		self.regionCoordinate_base_Shape = (2141, 2969)
	
	def getText(self, image):
		_img = self.getRegion(image)
		self.getCode_resizeByContent()
		if self.imgcode_8H is None:
			'''空白图片'''
			return ''
		# 从数据库查询相似的图形码，如没有则进行OCR识别
		code = Get_ImgText(self.imgcode_shape, self.imgcode_8H)
		if code is None:
			if self.BlodFlag is True:
				operatelist = ['Resize_500H', ]
			else:
				operatelist = ['Resize_500H', 'Erode_5', 'Erode_5', 'GaussianBlur']
			_img = ImageOptimization(_img, operatelist)
			'''整图识别'''
			# _imgH, _imgW = _img.shape[:2]
			# _rate_WH = _imgW / _imgH
			# kernel = np.ones((5, 5), np.uint8)
			# # 放大
			# _img = cv2.resize(_img, (int(500 * _rate_WH), int(500)), interpolation=cv2.INTER_CUBIC)
			# # 腐蚀加粗
			# _img = cv2.erode(_img, kernel, iterations=2)
			# # cv2.imwrite('RO HLJ23A.05.099\\resizeByContent\\erode-%s.bmp' % ImageIndex, _img)
			# # 高斯平滑
			# _img = cv2.GaussianBlur(_img, (9, 9), 2)
			# # 缩小
			# _img = cv2.resize(_img, (int(31 * _rate_WH), int(31)), interpolation=cv2.INTER_CUBIC)
			# cv2.imwrite('RO HLJ23A.05.099\\resizeByContent\\resize-%s.bmp' % ImageIndex, _img)
			# code = pytesseract.image_to_string((_img), lang=language, config="-psm 7 ")
			# cv2.imwrite('RO HLJ23A.05.099\\resizeByContent\\image_to_string-%s.bmp' % ImageIndex, _img)
			code = pytesseract.image_to_string((_img), lang='chi_sim', config="-psm 7 ")
		return code
	
	# 根据图片中字符真实尺寸缩放至8px高，高宽比不变
	def getCode_resizeByContent(self):
		# realimg = getRealImage(image)
		realimg = getRealImage(self.img.copy())
		if realimg is None:
			self.imgcode_8H = None
			self.imgcode_shape = None
			return None
		_imgH, _imgW = realimg.shape[:2]
		_rate_WH = math.ceil(_imgW / _imgH)
		_codeimg_H = 8
		_codeimg_W = int(8 * _rate_WH)
		kernel = np.ones((15, 15), np.uint8)
		
		# 放大到500高
		realimg = cv2.resize(realimg, (int(500 * _rate_WH), int(500)), interpolation=cv2.INTER_CUBIC)
		# 腐蚀
		realimg = cv2.erode(realimg, kernel, iterations=1)
		# cv2.imwrite('RO HLJ23A.05.099\\resizeByContent\\erode-%s.bmp' % ImageIndex, realimg)
		# # 二值化
		# ret2, realimg = cv2.threshold(realimg, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
		# 缩小到8高
		realimg = cv2.resize(realimg, (_codeimg_W, _codeimg_H), interpolation=cv2.INTER_CUBIC)
		# 二值化
		ret2, realimg = cv2.threshold(realimg, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
		# Resize = lambda img: cv2.resize(img, (int(_codeimg_H * _rate_WH), int(_codeimg_H)), interpolation=cv2.INTER_CUBIC)
		
		# cv2.imwrite('RO HLJ23A.05.099\\resizeByContent\\%s.bmp' % ImageIndex, realimg)
		self.imgcode_8H = getImgCode(realimg)
		self.imgcode_shape = (_codeimg_W, _codeimg_H)


# 工艺规程 过程卡 工序号
class PDFCutImageRectangle_Regulation_ProcessNumber(PDFCutImageRectangle):
	def __init__(self, fatherImageShape, lineid):
		super(PDFCutImageRectangle_Regulation_ProcessNumber, self).__init__(fatherImageShape)
		_regionCoordinate = {
			0: [333, 305, 557, 371],
			1: [333, 380, 557, 446],
			2: [333, 454, 557, 521],
			3: [333, 529, 557, 596],
			4: [333, 604, 557, 671],
			5: [333, 679, 557, 746],
			6: [333, 754, 557, 821],
			7: [333, 829, 557, 896],
			8: [333, 904, 557, 970],
			9: [333, 979, 557, 1045],
			10: [333, 1053, 557, 1120],
			11: [333, 1128, 557, 1195],
			12: [333, 1203, 557, 1270],
			13: [333, 1278, 557, 1345],
			14: [333, 1353, 557, 1420],
			15: [333, 1428, 557, 1495],
			16: [333, 1503, 557, 1570],
			17: [333, 1578, 557, 1644],
			18: [333, 1652, 557, 1719],
			19: [333, 1727, 557, 1794]
		}
		self.regionCoordinate = _regionCoordinate[lineid]
		self.regionCoordinate_base_Shape = (2141, 2969)
	
	def getText(self, image):
		# global language
		# global ImageIndex_char
		_img = self.getRegion(image)
		if not _img is None and len(_img)>0:
			if self.BlodFlag:
				operatelist = ['Resize_500H']
			else:
				operatelist = ['Resize_500H', 'Erode_5', 'Erode_5', 'GaussianBlur']
			_img = ImageOptimization(_img, operatelist)
			'''整图识别'''
			# _imgH, _imgW = _img.shape[:2]
			# _rate_WH = _imgW / _imgH
			#
			# kernel = np.ones((5, 5), np.uint8)
			# # 放大
			# _img = cv2.resize(_img, (int(500 * _rate_WH), int(500)), interpolation=cv2.INTER_CUBIC)
			# # 腐蚀加粗
			# _img = cv2.erode(_img, kernel, iterations=2)
			# # 高斯平滑
			# _img = cv2.GaussianBlur(_img, (9, 9), 2)
			# # # 缩小
			# # _img = cv2.resize(_img, (int(31 * _rate_WH), int(31)), interpolation=cv2.INTER_CUBIC)
			# # # 加边框
			# _img = cv2.copyMakeBorder(_img, 5, 5, 5, 5, cv2.BORDER_CONSTANT, value=255)
			code = pytesseract.image_to_string((_img), lang='eng', config="-psm 7 digits_ProcessNumber")
			cv2.imwrite('PracticalTools\\MPM-PTZJ-GC-002A\\GXH.bmp', _img)
			# 筛除掉工步"10-1", "10-3"
			if not code.isnumeric():
				# if '-' in code:
				code = ''
		else:
			code = ''
		return code


count = 0


class PDFFormPage():
	def __init__(self, Image):
		self.Image = Image
		self.shape = Image.shape
		self.ifFirstPage = False
		self.ifTemporaryFile = False
		# 判断是否加粗
		self.BlodRegion = PDFCutImageRectangle_BlodRegion(self.shape)
		self.BlodRate = None
		self.BlodFlag = None
		# 表式号 实例
		self.FormCode = PDFCutImageRectangle_FormCode(self.shape)
		# 表式号 字符串
		self.FormCode_str = None
		
		# 技术文件
		self.TechFileCode = None
		self.TechFileCode_str = None
		# 产品编号
		self.ProductCode = None
		self.ProductCode_str = None
		# 工序信息
		self.ProcessNameStrList = []
		self.ProcessNumberStrList = []
		self.ProcessNameCodeIMGList = []
		self.ProcessNameList = []
		self.ProcessNumberList = []
		
		
	def checkBlodRate(self):
		self.BlodRate = self.BlodRegion.getBlodRate(self.Image)
		# print(self.BlodRate)
		self.BlodFlag = True if self.BlodRate > 0.35 else False
		self.FormCode.setBlodFlag(self.BlodFlag)
		
	def setChildnodesBlodStyle(self):
		for _child in self.childnodeslist:
			if type(_child) is list:
				for _secondary_child in _child:
					_secondary_child.setBlodFlag(self.BlodFlag)
			elif not _child is None:
				_child.setBlodFlag(self.BlodFlag)
			else:
				pass
		pass
	def checkFormCode(self):
		global language
		# global ImageIndex
		# _img = self.FormCode.getRegion(self.Image)
		code = self.FormCode.getText(self.Image)
		# code = pytesseract.image_to_string((_img), lang=language, config="-psm 7")
		
		replacelist = [
			(' ', ''),
			('I', '1'),
			('l', '1'),
			('z', '2'),
			('Z', '2'),
			('7v', '7.'),
			('丁', '7'),
			('工', '7.'),

		]
		for _r in replacelist:
			code = code.replace(_r[0], _r[1])
		self.FormCode_str = code
		print(code)
	def InitPage_By_FormCode(self):
		'''
		'CNC-digits-positive'
		'eng'
		'digits'
		'''
		# global ImageIndex
		# if '7.1' in self.FormCode_str or '9.1' in self.FormCode_str:
		self.childnodeslist = []
		if self.FormCode_str in ['7.1', '9.1']:
		# if self.ifFirstPage and self.ifTemporaryFile:
			# RO/TFO 首页
			self.TechFileCode = PDFCutImageRectangle_Order_TechFileCode(self.shape)
			self.ProductCode = PDFCutImageRectangle_Order_ProductCode(self.shape)
			self.childnodeslist = [self.FormCode, self.TechFileCode, self.ProductCode]
		
		# elif '7.2' in self.FormCode_str or '9.2' in self.FormCode_str:
		elif self.FormCode_str in ['7.2', '9.2']:
			# RO/TFO 过程卡
			self.ProcessNameList = [PDFCutImageRectangle_Order_ProcessName(self.shape, i) for i in range(20)]
			self.ProcessNumberList = [PDFCutImageRectangle_Order_ProcessNumber(self.shape, i) for i in range(20)]
			self.childnodeslist = [self.FormCode, self.ProcessNameList, self.ProcessNumberList]
		elif self.FormCode_str in ['10.2']:
			# 工艺规程 过程卡
			self.ProcessNameList = [PDFCutImageRectangle_Regulation_ProcessName(self.shape, i) for i in range(20)]
			self.ProcessNumberList = [PDFCutImageRectangle_Regulation_ProcessNumber(self.shape, i) for i in range(20)]
			self.childnodeslist = [self.FormCode, self.ProcessNameList, self.ProcessNumberList]
			
	
	def GetChildFieldText(self, TechInstID, basicProgressBarValue, oneProgressBarStep):
		'''
		'CNC-digits-positive'
		'eng'
		'digits'
		'''
		if self.FormCode_str in ['7.1', '9.1']:
			# 文件编号
			self.TechFileCode_str = self.TechFileCode.getText(self.Image)
			# 产品编号
			self.ProductCode_str = self.ProductCode.getText(self.Image)
		# elif '7.2' in self.FormCode_str or '9.2' in self.FormCode_str:
		elif self.FormCode_str in ['7.2', '9.2']:
			# 工序名称
			# self.ProcessItemList = []
			self.ProcessNameStrList = []
			self.ProcessNumberStrList = []
			self.ProcessNameCodeIMGList = []
			for lineid, (processname, processnumber) in enumerate(zip(self.ProcessNameList, self.ProcessNumberList)):
				# 更新进度条
				CacheOperator('ProgressBarValue_New_LAMTechInstSerial_UploadPDFFile_By_TechInstID', False, TechInstID,
				              basicProgressBarValue + oneProgressBarStep * (lineid + 1) / len(self.ProcessNameList))
				# 工序栏
				code = processname.getText(self.Image)
				self.ProcessNameStrList.append(code)
				imgcode_shape, imgcode_8H = processname.imgcode_shape, processname.imgcode_8H
				if imgcode_8H:
					self.ProcessNameCodeIMGList.append((imgcode_shape, imgcode_8H))
				else:
					self.ProcessNameCodeIMGList.append(None)
				# 序号栏
				number = processnumber.getText(self.Image)
				self.ProcessNumberStrList.append(number)
			
			pass
		elif self.FormCode_str in ['10.2']:
			# 工序名称
			# self.ProcessItemList = []
			self.ProcessNameStrList = []
			self.ProcessNumberStrList = []
			self.ProcessNameCodeIMGList = []
			for lineid, (processname, processnumber) in enumerate(zip(self.ProcessNameList, self.ProcessNumberList)):
				# 更新进度条
				CacheOperator('ProgressBarValue_New_LAMTechInstSerial_UploadPDFFile_By_TechInstID', False, TechInstID,
				              basicProgressBarValue + oneProgressBarStep * (lineid + 1) / len(self.ProcessNameList))
				# 工序栏
				code = processname.getText(self.Image)
				self.ProcessNameStrList.append(code)
				imgcode_shape, imgcode_8H = processname.imgcode_shape, processname.imgcode_8H
				if imgcode_8H:
					self.ProcessNameCodeIMGList.append((imgcode_shape, imgcode_8H))
				else:
					self.ProcessNameCodeIMGList.append(None)
				# 序号栏
				number = processnumber.getText(self.Image)
				self.ProcessNumberStrList.append(number)
			


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
	return re


def getImgCode(image):
	re = dHash_ndarray(image)
	del image
	return re


# 暂时未用
def wind_imagemagick_ghostscript(pdf_path, imgs_dir):
	# 将pdf文件转为jpg图片文件
	# ./PDF_FILE_NAME 为pdf文件路径和名称
	# image_pdf = Image(filename='./demo1.pdf', resolution=300)
	image_pdf = Image(filename=pdf_path)
	image_jpeg = image_pdf.convert('tiff')
	
	# wand已经将PDF中所有的独立页面都转成了独立的二进制图像对象。我们可以遍历这个大对象，并把它们加入到req_image序列中去。
	req_image = []
	for img in image_jpeg.sequence:
		img_page = Image(image=img)
		req_image.append(img_page.make_blob('tiff'))
	
	# 遍历req_image,保存为图片文件
	i = 0
	for img in req_image:
		ff = open(imgs_dir + '\\' + str(i) + '.tiff', 'wb')
		ff.write(img)
		ff.close()
		i += 1


def getRealImage(image):
	if image is None:
		return
	# 黑底白字
	height, width = image.shape[:2]
	minh, maxh = 0, width
	minw, maxw = 0, height
	for _h_id in range(height):
		if int(sum(image[_h_id])) < 255*width:
			minh=_h_id
			break
	for _h_id in range(height-1, 0, -1):
		if int(sum(image[_h_id])) < 255*width:
			maxh=_h_id+1
			break
	for _w_id in range(width):
		if int(sum(image[0:height, _w_id])) < 255*height:
			minw = _w_id
			break
	for _w_id in range(width-1, 0, -1):
		if int(sum(image[0:height, _w_id])) < 255*height:
			maxw = _w_id+1
			break
	# # cv2.imshow("image0", image)
	# # 投影在Y轴，得到h列表，最终得到字符真实高度
	# h = [(i, width * 255 - sum(image[i])) for i in range(0, height)]
	# mappedOnY = [item[0] for item in h if item[1] > 0]
	# if len(mappedOnY) == 0:
	# 	return
	# minh, maxh = min(mappedOnY), max(mappedOnY) + 1
	# # real_height = maxh - minh
	#
	# # 投影在X轴，得到w列表，最终得到字符真实宽度
	# w = [(i, height * 255 - sum(image[0:height, i])) for i in range(0, width)]
	# mappedOnX = [item[0] for item in w if item[1] > 0]
	# minw, maxw = min(mappedOnX), max(mappedOnX) + 1
	# real_width = maxw - minw
	real_image = image[minh:maxh, minw: maxw]
	return real_image


def pyMuPDF_fitz(pdfPath = None,stream = None,filetype=None, ifTemporaryFile=False, TechInstID=None):
	startTime_pdf2img = datetime.datetime.now()  # 开始时间
	
	pdfDoc = fitz.open(filename = pdfPath, stream=stream, filetype=filetype)
	PDFFormPage_List = []
	for pg in range(pdfDoc.pageCount):
		# if pg != 1:continue
		t1 = time.time()
		if_first_page = True if pg == 0 else False
		page = pdfDoc[pg]
		rotate = int(0)
		# 每个尺寸的缩放系数为1.3，这将为我们生成分辨率提高2.6的图像。
		# 此处若是不做设置，默认图片大小为：792X612, dpi=96
		# zoom_x = 1.33333333  # (1.33333333-->1056x816)   (2-->1584x1224)
		# zoom_y = 1.33333333
		# zoom_x = 2.5  # (1.33333333-->1056x816)   (2-->1584x1224)
		# zoom_x = 2.5 if pg == 0 else 1.99
		# zoom_x = 6 if pg == 0 else 6
		zoom_x = 4.5
		zoom_y = zoom_x
		mat = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
		pix = page.getPixmap(matrix=mat, alpha=False)
		t2 = time.time()
		print('t2-t1',t2-t1)
		# if not os.path.exists(imagePath):  # 判断存放图片的文件夹是否存在
		# 	os.makedirs(imagePath)  # 若图片文件夹不存在就创建
		# pix.writePNG(imagePath + '/' + 'images_%s.png' % pg)  # 将图片写入指定的文件夹内
		
		# getpngdata = pix.getImageData(output="png")
		# # 解码为 np.uint8
		# image_array = np.frombuffer(getpngdata, dtype=np.uint8)
		# img_cv = cv2.imdecode(image_array, cv2.IMREAD_ANYCOLOR)
		# ret2, _img = getCutImg(img_cv, _ImageSection[1])
		# retext = pytesseract.image_to_string((_img), lang='chi_sim', config="-psm 5")
		# retext = retext.replace('\n','')[::-1]
		# print(retext)
		
		# 这里获取到数据流，看了下源码，下面可以直接用getPNGdata()
		getpngdata = pix.getImageData(output="png")
		# 解码为 np.uint8
		image_array = np.frombuffer(getpngdata, dtype=np.uint8)
		img_cv = cv2.imdecode(image_array, cv2.IMREAD_ANYCOLOR)
		grayImage = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
		ret2, thresholdImage = cv2.threshold(grayImage, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
		t3 = time.time()
		print('t3-t2', t3 - t2)
		# 剪去四周空白边界
		realImage = getRealImage(thresholdImage)
		t3_5 = time.time()
		print('t3_5-t3', t3_5 - t3)
		_page = PDFFormPage(realImage)
		t4 = time.time()
		print('t4-t3', t4 - t3)
		# 是否首页
		_page.ifFirstPage = if_first_page
		# 是否临时文件
		_page.ifTemporaryFile = ifTemporaryFile
		'''检查本PDF是否加粗'''
		_page.checkBlodRate()
		t5 = time.time()
		print('t5-t4', t5 - t4)
		
		'''检查表式的代码，用if_first_page来判断是否首页'''
		_page.checkFormCode()
		'''对页内图片信息进行识别'''
		_page.InitPage_By_FormCode()
		t6 = time.time()
		print('t6-t5', t6 - t5)
		
		'''对子对象的加粗属性赋值'''
		_page.setChildnodesBlodStyle()
		_page.GetChildFieldText(TechInstID, basicProgressBarValue = pg / pdfDoc.pageCount, oneProgressBarStep = 1.0/pdfDoc.pageCount)
		PDFFormPage_List.append(_page)
		t7 = time.time()
		print('t7-t6', t7 - t6)
		# # 保存为图片测试看看
		# cv2.imwrite('PracticalTools\\MPM-PTZJ-GC-002A\\%s-%f.png' % (pg, zoom_x), realImage)
		# cv2.imwrite('RO HLJ23A.05.099\\%s-%f.png' % (pg, zoom_x), realImage)
		# cv2.imwrite('RO HLJ23A.05.099\\checkFormCode %s-%f.png' % (pg, zoom_x), _page.FormCode.img)
		# 更新进度条
		CacheOperator('ProgressBarValue_New_LAMTechInstSerial_UploadPDFFile_By_TechInstID', False, TechInstID,
		              (pg + 1) / pdfDoc.pageCount)
	
	# for page_id, _pdf_form_page in enumerate(PDFFormPage_List):
	'''
		# 工序信息
		self.ProcessNameStrList = []
		self.ProcessNumberStrList = []
		self.ProcessNameCodeIMGList = []
	'''
	'''将工序号、工序名整合后返回'''
	_NameStrList = reduce(lambda x, y: x + y, [_page.ProcessNameStrList for _page in PDFFormPage_List])
	_NumberStrList = reduce(lambda x, y: x + y, [_page.ProcessNumberStrList for _page in PDFFormPage_List])
	_NameCodeIMGList = reduce(lambda x, y: x + y, [_page.ProcessNameCodeIMGList for _page in PDFFormPage_List])
	_NameImgList = reduce(lambda x, y: x + y, [[_name.img for _name in _page.ProcessNameList] for _page in PDFFormPage_List])
	
	# return {
	# 	'NameStrList':_NameStrList,
	# 	'NumberStrList':_NumberStrList,
	# 	'NameCodeIMGList':_NameCodeIMGList,
	# 	'NameImgList':_NameImgList
	# }
	_name = None
	_number = None
	_name_lineid = None
	_notelist = []
	_imglist = []
	_imgcodelist = []
	_note_lineid_list=[]
	_serial_itemlist = []
	for i in range(len(_NumberStrList)):
		if len(_NumberStrList[i]) != 0:
			if not _name is None:
				# 	存入
				_serial_itemlist.append({
					'name': _name,
					'number': _number,
					# 'imglist': _imglist,
					'imgcodelist': _imgcodelist,
					'name_lineid':_name_lineid,
					'note_lineid_list':_note_lineid_list,
					'notelist': ','.join(_notelist),
				})
				_name = None
				_number = None
				_name_lineid = None
				_notelist = []
				_imglist = []
				_imgcodelist = []
				_note_lineid_list = []

			_number = _NumberStrList[i]
			_name = _NameStrList[i]
			_name_lineid = i
			_imglist.append(_NameImgList[i])
			_imgcodelist.append(_NameCodeIMGList[i])
		else:
			if len(_NameStrList[i])>0:
				_notelist.append(_NameStrList[i])
				_note_lineid_list.append(i)
				_imglist.append(_NameImgList[i])
				_imgcodelist.append(_NameCodeIMGList[i])
	if not _name is None:
		# 	存入
		_serial_itemlist.append({
			'name': _name,
			'number': _number,
			# 'imglist': _imglist,
			'imgcodelist': _imgcodelist,
			'name_lineid':_name_lineid,
			'note_lineid_list':_note_lineid_list,
			'notelist': ','.join(_notelist),
		})
		_name = None
		_number = None
		_notelist = []
		_imglist = []
	re_dict = {
		'TechFileCode': PDFFormPage_List[0].TechFileCode_str,
		'ProductCode': PDFFormPage_List[0].ProductCode_str,
		'Serial_Item_List': _serial_itemlist,
		'NameStrList': _NameStrList,
		'NumberStrList': _NumberStrList,
		'NameCodeIMGList': _NameCodeIMGList,
		'NameImgList': _NameImgList
	}
	endTime_pdf2img = datetime.datetime.now()  # 结束时间
	print('pdf2img时间=', (endTime_pdf2img - startTime_pdf2img).seconds)
	return re_dict


def Save_ImgCode(text, imgshape, imgcode, img):
	'''查找是否有text已存在，如有，则退出，如无，则保存'''
	all_objects = PDFImageCode.objects.filter((Q(imagecode=imgcode)))
	if len(list(all_objects))==0:
		_file_path = '.'+PDFCode_OriginalImage_URL+tempfile.mkdtemp().split('\\')[-1]+'.png'
		# _temp_path = os.path.join(tempfile.mkdtemp()+'.png')
		originalImg = cv2.imwrite(_file_path, img)
		# originalImg = img.tobytes()
		_pdfImgCode = PDFImageCode.objects.create(
			image_width = imgshape[0],
			image_height = imgshape[1],
			imagecode = imgcode,
			text = text,
			OriginalImage = _file_path,
		)
		_pdfImgCode.save()
		# os.remove(_temp_path)
	
def Get_ImgText(imgshape, imgcode):
	'''遍历数据库，查找形状、code，如相同或相近，则返回text'''
	qset = (
			Q(image_width=imgshape[0]) &
			Q(image_height=imgshape[1]) &
			Q(imagecode=imgcode)
	)
	_objects = PDFImageCode.objects.filter(qset)
	try:
		return _objects[0].text
	except:
		qset = (
				Q(image_width=imgshape[0]) &
				Q(image_height=imgshape[1])
		)
		EQ = lambda a, b: 1 if a == b else 0
		def getSimilarityRatio(str1, str2):
			return sum(map(EQ, str1, str2))/len(str1)
		sameshape_objects = PDFImageCode.objects.filter(qset)
		if len(sameshape_objects) == 0:
			return None
		simlarity_list = list(map(lambda obj: (obj, getSimilarityRatio(imgcode, obj.imagecode)), sameshape_objects))
		simlarity_list.sort(reverse=True, key=lambda item:item[1])
		if simlarity_list is None:
			return None
		elif simlarity_list[0][1]>0.80:
			return simlarity_list[0][0].text
		else:
			return None
		
	
		
	

if __name__ == '__main__':
	with open('saveimagenumber.txt', 'r') as f:
		ImageIndex = int(f.readline())
	ImageIndex = 0
	ImageIndex_char = 0
	pdf_path = r"RO HLJ23A.05.099.pdf"
	imgs_dir = r"imgs"
	# wind_imagemagick_ghostscript(pdf_path, imgs_dir)
	pyMuPDF_fitz(pdf_path)
	with open('saveimagenumber.txt', 'w') as f:
		f.write(str(ImageIndex - 1))
