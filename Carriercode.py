from array import array
from hashlib import new
from tkinter import W
from turtle import color
import numpy as np
import cv2
import math
from img_pro import *
# load img,imggray
img_org = cv2.imread(r"F:\Vision Machine Learning\Opencv\Carrier code\ImageLog_\20220107\20220107_010449.jpg")
img_gray = cv2.cvtColor(img_org, cv2.COLOR_BGR2GRAY)
cv2.imwrite("F:\Vision Machine Learning\Opencv\Carrier code\Debug\imggray.jpg", img_gray)
# roi
img_cnt = img_org[400:1570,: ]

img_roi = img_gray[400:1570,: ]

ret,img_roi = cv2.threshold(img_roi, 120, 255, cv2.THRESH_BINARY)
cv2.imwrite("F:\Vision Machine Learning\Opencv\Carrier code\Debug\imgroi.jpg", img_roi)

img_blur = cv2.medianBlur(img_roi, 5)
cv2.imwrite("F:\Vision Machine Learning\Opencv\Carrier code\Debug\imgroiblur.jpg", img_blur)

#find contour
contours, hierarchy = cv2.findContours(img_blur, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# cv2.drawContours(img_cnt, contours,-1, (0,0,255), 3)

print(len(contours))
for cnt in contours:
    a = 10
    cnt_perimeter = cv2.arcLength(cnt, True)
    cnt_area = cv2.contourArea(cnt)
    if (100000 < cnt_area < 140000):
        # cv2.drawContours(img_cnt, [cnt],-1, (0,0,255), 3)
        print(" chu vi = {}, dientich = {}".format(cnt_perimeter, cnt_area))
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(img_cnt,[box],0,(0,0,255),3)
        print("angle_caculate = {}".format(rect[2]))
        angle = rect[2]
        
        x, y = rect[0]  
        cv2.circle(img_cnt,(int(x), int(y)), 2, (255,0,0) ,-1)
        cv2.imwrite("F:\Vision Machine Learning\Opencv\Carrier code\Debug\imgroi_contour.jpg", img_cnt)
        # print("point1 = {} , point2 = {}, point3 = {}, point4 = {}".format(box[0], box[1], box[2], box[3]))
        w = int(rect[1][0])
        h = int(rect[1][1])
        print(" Rect tuple = {}".format(rect))

        new_box = []
        for point in box:
            point_new = cacl_coordi_after_rotate(x_center= x, y_center=y, x_org= point[0], y_org=point[1], angle=angle)
            new_box.append(point_new)
            print(point_new)

new_box = np.asarray(new_box)
sum = np.sum(new_box, axis = -1)
min = np.amin(sum)
indexOfStartPoint = np.where(sum == min)[0]
startPointRect = new_box[indexOfStartPoint].reshape(-1,)

if angle > 0 and w<h:
    img_cnt =  rotate(img_cnt, angle-90, (int(x), int(y)))
elif angle > 0 and w>h:
    img_cnt =  rotate(img_cnt, angle - 90, (int(x), int(y)))

    
cv2.imwrite("F:\Vision Machine Learning\Opencv\Carrier code\Debug\imgroi_rotate.jpg", img_cnt)

img_code = img_cnt[int(startPointRect[1]):(int(startPointRect[1]) + h), int(startPointRect[0]):(int(startPointRect[0]) + w)]
cv2.imwrite("F:\Vision Machine Learning\Opencv\Carrier code\Debug\imgroi_code.jpg", img_code)
# 

