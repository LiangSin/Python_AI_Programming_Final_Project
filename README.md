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
We develop our own GUI with PyQt5, you can add functions to fit your requirements.

![UI](https://hackmd.io/_uploads/Hk94B7o7Je.jpg)

## Experiment: Impact of Training Dataset Size

We conducted experiments to evaluate how the size of the training dataset affects model performance. We trained YOLOv8 models on subsets of the COCO dataset with varying sizes (e.g., 1%, 5%, 20%, 60% of the original data) and analyzed the results in terms of metrics such as mAP (mean Average Precision), precision, and recall. Our findings are particularly useful for those with limited hardware resources or data, as they provide insights into the trade-offs between performance and dataset size.

### Key Findings
> You can see [Full Results](https://hackmd.io/1Gch-BFSQ5eFCG9Xu4EOLw) here.

![category_performnace_map5095](https://hackmd.io/_uploads/SJijemsXyx.png)
![model_performance_dataset_size](https://hackmd.io/_uploads/rJNPKbsQ1l.png)
- **40% as a Sweet Spot**: Training with 40% of the dataset provides a strong performance baseline. Further increasing the dataset size shows diminishing returns in model improvement.
- **Low Data Requirement for Distinct Objects**: If your target object is large and distinct (e.g., a "cat"), approximately 1,700 images are sufficient for training.
- **High Data Requirement for Confusing Objects**: For objects that are easily confused with others, you'll need a significantly larger dataset, with at least 6,000 images recommended for reliable performance.

## Setup
To learn how to use our tools and scripts, refer to `useful_scripts.ipynb`, which provides an overview of file usage and instructions. 

### Datatset Preparation

1. **Download COCO dataset annotation files**: 
 COCO annotation files provide structured data to describe images in the COCO dataset. These files use JSON format to store metadata, including image IDs, categories, bounding boxes, segmentation masks, and keypoints.  
    
1. **Download COCO dataset images**

2. **Parse COCO annotation files**:  `COCO_tool/create_subset.py` creates a subset of a COCO dataset based on a specified proportion, ensuring every category is represented at least once. It randomly selects images while maintaining category diversity, extracts their annotations, and saves the subset in COCO format as a new JSON file. The output is stored in a  `annotations/subsets` directory for further use.
3. **Convert COCO annotation files to YOLO annotation format**: 
`COCO_tool/create_YOLO_dataset.py` transforms COCO annotation files into YOLO-compatible format. It also removes images without annotation files from the dataset.

### Train

`YOLO_tool/train.py` trains the YOLO model on a given dataset. The basic arguments we defined include : 

1. `--model` : train from scratch or load model checkpoints. Default to `yolov8n.yaml`.
2. `--config` : configuration files for training. Default to `coco.yaml`.
3. `--device` : select the device to run on. Default to GPU:0.
   - a single GPU (device=0)
   - multiple GPUs (device=0,1)
   - CPU (device=cpu)
   - MPS for Apple silicon (device=mps).
4. `--batch` : select batch size for training. Default to -1 (auto mode for 60% GPU memory utilization).

For more parameter informations, see [official documentation](https://docs.ultralytics.com/modes/train/#introduction).

Trained results will automatically be stored to `YOLO_tool/runs/detect` directory. 