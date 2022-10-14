import numpy as np
import cv2
import os
import time
import dead_zone as dz

from lane_detect import show_lane
from dead_zone import stitch
from detect import detect

if __name__ == "__main__":
    cv2.namedWindow('video',cv2.WINDOW_NORMAL)
    CAPTURE = cv2.VideoCapture('3.mp4')
    while CAPTURE.isOpened():
        ret, frame = CAPTURE.read()
        show_lane(frame)
        dz.draw_backup_line(frame)
        cv2.imshow('video', frame)
        if cv2.waitKey(50) == ord('q'):
            cv2.destroyAllWindows()
            break
