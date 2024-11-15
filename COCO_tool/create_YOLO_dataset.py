import argparse
import os
import json
import shutil
from tqdm import tqdm
from pycocotools.coco import COCO

def create_labels(annFile, output_dir):
    # Helper function to convert COCO bbox format to YOLO format
    def convert_bbox(size, box):
        dw = 1.0 / size[0]
        dh = 1.0 / size[1]
        x = box[0] + box[2] / 2.0
        y = box[1] + box[3] / 2.0
        w = box[2]
        h = box[3]
        return x * dw, y * dh, w * dw, h * dh
    
    coco = COCO(annFile)
    os.makedirs(output_dir, exist_ok=True)

    # Load image and annotation information
    imgIds = coco.getImgIds()
    cats = coco.loadCats(coco.getCatIds())

    # Create a mapping from category ID to YOLO class index
    catid_to_yolo = {cat['id']: idx for idx, cat in enumerate(cats)}
    cat_map = [cat['name'] for cat in cats]

    for imgId in tqdm(imgIds, desc="Create labels"):
        img_info = coco.loadImgs(imgId)[0]
        annIds = coco.getAnnIds(imgIds=imgId)
        anns = coco.loadAnns(annIds)

        label_file_path = os.path.join(output_dir, f"{os.path.splitext(img_info['file_name'])[0]}.txt")
        with open(label_file_path, 'w') as f:
            for ann in anns:
                if ann['iscrowd'] == 1:
                    continue
                bbox = convert_bbox((img_info['width'], img_info['height']), ann['bbox'])
                category_id = catid_to_yolo[ann['category_id']]
                f.write(f"{category_id} {' '.join(map(str, bbox))}\n")
    
    return cat_map

def clean_train_image(image_path, label_path):
    Sel = set()
    for label_file in os.listdir(label_path):
        if label_file.endswith('.txt'):  # Ensure we're only considering text files
            Sel.add(os.path.splitext(label_file)[0])  # Store the basename without extension

    for image_file in tqdm(os.listdir(image_path), desc="Clean train image set"):
        if image_file.endswith(('.jpg', '.jpeg', '.png')):  # Consider common image formats
            image_basename = os.path.splitext(image_file)[0]  # Get the basename without extension
            if image_basename not in Sel:  # If the image basename is not in Sel
                image_full_path = os.path.join(image_path, image_file)
                os.remove(image_full_path)  # Remove the image


def main(annTrain, annVal, annTest, output_dir, yaml_path):

    images_dir = os.path.join(output_dir, 'images')
    labels_dir = os.path.join(output_dir, 'labels')

    os.makedirs(labels_dir, exist_ok=True)

    if annTrain is not None:
        print("Processing train images and annotations...")
        cat_map = create_labels(annTrain, os.path.join(labels_dir, "train"))
        clean_train_image(os.path.join(images_dir, "train"), os.path.join(labels_dir, "train"))
    if annVal is not None:
        print("Processing val annotations...")
        create_labels(annVal, os.path.join(labels_dir, "val"))
    if annTest is not None:
        print("Processing test annotations...")
        create_labels(annTest, os.path.join(labels_dir, "test"))


    # Create a data.yaml file for YOLO
    if yaml_path is not None:
        print("Create yaml file")
        data_yaml = f"""
path: {os.path.abspath(output_dir)}
train: images/train
val: images/val
test: images/test

nc: {len(cat_map)}
names: {cat_map}
"""

        with open(yaml_path, 'w') as f:
            f.write(data_yaml)

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("--annTrain", type=str, default=None, help="Path to the train annotations file")
    parser.add_argument("--annVal", type=str, default=None, help="Path to the val annotations file")
    parser.add_argument("--annTest", type=str, default=None, help="Path to the test annotations file")
    parser.add_argument("--dataset", type=str, required=True, help="Path to the YOLO form dataset directory")
    parser.add_argument("--yaml", type=str, default=None, help="Path to save the yaml file used for YOLO.")
    args = parser.parse_args()

    # Run the main function
    main(args.annTrain, args.annVal, args.annTest, args.dataset, args.yaml)