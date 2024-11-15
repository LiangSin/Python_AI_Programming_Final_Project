# Train YOLO Object Detection Model with Different Dataset Size

In this project, we wish to create an easy-to-use object detection service.
We trained YOLOv8 model for object detection on the COCO dataset. 
Also, we write an user interface with PyQT5 which features loading model, inferencing large amount of images, and save and view the results automatically.

We also provide suggestion for the beginners on preparing the dataset.
We discuss the impact of training dataset size by experiment and show the performance of different sizes.
For the ones who are not able to prepare large dataset, our results is useful to decide on the trade-off between performance and efforts to collect data.


## YOLO

[YOLOv8](https://docs.ultralytics.com/models/yolov8/)

## COCO Dataset

[COCO](https://cocodataset.org/#home) is a large-scale common object image dataset.

COCO dataset supplies API for easy usage.

### Create COCO Subset

To train with smaller dataset, we analyze the distribution of the dataset with pandas and

## GUI

## User Guide

### Train a model

Training with COCO API, only the annotation files are needed to be download.

### Inferencing