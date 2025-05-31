import cv2
import os
import torch
import torchvision
from ultralytics import YOLO

# Load the YOLO model
model = YOLO("yolo11s_36.pt")

# Load the image
image_path = "F:\\Downloads\\images2.jpeg"
image = cv2.imread(image_path)
file_name, file_extension = os.path.splitext(os.path.basename(image_path))

# Run YOLOv8 prediction
results = model.predict(source=image_path, conf=0.5)

# Create output folders
output_folder = "output_crops"
os.makedirs(output_folder, exist_ok=True)

annotated_image = image.copy()  # Copy for full image labeling

# Extract bounding boxes, confidences, and class IDs
boxes = torch.tensor([box.xyxy[0].tolist() for box in results[0].boxes])
scores = torch.tensor([box.conf[0].item() for box in results[0].boxes])
iou_threshold = 0.4  # Adjust based on requirements

# Apply NMS to remove duplicate bounding boxes
indices = torchvision.ops.nms(boxes, scores, iou_threshold)

# Process detection results after NMS filtering
for i in indices:
    x1, y1, x2, y2 = [round(x) for x in boxes[i].tolist()]  # Get bounding box
    label = f"fb_{i+1}"  # Assign unique label

    # Crop detected object
    cropped_obj = image[y1:y2, x1:x2]
    save_path = f"{output_folder}/{label}{file_extension}"
    cv2.imwrite(save_path, cropped_obj)  # Save cropped image

    # Annotate full image with bounding box
    cv2.rectangle(annotated_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv2.putText(annotated_image, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)

# Save the annotated full image
cv2.imwrite(f"{output_folder}/{file_name}{file_extension}", annotated_image)

print("Processing complete with NMS applied!")
