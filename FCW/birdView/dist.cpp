#include <iostream>
#include <opencv2/opencv.hpp>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/imgcodecs/imgcodecs.hpp>
#include <opencv2/imgproc/imgproc_c.h>
#include <fstream>  
#include <stdio.h>
#include <string>
#include <math.h>

using namespace cv;
using namespace std;

int numOfStream;

#define OFFSET_Y 338.073
#define OFFSET_X 58
#define LperP_Y 1.524
#define LperP_X 0.836

string input_image;
constexpr auto pi = 3.1415;
Point2f vp;
//相机参数值：
/*
[874.1474587484332, 0, 960.8640194972594;
 0, 995.1257922739674, 536.7531349377706;
 0, 0, 1]
*/
/*[959.3372971768842, 0, 966.9040371587082;
0, 964.9893800310733, 514.4411457967556;
0, 0, 1]*/
struct camera_information {
    float   focalLengthX = 959;
    float   focalLengthY = 964;
    float   opticalCenterX = 966;
    float   opticalCenterY = 514;
    float   pitch = -12.5;
    float   yaw = 0;
    float   width = 1920;
    float   height = 1080;
    float   cam_height = 1210;
}cam_info;

//鸟瞰图数值
struct ipm_info {
   float ipmwidth = 1920;
   float ipmheight = 1080;
   float ipmleft = 320;
   float ipmright = 1600;
   float ipmtop = 790;
   float ipmbottom = 1000;
   float ipmInterpolation = 0;
   float ipmVpPortion = 0;
}ipi;

float uvLimitsp[2][4] = {0};  //选取像素图像中感兴趣区域的4个点坐标
float xyLimts[2][4] = {0};    //与之对应的在世界坐标下的4个点坐标，其Z坐标均为0
Mat outimage = Mat::zeros(Size(ipi.ipmwidth, ipi.ipmheight), CV_32FC1);
//计算消失点
Point2f detvanPoint() {
    //根据参数获取消失点的世界坐标：
    float vpp_info[3][1] = { sin(cam_info.yaw * pi / 180) / cos(cam_info.pitch * pi / 180),
                    cos(cam_info.yaw * pi / 180) / cos(cam_info.pitch * pi / 180),
                    0 };
    //cout << vpp_info[3][3] << endl;
    Mat vpp = Mat(Size(1, 3), CV_32FC1, vpp_info);
    //偏航角旋转
    float yaw_info[3][3] = { cos(cam_info.yaw * pi / 180), -sin(cam_info.yaw * pi / 180) , 0,
                            sin(cam_info.yaw * pi / 180),  cos(cam_info.yaw * pi / 180), 0,
                            0, 0, 1 };
    Mat tyaw = Mat(Size(3, 3), CV_32FC1, yaw_info);
    //俯仰角旋转
    float pitch_info[3][3] = { 1, 0, 0,
                               0, -sin(cam_info.pitch * pi / 180),-cos(cam_info.pitch * pi / 180) ,
                               0, cos(cam_info.pitch * pi / 180) ,-sin(cam_info.pitch * pi / 180)};
    Mat tpitch = Mat(Size(3, 3), CV_32FC1, pitch_info);

    cout << tpitch.at<float>(0, 2) << endl;
    cout << tpitch.at<float>(0, 0) << endl;
    Mat transform = tyaw * tpitch;//这里还差一步，去除以其Z坐标然后再进转换
    //Mat zpp = transform * vpp;
    //cout << zpp.cols << endl;
    //cout << zpp.rows << endl;
    //zpp.at<float>(0, 0) = zpp.at<float>(0, 0) / zpp.at<float>(2, 0);
    //zpp.at<float>(1, 0) = zpp.at<float>(1, 0) / zpp.at<float>(2, 0);
    //相机内参矩阵
    float inpar_info[3][3] = { cam_info.focalLengthX, 0, cam_info.opticalCenterX,
                              0, cam_info.focalLengthY, cam_info.opticalCenterY,
                              0, 0, 1 };
    Mat inpar = Mat(Size(3 , 3), CV_32FC1, inpar_info);

    transform = inpar * transform;
    //获取的3行1列的关于消失点在像素中的坐标
    Mat vp_info = transform * vpp;
    
    cout << "vp_info 列: " << vp_info.cols << endl;
    cout << "vp_info 行：" << vp_info.rows << endl;

    vp.x = vp_info.at<float>(0 , 0);
    vp.y = vp_info.at<float>(1 , 0);
    
    //Mat input_image1 = imread("../../Images/" + input_image);
    Mat input_image1 = imread("./Images/"+to_string(numOfStream)+".jpg");
    circle(input_image1,vp,5,Scalar(0,255,255),4);
    imwrite("./Images/vp_"+to_string(numOfStream)+".jpg", input_image1);
    
    return vp;
}

