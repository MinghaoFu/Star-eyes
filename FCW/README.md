#预碰撞系统原型(Prototype of Pre-Collision System)
1.structure:
pics->yolov3->original coordinates->birdView->bird view coordinats and distance for each object->interface
2.intro for every folders:
share:用来存放坐标，距离数值信息。
runs:yolov3 run出来的画了框框的图片。
interface:一个封装好的C++类，包含目标名称，原始坐标，变换后坐标，距离。
yolov3:就是yolo，你懂的。
Images:yolo和鸟瞰图代码读取图片的地方，初拟之后，将视频切成一张张图片放入此文件夹来读。
Images_backup:备份的一些图片。
birdView:从Images里读图片，从share里读原始坐标，再share里生成变换后的坐标和距离。
3.使用说明
终端进入Pre-CollisionSystem文件夹，运行 'python3 run.py'.
