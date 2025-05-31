from ultralytics import YOLO
model=YOLO("yolo11s.pt")
image_path= "F:\\Downloads\\images.jpeg"
results = model.predict(source=image_path,show=True,save=True,show_labels=False,show_conf=False,conf=0.5,save_txt=False,save_crop=False,line_width=2)
masks = results[0].masks

import cv2
import os

image = cv2.imread(image_path)
print(image)
# Ensure output folder exists
output_folder = "output_crops"
os.makedirs(output_folder, exist_ok=True)

# Process detection results
for i, box in enumerate(results[0].boxes):
    x1, y1, x2, y2 = [round(x) for x in box.xyxy[0].tolist()]  # Get bounding box
    cropped_obj = image[y1:y2, x1:x2]  # Crop detected region
    
    # Define save path
    save_path = f"{output_folder}/fp_{i}.jpg"
    cv2.imwrite(save_path, cropped_obj)  # Save cropped object
    print(f"Saved detected object {i} at {save_path}")