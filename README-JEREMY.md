# DOCUMENTATION AS OF 27/01/2026 (JEREMY)

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
>>> pip install -r requirements.txt

# 4. Correct fisheye lens and manual crop to visuotactile gel surface
>>> python videoInputProcess/correction.py

# 4. Extract frames from corrected video (.mp4 to .png)
>>> python extract_frames.py --video_path videoInputProcess/knee-vid-ACcorrected.mp4 --out_dir data/vids/knee_test_corrected

# 5. Run script to process frames [DYNAMIC MODE] --- REMINDER TO CHANGE AMPLITUDE FACTOR AS REQUIRED (e.g. 10)
>>> (10 AMP_FACTOR): python main.py --phase run --config_file configs/o3f_hmhm2_bg_qnoise_mix4_nl_n_t_ds3.conf --vid_dir data/vids/knee_test_corrected --amplification_factor 10 --out_dir data/output/knee_magnified_corrected
>>> (50 AMP_FACTOR): python main.py --phase run --config_file configs/o3f_hmhm2_bg_qnoise_mix4_nl_n_t_ds3.conf --vid_dir data/vids/knee_test_corrected --amplification_factor 10 --out_dir data/output/knee_magnified_corrected50

# Stitch magnified frames into video (optional*)
>>> python stitch_vid.py