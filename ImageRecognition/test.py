# -*- coding: gbk -*-
import os
import cv2
import os,shutil
import numpy as np
import time
import matplotlib.pyplot as plt

image = cv2.imread(r"E:\chenbo\Program\14-PrintScreen\template\1.png")
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
ret,th1 = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
plt.imshow(th1)
# plt.axis("off")  # 去除坐标轴
plt.show()
th2 = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 2)
th3 = cv2.adaptiveThreshold(image,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,5,2)
titles = ['Original Image', 'Global Thresholding (v = 127)',
            'Adaptive Mean Thresholding', 'Adaptive Gaussian Thresholding']

# image, contours, hierarchy = cv2.findContours(th1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

# images = [image, th1, th2, th3]
images = [image, th1, th2, th3]
for i in range(4):
    plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])
plt.show()


#
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#
# gradX = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
# gradY = cv2.Sobel(gradX, ddepth=cv2.CV_32F, dx=0, dy=1, ksize=-1)
#
# (_, thresh) = cv2.threshold(gray, 90, 255, cv2.THRESH_TOZERO)
# plt.imshow(thresh)
# plt.axis("off")#去除坐标轴
# plt.show()
#
#
# # subtract the y-gradient from the x-gradient
# gradient = cv2.subtract(gradX, gradY)
# gradient = cv2.convertScaleAbs(gradient)
#
# # blur and threshold the image
# blurred = cv2.blur(gradient, (9, 9))
# (_, thresh) = cv2.threshold(blurred, 90, 255, cv2.THRESH_BINARY)
#
#
# kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
# closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
#
# plt.imshow(gradX)
# plt.axis("off")#去除坐标轴
# plt.show()