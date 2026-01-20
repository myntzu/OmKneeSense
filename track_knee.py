import cv2
import numpy as np
import os
import csv
import glob

image_folder = 'data/output/knee_magnified'
output_csv = 'knee_tracking_data.csv'

#old:
# images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
# images.sort()

images = sorted(glob.glob('data/output/knee_magnified/*.png'))

data_log = []

print("Starting tracking...")
for i, path in enumerate(images):
    frame = cv2.imread(path)
    frame = cv2.imread(path)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Convert to grayscale to find the "brightness" of the force
    
    # 1. Clean up noise (Thresholding)
    # Adjust '30' if it's too sensitive or not sensitive enough
    _, thresh = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)
    
    # 2. Find the "Center of Mass" (Moments)
    M = cv2.moments(thresh)
    
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        # Sum of pixel brightness = proxy for total force
        force_proxy = np.sum(gray) / 1000 # Scaling for readability
    else:
        cX, cY, force_proxy = 0, 0, 0

    data_log.append([i, cX, cY, force_proxy])

# Save to CSV
with open(output_csv, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Frame", "X_Center", "Y_Center", "Force_Intensity"])
    writer.writerows(data_log)

print(f"Tracking complete! Data saved to {output_csv}")