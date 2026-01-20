import cv2
import os

# To extract video frames into PNG images for Frame Decomposition
video_path = 'data/vids/knee-vid.mp4' # Path to the input video file
output_folder = 'data/vids/knee_test'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

vidcap = cv2.VideoCapture(video_path)
success, image = vidcap.read()
count = 0

while success:
    # Saves frames as 000001.png, 000002.png, etc.
    cv2.imwrite(f"{output_folder}/{count:06d}.png", image)     
    success, image = vidcap.read()
    count += 1

print(f"Done! Extracted {count} frames to {output_folder}")