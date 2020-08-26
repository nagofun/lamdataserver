# -*- coding: gbk -*-
# import os
import cv2
import pytesseract
import os, shutil
from lamdataserver.settings import APP_PATH
# import matplotlib.pyplot as plt
import ImageRecognition.ImageBinaryCode as ImgBC
# import initImageSectionJsonFile as initImageSectionJsonFile
import numpy as np
# import numpy.core._dtype_ctypes
import urllib.request
import time
import json
# from datetime import datetime
from ImageRecognition.LoadSettings import SettingDict
# import threading
import multiprocessing
import requests
import gc
import sys
# import objgraph
# import tracemalloc
import os
import tempfile
import logging

print('--***--  SSTTAARRTT  --***--')
TemplateHASHList = []
ClassifyDir = []
TemplateImageName = []
# with open("./ImageRecognition/IMAGE Templates/ImageSectionInfo_code.json", 'r') as load_f:
# 	ImageSectionInfo_dict = json.load(load_f)
with open(os.path.join(APP_PATH,'ImageSectionInfo_code.json').replace('\\','/'), 'r') as load_f:
    ImageSectionInfo_dict = json.load(load_f)
    pass


# print('before ImageStatus')
class ImageStatus():
	def __init__(self, DeviceCode, time=time.time()):
		self.DeviceCode = DeviceCode
		self.Ticks = time
		self.XValue = None
		self.YValue = None
		self.ZValue = None
		self.ScanningRate = None
		self.Sreal = None
		self.FeedRate = None
		self.GState = None
		self.MState = None
		self.ProgramName = ''
		# self.if_auto_exec_intr = False
		# self.if_exec_intr = False

	# def __del__(self):
	# 	# print('ImageStatus class end')
	# 	pass

	def __str__(self):
		print('%s,%f,%f,%f,%f,%f,%d,%s,%s' % (
		self.DeviceCode, self.XValue, self.YValue, self.ZValue, self.ScanningRate, self.ScanningRate, self.FeedRate, self.GState,
		self.MState))


# print('before movefile')
def movefile(srcfile, dstfile):
	if not os.path.isfile(srcfile):
		# print("%s not exist!" % (srcfile))
		logger.info("%s not exist!" % (srcfile))
	else:
		fpath, fname = os.path.split(dstfile)  # �����ļ�����·��
		if not os.path.exists(fpath):
			os.makedirs(fpath)  # ����·��
		shutil.move(srcfile, dstfile)  # �ƶ��ļ�
		# print("move %s -> %s" % (srcfile, dstfile))
		logger.info("move %s -> %s" % (srcfile, dstfile))


# print('before aHash')
# ��ֵ��ϣ�㷨
def aHash(img):
	# ����Ϊ8*8
	img = cv2.resize(img, (8, 8), interpolation=cv2.INTER_CUBIC)
	# ת��Ϊ�Ҷ�ͼ
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	# sΪ���غͳ�ֵΪ0��hash_strΪhashֵ��ֵΪ''
	s = 0
	hash_str = ''
	# �����ۼ������غ�
	for i in range(8):
		for j in range(8):
			s = s + gray[i, j]
			# ��ƽ���Ҷ�
	avg = s / 64
	# �Ҷȴ���ƽ��ֵΪ1�෴Ϊ0����ͼƬ��hashֵ
	for i in range(8):
		for j in range(8):
			if gray[i, j] > avg:
				hash_str = hash_str + '1'
			else:
				hash_str = hash_str + '0'
	return hash_str


# print('before dHash')
# ��ֵ��֪�㷨
def dHash(img):
	# ����8*8
	img = cv2.resize(img, (9, 8), interpolation=cv2.INTER_CUBIC)
	# ת���Ҷ�ͼ
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	hash_str = ''
	# ÿ��ǰһ�����ش��ں�һ������Ϊ1���෴Ϊ0�����ɹ�ϣ
	for i in range(8):
		for j in range(8):
			hash_str = hash_str + ['0', '1'][gray[i, j] > gray[i, j + 1]]
			# if gray[i,j]>gray[i,j+1]:
			#     hash_str=hash_str+'1'
			# else:
			#     hash_str=hash_str+'0'
	return hash_str


# print('before dHash_ndarray')
# ��ֵ��֪�㷨 adarray����
def dHash_ndarray(array):
	hash_str = ''
	shape = array.shape
	newarray = array.reshape(1, shape[0] * shape[1])[0]
	for i in newarray:
		# print(hash_str + '1' if i > 125 else hash_str + '0', hash_str + ['0', '1'][i>125])
		hash_str = hash_str + '1' if i > 125 else hash_str + '0'
		# hash_str = hash_str + ['0', '1'][i>125]
	return hash_str


# print('before cmpHash')
# Hashֵ�Ա�
def cmpHash(hash1, hash2):
	n = 0
	# hash���Ȳ�ͬ�򷵻�-1�����γ���
	if len(hash1) != len(hash2):
		return -1
	# �����ж�
	for i in range(len(hash1)):
		# �������n����+1��n����Ϊ���ƶ�
		if hash1[i] != hash2[i]:
			n = n + 1
	return 1 - n / 64


# print('before hammingDist')
def hammingDist(s1, s2):
	# assert len(s1) == len(s2)
	return 1 - sum([ch1 != ch2 for ch1, ch2 in zip(s1, s2)]) * 1. / (32 * 32 / 4)


# print('before initParam')
def initParam(rootdir, classifydir):
	list = os.listdir(rootdir)  # �г��ļ��������е�Ŀ¼���ļ�
	for i in range(0, len(list)):
		path = os.path.join(rootdir, list[i])
		if os.path.isfile(path):
			fpath, fname = os.path.split(path)
			TemplateImageName.append(path)
			ClassifyDir.append(classifydir + '\%s' % fname.split('.')[0])


# print('before Imageclassify')
def Imageclassify(rootdir):
	list = os.listdir(rootdir)  # �г��ļ��������е�Ŀ¼���ļ�
	for i in range(0, len(list)):
		path = os.path.join(rootdir, list[i])
		if os.path.isfile(path):
			hash = aHash(cv2.imread(path))
			maxN = 0
			maxID = None
			for id, template_hash in enumerate(TemplateHASHList):
				n = cmpHash(hash, template_hash)
				if n > maxN:
					maxN = n
					maxID = id
			print(maxID)
			fpath, fname = os.path.split(path)
			movefile(path, ClassifyDir[maxID] + '\%s' % fname)
			pass


# print('before CutIdentifyImage_and_RESAVE')
def CutIdentifyImage_and_RESAVE(rootdir, resavedir):
	list = os.listdir(rootdir)  # �г��ļ��������е�Ŀ¼���ļ�
	for i in range(0, len(list)):
		path = os.path.join(rootdir, list[i])
		fpath, fname = os.path.split(path)
		if os.path.isfile(path):
			image = cv2.imread(path)

			# cutarea = CutAreaDic[image.shape[:2]]
			# cutImg = image[cutarea[0]:cutarea[1], cutarea[2]:cutarea[3]]
			y1, y2 = [image.shape[1] - 106, image.shape[1] - 2]
			cutImg = image[2:24, y1: y2]
			cv2.imshow('thresh', cutImg)
			# cv2.waitKey(0)
			cutImg = cv2.cvtColor(cutImg, cv2.COLOR_BGR2GRAY)

			# ��ͼƬ��ֵ�� �׵׺���
			ret, thresh = cv2.threshold(cutImg, 250, 255, cv2.THRESH_BINARY_INV)
			cv2.imshow('thresh', thresh)
			# cv2.waitKey(0)

			# ͶӰ��X�ᣬ�õ�v�б�
			height, width = thresh.shape[:2]
			v = [0] * width
			a = 0
			for x in range(0, width):
				for y in range(0, height):
					if thresh[y, x] == 0:
						a = a + 1
					else:
						continue
				v[x] = a
				a = 0
			# print(v)

			# �з��ַ�
			cutPlace = []
			ifBlock = False
			for i in range(0, width):
				if not ifBlock and v[i] > 0:
					i_start = i
					ifBlock = True
					continue
				if ifBlock and v[i] == 0:
					i_end = i
					ifBlock = False
					cutPlace.append([i_start, i_end])
			if ifBlock:
				i_end = width
				ifBlock = False
				cutPlace.append([i_start, i_end])
			# print(cutPlace)

			# ���з����ַ�  ȡ��һ���ַ�
			for id, i in enumerate(cutPlace):
				i_start, i_end = i
				singleChar = thresh[0:height, i_start:i_end]
				# print(dHash_ndarray(singleChar))

				_w = (int)((height - i_end + i_start) / 2)
				try:
					cubeChar = cv2.copyMakeBorder(singleChar, 0, 0, _w, height - _w - i_end + i_start,
					                              cv2.BORDER_CONSTANT, value=255)
					# print(dHash_ndarray(cubeChar))
					if dHash_ndarray(cubeChar) in ImgBC.ImageBinaryCode_AutoFirst:
						# print()
						# k=0.5
						# cv2.imwrite('%s/%s-%d.png' % (resavedir, fname.split('.')[0], id), cv2.resize(image, (800, 600), interpolation = cv2.INTER_CUBIC))
						cv2.imwrite('%s/%s-%d.png' % (resavedir, fname.split('.')[0], id), image)
				except:
					# cv2.imwrite('%s/%s-%d.png' % (resavedir, fname.split('.')[0], id), singleChar)
					print('error')
				break


