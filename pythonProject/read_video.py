import cv2
import numpy as np

# if __name__ == "__main__":
#     cap1 = cv2.VideoCapture(1)
#     cap2 = cv2.VideoCapture(2)
#     cap3 = cv2.VideoCapture(3)
#     cap4 = cv2.VideoCapture(4)
#     fourcc1 = cv2.VideoWriter_fourcc('I','4','2','0')
#     fourcc2 = cv2.VideoWriter_fourcc('I','4','2','0')
#     fourcc3 = cv2.VideoWriter_fourcc('I','4','2','0')
#     fourcc4 = cv2.VideoWriter_fourcc('I','4','2','0')
#     out1 = cv2.VideoWriter('pano/video1.avi', fourcc1, 20, (1080,720))
#     out2 = cv2.VideoWriter('pano/video2.avi', fourcc2, 20, (1080,720))
#     out3 = cv2.VideoWriter('pano/video3.avi', fourcc3, 20, (1080,720))
#     out4 = cv2.VideoWriter('pano/video4.avi', fourcc4, 20, (1080,720))
#     while cap1.isOpened() and cap2.isOpened() and cap3.isOpened() and cap4.isOpened():
#         ret1, frame1 = cap1.read()
#         ret2, frame2 = cap2.read()
#         ret3, frame3 = cap3.read()
#         ret4, frame4 = cap4.read()
#         if ret1 == True and ret2 == True and ret3 == True and ret4 == True:
#             out1.write(frame1)
#             out2.write(frame2)
#             out3.write(frame3)
#             out4.write(frame4)
#             cv2.imshow('video1', frame1)
#             cv2.imshow('video2', frame2)
#             cv2.imshow('video3', frame3)
#             cv2.imshow('video4', frame4)
#         else:
#             break
#         if cv2.waitKey(40) == ord('q'):
#             break



    # cap1 = cv2.VideoCapture(0)
    # fourcc1 = cv2.VideoWriter_fourcc('I','4','2','0')
    # out1 = cv2.VideoWriter('pano/video1.avi', fourcc1, 20, (1080,720))
    # while cap1.isOpened():
    #     ret1, frame1 = cap1.read()
    #     if ret1 == True:
    #         out1.write(frame1)
    #         cv2.imshow('video1', frame1)
    #     else:
    #         break
    #     if cv2.waitKey(1) == ord('q'):
    #         break
if __name__ == "__main__":
    cv2.namedWindow('video',cv2.WINDOW_NORMAL)
    CAPTURE = cv2.VideoCapture('video/video1.avi')
    while CAPTURE.isOpened():
        ret, frame = CAPTURE.read()
        cv2.imshow('video', frame)
        if cv2.waitKey(50) == ord('q'):
            cv2.destroyAllWindows()
            break
