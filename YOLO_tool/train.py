import argparse
from ultralytics import YOLO

def train(model_path, yaml_path, device):
    # Load a model
    model = YOLO(model_path)  # build a new model from scratch

    # Use the model
    if model_path.endswith('.yaml'):
        results = model.train(data=yaml_path, imgsz=256, device=device, verbose=True,
                            epochs=300, patience=50, 
                            weight_decay=0.001, dropout=0.3)
    elif model_path.endswith('.pt'):
        results = model.train(resume=True)

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, default="yolov8n.yaml", help="The default is training from scratch. Input the existing .pt model file to continue the training process.")
    parser.add_argument("--config", type=str, default="coco.yaml", help="Path to the config file")
    parser.add_argument("--device", type=str, default=0, help="device number")
    args = parser.parse_args()

    # Run the main function
    train(args.model, args.config, args.device)