//根据消失点选取的在像素中的4个坐标，计算其在世界坐标系下的坐标

void uv2xy() {
    // 根据消失点来选取像素中感兴趣的坐标；
    Point2f vp = detvanPoint();
    cout << "vp.x: "<<  vp.x << endl;
    cout << "vp.y: " << vp.y << endl;
    
    uvLimitsp[0][0] = vp.x;
    uvLimitsp[0][1] = ipi.ipmright;
    uvLimitsp[0][2] = ipi.ipmleft;
    uvLimitsp[0][3] = vp.x;
    uvLimitsp[1][0] = ipi.ipmtop;
    uvLimitsp[1][1] = ipi.ipmtop;
    uvLimitsp[1][2] = ipi.ipmtop;
    uvLimitsp[1][3] = ipi.ipmbottom;
    
    float uvLimitsp_s[3][4] = { vp.x, ipi.ipmright, ipi.ipmleft, vp.x,
                ipi.ipmtop, ipi.ipmtop, ipi.ipmtop, ipi.ipmbottom ,
                1, 1, 1, 1};
    Mat uvL = Mat(Size(4, 3), CV_32FC1, uvLimitsp_s);
    float c1 = cos(cam_info.pitch * pi / 180);
    float s1 = sin(cam_info.pitch * pi / 180);
    float c2 = cos(cam_info.yaw * pi / 180);
    float s2 = sin(cam_info.yaw * pi / 180);

    //逆透视变换矩阵
    float matp_info[4][3] = { -cam_info.cam_height * c2 / cam_info.focalLengthX,
                             cam_info.cam_height* s1 * s2 / cam_info.focalLengthY,
                             (cam_info.cam_height * c2 * cam_info.opticalCenterX / cam_info.focalLengthX) - (cam_info.cam_height * s1 * s2 * cam_info.opticalCenterY / cam_info.focalLengthY) - cam_info.cam_height * c1 * s2,
                             cam_info.cam_height* s2 / cam_info.focalLengthX,
                             cam_info.cam_height* s1 * c2 / cam_info.focalLengthY,
                             (-cam_info.cam_height * s2 * cam_info.opticalCenterX / cam_info.focalLengthX) - (cam_info.cam_height * s1 * c2 * cam_info.opticalCenterY / cam_info.focalLengthY) - cam_info.cam_height * c1 * c2,
                             0,
                             cam_info.cam_height* c1 / cam_info.focalLengthY,
                             (-cam_info.cam_height * c1 * cam_info.opticalCenterY / cam_info.focalLengthY) + cam_info.cam_height * s1,
                             0,
                             -c1 / cam_info.focalLengthY,
                             (c1 * cam_info.opticalCenterY / cam_info.focalLengthY) - s1
    };

    Mat matp = Mat(Size(3, 4), CV_32FC1, matp_info);
    Mat points4 = matp * uvL;
    //float xyLimts[3][4] = {0};
    for (int i = 0; i < 4; i++) {

        //points4.at<float>(i, 0) = points4.at<float>(i, 0) / points4.at<float>(i, 3);
        xyLimts[0][i] = points4.at<float>(0, i) / points4.at<float>(3, i);
        
        //points4.at<float>(i, 1) = points4.at<float>(i, 1) / points4.at<float>(i, 3);
        xyLimts[1][i] = points4.at<float>(1, i) / points4.at<float>(3, i);
        //xyLimts[2][i] = 0;
    }
    
}
/**********************************************************************************
    此函数是根据uv2xy()所选择的坐标，在world cordinate系中的范围，来确定鸟瞰图的投影
    映射范围。


**********************************************************************************/
Mat out() {

    int u = cam_info.height;
    int v = cam_info.width;
    int i,j;

    //获取根据消失点选择出来的世界坐标系下的范围
    uv2xy();

    Mat row1 = Mat(Size(4, 1), CV_32FC1);
    Mat row2 = Mat(Size(4, 1), CV_32FC1);
    float  xfmin, xfmax, yfmin, yfmax;
    xfmin = xyLimts[0][0];
    xfmax = xyLimts[0][0];
    yfmin = xyLimts[1][0];
    yfmax = xyLimts[1][0];
    for (i = 0; i < 4; i++) {
        row1.at<float>(0, i) = xyLimts[0][i];
        if (row1.at<float>(0, i) < xfmin) xfmin = row1.at<float>(0, i);
        if (row1.at<float>(0, i) > xfmax) xfmax = row1.at<float>(0, i);
        row2.at<float>(0, i) = xyLimts[1][i];
        if (row2.at<float>(0, i) < yfmin) yfmin = row2.at<float>(0, i);
        if (row2.at<float>(0, i) > yfmax) yfmax = row2.at<float>(0, i);
    }
    int outRow = outimage.rows;
    int outCol = outimage.cols;
    float stepRow = (yfmax - yfmin) / outRow;
    float stepCol = (xfmax - xfmin) / outCol;

    Mat xyGrid = Mat::zeros(Size(outRow * outCol, 2), CV_32FC1);//初始化赋值为0
    Mat inPoints3 = Mat::ones(Size(outRow * outCol, 3), CV_32FC1);//初始化赋值为1；
    float y, x;
    y = yfmax - 0.5 * stepRow;

    for (i = 1; i < outRow+1; i++) {
        x = xfmin + 0.5 * stepCol;
        for (j = 0; j < outCol; j++) {
            xyGrid.at<float>(0, (i - 1) * outCol + j) = x;
            xyGrid.at<float>(1, (i - 1) * outCol + j) = y;
            inPoints3.at<float>(0, (i - 1) * outCol + j) = x;
            inPoints3.at<float>(1, (i - 1) * outCol + j) = y;
            inPoints3.at<float>(2, (i - 1) * outCol + j) = inPoints3.at<float>(2, (i - 1) * outCol + j)*(-cam_info.cam_height);
            x += stepCol;
        }
        y -= stepRow;
    }

    float c1 = cos(cam_info.pitch * pi / 180);
    float s1 = sin(cam_info.pitch * pi / 180);
    float c2 = cos(cam_info.yaw * pi / 180);
    float s2 = sin(cam_info.yaw * pi / 180);

    float matp_info[3][3] = {
                        cam_info.focalLengthX * c2 + c1 * s2 * cam_info.opticalCenterX,
                        cam_info.focalLengthX * s2 + c1 * c2 * cam_info.opticalCenterX,
                        -s1 * cam_info.opticalCenterX,
                        s2* (-cam_info.focalLengthY * s1 + c1 * cam_info.opticalCenterY),
                        c2* (-cam_info.focalLengthY * s1 + c1 * cam_info.opticalCenterY),
                        - cam_info.focalLengthY * c1 - s1 * cam_info.opticalCenterY,
                        c1* s2, c1* c2, -s1 
                        };
    Mat matp = Mat(Size(3, 3), CV_32FC1, matp_info);
    Mat uvGrid = Mat(Size(outRow * outCol, 2), CV_32FC1);

    inPoints3 = matp * inPoints3;
    for (i = 0; i < outRow * outCol; i++) {
        uvGrid.at<float>(0, i) = inPoints3.at<float>(0, i) / inPoints3.at<float>(2, i);
        uvGrid.at<float>(1, i) = inPoints3.at<float>(1, i) / inPoints3.at<float>(2, i);
    }
    return uvGrid;
}

