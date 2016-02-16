__author__ = 'windmgc'
# coding: UTF-8
# import urllib
# import cv2
# import numpy as np


# stream=urllib.urlopen('http://192.168.8.1:8083/?action=stream')
# bytes=''
# outputStream = cv2.VideoWriter('/home/windmgc/training.avi',cv2.cv.CV_FOURCC('X','V','I','D'),10.0,(240,240))
#
# while 1:
#     bytes+=stream.read(1024)
#     a = bytes.find('\xff\xd8')
#     b = bytes.find('\xff\xd9')
#     if a != -1 and b != -1:
#         jpg = bytes[a:b+2]
#         bytes = bytes[b+2:]
#         i = cv2.imdecode(np.fromstring(jpg,dtype=np.uint8),cv2.CV_LOAD_IMAGE_COLOR)
#         # gray = cv2.cvtColor(i,cv2.COLOR_BGR2GRAY)
#         # cv2.imshow('i',gray)
#         # print i[1][1]
#         # print i[239][239]
#         # print i[120][120]
#         # print gray[120][239]
#         # print i[239][120]
#         hsv=cv2.cvtColor(i,cv2.COLOR_BGR2HSV)
#
#         # lower_blue = np.array([110,50,50])
#         lower_blue = np.array([80,0,0])
#         # upper_blue = np.array([130,255,255])
#         upper_blue = np.array([160,255,255])
#         mask = cv2.inRange(hsv,lower_blue,upper_blue)
#         res = cv2.bitwise_and(i,i,mask=mask)
#         kernelOpening = np.ones((3,3),np.uint8)
#         # opening = cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelOpening)
#         kernelClosing = np.ones((7,7),np.uint8)
#         # closing = cv2.morphologyEx(opening,cv2.MORPH_CLOSE,kernelClosing)
#         closing = cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernelClosing,iterations=2)
#         opening = cv2.morphologyEx(closing,cv2.MORPH_OPEN,kernelOpening,iterations=6)
#         cv2.imshow('frame',i)
#         cv2.imshow('mask',mask)
#         cv2.imshow('res',res)
#         cv2.imshow('closing',opening)
#         outputStream.write(opening)
#         #ESC KEY TO ESCAPE
#         if cv2.waitKey(1) == 27:
#             outputStream.release()
#             exit(0)

## ALSO USEFUL ##
import cv2
import numpy as np
# cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture('http://192.168.8.1:8083/?action=stream')
# outputStream = cv2.VideoWriter('/home/windmgc/training.avi',cv2.cv.CV_FOURCC('M','J','P','G'),25.0,(320,240))
# outputStream = cv2.VideoWriter('/home/windmgc/training.avi',cv2.cv.CV_FOURCC('F','M','P','4'),25.0,(640,480))
outputStream = file('/home/windmgc/training.txt','w')
fourcc = cv2.cv.FOURCC(*'MJPG')
outputVideo = cv2.VideoWriter('/home/windmgc/training.avi',fourcc,25.0,(320,240))

while (1):
    ret, i = cap.read()
    # ret = cap.set(3,320)
    # ret = cap.set(4,240)
    # print ret
    hsv=cv2.cvtColor(i,cv2.COLOR_BGR2HSV)

    lower_blue = np.array([110,50,50])
    # lower_blue = np.array([80,0,0]) #FOR DAYLIGHT
    # upper_blue = np.array([130,255,255])
    upper_blue = np.array([160,255,255])
    mask = cv2.inRange(hsv,lower_blue,upper_blue)
    res = cv2.bitwise_and(i,i,mask=mask)
    kernelOpening = np.ones((3,3),np.uint8)
    # opening = cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelOpening)
    kernelClosing = np.ones((7,7),np.uint8)
    # closing = cv2.morphologyEx(opening,cv2.MORPH_CLOSE,kernelClosing)
    closing = cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernelClosing,iterations=2)
    opening = cv2.morphologyEx(closing,cv2.MORPH_OPEN,kernelOpening,iterations=6)
    cv2.imshow('frame',i)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)
    cv2.imshow('closing',opening)
    # print cv2.flip(opening,1)
    print cap.get(cv2.cv.CV_CAP_PROP_FPS)
    print cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)
    print cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)
    print cap.get(cv2.cv.CV_CAP_PROP_FOURCC)
    # print opening[239][319]
    # print np.char(opening[160][120])
    # outputStream.write("%u\t" % opening[160][120])
    # outputStream.write(opening)
    # openingRGB=cv2.cvtColor(opening,cv2.COLOR_HSV2BGR)
    # outputVideo.write(openingRGB)
    for i in range(0,319):
        avg=0
        for j in range(0,239):
            avg = avg + opening[j][i]
        avg = avg / 240
        outputStream.write("%u " % avg)
    outputStream.write('\n')
    if cv2.waitKey(1) == 27:
        exit(0)


cap.release()
outputStream.close()
outputVideo.close()
cv2.destroyAllWindows()