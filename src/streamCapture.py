__author__ = 'windmgc'
# coding: UTF-8

'''This is the source code file for capturing videos and collecting training data.
The video stream address here is http://192.168.8.1:8083/?action=stream, just an example.
'''

import urllib
import cv2
import numpy as np


def main():
    stream=urllib.urlopen('http://192.168.8.1:8083/?action=stream')
    bytes=''
    # Uncomment this line to save captured videos.
    # outputStream = cv2.VideoWriter('/home/windmgc/training.avi',cv2.cv.CV_FOURCC('X','V','I','D'),10.0,(240,240))
    outputStream = file('/home/windmgc/training.txt','w')

    while 1:
        bytes+=stream.read(1024)
        a = bytes.find('\xff\xd8')
        b = bytes.find('\xff\xd9')
        if a != -1 and b != -1:
            jpg = bytes[a:b+2]
            bytes = bytes[b+2:]
            i = cv2.imdecode(np.fromstring(jpg,dtype=np.uint8),cv2.CV_LOAD_IMAGE_COLOR)
            hsv=cv2.cvtColor(i,cv2.COLOR_BGR2HSV)

            # lower_blue = np.array([110,50,50])
            lower_blue = np.array([80,0,0])
            # upper_blue = np.array([130,255,255])
            upper_blue = np.array([160,255,255])
            mask = cv2.inRange(hsv,lower_blue,upper_blue)
            res = cv2.bitwise_and(i,i,mask=mask)
            kernelOpening = np.ones((3,3),np.uint8)
            kernelClosing = np.ones((7,7),np.uint8)
            closing = cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernelClosing,iterations=2)
            opening = cv2.morphologyEx(closing,cv2.MORPH_OPEN,kernelOpening,iterations=6)
            # cv2.imshow('frame',i)
            # cv2.imshow('mask',mask)
            # cv2.imshow('res',res)
            # cv2.imshow('closing',opening)
            for i in range(0,319):
                avg=0
                for j in range(0,239):
                    avg = avg + opening[j][i]
                avg = avg / 240
                outputStream.write("%u " % avg)
            outputStream.write('\n')
            #ESC KEY TO ESCAPE
            if cv2.waitKey(1) == 27:
                outputStream.release()
                exit(0)

if __name__=="__main__":
    main()