int main()
{
       ifstream infile;
       ofstream outfile;
       infile.open("./share/from_yolo.txt");
       
       ifstream index_file;
       index_file.open("./share/index.txt");
       index_file >> numOfStream;
       index_file.close();

       int i, j;
       float  mean = 0 ,sum = 0;
       int outRow = 1080;//后面需要换掉
       int outCol = 1920;//

       //cin>>input_image;
       //Mat imageinput = imread("../../Images/" + input_image);//读取图片路径
       Mat imageinput = imread("./Images/"+to_string(numOfStream)+".jpg");//读取图片路径
       cout << "read image successfully." << endl;

       IplImage pSrcImage_info = cvIplImage(imageinput);
       IplImage* pSrcImage = &pSrcImage_info;
       IplImage* pR_Plane = cvCreateImage(cvGetSize(pSrcImage), IPL_DEPTH_8U, 1);
       IplImage* pG_Plane = cvCloneImage(pR_Plane);
       IplImage* pB_Plane = cvCloneImage(pR_Plane);
       cvSplit(pSrcImage, pB_Plane, pG_Plane, pR_Plane, NULL);

       Mat R = cvarrToMat(pR_Plane, true);
       Mat RR = Mat(Size(R.cols, R.rows), CV_32FC1);

       cout << R.cols << " " << R.rows << endl;
       for (i = 0; i < R.rows; i++) {
           for (j = 0; j < R.cols; j++) {
               sum += R.at<unsigned char>(i, j);
               RR.at<float>(i, j) = (float)R.at<unsigned char>(i, j) / 255;
           }
       }
       mean = sum / (R.rows * R.cols);

       float ui, vi, x, y, val;
       int x1, x2, y1, y2;
       // cout << mean << endl;
       Mat uvGrid = out();
       cout << uvGrid.rows << endl;
       cout << uvGrid.cols << endl;

       int ox,oy;
       int object_id;
       string label;
       outfile.open("./share/dist-from_yolo"+to_string(numOfStream)+".txt");
       outfile << numOfStream << endl;
       while(infile >> label)
       {
           int flag=0;
           infile >> object_id;
           infile >> ox >> oy;
           for (i = 1; i < outRow+1; i++) {
               for (j = 0; j < outCol; j++) {
                   ui = uvGrid.at<float>(0, (i - 1) * outCol + j);
                   vi = uvGrid.at<float>(1, (i - 1) * outCol + j);
                   if (ui<ipi.ipmleft || ui>ipi.ipmright || vi<ipi.ipmtop || vi>ipi.ipmbottom)
                       outimage.at<float>(i-1, j) = mean;
                   else {
                       x1 = int(ui); x2 = int(ui + 1);
                       y1 = int(vi); y2 = int(vi + 1);
                       x = ui - double(x1); y = vi - double(y1);
                       val = RR.at<float>(y1,x1) * (1 - x) * (1 - y) + RR.at<float>(y1, x2) * x * (1 - y) + RR.at<float>(y2, x1) * (1 - x) * y + RR.at<float>(y2, x2) * x * y;
                       outimage.at<float>(i-1, j) = val;

                       if(flag==0 && y1>=oy && x1==ox)
                       {
                           outfile << label << " " << object_id << endl;
                           outfile << ox << " " << oy << endl;
                           outfile << j << " " << i-1 << endl;
                           //outfile << LperP*(cam_info.height+OFFSET-(i-1))<< endl;
                           outfile << sqrt( ((j-(int)vp.x)*LperP_X-OFFSET_X)*((j-(int)vp.x)*LperP_X-OFFSET_X) + ((cam_info.height-(i-1))*LperP_Y+OFFSET_Y)*((cam_info.height-(i-1))*LperP_Y+OFFSET_Y) );
                           //outfile << LperP*sqrt((ox-cam_info.width/2)*(ox-cam_info.width/2) + (cam_info.height+OFFSET-(i-1))*(cam_info.height+OFFSET-(i-1))) << endl;
                           flag=1;
                           outfile << endl;
                       }
                   }
               }
           }
       }
       outfile << endl;
       infile.close();
       outfile.close();
       //imshow("showwww", outimage);
       outimage*=255;
       //imwrite("../Images/out_" + input_image, outimage);
       imwrite("./Images/out_"+to_string(numOfStream)+".jpg", outimage);
       waitKey(0);
       return 0;
}