# print('before MakeStandardizedImage')
def MakeStandardizedImage(image, ImageSize, FontSizeHeight):
	# �ڵװ���
	height, width = image.shape[:2]
	# cv2.imshow("image0", image)
	# ͶӰ��Y�ᣬ�õ�h�б����յõ��ַ���ʵ�߶�
	h = [(i, sum(image[i])) for i in range(0, height)]
	mappedOnY = [item[0] for item in h if item[1] > 0]
	minh, maxh = min(mappedOnY), max(mappedOnY) + 1
	real_height = maxh - minh

	# ͶӰ��X�ᣬ�õ�w�б����յõ��ַ���ʵ���
	w = [(i, sum(image[0:height, i])) for i in range(0, width)]
	mappedOnX = [item[0] for item in w if item[1] > 0]
	minw, maxw = min(mappedOnX), max(mappedOnX) + 1
	real_width = maxw - minw
	real_image = image[minh:maxh, minw: maxw]

	# �õ���ɫ��ռ����
	ret2, thresh = cv2.threshold(real_image, 0, 1, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
	proportion = sum(sum(thresh)) * 1.0 / (real_width * real_height)
	# print(1.0*real_height/real_width)
	# cv2.imshow("image", image)
	# cv2.imshow("real_image", real_image)
	# cv2.waitKey(0)
	re_img = real_image
	if real_height > real_width:
		#     ��ȥ"."��"-"
		k = 1.0 * FontSizeHeight / real_height

		tempimg = cv2.resize(real_image, ((int)(k * real_width), FontSizeHeight), cv2.INTER_LINEAR)
		rsz_height, rsz_width = tempimg.shape[:2]
		border_w = (int)((ImageSize - rsz_width) / 2)
		border_h = (int)((ImageSize - rsz_height) / 2)
		re_img = cv2.copyMakeBorder(tempimg, border_h, border_h, border_w, border_w, cv2.BORDER_CONSTANT, value=0)

	elif real_height == real_width:
		newImg = np.zeros((ImageSize, ImageSize), np.uint8)
		newImg[29:33, 15:19] = np.ones((4, 4)) * 255
		# cutimageCoordinate = [[15, 29], [18, 32]]
		# newImg[image[cutimageCoordinate[0][1]:cutimageCoordinate[1][1], cutimageCoordinate[0][0]:cutimageCoordinate[1][0]]] = np.ones((3,3))*255
		re_img = newImg

	elif real_height < real_width:
		newImg = np.zeros((ImageSize, ImageSize), np.uint8)
		newImg[19:23, 11:23] = np.ones((4, 12)) * 255
		# cutimageCoordinate = [[11, 19], [22, 22]]
		# newImg[image[cutimageCoordinate[0][1]:cutimageCoordinate[1][1],
		#        cutimageCoordinate[0][0]:cutimageCoordinate[1][0]]] = np.ones((4, 12)) * 255
		re_img = newImg

	if proportion <= 0.35:
		# ����
		kernel = np.ones((2, 2), np.uint8)
		re_img = cv2.dilate(re_img, kernel, iterations=1)

	# # ��ʴ
	# kernel = np.ones((2, 2), np.uint8)
	# re_img = cv2.erode(re_img, kernel, iterations=1)
	# ��ֵ��
	ret2, re_img = cv2.threshold(re_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
	# # ��
	# kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], np.float32)
	# re_img = cv2.filter2D(re_img, -1, kernel=kernel)

	return re_img


# print('before MakeStandardizedLineImage')
def MakeStandardizedLineImage(image,re_img, Type='common'):
	'''����ͼ�����'''
	kernel = np.ones((2, 2), np.uint8)
	# �ӱ߿� �ڵװ���
	MakeBorder = lambda img: cv2.copyMakeBorder(img, 5, 5, 5, 5, cv2.BORDER_CONSTANT, value=0)
	# ����
	Dilate = lambda img: cv2.dilate(img, kernel, iterations=1)
	# Dilate2 = lambda img: cv2.dilate(img, kernel, iterations=2)
	# Dilate3 = lambda img: cv2.dilate(img, kernel, iterations=3)
	# Dilate4 = lambda img: cv2.dilate(img, kernel, iterations=4)
	# ��ʴ
	Erode = lambda img: cv2.erode(img, kernel, iterations=1)
	# ��ֵ��
	# Threshold = lambda img: cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
	# ��
	kernel_Filter = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], np.float32)
	# Filter2D = lambda img: cv2.filter2D(img, -1, kernel=kernel_Filter)
	# ��˹ƽ��
	GaussianBlur = lambda img: cv2.GaussianBlur(img, (9, 9), 2)

	try:
		'''��ȥ��������'''
		# image = changeColorBlackBackWhiteFront(image)
		changeColorBlackBackWhiteFront(image)
		height, width = image.shape[:2]
		# cv2.imshow("image0", image)
		# ͶӰ��Y�ᣬ�õ�h�б����յõ��ַ���ʵ�߶�
		h = [(i, sum(image[i])) for i in range(0, height)]
		mappedOnY = [item[0] for item in h if item[1] > 0]
		minh, maxh = min(mappedOnY), max(mappedOnY) + 1
		real_height = maxh - minh

		# ͶӰ��X�ᣬ�õ�w�б����յõ��ַ���ʵ���
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
		# re_img = Filter2D(re_img)
		# re_img = Dilate3(re_img)
		# cv2.imshow("Image", re_img)
		# cv2.waitKey(0)
		# re_img = Dilate2(re_img)
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


# print('before MakeStandardizedLineImage_CutDot')
def MakeStandardizedLineImage_CutDot(image, _psm1, img1,_psm2, img2, Type='common', dotsize=3):
	re_Image1, re_Image2 = [],[]
	Image1, Image2 = splitLineImageIntoCharacterByDot(image, re_Image1, re_Image2, dotsize)
	re_img = []
	_psm1, img1 = MakeStandardizedLineImage(Image1, re_img, Type)
	_psm2, img2 = MakeStandardizedLineImage(Image2, re_img, Type)
	return [(_psm1, img1), (_psm2, img2)]


# print('before changeColorBlackBackWhiteFront')
def changeColorBlackBackWhiteFront(image):
	# ͳһ��ɫ �ڵװ���
	height, width = image.shape[:2]
	max = image.max()
	if np.mean(image) > 127.5:
		for y in range(0, height):
			for x in range(0, width):
				image[y, x] = max - image[y, x]
	# return image


