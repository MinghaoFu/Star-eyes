import cv2
import numpy as np

if __name__ == "__main__":
    cap1 = cv2.VideoCapture(0)
    cap2 = cv2.VideoCapture(4)
    cap3 = cv2.VideoCapture(6)
    cap4 = cv2.VideoCapture(8)
    cap1.set(3, 5000)
    cap1.set(4, 5000)
    size1 = (int(cap1.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(cap1.get(cv2.CAP_PROP_FRAME_WIDTH)))  # 获得原始分辨率
    cap2.set(3, 5000)
    cap2.set(4, 5000)
    size2 = (int(cap2.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(cap2.get(cv2.CAP_PROP_FRAME_WIDTH)))  # 获得原始分辨率
    cap3.set(3, 5000)
    cap3.set(4, 5000)
    size3 = (int(cap3.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(cap3.get(cv2.CAP_PROP_FRAME_WIDTH)))  # 获得原始分辨率
    cap4.set(3, 5000)
    cap4.set(4, 5000)
    size4 = (int(cap4.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(cap4.get(cv2.CAP_PROP_FRAME_WIDTH)))  # 获得原始分辨率
    fourcc1 = cv2.VideoWriter_fourcc('I','4','2','0')
    fourcc2 = cv2.VideoWriter_fourcc('I','4','2','0')
    fourcc3 = cv2.VideoWriter_fourcc('I','4','2','0')
    fourcc4 = cv2.VideoWriter_fourcc('I','4','2','0')
    out1 = cv2.VideoWriter('pano1/video1.avi', fourcc1, 20, size1)
    out2 = cv2.VideoWriter('pano1/video2.avi', fourcc2, 20, size2)
    out3 = cv2.VideoWriter('pano1/video3.avi', fourcc3, 20, size3)
    out4 = cv2.VideoWriter('pano1/video4.avi', fourcc4, 20, size4)
    


    while cap1.isOpened() and cap2.isOpened() and cap3.isOpened() and cap4.isOpened():
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()
        ret3, frame3 = cap3.read()
        ret4, frame4 = cap4.read()
        if ret1 == True and ret2 == True and ret3 == True and ret4 == True:
            out1.write(frame1)
            out2.write(frame2)
            out3.write(frame3)
            out4.write(frame4)
            cv2.imshow('video1', frame1)
            cv2.imshow('video2', frame2)
            cv2.imshow('video3', frame3)
            cv2.imshow('video4', frame4)
        else:
            break
        if cv2.waitKey(40) == ord('q'):
            break

'''

cap1 = cv2.VideoCapture(2)

fourcc1 = cv2.VideoWriter_fourcc('I','4','2','0')
out1 = cv2.VideoWriter('pano/video1.avi', fourcc1, 20, (640, 480))
while cap1.isOpened():
     ret1, frame1 = cap1.read()
     if ret1 == True:
         out1.write(frame1)
         cv2.imshow('video1', frame1)
         print(frame1.shape)
     else:
         break
     if cv2.waitKey(1) == ord('q'):
         break
'''
