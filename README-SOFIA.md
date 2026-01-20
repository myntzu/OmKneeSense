# DOCUMENTATION AS OF 19/01/2026 (SOFIA)

# 1. Ensure venv_mag is active/present in the folder directory.
*If not found, run the following command:
>>> python -m venv venv_mag

# 2. Activate it (The prompt should now show (venv_mag) in green)
>>> .\venv_mag\Scripts\activate

** NOTE: If error pops up (e.g. SecurityError) during this stage, run the following command:
>>> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
** REACTIVATE: *venv_mag should appear green in the explorer
>>> .\venv_mag\Scripts\activate

# 3. Run the following commands to install the libraries required *IMPORTANT*
** For AI to transform raw sensor RGB frames into localized force data
>>> pip install tqdm
>>> pip install configobj
>>> pip install tensorflow tqdm configobj tf_slim opencv-python
>>> pip install scipy 
>>> pip install setproctitle
>>> pip install opencv-python numpy

# 4. Extract frames from sample video (.mp4 to .png)
>>> python extract_frames.py --video_path data/vids/knee-vid.mp4 --out_dir data/vids/knee_test

# 5. Run script to process frames [DYNAMIC MODE] --- REMINDER TO CHANGE AMPLITUDE FACTOR AS REQUIRED (e.g. 10)
>>> (10 AMP_FACTOR): python main.py --phase run --config_file configs/o3f_hmhm2_bg_qnoise_mix4_nl_n_t_ds3.conf --vid_dir data/vids/knee_test --amplification_factor 10 --out_dir data/output/knee_magnified
>>> (50 AMP_FACTOR): python main.py --phase run --config_file configs/o3f_hmhm2_bg_qnoise_mix4_nl_n_t_ds3.conf --vid_dir data/vids/knee_test --amplification_factor 50 --out_dir data/output/knee_magnified_50

# Stitch magnified frames into video (optional*)
>>> python stitch_vid.py

# 6. Knee Tracking Data (force localization)
>>> python track_knee.py