# Train YOLO Object Detection Model with Different Dataset Size

In this project, we aim to create an easy-to-use object detection service. We trained a YOLOv8 model for object detection on the COCO dataset and developed a user interface using PyQT5, which features the ability to load models, perform inference on a large number of images, and automatically save and view the results.

We also provide recommendations for beginners on how to prepare their datasets effectively. Additionally, we explore the impact of training dataset size on model performance through a series of experiments, demonstrating how performance varies with different dataset sizes. For those who may have limited resources or are unable to collect a large dataset, our results offer valuable insights into the trade-offs between performance and the effort required to gather data.


## YOLO

[YOLOv8](https://docs.ultralytics.com/models/yolov8/) is renowned for its speed and accuracy in object detection tasks. It offers a flexible API that makes training and testing straightforward. In this project, we chose the YOLOv8 Nano model (YOLOv8n) to train our detection model, striking a balance between performance and efficiency.

## COCO Dataset

The [COCO](https://cocodataset.org/#home) dataset is a large-scale dataset for common object detection, segmentation, and captioning. It contains over 100,000 labeled images and 80 object categories, making it an popular choice for training and evaluating object detection models.

The COCO dataset comes with an API that simplifies data handling, making tasks such as data analysis and preprocessing efficient and convenient.

### Create COCO Subset

Our scripts for working with COCO data can be found in the `COCO_tool` folder.

To experiment with smaller datasets, we use the COCO API to extract and prepare subsets while preserving the original data distribution. We employ pandas for analyzing the distribution of images and annotations, ensuring that our experiments are well-founded. This method enables us to evaluate how the YOLOv8 model performs with different dataset sizes. After segmenting the dataset, we download the corresponding image files and convert the annotations to a YOLO-compatible format.

## GUI

## Experiment: Impact of Training Dataset Size

We conducted experiments to evaluate how the size of the training dataset affects model performance. We trained YOLOv8 models on subsets of the COCO dataset with varying sizes (e.g., 1%, 5%, 20%, 60% of the original data) and analyzed the results in terms of metrics such as mAP (mean Average Precision), precision, and recall. Our findings are particularly useful for those with limited hardware resources or data, as they provide insights into the trade-offs between performance and dataset size.

### Key Findings


## User Guide

To learn how to use our tools and scripts, refer to `useful_scripts.ipynb`, which provides an overview of file usage and instructions.

### Train a Model


### Use Our Model
