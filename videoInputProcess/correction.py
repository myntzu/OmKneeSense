import cv2
import numpy as np
import os

VIDEO_PATH = "videoInputProcess/knee-vid.mp4"
OUTPUT_PATH = "videoInputProcess/knee-vid-corrected.mp4"

# ==========================
# MANUAL VALUES (KEEP THESE)
# ==========================
K1 = -0.05        # mild barrel correction
FX_SCALE = 0.9
FY_SCALE = 0.9

# Crop AFTER fisheye correction
CROP = {
    "LEFT": 700,
    "RIGHT": 550,
    "TOP": 600,
    "BOTTOM": 400
}

DEBUG_SINGLE_FRAME = False


# ==========================
# CORE FUNCTIONS
# ==========================
def fisheye_correct(frame):
    h, w = frame.shape[:2]

    fx = FX_SCALE * w
    fy = FY_SCALE * h
    cx = w / 2
    cy = h / 2

    K = np.array([[fx, 0, cx],
                  [0, fy, cy],
                  [0,  0,  1]], dtype=np.float32)

    D = np.array([K1, 0, 0, 0], dtype=np.float32)

    return cv2.undistort(frame, K, D)


def crop_frame(img):
    h, w = img.shape[:2]
    return img[
        CROP["TOP"]:h - CROP["BOTTOM"],
        CROP["LEFT"]:w - CROP["RIGHT"]
    ]


def process_frame(frame):
    corrected = fisheye_correct(frame)
    cropped = crop_frame(corrected)
    return cropped


# ==========================
# MAIN
# ==========================
if __name__ == "__main__":

    if not os.path.exists(VIDEO_PATH):
        raise FileNotFoundError(f"❌ Video not found: {VIDEO_PATH}")

    cap = cv2.VideoCapture(VIDEO_PATH)
    if not cap.isOpened():
        raise RuntimeError("❌ Cannot open video")

    print("✅ Video opened")
    print(f"Using k1={K1}, fx_scale={FX_SCALE}, fy_scale={FY_SCALE}")
    print(f"Crop = {CROP}")

    if DEBUG_SINGLE_FRAME:
        ret, frame = cap.read()
        if not ret:
            raise RuntimeError("❌ Cannot read frame")

        out = process_frame(frame)

        stacked = cv2.hconcat([
            frame,
            cv2.resize(out, (frame.shape[1], frame.shape[0]))
        ])

        cv2.imshow("Raw (Left) | Corrected + Cropped (Right)", stacked)
        cv2.imwrite("videoInputProcess/debug-frame1.jpg", stacked)
        print("💾 Saved debug-frame1.jpg")

        cv2.waitKey(0)
        cv2.destroyAllWindows()
        cap.release()

    else:
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        ret, first = cap.read()
        if not ret:
            raise RuntimeError("❌ Cannot read first frame")

        first_out = process_frame(first)
        h, w = first_out.shape[:2]

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        writer = cv2.VideoWriter(OUTPUT_PATH, fourcc, fps, (w, h))

        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

        print(f"▶️ Processing {total} frames")

        idx = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            writer.write(process_frame(frame))
            idx += 1

            if idx % 30 == 0:
                print(f"{idx}/{total}")

        cap.release()
        writer.release()
        print(f"✅ Saved: {OUTPUT_PATH}")
