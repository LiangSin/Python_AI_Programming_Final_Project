import os

from ultralytics import YOLO
import cv2
import numpy as np
from utils import *

class API:
  def __init__(self):
    self.model = None
    self.save_path = None

  def Set_Parameter(self, model_path=None, save_path=None):
    """All paths must be ABSOLUTE PATH"""
    if model_path is not None:
      self.model = YOLO(model_path)
    if save_path is not None:
      self.save_path = save_path


  def predict_image(self, input_path, conf_threshold=0.5):
      """All paths must be ABSOLUTE PATH"""
      if self.model is None:
          return "Please set model path before predicting"
          
      image = cv2.imread(input_path)
      if image is None:
        return -1
      # Remove image_size and imgsz parameter
      results = self.model.predict(image, conf=conf_threshold)[0]
      if not os.path.exists(self.save_path):
          os.makedirs(self.save_path)

      draw_and_save(results, find_output_path(input_path, self.save_path), image)
      generate_text(results, find_output_path(input_path, self.save_path, ".txt"))

  def predict_list(self, input_path_list, conf_threshold=0.5):
      """All paths must be ABSOLUTE PATH"""
      if self.model is None:
          return "Please set model path before predicting"
      
      return_value = 0
      
      for input_path in input_path_list:
          image = cv2.imread(input_path)
          if image is None:
             return_value = -1
             continue
          # Remove image_size and imgsz parameter
          results = self.model.predict(image, conf=conf_threshold)[0]
          if not os.path.exists(self.save_path):
              os.makedirs(self.save_path)

          draw_and_save(results, find_output_path(input_path, self.save_path), image)
          generate_text(results, find_output_path(input_path, self.save_path, ".txt"))
      return return_value



def draw_and_save(results, output_path, image):
    # Compute scale factors based on image size
    height, width = image.shape[:2]
    scale_factor = max(height, width) / 600.0  # 600.0 is the base size for scaling
    
    # Set minimum and maximum values for thickness and fontScale
    thickness = max(int(2 * scale_factor), 1)  # Ensure thickness is at least 1
    fontScale = max(0.5 * scale_factor, 0.5)   # Ensure fontScale is at least 0.5

    for x1, y1, x2, y2, score, class_id in results.boxes.data.tolist():
        # Convert coordinates to integers
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        
        # Class name and score
        class_name = results.names[int(class_id)]
        label = f"{round(score, 2)} {class_name}"
        
        # Color settings
        color = (0, 255, 0)  # Green box (can change to other colors)
        
        # Draw rectangle box with scaled thickness
        cv2.rectangle(image, (x1, y1), (x2, y2), color, thickness)
        
        # Display class name and score above the rectangle with scaled font size and thickness
        cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=fontScale, color=color, thickness=thickness, lineType=cv2.LINE_AA)
    
    # Save the processed image
    cv2.imwrite(output_path, image)



def generate_text(results, output_path):
  cell_count = [0] * len(results.names)
  for result in results.boxes.data.tolist():
    x1, y1, x2, y2, score, class_id = result
    cell_count[int(class_id)] += 1
  text = ""
  for i in range(len(results.names)):
    text += f"{results.names[i]}: {cell_count[i]}\n"
  with open(output_path, 'w') as f:
    f.write(text)