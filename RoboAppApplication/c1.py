import subprocess


eye_tracking_process = subprocess.Popen(["python", "face_detect.py"])
eye_tracking_process.communicate()