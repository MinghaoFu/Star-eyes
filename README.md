# STAR EYES

## Introduction

Advanced driver assistance systems (ADAS) have achieved a compelling
success. However, existing methods met some inevitable drawbacks in security and cost. For instance, deep-learning-based detection algorithm are unstable in real-world applications, and the hardware configurations are too
expensive to be deployed on most of vehicles. To address these issues, we
build a novel ADAS, termed as **STAR EYES**. We combine conventional computer vision technology and
deep-learning-based methods to build more precise and steady algorithms, meanwhile develop the algorithm of monocular ranging distance with assistance of only cameras. Besides, in order to help drivers, we first add a panoramic stitching and 3D live road model into ADAS
products for comfortable feelings.

## Predictive Forward Collision Warning System

Avoid hazards: Lane Detection, Object Recognization and Ranging

### Lane Detection

Lane detection can help us to concentrate on objects in the same road with driver. The most familiar approach to fit line is proposed. In this method, Hough transform and least square have been combined to process experiment data and the contour of binary images.

### Object Recognization

YOLOv3 is a real-time object detection algorithm that identifies specific objects in videos, live feeds, or images. YOLO uses features learned by a deep convolutional neural network to detect an object.

In the case of real-time driving, YOLOv3 has better performance that the other models in reaction and accuracy. 

### Ranging Distance

Monocular camera ranging is really a huge challenge to everyone engaged in computer vision. To avoid the deviation caused by the different parameters of cameras, the best way is to recaculate the **Distortion Coefficients** and **Calibration Matrix**. The specific process to repeat **Affine transformation** over and over again, colloquaily, up and down.

## Blind Spot Monitoring System

Perceive like a sensor: Panoramic stitching and 3D Mapping

### Panoramic Stitching

By mixing camera pictures from four differnent sides, we could get an aerial view of car and its around. It helps drivers observe around more precisely.

### 3D-Live Road Model

Obviously, large amounts of products can obtain data and handle it with programming like image process or machine learning. In real-time driving, all the objects coordinate was mapping to 3D model in screen. This function builds a succinct picture to express relative positions of every vehicles, thus helping drivers observe the road more precisely.


