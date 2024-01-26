import cv2
import numpy as np
import pyk4a
from pyk4a import Config, PyK4A
from simple_facerec_FORFACERECOG import SimpleFacerec
import ExtraTTS
import ExtraMicrophone
from NameExtract import get_name
import random
import os
import string

def NameNew(languagecode):
    if languagecode == "en-US":
        list = ["What is your name", "Remind of your name again"]
        ExtraTTS.tts(random.choice(list), 'en-US')
    else:
        list = ["زَكِّرْنِ  بإِسْمَكْ", "زَكِّرْنِ  شُو إِسْمَكْ", "طَيِّبْ، شُو إِسْمَكْ"]
        ExtraTTS.tts(random.choice(list), 'ar-LB')
    newName = ExtraMicrophone.stt(languagecode)
    newName = get_name(newName, languagecode)
    while not newName:
        newName = ExtraMicrophone.stt(languagecode)
        newName = get_name(newName, languagecode)

    main(newName)

def main(newName):
    sfr = SimpleFacerec()
    k4a = PyK4A(
        Config(
            color_resolution=pyk4a.ColorResolution.RES_720P,
            depth_mode=pyk4a.DepthMode.NFOV_UNBINNED,
            synchronized_images_only=True,
        )
    )
    k4a.start()

    # getters and setters directly get and set on device
    k4a.whitebalance = 4500
    assert k4a.whitebalance == 4500
    k4a.whitebalance = 4510
    assert k4a.whitebalance == 4510

    # Get the first frame
    first_frame = None

    while True:
        capture = k4a.get_capture()
        if first_frame is None and np.any(capture.color):
            first_frame = capture.color[:, :, :3]

        if np.any(capture.color):
            face_locations, _ = sfr.detect_known_faces(capture.color[:, :, :3])
        if face_locations.size > 0:  # Check if the array is not empty
                for face_loc in face_locations:
                    y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
                    # Adjust the margin to include more or less of the surrounding area
                    margin = 20
                    y1 = max(0, y1 - margin)
                    x1 = max(0, x1 - margin)
                    y2 = min(capture.color[:, :, :3].shape[0], y2 + margin)
                    x2 = min(capture.color[:, :, :3].shape[1], x2 + margin)
                    # Crop the frame around the detected face
                    face_frame = capture.color[:, :, :3][y1:y2, x1:x2]
                    # Save the cropped frame to an image 
                    file_path=f"images/{newName}.jpg"
                    if os.path.exists(file_path):
                        characters = string.ascii_letters + string.digits
                        characters =  ''.join(random.choice(characters) for _ in range(3))
                        cv2.imwrite(f"images/{characters}-{newName}.jpg",face_frame)
                    else:
                        cv2.imwrite(f"images/{newName}.jpg", face_frame)

                cv2.destroyAllWindows()
                break

    k4a.stop()

if __name__ == "__main__":
    NameNew("ar-LB")
