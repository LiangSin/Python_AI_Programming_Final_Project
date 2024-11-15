import argparse
from ultralytics import YOLO

def test(model_path, yaml_path, device):
    # Load a model
    model = YOLO(model_path)  # build a new model from scratch

    # Use the model
    results = model.val(data=yaml_path, imgsz=256, device=device)

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, default="best.pt", help="Input the .pt model file to be test.")
    parser.add_argument("--config", type=str, default="coco.yaml", help="Path to the config file")
    parser.add_argument("--device", type=str, default=0, help="device number")
    args = parser.parse_args()

    # Run the main function
    test(args.model, args.config, args.device)