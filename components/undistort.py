import cv2
import numpy as np
import cam_info as cf

def initUndistAndRemap(img,cameraMatrix, disCoeffs):

    undist_img = cv2.undistort(img,cameraMatrix,disCoeffs)
    return undist_img