# print('before changeColorWhiteBackBlackFront')
'''unused'''
def changeColorWhiteBackBlackFront(image):
	# ͳһ��ɫ �׵׺���
	height, width = image.shape[:2]
	max = image.max()
	if np.mean(image) <= 127.5:
		for y in range(0, height):
			for x in range(0, width):
				image[y, x] = max - image[y, x]
	return image


# print('before splitImageIntoCharacter')
'''unused'''
def splitImageIntoCharacter(image):
	# �и����ͼ�� ��ͶӰY����ͶӰX
	if image is None:
		return [None]
	# ͶӰ��Y�ᣬ�õ�h�б�
	height, width = image.shape[:2]
	# cv2.imshow("Image", image)
	# cv2.waitKey(0)

	# image = changeColorBlackBackWhiteFront(image)
	changeColorBlackBackWhiteFront(image)
	# ͶӰ��Y�ᣬ�õ�h�б�
	h = [sum(image[i]) for i in range(0, height)]

	# ����е�Y������ͶӰ��Χ���õ�linePixID_InHeight
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

	# �õ��������ַ�
	LineImage = [image[start_i:end_i + 1, 0:width] for start_i, end_i in linePixID_InHeight]
	# LineImage = map(changeColorWhiteBackBlackFront, LineImage)
	# return LineImage
	# ��ÿ�е��ַ�������CharacterImage��
	CharacterImage = []
	for img_inLine in LineImage:
		# cv2.imshow("Image", img_inLine)
		# cv2.waitKey(0)
		# ͶӰ��X�ᣬ�õ�v�б�
		_height, _width = img_inLine.shape[:2]
		v = [sum(img_inLine[0:_height, i]) for i in range(0, _width)]

		# ����ַ���X������ͶӰ��Χ���õ�CharacterPixID_InWidth
		CharacterPixID_InWidth = []
		startId = None
		for i in range(0, _width):
			if v[i] == 0:
				if not startId is None:
					CharacterPixID_InWidth.append([startId, i])
					startId = None
			else:
				if startId is None:
					startId = i
		if not startId is None:
			CharacterPixID_InWidth.append([startId, i])
		_lineCharacterImage = [img_inLine[0:_height, start_i:end_i] for start_i, end_i in CharacterPixID_InWidth]
		# for img in _lineCharacterImage:
		#     cv2.imshow("Image", img)
		#     cv2.waitKey(0)
		# _lineCharacterImage = map(changeColorWhiteBackBlackFront, _lineCharacterImage)
		CharacterImage.extend(_lineCharacterImage)

	return CharacterImage


# print('before splitLineImageIntoCharacterByDot')
def splitLineImageIntoCharacterByDot(image,re_Image1, re_Image2, dotsize=3):
	# �и��ͼ����ͶӰX,��ͶӰY
	if image is None:
		return [None]
	# �ڵװ���
	# image = changeColorBlackBackWhiteFront(image)
	changeColorBlackBackWhiteFront(image)

	height, width = image.shape[:2]

	v = [sum(image[0:height, i]) for i in range(0, width)]
	# ����ַ���X������ͶӰ��Χ�������ж�
	# startId = None
	dotstartId = None
	dotendId = None
	for i in range(0, width):
		if v[i] == 0:
			if not dotstartId is None:
				#  �ж��Ƿ�Ϊdot
				if i - dotstartId <= dotsize:
					_tryimg = image[0:height, dotstartId:i]
					h = [(j, sum(_tryimg[j])) for j in range(0, height)]
					mappedOnY = [item[0] for item in h if item[1] > 0]
					minh, maxh = min(mappedOnY), max(mappedOnY) + 1
					# real_height = maxh - minh
					if maxh - minh <= dotsize:
						dotstartId = dotstartId
						dotendId = i
						break
				#     ---------------------------------------------
				# CharacterPixID_InWidth.append([startId, i])
				dotstartId = None

		else:
			if dotstartId is None:
				dotstartId = i
	re_Image1, re_Image2 = image, None
	if not dotstartId is None and not dotendId is None:
		# ʶ���dot��ʼλ��
		re_Image1 = image[0:height, 0:dotstartId]
		re_Image2 = image[0:height, dotendId:width]
	return (re_Image1, re_Image2)

	# if not startId is None:
	#     CharacterPixID_InWidth.append([startId, i])
	# _lineCharacterImage = [image[0:height, start_i:end_i] for start_i, end_i in CharacterPixID_InWidth]
	#
	# # �ֱ�ͶӰ��Y�ᣬ�õ�h�б�
	# for singleImage in _lineCharacterImage:
	#     _height, _width = singleImage.shape[:2]
	#
	#     # ͶӰ��Y�ᣬ�õ�h�б����յõ��ַ���ʵ�߶�
	#     h = [(i, sum(image[i])) for i in range(0, _height)]
	#     mappedOnY = [item[0] for item in h if item[1] > 0]
	#     minh, maxh = min(mappedOnY), max(mappedOnY) + 1
	#     real_height = maxh - minh
	#
	#
	# CharacterImage.extend(_lineCharacterImage)
	#
	#
	#
	# # ͶӰ��Y�ᣬ�õ�h�б�
	# h = [sum(image[i]) for i in range(0, height)]
	#
	# # ����е�Y������ͶӰ��Χ���õ�linePixID_InHeight
	# linePixID_InHeight = []
	# startId = None
	# for i in range(0, height):
	#     if h[i] == 0:
	#         if not startId is None:
	#             linePixID_InHeight.append([startId, i])
	#             startId = None
	#     else:
	#         if startId is None:
	#             startId = i
	# if not startId is None:
	#     linePixID_InHeight.append([startId, i])
	#
	# # �õ��������ַ�
	# LineImage = [image[start_i:end_i + 1, 0:width] for start_i, end_i in linePixID_InHeight]
	# # LineImage = map(changeColorWhiteBackBlackFront, LineImage)
	# # return LineImage
	# # ��ÿ�е��ַ�������CharacterImage��
	# CharacterImage = []
	# for img_inLine in LineImage:
	#     # cv2.imshow("Image", img_inLine)
	#     # cv2.waitKey(0)
	#     # ͶӰ��X�ᣬ�õ�v�б�
	#     _height, _width = img_inLine.shape[:2]
	#     v = [sum(img_inLine[0:_height, i]) for i in range(0, _width)]
	#
	#     # ����ַ���X������ͶӰ��Χ���õ�CharacterPixID_InWidth
	#     CharacterPixID_InWidth = []
	#     startId = None
	#     for i in range(0, _width):
	#         if v[i] == 0:
	#             if not startId is None:
	#                 CharacterPixID_InWidth.append([startId, i])
	#                 startId = None
	#         else:
	#             if startId is None:
	#                 startId = i
	#     if not startId is None:
	#         CharacterPixID_InWidth.append([startId, i])
	#     _lineCharacterImage = [img_inLine[0:_height, start_i:end_i] for start_i, end_i in CharacterPixID_InWidth]
	#     # for img in _lineCharacterImage:
	#     #     cv2.imshow("Image", img)
	#     #     cv2.waitKey(0)
	#     # _lineCharacterImage = map(changeColorWhiteBackBlackFront, _lineCharacterImage)
	#     CharacterImage.extend(_lineCharacterImage)
	#
	# return CharacterImage


# print('before GenerateOneImage')
'''disable'''
def GenerateOneImage(CharacterImageList, SingleSize):
	ImageNumber = len(CharacterImageList)
	OneImage = np.ones((SingleSize, SingleSize * ImageNumber), dtype=np.uint8)

	def PasteImg(img, i):
		h, w = img.shape[:2]
		OneImage[0:h, i * SingleSize:i * SingleSize + w] = img

	for i, img in enumerate(CharacterImageList):
		PasteImg(img, i)
	# map(PasteImg, CharacterImageList, range(len(CharacterImageList)))
	# cv2.imshow("Image", OneImage)
	# cv2.waitKey(0)
	return OneImage
	# for img in CharacterImageList:
	#     OneImage[0:SingleSize,0*]
	# pass

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
	# gc.collect()
	return ret2, thresh

