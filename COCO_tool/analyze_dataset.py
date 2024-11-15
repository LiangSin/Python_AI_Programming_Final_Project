import argparse
import numpy as np
import pandas as pd
from pycocotools.coco import COCO
import matplotlib.pyplot as plt

def main(annFile):

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

    # Create a mapping from category IDs to category names
    cats_df.set_index('id', inplace=True)
    catid_to_name = cats_df['name'].to_dict()
    anns_df['category_name'] = anns_df['category_id'].map(catid_to_name)

    # Analyze the number of annotations per category
    category_counts = anns_df['category_name'].value_counts()
    print("Number of annotations per category:")
    print(category_counts)

    # Visualize the distribution of annotations per category
    plt.figure(figsize=(12, 6))
    category_counts.sort_values().plot(kind='bar')
    plt.title('Number of Annotations per Category')
    plt.xlabel('Category')
    plt.ylabel('Number of Annotations')
    plt.tight_layout()
    plt.show()

    # Analyze the number of annotations per image
    anns_per_image = anns_df['image_id'].value_counts()
    print("\nNumber of annotations per image:")
    print(anns_per_image.describe())

    # Visualize the distribution of annotations per image
    plt.figure()
    anns_per_image.hist(bins=50)
    plt.title('Histogram of Number of Annotations per Image')
    plt.xlabel('Number of Annotations')
    plt.ylabel('Number of Images')
    plt.show()

    # Analyze area distribution of annotations
    print("\nArea statistics:")
    print(anns_df['area'].describe())

    # Visualize the area distribution
    plt.figure()
    anns_df['area'].hist(bins=50, range=(0, 50000))
    plt.title('Histogram of Annotation Areas')
    plt.xlabel('Area')
    plt.ylabel('Number of Annotations')
    plt.show()

    # Extract bounding box width and height from the 'bbox' field
    anns_df['bbox_width'] = anns_df['bbox'].apply(lambda x: x[2])
    anns_df['bbox_height'] = anns_df['bbox'].apply(lambda x: x[3])

    # Analyze bounding box width and height statistics
    print("\nBounding box width statistics:")
    print(anns_df['bbox_width'].describe())

    print("\nBounding box height statistics:")
    print(anns_df['bbox_height'].describe())

    # Visualize bounding box width distribution
    plt.figure()
    anns_df['bbox_width'].hist(bins=50, range=(0, 500))
    plt.title('Histogram of Bounding Box Widths')
    plt.xlabel('Width')
    plt.ylabel('Number of Annotations')
    plt.show()

    # Visualize bounding box height distribution
    plt.figure()
    anns_df['bbox_height'].hist(bins=50, range=(0, 500))
    plt.title('Histogram of Bounding Box Heights')
    plt.xlabel('Height')
    plt.ylabel('Number of Annotations')
    plt.show()


if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Create a subset of the COCO dataset.")
    parser.add_argument("--annFile", type=str, default="../annotations/instances_train2017.json", help="Path to the COCO annotations file")
    args = parser.parse_args()

    # Run the main function
    main(args.annFile)