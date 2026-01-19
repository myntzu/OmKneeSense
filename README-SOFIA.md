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

# 3. Run the following commands to install the library required 
** For AI to transform raw sensor RGB frames into localized force data
>>> pip install tqdm
>>> pip install configobj

# 4. Run script to process frames
>>> python main.py --phase run --config_file configs/o3f_hmhm2_bg_qnoise_mix4_nl_n_t_ds3.ini --vid_dir data/vids/knee_test --amplification_factor 10 --out_dir data/output/knee_magnified