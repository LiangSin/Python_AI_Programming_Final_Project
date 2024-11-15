# Create an python venv or conda environment and activate it before setting up
USAGE="Usage: Give argument --env, --dataset [1/0.8/0.6/0.4/0.2/0.05/0.01], --train [device], OR --UI.\nPlease activate virtual environment before setting up the env."
valid_values=("1" "0.8" "0.6" "0.4" "0.2" "0.05" "0.01")

Dataset(){
    echo "Downloading dataset..."
    echo "This may take a long time (~1hr)"
    mkdir dataset
    cd dataset
    mkdir images
    cd images
    wget http://images.cocodataset.org/zips/train2017.zip
    wget http://images.cocodataset.org/zips/val2017.zip
    wget http://images.cocodataset.org/zips/test2017.zip
    unzip *.zip
    rm *.zip
    mv train2017 train
    mv val2017 val
    mv test2017 test
    cd ..
    case $1 in
    "1") train_json="../annotations/instances_train2017.json" ;;
    "0.8") train_json="../annotations/subsets/instances_train2017_subset_0.8.json" ;;
    "0.6") train_json="../annotations/subsets/instances_train2017_subset_0.6.json" ;;
    "0.4") train_json="../annotations/subsets/instances_train2017_subset_0.4.json" ;;
    "0.2") train_json="../annotations/subsets/instances_train2017_subset_0.2.json" ;;
    "0.05") train_json="../annotations/subsets/instances_train2017_subset_0.05.json" ;;
    "0.01") train_json="../annotations/subsets/instances_train2017_subset_0.01.json" ;;
    esac
    val_json="../annotations/instances_val2017.json"
    test_json="../annotations/image_info_test2017.json"
    yaml_out="../YOLO_tool/coco.yaml"
    python ../COCO_tool/create_YOLO_dataset.py \
        --annTrain $train_json \
        --annVal $val_json \
        --annTest $test_json \
        --dataset . \
        --yaml $yaml_out
}

Train(){
    cd YOLO_tool
    python train.py --device $1
}

UI(){
    cd UI
    python main.py
}

if [[ $# -eq 0 ]] || [[ $# -gt 2 ]]; then
    echo $USAGE
    exit 1
fi

case "$1" in
    --env)
    echo "Set up the envorinment..."
    pip install -r requirement.txt
    ;;
    --dataset)
    if [[ ! " ${valid_values[@]} " =~ " $2 " ]]; then
        echo $USAGE
        exit 1
    fi
    Dataset $2
    ;;
    --train)
    if [[ ! " ${valid_values[@]} " =~ " $2 " ]]; then
        echo $USAGE
        exit 1
    fi
    Train $2
    ;;
    --UI)
    UI
    ;;
esac


