# Prototype of Pre-Collision System

## Structure
pics->yolov3->original coordinates->birdView->bird view coordinats and distance for each object->interface

## Introduction:
**share**: Used to store coordinates, distance numerical information.

**runs**: Yolov3 runs out with framed pictures

**interface**: An encapsulated C++ class that contains the target name, original **coordinates**, transformed coordinates, and distance.

**Images**: The yolov3 and aerial view code reads the picture, and after the initial **drafting**, the video is cut into pictures and put into this folder to read.

**Images_backup**: Backup images.

**birdView**: Read the image from Images, read the original coordinates from share, and generate the transformed coordinates and distances in share.

## Run
>python3 run.py
