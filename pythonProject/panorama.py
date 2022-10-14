import cv2
import numpy as np
import cam_info as cf
import undistort as ud
import dead_zone as dz
import sys

def perspective_transformation_img(img,pts1,pts2):
    M = cv2.getPerspectiveTransform(pts1,pts2)
    dst = cv2.warpPerspective(img,M,(cf.panoImg[0],cf.panoImg[1]))
    return dst

# img = cv2.imread("image/39.jpg")
# cv2.imshow("100",img)
# cv2.waitKey(0)
# sys.exit()


#Get image's homography to bird-image by chessboard
def getWarp(img,corners1,corners2):
    H,_ = cv2.findHomography(corners1,corners2)
    img_warp = cv2.warpPerspective(img,H,(cf.width,cf.height))
    return img_warp

def combination(img1,img2,img3,img4):
    dst1 = perspective_transformation_img(ud.initUndistAndRemap(img1, cf.cameraMatrix, cf.disCoeffs), cf.f_pts1,
                                          cf.f_pts2)
    dst2 = perspective_transformation_img(ud.initUndistAndRemap(img2, cf.cameraMatrix, cf.disCoeffs), cf.r_pts1,
                                          cf.r_pts2)
    dst3 = perspective_transformation_img(ud.initUndistAndRemap(img3, cf.cameraMatrix, cf.disCoeffs), cf.b_pts1,
                                          cf.b_pts2)
    dst4 = perspective_transformation_img(ud.initUndistAndRemap(img4, cf.cameraMatrix, cf.disCoeffs), cf.l_pts1,
                                          cf.l_pts2)

    c = np.zeros_like(dst1)
    for i in range(cf.height):
        for j in range(cf.width):
            if not np.array_equal(dst1[i,j],np.array([0,0,0])):
                c[i][j] = dst1[i][j]
            elif not np.array_equal(dst1[i,j],np.array([0,0,0])):
                c[i][j] = dst1[i][j]*0.5 + dst2[i][j]*0.5
            elif not np.array_equal(dst2[i,j],np.array([0,0,0])):
                c[i][j] = dst2[i][j]
            elif not np.array_equal(dst3[i, j], np.array([0, 0, 0])):
                c[i][j] = dst3[i][j]
            else:
                c[i][j] = dst4[i][j]

    return c

def pano(img1,img2,img3,img4,car):

    #cv2.imshow("1",getWarp(img1,cf.f_corners1,cf.f_corners2))
    # front = ud.initUndistAndRemap(img1, cameraMatrix=cf.cameraMatrix, disCoeffs=cf.disCoeffs)
    # cv2.imshow("f",front)
    # left = ud.initUndistAndRemap(img4, cameraMatrix=cf.cameraMatrix, disCoeffs=cf.disCoeffs)
    # cv2.imshow("l", left)
    # right = ud.initUndistAndRemap(img2, cameraMatrix=cf.cameraMatrix, disCoeffs=cf.disCoeffs)
    # cv2.imshow("r", right)
    # back = ud.initUndistAndRemap(img3, cameraMatrix=cf.cameraMatrix, disCoeffs=cf.disCoeffs)
    # cv2.imshow("b", back)

    front = perspective_transformation_img(ud.initUndistAndRemap
                                                   (img1,cameraMatrix=cf.cameraMatrix,disCoeffs=cf.disCoeffs),
                                                   cf.f_pts1,cf.f_pts2)
    left = perspective_transformation_img(ud.initUndistAndRemap
                                                   (img4,cameraMatrix=cf.cameraMatrix,disCoeffs=cf.disCoeffs),
                                                   cf.l_pts1,cf.l_pts2)
    right = perspective_transformation_img(ud.initUndistAndRemap
                                                   (img2,cameraMatrix=cf.cameraMatrix,disCoeffs=cf.disCoeffs),
                                                   cf.r_pts1,cf.r_pts2)
    back = perspective_transformation_img(ud.initUndistAndRemap
                                                   (img3, cameraMatrix=cf.cameraMatrix, disCoeffs=cf.disCoeffs),
                                                   cf.b_pts1, cf.b_pts2)
    c1 = cv2.addWeighted(front,1,right,1,0)
    c2 = cv2.addWeighted(back,1,left,1,0)
    c3 = cv2.addWeighted(c1,1,c2,1,0)
    c4 = cv2.resize(c3,(480,720))
    roi = c4[108:608,93:393]
    dst = cv2.addWeighted(roi,1,car,1,0)
    c4[108:608,93:393] = dst
    return c4


if __name__ == "__main__":
    cap1 = cv2.VideoCapture(2)
    cap2 = cv2.VideoCapture(6)
    cap3 = cv2.VideoCapture(8)
    cap4 = cv2.VideoCapture(4)
    
    cap1.set(3,5000) # 设置一个比较大的分辨率值，如5000
    cap1.set(4,5000)
    size = (int(cap1.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(cap1.get(cv2.CAP_PROP_FRAME_WIDTH))) # 获得原始分辨率
    cap2.set(3,5000) # 设置一个比较大的分辨率值，如5000
    cap2.set(4,5000)
    size = (int(cap2.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(cap2.get(cv2.CAP_PROP_FRAME_WIDTH))) # 获得原始分辨率
    cap3.set(3,5000) # 设置一个比较大的分辨率值，如5000
    cap3.set(4,5000)
    size = (int(cap3.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(cap3.get(cv2.CAP_PROP_FRAME_WIDTH))) # 获得原始分辨率
    cap4.set(3,5000) # 设置一个比较大的分辨率值，如5000
    cap4.set(4,5000)
    size = (int(cap4.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(cap4.get(cv2.CAP_PROP_FRAME_WIDTH))) # 获得原始分辨率
    car = cv2.imread("image/car2.jpg")

    cv2.namedWindow("0",cv2.WINDOW_NORMAL)
    fourcc = cv2.VideoWriter_fourcc('I', '4', '2', '0')
    out = cv2.VideoWriter("video/pano.avi", cv2.VideoWriter_fourcc('I','4','2','0'), 5, (480, 720))

    while cap1.isOpened() and cap2.isOpened() and cap3.isOpened() and cap4.isOpened():
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()
        ret3, frame3 = cap3.read()
        ret4, frame4 = cap4.read()
        pano1 = pano(frame1, frame2, frame3, frame4, car)
        out.write(pano1)
        cv2.imshow("0",pano1)

        if cv2.waitKey(200) == ord('q'):
            cv2.destroyAllWindows()
            break
