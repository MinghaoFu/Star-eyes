import cv2
import numpy as np

if __name__ == "__main__":
    cv2.namedWindow('video', cv2.WINDOW_NORMAL)
    CAPTURE = cv2.VideoCapture('video/dianke.mp4')
    while CAPTURE.isOpened():
        ret, frame = CAPTURE.read()
        cv2.imshow('video', frame)

        if cv2.waitKey(500) == ord('q'):
            cv2.destroyAllWindows()
            break