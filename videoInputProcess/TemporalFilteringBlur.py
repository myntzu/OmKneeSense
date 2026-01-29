import cv2
import numpy as np
import time
import os
import glob

class TemporalSmoothingFrames:
    """
    Temporal smoothing (EMA) but using a folder of frames instead of a camera.
    """

    def __init__(self, input_folder, output_folder=None, target_fps=30):
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.target_fps = target_fps

        # Collect frames
        self.frame_paths = sorted(
            glob.glob(os.path.join(input_folder, "*.*"))
        )
        self.frame_paths = [
            p for p in self.frame_paths
            if p.lower().endswith((".png", ".jpg", ".jpeg", ".bmp"))
        ]

        if not self.frame_paths:
            raise RuntimeError(f"No image frames found in: {input_folder}")

        # Create output folder if saving
        if self.output_folder is not None:
            os.makedirs(self.output_folder, exist_ok=True)

        # EMA temporal smoothing
        self.enable_ema = True
        self.alpha = 0.20
        self.prev = None  # float32 BGR accumulator

        # Motion-adaptive EMA
        self.enable_motion_adapt = True
        self.motion_threshold = 10.0
        self.alpha_fast = 0.60

    def temporal_ema(self, frame_bgr):
        f = frame_bgr.astype(np.float32)

        if self.prev is None or not self.enable_ema:
            self.prev = f
            return frame_bgr

        a = float(self.alpha)

        if self.enable_motion_adapt:
            prev_u8 = np.clip(self.prev, 0, 255).astype(np.uint8)
            g1 = cv2.cvtColor(prev_u8, cv2.COLOR_BGR2GRAY)
            g2 = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
            motion = cv2.mean(cv2.absdiff(g1, g2))[0]

            if motion > self.motion_threshold:
                a = float(self.alpha_fast)

        self.prev = (1.0 - a) * self.prev + a * f
        return np.clip(self.prev, 0, 255).astype(np.uint8)

    def add_overlay(self, frame, idx, total):
        overlay = frame.copy()
        cv2.rectangle(overlay, (10, 10), (520, 130), (0, 0, 0), -1)
        frame = cv2.addWeighted(frame, 0.7, overlay, 0.3, 0)

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, f"Frame: {idx+1}/{total}", (20, 40), font, 0.8, (0, 255, 0), 2)
        cv2.putText(frame, f"EMA: {self.enable_ema}  alpha={self.alpha:.2f}", (20, 75), font, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"MotionAdapt: {self.enable_motion_adapt}  thr={self.motion_threshold:.1f}  alpha_fast={self.alpha_fast:.2f}",
                    (20, 110), font, 0.6, (0, 255, 0), 2)
        return frame

    def run(self):
        delay_ms = int(1000 / max(1, self.target_fps))
        paused = False

        total = len(self.frame_paths)
        idx = 0

        while idx < total:
            if not paused:
                path = self.frame_paths[idx]
                frame = cv2.imread(path, cv2.IMREAD_COLOR)
                if frame is None:
                    print("Failed to read:", path)
                    idx += 1
                    continue

                if self.enable_ema:
                    out = self.temporal_ema(frame)
                else:
                    self.prev = None
                    out = frame

                # AUTO SAVE every frame
                if self.output_folder is not None:
                    save_path = os.path.join(self.output_folder, f"{idx:06d}.png")
                    cv2.imwrite(save_path, out)

                disp = self.add_overlay(out.copy(), idx, total)
                cv2.imshow("Temporal Smoothing (Folder Frames)", disp)


            key = cv2.waitKey(delay_ms if not paused else 30) & 0xFF

            if not paused:
                idx += 1

        cv2.destroyAllWindows()


if __name__ == "__main__":
    input_folder = "./data/vids/knee_test_corrected"
    output_folder = "output_frames"  # set to None if you don't want saving

    app = TemporalSmoothingFrames(
        input_folder=input_folder,
        output_folder=output_folder,
        target_fps=15
    )
    app.run()
