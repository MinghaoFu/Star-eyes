# Star Eyes

## Abstract
Advanced driver assistance systems (ADAS) has achieved compelling
success in driving and parking functions. Through a safe human-machine interface, ADAS could increase car and road safety. However, existing methods
have inevitable drawbacks about security and hardware cost. For instance, deep-learning-based detection algorithm are unstable in real-world applications for the
approximation error during learning stage, and hardware of radio ranging is too
expensive to be deployed on widely-used personal cars. To address these issue, we
propose a novel Star-eyes ADAS. We combine conventional computer-vision and
deep-learning-based methods to build more concise and steady algorithms, and develop monocular ranging distance algorithm in ranging surrounding vehicles and
persons based on only cameras. Besides, in order to improve perceptual capacity
of drivers, we first add a panoramic stitching and 3D live road model into ADAS
products for a more concise view.

## Introduction

Star Eyes serves car drivers and provides drivers and occupants with a safer and more convenient driving experience. This system is designed to assist drivers in identifying hazards ahead and observing road conditions in a more concise and intuitive form just like **ADAS**.

Star Eyes consist of two main modules: **Predictive Forward Collision Warning System** and **Blind Spot Monitoring System**

## Avoid hazards: Lane Detection, Object Recognization and Ranging

### Lane detection

Lane detection can help us to concentrate on objects in the same road with driver. The most familiar approach to fit line is proposed. In this method, Hough transform and least square have been combined to process experiment data and the contour of binary images.

### Object Recognization

YOLOv3 is a real-time object detection algorithm that identifies specific objects in videos, live feeds, or images. YOLO uses features learned by a deep convolutional neural network to detect an object.

In the case of real-time driving, YOLOv3 has better performance that the other models in reaction and accuracy. 

### Ranging

Monocular camera ranging is really a huge challenge to everyone engaged in computer vision. To avoid the deviation caused by the different parameters of cameras, the best way is to recaculate the **Distortion Coefficients** and **Calibration Matrix**. The specific process to repeat **Affine transformation** over and over again, colloquaily, up and down.

## Perceive like a sensor: Panoramic stitching and 3D Mapping

### Panoramic stitching

By mixing camera pictures from four differnent sides, we could get an aerial view of car and its around. It helps drivers observe around more precisely.

### 3D live road model

Obviously, large amounts of products can obtain data and handle it with programming like image process or machine learning. In real-time driving, all the objects coordinate was mapping to 3D model in screen. This function builds a succinct picture to express relative positions of every vehicles, thus helping drivers observe the road more precisely.


