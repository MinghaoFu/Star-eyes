import os
import argparse

if __name__ == '__main__':
    '''parser = argparse.ArgumentParser()
    parser.add_argument("update", help="help you to update all more conveniently", type=int)
    args = parser.parse_args()

    if args.update == 0:
        os.system('python3 ./yolov3/detect.py --source 0 --weights ./yolov3/yolov3.pt')
        os.system('./birdView/build/dist')
        os.system('./interface/build/interface')
    else:
        os.system('pwd')
        os.system('cd ./birdView/build && make')
        os.system('cd ./interface/build && make')
    '''
    
    os.system('python3 ./yolov5/detect.py --source 2 --weights ./yolov5/yolov5l6.pt --conf 0.5')
    #os.system('python3 ./yolov3/detect.py --source ./raw/good.mp4 --weights ./yolov3/yolov3.pt --conf 0.5')