def getCutImgCode(image, regionCoordinate):
	ret2, thresh = getCutImg(image, regionCoordinate)
	re = dHash_ndarray(thresh)
	del thresh
	return re

def checkImage(image, Device):
	if not Device:
		pass
	if_auto_exec_intr = False
	if_exec_intr = False
	if_interrupt_intr = False  # ��if_exec_intr����
	'''�ж��Ƿ�Ϊ�Զ�����'''
	if getCutImgCode(image, Device["IdentifyAutoRegion"]) == Device["IdentifyAutoCode"]:
		if_auto_exec_intr = True
		'''�ж��Ƿ�ִ�г����ж�'''
		if getCutImgCode(image, Device["IdentifyInterruptRegion"]) == Device["IdentifyInterruptCode"]:
			if_interrupt_intr=True
		'''�ж��Ƿ���ִ�г���'''
		if getCutImgCode(image, Device["IdentifyExecuteRegion"]) == Device["IdentifyExecuteCode"]:
			if_exec_intr = True
	return if_auto_exec_intr, if_exec_intr, if_interrupt_intr
# print('before RecognitionImage')

def RecognitionImage(image, DeviceCode, language='eng', config='-c -psm %d %s'):
	Error_Flag = False
	# t0=time.time()
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
		# cutimageCoordinate = regionCoordinate
		# IdentifyRegion_Image = image[cutimageCoordinate[1]:cutimageCoordinate[3],
		#                        cutimageCoordinate[0]:cutimageCoordinate[2]]
		# grayImage = cv2.cvtColor(IdentifyRegion_Image, cv2.COLOR_BGR2GRAY)
		# ret2, thresh = cv2.threshold(grayImage, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
		re = dHash_ndarray(thresh)
		del thresh
		# gc.collect()
		return re

	def matchDeviceCode(device):
		return device["DeviceCode"] == DeviceCode

	debug_num = 0
	Img_XValue = None
	Img_YValue = None
	Img_ZValue = None
	Img_ScanningRate = None
	Img_Sreal = None
	Img_FeedRate = None
	Img_GState = None
	Img_MState = None
	Device = None
	# 'CNC-digits'
	configs_type = 'digits'
	try:
		if image is None:
			# Error_Flag=True
			raise ValueError
		debug_num = 1
		# print('debug_num ',debug_num)
		# reImage = []
		re_ImageStatus = None
		Device = filter(matchDeviceCode, ImageSectionInfo_dict).__next__()
		debug_num = 2
		# print('debug_num ',debug_num)
		if not Device:
			pass
		if_auto_exec_intr = False
		if_exec_intr = False
		if_interrupt_intr = False  # ��if_exec_intr����
		'''�ж��Ƿ�Ϊ�Զ�����'''
		debug_num = 3
		# print('debug_num ',debug_num)
		# print(getCutImgCode(image, Device["IdentifyAutoRegion"]) == Device["IdentifyAutoCode"])
		if getCutImgCode(image, Device["IdentifyAutoRegion"]) == Device["IdentifyAutoCode"]:
			if_auto_exec_intr = True
			debug_num = 4
			'''�ж��Ƿ�ִ�г����ж�'''
			if getCutImgCode(image, Device["IdentifyInterruptRegion"]) == Device["IdentifyInterruptCode"]:
				if_interrupt_intr=True
			'''�ж��Ƿ���ִ�г���'''
			if getCutImgCode(image, Device["IdentifyExecuteRegion"]) == Device["IdentifyExecuteCode"]:
				if_exec_intr = True
				debug_num = 5
				# print('debug_num ',debug_num)
				pageNum = 0

				try:
					Page = filter(
						lambda page: getCutImgCode(image, page["IdentifyPageRegion"]) == page["IdentifyPageCode"],
						Device["PageInfo"]).__next__()
				except:
					# Error_Flag = True
					raise ValueError

				debug_num = 6
				# print('debug_num ',debug_num)
				ret2, Img_XValue = getCutImg(image, Page["XValueRegion"])
				ret2, Img_YValue = getCutImg(image, Page["YValueRegion"])
				ret2, Img_ZValue = getCutImg(image, Page["ZValueRegion"])
				ret2, Img_ScanningRate = getCutImg(image, Page["ScanningRateRegion"])
				ret2, Img_Sreal = getCutImg(image, Page["SrealRegion"])
				ret2, Img_FeedRate = getCutImg(image, Page["FeedRateRegion"])
				ret2, Img_GState = getCutImg(image, Page["GStateRegion"])
				ret2, Img_MState = getCutImg(image, Page["MStateRegion"])
				ret2, Img_ProgramName = getCutImg(image, Device["IdentifyProgramNameRegion"])
				debug_num = 7
				# t2 = time.time()
				# print('debug_num ',debug_num)
				# kernel = np.ones((2, 2), np.uint8)
				# MakeBorder = lambda img:cv2.copyMakeBorder(img, 5, 5, 5, 5, cv2.BORDER_CONSTANT, value=0)
				# Dilate = lambda img:cv2.dilate(img, kernel, iterations=1)
				# CheckImg = lambda img: Dilate(MakeBorder(changeColorBlackBackWhiteFront(img)))
				# CheckImg = lambda img: MakeBorder(changeColorBlackBackWhiteFront(img))
				debug_num = 8
				re_ImageStatus = ImageStatus(DeviceCode)
				debug_num = 9
				re_img= []
				_psm, _img = MakeStandardizedLineImage(Img_XValue, re_img, Page["XYZValueType"])
				debug_num = 9.5
				re_ImageStatus.XValue = pytesseract.image_to_string(_img, lang=language,
				                                                    config=config % (_psm, configs_type)).replace(' ',
				                                                                                                  '')
				# print('start cleanup')
				debug_num = 9.6
				# pytesseract.pytesseract.cleanup('_img')
				# print('end cleanup')
				del _img
				debug_num = 10
				_psm, _img = MakeStandardizedLineImage(Img_YValue, re_img, Page["XYZValueType"])
				re_ImageStatus.YValue = pytesseract.image_to_string(_img, lang=language,
				                                                    config=config % (_psm, configs_type)).replace(' ',
				                                                                                                  '')
				# pytesseract.pytesseract.cleanup('_img')
				del _img
				_psm, _img = MakeStandardizedLineImage(Img_ZValue, re_img, Page["XYZValueType"])
				re_ImageStatus.ZValue = pytesseract.image_to_string(_img, lang=language,
				                                                    config=config % (_psm, configs_type)).replace(' ',
				                                                                                                  '')
				# pytesseract.pytesseract.cleanup('_img')
				del _img
				'''ɨ������'''
				if 'cutdot' in Page["ScanningRateType"]:
					_psm1, img1, _psm2, img2 = [],[],[],[]
					_psm_and_imglist = MakeStandardizedLineImage_CutDot(Img_ScanningRate, _psm1, img1,_psm2, img2, re_img, Page["ScanningRateType"])
					_word1 = pytesseract.image_to_string(_psm_and_imglist[0][1], lang=language,
					                                     config=config % (
					                                     _psm_and_imglist[0][0], 'CNC-digits-positive')).replace(' ', '')
					# pytesseract.pytesseract.cleanup('_psm_and_imglist[0][1]')
					_word2 = pytesseract.image_to_string(_psm_and_imglist[1][1], lang=language,
					                                     config=config % (
					                                     _psm_and_imglist[1][0], 'CNC-digits-positive')).replace(' ', '')
					# pytesseract.pytesseract.cleanup('_psm_and_imglist[1][1]')
					re_ImageStatus.ScanningRate = _word1 + '.' + _word2
					del _psm_and_imglist
				else:
					_psm, _img = MakeStandardizedLineImage(Img_ScanningRate, re_img, Page["ScanningRateType"])
					re_ImageStatus.ScanningRate = pytesseract.image_to_string(_img, lang=language,
					                                                          config=config % (
					                                                          _psm, 'CNC-digits-positive')).replace(' ', '')
					# pytesseract.pytesseract.cleanup('_img')
					del _img
				'''��ʾʵʱ����'''
				if 'cutdot' in Page["SrealType"]:
					_psm1, img1, _psm2, img2 = [],[],[],[]
					_psm_and_imglist = MakeStandardizedLineImage_CutDot(Img_Sreal, _psm1, img1,_psm2, img2, re_img, Page["SrealType"])
					_word1 = pytesseract.image_to_string(_psm_and_imglist[0][1], lang=language,
					                                     config=config % (
					                                     _psm_and_imglist[0][0], 'CNC-digits-positive')).replace(' ', '')
					# pytesseract.pytesseract.cleanup('_psm_and_imglist[0][1]')
					_word2 = pytesseract.image_to_string(_psm_and_imglist[1][1], lang=language,
					                                     config=config % (
					                                     _psm_and_imglist[1][0], 'CNC-digits-positive')).replace(' ', '')
					# pytesseract.pytesseract.cleanup('_psm_and_imglist[1][1]')
					re_ImageStatus.Sreal = _word1 + '.' + _word2
					del _psm_and_imglist
				else:
					_psm, _img = MakeStandardizedLineImage(Img_Sreal, re_img, Page["SrealType"])
					re_ImageStatus.Sreal = pytesseract.image_to_string(_img, lang=language,
					                                                          config=config % (
					                                                          _psm, 'CNC-digits-positive')).replace(' ', '')
					del _img
				# print(re_ImageStatus.Sreal)
				'''ʶ���ļ���'''
				_psm, _img = MakeStandardizedLineImage(Img_ProgramName, re_img)
				re_ImageStatus.ProgramName = pytesseract.image_to_string(_img, lang=language).replace(' ','')
				del _img

				if not Img_FeedRate is None:
					# print('debug_num ',debug_num)
					_psm, _img = MakeStandardizedLineImage(Img_FeedRate, re_img, Page["FeedRateType"])
					re_ImageStatus.FeedRate = pytesseract.image_to_string(_img, lang=language,
					                                                      config=config % (_psm, 'CNC-digits-positive')).replace(
						' ', '')
					# pytesseract.pytesseract.cleanup('_img')
					del _img
				# print('debug_num ',debug_num)

				if not Img_GState is None:
					_psm, _img = MakeStandardizedLineImage(Img_GState, re_img, Page["GStateType"])
					re_ImageStatus.GState = pytesseract.image_to_string(_img, lang=language,
					                                                    config=config % (_psm, 'CNC-GState')).replace(
						' ', '')
					# pytesseract.pytesseract.cleanup('_img')
					del _img

				if not Img_MState is None:
					_psm, _img = MakeStandardizedLineImage(Img_MState, re_img, Page["MStateType"])
					# t1 = time.time()
					re_ImageStatus.MState = pytesseract.image_to_string(_img, lang=language,
					                                                    config=config % (_psm, 'CNC-MState')).replace(
						' ', '')
					del _img
	except:
		# print('debug_num', debug_num)
		logger.debug('debug_num', debug_num)
		Error_Flag = True
	finally:
		del Img_XValue
		del Img_YValue
		del Img_ZValue
		del Img_ScanningRate
		del Img_Sreal
		del Img_FeedRate
		del Img_GState
		del Img_MState
		del Device
		# gc.collect()
		# print('-' * 10)
		# for x in locals().keys():
		# 	print('%s:\t' % x, sys.getsizeof(x))
		# print('end delete')

	if Error_Flag:
		logger.debug('return None')
		return (re_ImageStatus, if_auto_exec_intr, if_exec_intr, if_interrupt_intr)
	else:
		return (re_ImageStatus, if_auto_exec_intr, if_exec_intr, if_interrupt_intr)

