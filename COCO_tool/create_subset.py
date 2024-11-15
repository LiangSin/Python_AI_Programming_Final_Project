import argparse
import numpy as np
import pandas as pd
from pycocotools.coco import COCO
import json
import random
import os

def main(annFile, proportion):
    # Initialize COCO API
    coco = COCO(annFile)
    
    # Get all image IDs and annotation IDs
    imgIds = coco.getImgIds()
    annIds = coco.getAnnIds()

    # Load annotations and images into DataFrames
    anns = coco.loadAnns(annIds)
    imgs = coco.loadImgs(imgIds)
    anns_df = pd.DataFrame(anns)
    imgs_df = pd.DataFrame(imgs)

    # Load category information
    catIds = coco.getCatIds()
    cats = coco.loadCats(catIds)
    cats_df = pd.DataFrame(cats)

    # Map category IDs to category names
    cats_df.set_index('id', inplace=True)
    catid_to_name = cats_df['name'].to_dict()
    anns_df['category_name'] = anns_df['category_id'].map(catid_to_name)

    # Calculate the total number of images
    total_images = len(imgIds)

    # Calculate the absolute subset size based on the proportion
    subset_size = int(total_images * proportion)
    print(f"Total images in original dataset: {total_images}")
    print(f"Proportion: {proportion}")
    print(f"Subset size: {subset_size}")

    # Ensure every category appears at least once
    selected_imgIds = set()
    for cat_id in catIds:
        # Get all image IDs for the current category
        imgIds_per_cat = anns_df[anns_df['category_id'] == cat_id]['image_id'].unique()
        # Randomly select one image for this category
        if len(imgIds_per_cat) > 0:
            selected_imgIds.add(random.choice(imgIds_per_cat))

    # Calculate the remaining number of images needed
    remaining_size = subset_size - len(selected_imgIds)

    # Randomly select the remaining images from the full set
    remaining_imgs = list(set(imgIds) - selected_imgIds)
    additional_imgs = np.random.choice(remaining_imgs, remaining_size, replace=False)
    selected_imgIds.update(additional_imgs)

    # Create a new annotations file for the subset
    selected_imgIds = list(selected_imgIds)
    selected_imgs = [img for img in imgs if img['id'] in selected_imgIds]

    # Get all annotations for the selected images
    selected_annIds = coco.getAnnIds(imgIds=selected_imgIds)
    selected_anns = coco.loadAnns(selected_annIds)

    # Prepare the subset annotations in COCO format
    subset_annotations = {
        'info': coco.dataset['info'],
        'licenses': coco.dataset['licenses'],
        'images': selected_imgs,
        'annotations': selected_anns,
        'categories': coco.dataset['categories']
    }

    # Create output directory if it does not exist
    output_dir = os.path.join(os.path.dirname(annFile), 'subsets/')
    os.makedirs(output_dir, exist_ok=True)

    # Save the subset annotations to a new JSON file
    subset_annFile = os.path.join(output_dir, f'instances_train2017_subset_{proportion}.json')
    with open(subset_annFile, 'w') as f:
        json.dump(subset_annotations, f)

    print(f"Subset annotations saved to {subset_annFile}")
    print(f"Total images in subset: {len(selected_imgs)}")
    print(f"Total annotations in subset: {len(selected_anns)}")

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Create a subset of the COCO dataset.")
    parser.add_argument("--annFile", type=str, default="../annotations/instances_train2017.json", help="Path to the COCO annotations file")
    parser.add_argument("--proportion", type=float, required=True, help="Proportion of the original dataset to use (e.g., 0.1 for 10%)")
    args = parser.parse_args()

    # Run the main function
    main(args.annFile, args.proportion)
