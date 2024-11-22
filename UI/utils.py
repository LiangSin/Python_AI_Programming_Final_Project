import re, os
from PyQt5.QtGui import QImageReader

def natural_sort(list, key=lambda s:s):
  """
  Sort the list into natural alphanumeric order.
  """
  def get_alphanum_key_func(key):
      convert = lambda text: int(text) if text.isdigit() else text
      return lambda s: [convert(c) for c in re.split('([0-9]+)', key(s))]
  sort_key = get_alphanum_key_func(key)
  list.sort(key=sort_key)

def scan_all_images(folder_path):
  cv2_supported_formats = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif', '.webp')
  # extensions = ['.%s' % fmt.data().decode("ascii").lower() for fmt in QImageReader.supportedImageFormats()]
  images = []

  for root, dirs, files in os.walk(folder_path):
    for file in files:
      # if file.lower().endswith(tuple(extensions)):
      if file.lower().endswith(cv2_supported_formats):
        relative_path = os.path.join(root, file)
        path = os.path.abspath(relative_path)
        images.append(path)
  natural_sort(images, key=lambda x: x.lower())
  return images

def find_output_path(input_path, save_path, extension = None):
  basename = os.path.basename(input_path)
  name, ext = os.path.splitext(basename)
  if extension:
    new_name = f"{name}_predict{extension}"
  else:
    new_name = f"{name}_predict{ext}"
  return os.path.join(save_path, new_name)