def realtimeRecognizeImage(image, DeviceCode):
	# ʵʱʶ��ͼƬ
	def matchDeviceCode(device):
		return device["DeviceCode"].upper() == DeviceCode.upper()
	try:
		Device = filter(matchDeviceCode, ImageSectionInfo_dict).__next__()
		Page = filter(
			lambda page: getCutImgCode(image, page["IdentifyPageRegion"]) == page["IdentifyPageCode"],
			Device["PageInfo"]).__next__()
	except:
		# Error_Flag = True
		raise ValueError
	ret2, Img_XValue = getCutImg(image, Page["XValueRegion"])
	ret2, Img_YValue = getCutImg(image, Page["YValueRegion"])
	ret2, Img_ZValue = getCutImg(image, Page["ZValueRegion"])
	ret2, Img_ScanningRate = getCutImg(image, Page["ScanningRateRegion"])
	ret2, Img_FeedRate = getCutImg(image, Page["FeedRateRegion"])
	re_img = []
	_psm, _img = MakeStandardizedLineImage(Img_XValue, re_img, Page["XYZValueType"])
	XValue = pytesseract.image_to_string(_img,
	                                     lang='eng',
	                                     config='-c -psm %d %s' % (_psm, 'digits'),
	                                     timeout=200,
	                                     ).replace(' ','')
	_psm, _img = MakeStandardizedLineImage(Img_YValue, re_img, Page["XYZValueType"])
	YValue = pytesseract.image_to_string(_img,
	                                     lang='eng',
	                                     config='-c -psm %d %s' % (_psm, 'digits'),
	                                     timeout=200,
	                                     ).replace(' ','')
	_psm, _img = MakeStandardizedLineImage(Img_ZValue, re_img, Page["XYZValueType"])
	ZValue = pytesseract.image_to_string(_img,
	                                     lang='eng',
	                                     config='-c -psm %d %s' % (_psm, 'digits'),
	                                     timeout=200,
	                                     ).replace(' ','')
	'''ɨ������'''
	if 'cutdot' in Page["ScanningRateType"]:
		_psm1, img1, _psm2, img2 = [], [], [], []
		_psm_and_imglist = MakeStandardizedLineImage_CutDot(Img_ScanningRate, _psm1, img1, _psm2, img2, re_img,
		                                                    Page["ScanningRateType"])
		_word1 = pytesseract.image_to_string(_psm_and_imglist[0][1], lang='eng',
		                                     config='-c -psm %d %s' % (_psm_and_imglist[0][0], 'CNC-digits-positive')).replace(' ', '')
		_word2 = pytesseract.image_to_string(_psm_and_imglist[1][1], lang='eng',
		                                     config='-c -psm %d %s' % (_psm_and_imglist[1][0], 'CNC-digits-positive')).replace(' ', '')
		ScanningRate = _word1 + '.' + _word2
		del _psm_and_imglist
	else:
		_psm, _img = MakeStandardizedLineImage(Img_ScanningRate, re_img, Page["ScanningRateType"])
		ScanningRate = pytesseract.image_to_string(_img, lang='eng',
		                                           config='-c -psm %d %s' % (_psm, 'CNC-digits-positive')).replace(' ', '')
	if not Img_FeedRate is None:
		# print('debug_num ',debug_num)
		_psm, _img = MakeStandardizedLineImage(Img_FeedRate, re_img, Page["FeedRateType"])
		FeedRate = pytesseract.image_to_string(_img, lang='eng',
		                                       config='-c -psm %d %s' % (_psm, 'CNC-digits-positive')).replace(' ', '')

	redict = {
				'XValue': XValue,
				'YValue': YValue,
				'ZValue': ZValue,
				'ScanningRate': ScanningRate,
				'FeedRate': FeedRate,
			}
	return redict

