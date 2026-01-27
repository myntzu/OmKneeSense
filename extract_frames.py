import cv2
import os
import argparse

def extract_frames(video_path, out_dir):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    vidcap = cv2.VideoCapture(video_path)
    success, image = vidcap.read()
    count = 0

    while success:
        cv2.imwrite(os.path.join(out_dir, f"{count:06d}.png"), image)
        success, image = vidcap.read()
        count += 1

    print(f"Done! Extracted {count} frames to {out_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract frames from a video")
    parser.add_argument(
        "--video_path",
        type=str,
        required=True,
        help="Path to input video file"
    )
    parser.add_argument(
        "--out_dir",
        type=str,
        required=True,
        help="Directory to save extracted frames"
    )

    args = parser.parse_args()

    extract_frames(args.video_path, args.out_dir)
