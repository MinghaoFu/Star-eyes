import cv2
import numpy as np

'''
if __name__ == "__main__":
    cap1 = cv2.VideoCapture(2)
    fourcc1 = cv2.VideoWriter_fourcc('I','4','2','0')
    out1 = cv2.VideoWriter('pano/videoC2.avi', fourcc1, 20, (1280, 720))
    while cap1.isOpened():
        ret1, frame1 = cap1.read()
        if ret1 == True:
            out1.write(frame1)
            cv2.imshow('videoA', frame1)
        else:
            break
        if cv2.waitKey(40) == ord('q'):
            break
'''


cap1 = cv2.VideoCapture(0)
fourcc1 = cv2.VideoWriter_fourcc('I','4','2','0')
out1 = cv2.VideoWriter('pano/video.avi', fourcc1, 20, (1280, 720))

cap1.set(3,5000)
cap1.set(4,5000)
size = (int(cap1.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(cap1.get(cv2.CAP_PROP_FRAME_WIDTH))) # 获得原始分辨率


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