# print('before UpdateLAMProcessData_CNCData')
def UpdateLAMProcessData_CNCData(CNCProcessStatus_id, ImageStatus_value, UpdateScreenRecognition):
	# 20191017
	try:
		if CNCProcessStatus_id==1870444:
			pass
		updatedata = {}
		updatedata['CNCProcessStatus_id'] = CNCProcessStatus_id
		if ImageStatus_value == None:
			# û��ͼƬ
			updatedata['if_auto_exec_intr'] = False
			updatedata['if_exec_intr'] = False
			updatedata['if_interrupt_intr'] = False
		else:
			updatedata['if_auto_exec_intr'] = ImageStatus_value[1]
			updatedata['if_exec_intr'] = ImageStatus_value[2]
			updatedata['if_interrupt_intr'] = ImageStatus_value[3]
			if ImageStatus_value[0] != None:
				updatedata['DeviceCode'] = ImageStatus_value[0].DeviceCode
				updatedata['Ticks'] = ImageStatus_value[0].Ticks
				updatedata['XValue'] = ImageStatus_value[0].XValue
				updatedata['YValue'] = ImageStatus_value[0].YValue
				updatedata['ZValue'] = ImageStatus_value[0].ZValue
				updatedata['ScanningRate'] = ImageStatus_value[0].ScanningRate
				updatedata['Sreal'] = ImageStatus_value[0].Sreal
				updatedata['FeedRate'] = ImageStatus_value[0].FeedRate
				updatedata['GState'] = ImageStatus_value[0].GState
				updatedata['MState'] = ImageStatus_value[0].MState
				updatedata['ProgramName'] = ImageStatus_value[0].ProgramName

		requests.post(UpdateScreenRecognition, data=updatedata)
	except:
		# print('Update Error! id:%d\tvalue:%s\t%s\t%s\t%s' % (
		# CNCProcessStatus_id, ImageStatus_value[0], ImageStatus_value[1], ImageStatus_value[2], ImageStatus_value[3]))
		logger.error('Update Error! id:%d\tvalue:%s\t%s\t%s\t%s' % (
		CNCProcessStatus_id, ImageStatus_value[0], ImageStatus_value[1], ImageStatus_value[2], ImageStatus_value[3]))
		# print(CNCProcessStatus_id, ImageStatus_value)
	return

def cleanup():
	t0 = time.time()
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
	t1=time.time()
	print('CleanUp Cost:%.02f'%(t1-t0))
	logger.info('CleanUp Cost:%.02f'%(t1-t0))

# print('before AnalyseScreen')
def AnalyseScreen(QueryDataUrl, QueryImageUrl, UpdateScreenRecognition,imgid):
	while True:
		if imgid > 500:
			break
		t0 = time.time()
		# print('START AnalyseScreen  :  %s'%os.getpid())
		# try:
		r = requests.get(QueryDataUrl)
		downloaddict = json.loads(r.text)
		t0_5 = time.time()
		'''
		_dict = {
			'CNCProcessStatus_id': CNCProcessStatusid,
			'Worksection_code':Worksection_code,
		}
		'''
		# print('--1')
		# print(type(downloaddict['CNCProcessStatus_id']), downloaddict['CNCProcessStatus_id'])
		if downloaddict['CNCProcessStatus_id'] == -1:
			# print('continue')
			return
		CNCProcessStatus_id = downloaddict['CNCProcessStatus_id']
		Worksection_code = downloaddict['Worksection_code']
		# ��ȡͼƬ
		# r_getimage = requests.get(QueryImageUrl+str(CNCProcessStatus_id))
		resp = urllib.request.urlopen(QueryImageUrl + str(CNCProcessStatus_id) + '/')
		image1 = np.asarray(bytearray(resp.read()), dtype='uint8')
		# cv2.imshow('image1', image1)
		# cv2.waitKey(0)
		if image1 is None:
			# print('AnalyseScreen Error! image is None1')
			logger.info('Image is None Type,CNCProcessStatus_id:%d' % CNCProcessStatus_id)
		# print(CNCProcessStatus_id)
		image = cv2.imdecode(image1, cv2.IMREAD_COLOR)
		# cv2.imshow('image', image)
		# cv2.waitKey(0)
		# time.sleep(1)

		# del resp
		# print('--2')
		# cv2.imshow('image', image)
		# cv2.waitKey(0)
		# t3 = time.time()
		# ʶ��ͼƬ
		# if image is None:
		# print('Image is None')
		# print(' ------ RecognitionImage')

		'''----'''
		ImageStatus_value = None
		t1 = time.time()
		if image is not None:
			ImageStatus_value = RecognitionImage(image, Worksection_code.lower(), 'eng')
			# print(ImageStatus_value)
			# try:
			# 	print(ImageStatus_value[0].Sreal)
			# 	if float(ImageStatus_value[0].Sreal)>0:
			# 		print('-'*10)
			# 		print(CNCProcessStatus_id)
			# except:
			# 	print('PrintError')
			# 	pass
		else:
			# print(CNCProcessStatus_id)
			logger.info('Image is None Type,CNCProcessStatus_id:%d'%CNCProcessStatus_id)
		t2 = time.time()
		'''check data'''
		error_flag = False
		if ImageStatus_value is not None and ImageStatus_value[0] is not None:
			if not error_flag and ImageStatus_value[0].XValue is not None:
				try:
					a=float(ImageStatus_value[0].XValue)
				except:
					error_flag = True
			if not error_flag and ImageStatus_value[0].YValue is not None:
				try:
					a=float(ImageStatus_value[0].YValue)
				except:
					error_flag = True
			if not error_flag and ImageStatus_value[0].ZValue is not None:
				try:
					a=float(ImageStatus_value[0].ZValue)
				except:
					error_flag = True
			if not error_flag and ImageStatus_value[0].ScanningRate is not None:
				try:
					a=float(ImageStatus_value[0].ScanningRate)
				except:
					error_flag = True
			if not error_flag and ImageStatus_value[0].FeedRate is not None:
				try:
					a=float(ImageStatus_value[0].FeedRate)
				except:
					error_flag = True
			if error_flag:
				# print('Error! CNCProcessStatus_id:%d'%CNCProcessStatus_id,ImageStatus_value[0])
				logger.error('Value Recognite Error! CNCProcessStatus_id:%d '%CNCProcessStatus_id,ImageStatus_value[0])
		t3 = time.time()
		del image
		# if ImageStatus_value is not None:
		# 	# �ϴ�������������
		# 	UpdateLAMProcessData_CNCData(CNCProcessStatus_id, ImageStatus_value, UpdateScreenRecognition)
		UpdateLAMProcessData_CNCData(CNCProcessStatus_id, ImageStatus_value, UpdateScreenRecognition)
		t4 = time.time()
		# print('PPID:', os.getpid(), CNCProcessStatus_id, 'DwT:%.02f'%(t0_5 - t0),'RecT:%.02f'%(t2 - t1),'UpT:%.02f'%(t4 - t3),'SUMT:','%.02f'%(t4 - t0), 'imgid:',imgid)
		print('PPID:%d Status_id:%d  DwT:%.02f RecT:%.02f tUpT:%.02f SUMT:%.02f imgid:%d' % (
			os.getpid(),
			CNCProcessStatus_id,
			t0_5 - t0,
			t2 - t1,
			t4 - t3,
			t4 - t0,
			imgid))
		logger.info('PPID:%d\tStatus_id:%d\tDwT:%.02f\tRecT:%.02f\tUpT:%.02f\tSUMT:%.02f\timgid:%d'%(
			os.getpid(),
			CNCProcessStatus_id,
			t0_5 - t0,
			t2 - t1,
			t4 - t3,
			t4 - t0,
			imgid))
		imgid += 4
		del r
		del downloaddict
		del ImageStatus_value
		del resp
		del image1
		# gc.collect()
		'''----'''

# ProcessList = []
# print('outside main')

def restart_program():
	python = sys.executable
	os.execl(python, python, *sys.argv)


