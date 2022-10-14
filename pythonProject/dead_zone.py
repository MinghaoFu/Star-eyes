import cv2
import cam_info
import numpy as np
import undistort as ud
import cam_info as cf

def stitch(img1,img2):
    mode = cv2.Stitcher_PANORAMA
    stitcher = cv2.Stitcher_create(mode)
    (_result, pano) = stitcher.stitch((img1,img2))
    return pano

def draw_warn(img):
    pass

def recognize_person(img,y):
    if y > cam_info.width * 0.8:
        draw_warn(img)

def match_min(matches,good_match):
    # calculate max and min distance
    min_distance = 10000
    max_distance = 0
    for x in matches:
        if x.distance < min_distance:
            min_distance = x.distance
        elif x.distance > max_distance:
            max_distance = x.distance
    #print('max_distance:', max_distance, ' min_distance:', min_distance)
    for x in matches:
        if x.distance <= max(2*min_distance,20):
            good_match.append(x)


def orb_features(img1,img2):

    #initialize ORB
    orb = cv2.ORB_create()

    #find keypoints
    keypoints1 = orb.detect(img1)
    keypoints2 = orb.detect(img2)

    #calculate description
    keypoints1, descriptions1 = orb.compute(img1,keypoints1)
    keypoints2, descriptions2 = orb.compute(img2,keypoints2)

    #initialize BFMatcher
    matcher = cv2.BFMatcher(cv2.NORM_HAMMING)

    #description match
    matches = matcher.match(descriptions1,descriptions2)

    #get good_matches
    good_matches = []
    match_min(matches,good_matches)
    print('matches_size:',len(matches), ' good_mathces_size:',len(good_matches))

    #draw matches
    outimg = cv2.drawMatches(img1,keypoints1,img2,keypoints2,good_matches,outImg=None)
    cv2.imshow('3',outimg)

    #use RANSAC to screen result

def draw_backup_line(img):
    cv2.line(img,(200,720),(450,360),color=(255,255,0),thickness=5)
    cv2.line(img,(880,720),(630,360),color=(255,255,0),thickness=5)

if __name__ == "__main__":
    # cap1 = cv2.VideoCapture('pinjie1.mov')
    # cap2 = cv2.VideoCapture('pinjie2.mov')
    # while cap1.isOpened() and cap2.isOpened():
    #     ret1, frame1= cap1.read()
    #     ret2, frame2= cap2.read()
    #     # orb_features(ud.initUndistAndRemap(frame1, cf.cameraMatrix, cf.disCoeffs),
    #     #              ud.initUndistAndRemap(frame2, cf.cameraMatrix, cf.disCoeffs))
    #     orb_features(frame1,frame2)
    #
    #     cv2.waitKey(10)
    #     if cv2.waitKey(1) == ord('q'):
    #         cv2.destroyAllWindows()
    #         break
    cv2.namedWindow('video', cv2.WINDOW_NORMAL)
    CAPTURE = cv2.VideoCapture(8)
    
    CAPTURE.set(3,5000) # 设置一个比较大的分辨率值，如5000
    CAPTURE.set(4,5000)
    
    
    fourcc = cv2.VideoWriter_fourcc('I', '4', '2', '0')
    out = cv2.VideoWriter("video/dead_zone.avi", cv2.VideoWriter_fourcc('I','4','2','0'), 5, (1280, 720))
    while CAPTURE.isOpened():
        ret, frame = CAPTURE.read()
        dst = ud.initUndistAndRemap(frame,cameraMatrix=cf.cameraMatrix,disCoeffs=cf.disCoeffs)
        # left and right line
        cv2.line(dst,(130,720),(490,150),(0,255,0),thickness=5)
        cv2.line(dst,(1150,720),(790,150),(0,255,0),thickness=5)
        # 50cm
        cv2.line(dst,(200,610),(250,610),(0,255,0),thickness=5)
        cv2.line(dst,(1080,610),(1030,610),(0,255,0),thickness=5)
        # 100cm
        cv2.line(dst,(320,420),(370,420),(0,255,0),thickness=5)
        cv2.line(dst,(960,420),(910,420),(0,255,0),thickness=5)
        # 150cm
        cv2.line(dst,(390,310),(440,310),(0,255,0),thickness=5)
        cv2.line(dst,(890,310),(840,310),(0,255,0),thickness=5)
        # 200cm
        cv2.line(dst,(432,240),(482,240),(0,255,0),thickness=5)
        cv2.line(dst,(798,240),(848,240),(0,255,0),thickness=5)
        # 250cm
        cv2.line(dst,(465,190),(515,190),(0,255,0),thickness=5)
        cv2.line(dst,(765,190),(815,190),(0,255,0),thickness=5)
        # 300cm
        cv2.line(dst,(490,150),(540,150),(0,255,0),thickness=5)
        cv2.line(dst,(790,150),(740,150),(0,255,0),thickness=5)
        out.write(dst)
        cv2.imshow('video', dst)
        if cv2.waitKey(40) == ord('q'):
            cv2.destroyAllWindows()
            break
