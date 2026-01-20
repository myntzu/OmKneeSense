import cv2
import os

# Path to magnified images (change as needed - e.g. filename)
image_folder = 'data/output/knee_magnified_50'
video_name = 'knee_sense_magnified_50.mp4'

images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
images.sort() # Ensure frames are in order (0001, 0002...)

# Get dimensions from the first image
frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape

video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'mp4v'), 30, (width,height))

for image in images:
    video.write(cv2.imread(os.path.join(image_folder, image)))

cv2.destroyAllWindows()
video.release()
print("Video created successfully!")