'''��־����'''
logging.basicConfig(level=logging.DEBUG,
	                    filename=time.strftime('%Y-%m-%d.log', time.localtime()),
	                    # filename='outlog.log',
	                    filemode='a',
	                    datefmt='%Y-%m-%d %a %H:%M:%S',
	                    format='%(asctime)s %(filename)s %(funcName)s %(lineno)d - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

if __name__ == '__main__':


	multiprocessing.freeze_support()
	filenum = 40000
	CharCodeList = []
	SingleImageSize = 35
	# imgid = 0
	QueryDataUrl = SettingDict['[QueryData]']
	QueryImageUrl = SettingDict['[QueryImage]']
	# DecliendSeconds = int(SettingDict['[DeclinedSeconds]'])
	UpdateScreenRecognition = SettingDict['[UpdateScreenRecognition]']
	# ProcessNumber = int(SettingDict['[ProcessNumber]'])
	# ProcessStopTime = float(SettingDict['[ProcessStopTime]'])

	# objgraph.show_growth()
	AnalyseScreenProcess1 = multiprocessing.Process(target=AnalyseScreen, args=(QueryDataUrl, QueryImageUrl, UpdateScreenRecognition, 0))
	AnalyseScreenProcess1.start()
	# AnalyseScreenProcess1.join()

	time.sleep(0.25)
	AnalyseScreenProcess2 = multiprocessing.Process(target=AnalyseScreen, args=(QueryDataUrl, QueryImageUrl, UpdateScreenRecognition, 1))
	AnalyseScreenProcess2.start()
	# AnalyseScreenProcess2.join()
	time.sleep(0.25)
	AnalyseScreenProcess3 = multiprocessing.Process(target=AnalyseScreen, args=(QueryDataUrl, QueryImageUrl, UpdateScreenRecognition, 2))
	AnalyseScreenProcess3.start()
	# AnalyseScreenProcess3.join()
	time.sleep(0.25)
	AnalyseScreenProcess4 = multiprocessing.Process(target=AnalyseScreen, args=(QueryDataUrl, QueryImageUrl, UpdateScreenRecognition, 3))
	AnalyseScreenProcess4.start()
	AnalyseScreenProcess4.join()




	# p = multiprocessing.Pool(4)
	# for i in range(5):
	# 	p.apply_async(AnalyseScreen,args=(QueryDataUrl, QueryImageUrl, UpdateScreenRecognition))
	# p.close()
	# p.join()
	# AnalyseScreen(QueryDataUrl, QueryImageUrl, UpdateScreenRecognition)
	gc.collect()
	cleanup()
	print('Restarting...')
	restart_program()

	# objgraph.show_growth()
	# objgraph.show_most_common_types()
	# print('3--------------------------')
	# objgraph.show_growth()
	#
	# objgraph.show_backrefs(objgraph.by_type('function')[0], max_depth=10,
	#                        filename='function.dot')
	# objgraph.show_backrefs(objgraph.by_type('function')[1], max_depth=10,
	#                        filename='function-1.dot')
	# objgraph.show_backrefs(objgraph.by_type('tuple')[0], max_depth=10,
	#                        filename='tuple.dot')
	# objgraph.show_backrefs(objgraph.by_type('tuple')[1], max_depth=10,
	#                        filename='tuple-1.dot')
	# objgraph.show_backrefs(objgraph.by_type('builtin_function_or_method')[0], max_depth=10,
	#                        filename='builtin_function_or_method.dot')
	# objgraph.show_backrefs(objgraph.by_type('builtin_function_or_method')[1], max_depth=10,
	#                        filename='builtin_function_or_method-1.dot')
	# objgraph.show_backrefs(objgraph.by_type('dict')[0], max_depth=10,
	#                        filename='dict.dot')
	# objgraph.show_backrefs(objgraph.by_type('dict')[1], max_depth=10,
	#                        filename='dict-1.dot')
	'''��������'''
	# print('Restarting...')
	# restart_program()



	'''�ڴ�ռ�÷���'''
	# tracemalloc.start()  # ��ʼ����ڴ�
	# snapshot = tracemalloc.take_snapshot()  # ��¼�ڴ����
	# top_stats = snapshot.statistics('lineno')  # ��lineno�����ڴ����״̬
	# for stat in top_stats[:20]:
	# 	print(stat)
	#
	# for i in range(5):
	# 	print('-'*100,i)
	# 	imgid = 0
	# 	AnalyseScreen(QueryDataUrl, QueryImageUrl, UpdateScreenRecognition)
	#
	# 	snapshot_2 = tracemalloc.take_snapshot()  # ��¼�µ��ڴ����
	# 	top_stats = snapshot_2.compare_to(snapshot, 'lineno')  # �Ա������ڴ���յ���Ϣ
	# 	for stat in top_stats[:50]:  # ��ӡǰ10���ڴ�ռ�����
	# 		print(stat)
	# 	snapshot = snapshot_2
	# 	print(gc.garbage)



	'''ע����20191017 ֱ��20191017-end'''
	# # print('ready go into Procss')
	# # ProcessList = []
	# p = threading.Thread(target=AnalyseScreen, args=(QueryDataUrl, QueryImageUrl, UpdateScreenRecognition))
	#
	# # p = multiprocessing.Process(target=AnalyseScreen, args=(QueryDataUrl, QueryImageUrl, UpdateScreenRecognition))
	# # print('go out of Procss')
	# # ProcessList.append(p)
	# # print('before START')
	# p.start()
	# # time.sleep(1)
	# # print('after START')
	# p.join(0.5)
	# # print('end')
	# # for i in range(4):
	# #     p = Process(target = AnalyseScreen,args=())
	# #     ProcessList.append(p)
	# #     p.start()
	# #     p.join(0.5)
	#
	# # pool = Pool(processes=4)
	# # for i in range(4):
	# #     pool.apply_async(AnalyseScreen)
	# # pool.close()
	# # pool.join()
	# # print('The End')
	'''20191017-end'''

	# AnalyseScreenProcess1 = AnalyseScreenProcess()
	# AnalyseScreenProcess2 = AnalyseScreenProcess()
	# AnalyseScreenProcess3 = AnalyseScreenProcess()
	# # AnalyseScreenProcess4 = AnalyseScreenProcess()
	# # ProcessList.extend([AnalyseScreenProcess1,AnalyseScreenProcess2,AnalyseScreenProcess3,AnalyseScreenProcess4])
	# print('***   Start One Loop   ***')
	# AnalyseScreenProcess1.start()
	# time.sleep(1)
	# AnalyseScreenProcess2.start()
	# time.sleep(1)
	# AnalyseScreenProcess3.start()
	# time.sleep(1)
	# # AnalyseScreenProcess4.start()
	# # time.sleep(1)
	# AnalyseScreenProcess1.join(2)
	# AnalyseScreenProcess2.join(2)
	# AnalyseScreenProcess3.join(2)
	# AnalyseScreenProcess4.join(2)
	# while True:
	#     AnalyseScreenProcess1 = AnalyseScreenProcess()
	#     AnalyseScreenProcess2 = AnalyseScreenProcess()
	#     AnalyseScreenProcess3 = AnalyseScreenProcess()
	#     AnalyseScreenProcess4 = AnalyseScreenProcess()
	#     # ProcessList.extend([AnalyseScreenProcess1,AnalyseScreenProcess2,AnalyseScreenProcess3,AnalyseScreenProcess4])
	#     print('***   Start One Loop   ***')
	#     AnalyseScreenProcess1.start()
	#     time.sleep(1)
	#     AnalyseScreenProcess2.start()
	#     time.sleep(1)
	#     AnalyseScreenProcess3.start()
	#     time.sleep(1)
	#     AnalyseScreenProcess4.start()
	#     time.sleep(1)
	#     AnalyseScreenProcess1.join()
	#     AnalyseScreenProcess2.join()
	#     AnalyseScreenProcess3.join()
	#     AnalyseScreenProcess4.join()
	# ProcessList = [AnalyseScreenProcess(ProcessList)] * ProcessNumber
	# print(ProcessList)
	# for i in range(ProcessNumber):
	#     ProcessList[i].start()
	#
	#     ProcessList[i].join()
	#     # _p.start()
	#     time.sleep(1)

	# for i in range(ProcessNumber):
	#     print('Process New')
	#     _process = AnalyseScreenProcess(ProcessList)
	#     ProcessList.append(_process)
	#     print('Process Start')
	#     ProcessList[-1].start()
	#
	#     time.sleep(1)
	# AnalyseScreenProcess1 = AnalyseScreenProcess()
	# AnalyseScreenProcess2 = AnalyseScreenProcess()
	# AnalyseScreenProcess3 = AnalyseScreenProcess()
	# AnalyseScreenProcess1.start()
	# time.sleep(1)
	# AnalyseScreenProcess2.start()
	# time.sleep(1)
	# AnalyseScreenProcess3.start()
	# AnalyseScreenProcess1.join()
	# AnalyseScreenProcess2.join()
	# AnalyseScreenProcess3.join()
	# for _thread in AnalyseScreenThreadlist:
	#     _thread.start()
	#     _thread.join(2)

	# ��ȡ��¼��ż����κ�

	# -------- ʶ��ͼ�� ---------

	# image = cv2.imread(r'E:\chenbo\Program\14-PrintScreen\DATA CT04\0.png')
	# RecognitionImage(image, "sc-ct-04")
	#
	# # ���ڵװ���תΪ�׵׺���
	# rootdir = r"E:\chenbo\Program\14-PrintScreen\selectedImage"
	# list = os.listdir(rootdir)  # �г��ļ��������е�Ŀ¼���ļ�
	# path = map(os.path.join, [rootdir] * len(list), list)
	#
	# i=0
	# for _path in path:
	#     i+=1
	#     _image = cv2.imread(_path)
	#     grayImage = cv2.cvtColor(_image, cv2.COLOR_BGR2GRAY)
	#     ret2, thresh = cv2.threshold(grayImage, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
	#     # WBimage = changeColorWhiteBackBlackFront(thresh)
	#     WBimage = thresh
	#     # WBimage = cv2.copyMakeBorder(WBimage, 10, 10, 10, 10, cv2.BORDER_CONSTANT,value=[0,0,0])
	#     # cv2.imshow("Image", WBimage)
	#     # cv2.waitKey(0)
	#     cv2.imwrite(r'E:\chenbo\Program\14-PrintScreen\selectedImage\WB\%d.tif'%i,WBimage )
	'''========================================================='''
	'''��ÿ�����ֽ��б�׼������ �Ӵ� ��ֵ��'''
	# image = cv2.imread(r"E:\1.chenbo\1-program\14-PrintScreen\selectedImage\OneImage\SCCT1246.tif")
	# grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	# ret2, thresh = cv2.threshold(grayImage, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
	# CharImages = splitImageIntoCharacter(thresh)
	# reImage = []
	# for charimage in CharImages:
	#     re = MakeStandardizedImage(charimage, 34, 30)
	#     reImage.append(re)
	#     # img = cv2.resize(re, (8, 8), interpolation=cv2.INTER_CUBIC)
	#     # cv2.imshow("image0", img)
	#     cv2.waitKey(0)
	#
	# OneImage = GenerateOneImage(reImage, SingleImageSize)
	# cv2.imwrite(r'E:\1.chenbo\1-program\14-PrintScreen\selectedImage\OneImage\template.tif', OneImage)
	'''========================================================='''

	# height, width = charimage.shape[:2]
	# border_w = (int)((SingleImageSize - width) / 2)
	# border_h = (int)((SingleImageSize - height) / 2)
	# img = cv2.copyMakeBorder(charimage, border_h, border_h, border_w, border_w, cv2.BORDER_CONSTANT, value=0)
	# # [for line in charimage]
	# # proportion = sum(sum(th1))*1.0/(SingleImageSize*SingleImageSize)
	# # print(proportion)
	# # cv2.imshow("%f"%proportion, charimage)
	# cv2.imshow("image0", img)
	# cv2.waitKey(0)
	#
	#
	# kernel = np.ones((3, 3), np.uint8)
	# dilation = cv2.dilate(charimage, kernel, iterations=1)
	# height, width = dilation.shape[:2]
	# border_w = (int)((SingleImageSize - width) / 2)
	# border_h = (int)((SingleImageSize - height) / 2)
	# img = cv2.copyMakeBorder(dilation, border_h, border_h, border_w, border_w, cv2.BORDER_CONSTANT, value=0)
	# cv2.imshow("image1", img)
	# cv2.waitKey(0)

	'''���������ͼ��'''
	# # image = cv2.imread(r'E:\1.chenbo\1-program\14-PrintScreen\DATA CT01\20190314 083830.png')
	# # DeviceCode = "sc-ct-01"
	# # re_ImageStatus = RecognitionImage(image, DeviceCode, 'eng')
	# rootdir = r'E:\1.chenbo\1-program\14-PrintScreen\IMAGE Templates\test'
	# DeviceCode = "sc-ct-01"
	# list = os.listdir(rootdir)  # �г��ļ��������е�Ŀ¼���ļ�
	# imagelist = []
	# for i in range(0, len(list)):
	#     path = os.path.join(rootdir, list[i])
	#     if os.path.isfile(path):
	#         if list[i].startswith('CT01'):
	#             DeviceCode = "sc-ct-01"
	#             continue
	#         elif list[i].startswith('CT02'):
	#             DeviceCode = "sc-ct-02"
	#         elif list[i].startswith('CT04'):
	#             DeviceCode = "sc-ct-04"
	#         elif list[i].startswith('CT06'):
	#             DeviceCode = "sc-ct-06"
	#         # print(path)
	#         image = cv2.imread(path)
	#         t1 = time.time()
	#         re_ImageStatus = RecognitionImage(image,DeviceCode, 'eng')
	#         print(time.time()-t1)
	#         # print(str(re_ImageStatus))
	#         pass
	#         # if re_image:
	#         #     imagelist.extend(re_image)
	#
	#         # cv2.imshow("Image", i)
	#         # cv2.waitKey(0)
	# # print(imagelist)
	# # OneImage = GenerateOneImage(imagelist, SingleImageSize)
	# # cv2.imwrite(r'E:\chenbo\Program\14-PrintScreen\selectedImage\OneImage\%s.tif' % str(DeviceCode), OneImage)

	# ------ test1 -----
	# TemplateImageList = []
	# initParam(r'E:\chenbo\Program\14-PrintScreen\template', r'E:\chenbo\Program\14-PrintScreen\classify')
	# TemplateImageList = list(map(cv2.imread, TemplateImageName))
	# TemplateHASHList = list(map(aHash, TemplateImageList))
	# print(TemplateHASHList)
	#
	# Imageclassify(r'E:\chenbo\Program\14-PrintScreen\DATA')

	# ------ �и����Ͻ�-----
	# CutAreaDic={(600,800):(5,24,692,794),
	#             (768,1024):(3,22,919,1021)}
	# CutIdentifyImage_and_RESAVE(r'E:\chenbo\Program\14-PrintScreen\DATA',r'E:\chenbo\Program\14-PrintScreen\cut1', CutAreaDic)
	# CutIdentifyImage_and_RESAVE(r'E:\chenbo\Program\14-PrintScreen\template',r'E:\chenbo\Program\14-PrintScreen\template\cut1')

	# CutIdentifyImage_and_RESAVE(r'E:\chenbo\Program\14-PrintScreen\template\auto',
	#                             r'E:\chenbo\Program\14-PrintScreen\template\auto\cut1')
	# CutIdentifyImage_and_RESAVE(r'G:\1-program\14-PrintScreen\template\auto',
	#                             r'G:\1-program\14-PrintScreen\template\auto\cut1')
	# # ------�ҶȻ���ֵ��-----
	# image = cv2.imread(r"E:\chenbo\Program\14-PrintScreen\cut1\20180919 083502.png")
	#
	# image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
	# image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	# ret, thresh = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY_INV)
	# cv2.namedWindow("Image")
	# cv2.imshow("Image", thresh)
	# cv2.waitKey(0)
	#
	# cv2.destroyAllWindows()

	# plt.imshow(thresh)
	# plt.axis("off")  # ȥ��������
	# plt.show()

	# print('EEENNNDDD')
