import cv2
import numpy as np
import math
import cam_info as cf

poly_pts = cf.maskpoints1
Ytop = poly_pts[0][0][1]
Ybottom = poly_pts[0][2][1]
poly_pts_in = np.array([[[870, Ytop], [944, Ytop], [1153, Ybottom], [615, Ybottom]]])

def get_edge_img(color_img, gaussian_ksize=5, gaussian_sigmax=1,canny_threshold1=50, canny_threshold2=100):
    gaussian = cv2.GaussianBlur(color_img, (gaussian_ksize, gaussian_ksize),
                                gaussian_sigmax)
    gray_img = cv2.cvtColor(gaussian, cv2.COLOR_BGR2GRAY)
    edges_img = cv2.Canny(gray_img, canny_threshold1, canny_threshold2)
    return edges_img


def roi_mask(gray_img):
    mask = np.zeros_like(gray_img)
    mask = cv2.fillPoly(mask, pts=poly_pts, color=255)
    mask = cv2.fillPoly(mask, pts=poly_pts_in, color=0)
    img_mask = cv2.bitwise_and(gray_img, mask)
    cv2.namedWindow('1',cv2.WINDOW_NORMAL)
    cv2.imshow('1',img_mask)
    return img_mask

def get_lines(edge_img):
    #calculate slope
    def calculate_slope(line):
        x_1, y_1, x_2, y_2 = line[0]
        return (y_2 - y_1) / (x_2 - x_1)

    #filtrate outlier
    def reject_abnormal_lines(lines, threshold=0.2):
        slopes = [calculate_slope(line) for line in lines]
        while len(lines) > 0:
            mean = np.mean(slopes)
            diff = [abs(s - mean) for s in slopes]
            idx = np.argmax(diff)
            if diff[idx] > threshold:
                slopes.pop(idx)
                lines.pop(idx)
            else:
                break
        return lines

    #generate one line
    def least_squares_fit(lines):
        x_coords = np.ravel([[line[0][0], line[0][2]] for line in lines])
        y_coords = np.ravel([[line[0][1], line[0][3]] for line in lines])
        poly = np.polyfit(x_coords, y_coords, deg=1)
        point_min = (np.min(x_coords), np.polyval(poly, np.min(x_coords)))
        point_max = (np.max(x_coords), np.polyval(poly, np.max(x_coords)))
        return np.array([point_min, point_max], dtype=np.int)

    #Houghline detect
    lines = cv2.HoughLinesP(edge_img, 1, np.pi / 180, 15, minLineLength=10,
                            maxLineGap=30)
    #divide into left and right line
    left_lines = [line for line in lines if calculate_slope(line) < 0]
    right_lines = [line for line in lines if calculate_slope(line) > 0]
    #filtrate
    left_lines = reject_abnormal_lines(left_lines)
    right_lines = reject_abnormal_lines(right_lines)

    return least_squares_fit(left_lines), least_squares_fit(right_lines)

def draw_dotted_line(img,point0,point1,n):
    X = (point0[0] - point1[0])/n
    Y = (point1[1] - point0[1])/n
    i = 0
    while i < n:
        x1 = point0[0] - i*X
        y1 = point0[1] + i*Y
        i += 1
        x2 = point0[0] - i*X
        y2 = point0[1] + i*Y
        cv2.line(img,(int(x1),int(y1)),(int(x2),int(y2)),color=(0,255,255),thickness=2)
        i += 1

def draw_lines(img, lines):
    left_line, right_line = lines

    #get slope,point to draw lines
    #left
    lk = (left_line[0][1] - left_line[1][1]) / (left_line[0][0] - left_line[1][0])
    lx1 = (Ytop - left_line[0][1]) / lk + left_line[0][0]
    lx2 = (Ybottom - left_line[0][1]) / lk + left_line[0][0]
    ll = math.pow((left_line[0][1] - left_line[1][1]),2) + math.pow((left_line[0][0] - left_line[1][0]),2)
    print(ll)
    #cv2.line(img, tuple(left_line[0]), tuple(left_line[1]), color=(0, 255, 255),thickness=2)
    if ll > 90000:#detect dotted_line by length
        cv2.line(img, (int(lx1), Ytop), (int(lx2), Ybottom), color=(0, 255, 255), thickness=2)
    else:
        draw_dotted_line(img,(int(lx1), Ytop),(int(lx2), Ybottom),8)

    #right
    rk = (right_line[0][1] - right_line[1][1]) / (right_line[0][0] - right_line[1][0])
    rx1 = (Ytop - right_line[0][1]) / rk + right_line[0][0]
    rx2 = (Ybottom - right_line[0][1]) / rk + right_line[0][0]
    rl = math.pow((right_line[0][1] - right_line[1][1]), 2) + math.pow((right_line[0][0] - right_line[1][0]), 2)
    print(rl)
    #cv2.line(img, tuple(right_line[0]), tuple(right_line[1]), color=(0, 255, 255), thickness=2)
    if rl > 90000:
        cv2.line(img, (int(rx1), Ytop), (int(rx2), Ybottom), color=(0, 255, 255), thickness=2)
    else:
        draw_dotted_line(img, (int(rx1), Ytop), (int(rx2), Ybottom),8)

    #Write line points
    fo = open(f"./from_yolo.txt","a+")
    fo.write(f"{int((lx2+lx1)/2)} {int((Ytop+Ybottom)/2)}\n") #left middle point
    fo.write(f"{int((rx2+rx1)/2)} {int((Ytop+Ybottom)/2)}\n") #right middle point
    fo.close()

    #draw poly
    pts = np.array([[int(lx1),Ytop],[int(rx1),Ytop],[int(rx2),Ybottom],[int(lx2),Ybottom]],np.int32)
    mask = np.zeros_like(img)
    mask = cv2.fillPoly(mask, pts=[pts], color=(0,255,255))
    cv2.addWeighted(img,1,mask,0.3,0,img)

def show_lane(color_img):
    #draw lines in image
    edge_img = get_edge_img(color_img)
    mask_gray_img = roi_mask(edge_img)
    lines = get_lines(mask_gray_img)
    draw_lines(color_img, lines)


if __name__ == '__main__':
    #example
    cv2.namedWindow('video', cv2.WINDOW_NORMAL)
    CAPTURE = cv2.VideoCapture('video/2.mp4')
    fourcc = cv2.VideoWriter_fourcc('I','4','2','0')
    out = cv2.VideoWriter('video/draw_lane.avi',fourcc,5,(1920,1080))
    while CAPTURE.isOpened():
        ret, frame = CAPTURE.read()
        show_lane(frame)
        cv2.imshow('video', frame)
        out.write(frame)

        if cv2.waitKey(400) == ord('q'):
            cv2.destroyAllWindows()
            break
