# import cv2
# from objectLogicArabic import analyze_image
# from time import sleep
# # Initialize the camera
# cap = cv2.VideoCapture(0)
# x, y, width, height = 300, 000, 700, 700  # Example values, adjust these as needed


# ret, frame = cap.read()
# frame_height = frame.shape[0]


# # Crop the frame to the ROI
# frame = frame[y:y+height, x:x+width]
# # Display the camera preview

# # cv2.imshow('Camera Preview', frame)
# if ret:
#     # Save the screenshot as "screenshot.png"
#     cv2.imwrite('sample.jpg', frame)
#     print("Screenshot saved as 'screenshot.png'")
#     analyze_image()

# # Release the camera and close all OpenCV windows
# cap.release()
# cv2.destroyAllWindows()
import face_recognition
import os, sys
import cv2
import numpy as np
import math
from multiprocessing import Process, Event, Manager, Lock
import pvporcupine
import pyaudio
from concurrent.futures import ThreadPoolExecutor
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
from ExtraTTS import tts
from ExtraMicrophone import stt
import NameExtract
import os
import cv2
import pyk4a
from pyk4a import Config, PyK4A
import numpy as np
import math


face_classifier = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_alt.xml"
    )
    #_______________________________________________________________________________

exit = False

def detect_bounding_box(vid,name_given):
    global take_screenshot
    name_counter = 0
    # gray_image = cv2.cvtColor(vid, cv2.COLOR_BGR2GRAY)
    gray_image = vid.copy()
    faces = face_classifier.detectMultiScale(gray_image, 1.1, 5, minSize=(40, 40))
    if len(faces) >0:
        for (x, y, w, h) in faces:
            # cv2.rectangle(vid, (x, y), (x + w, y + h), (0, 255, 0), 4)

           
            frame_copy = gray_image.copy()
            remaining_dimensionX = (x+w) - x
            remaining_dimensionY  = (y+h) - y
            adding_dimensionsX = 250 - remaining_dimensionX
            adding_dimensionsY = 250 - remaining_dimensionY            

            cropped_face = frame_copy[int(y - adding_dimensionsY/2):int(y+h+adding_dimensionsY/2),
                                    int(x - adding_dimensionsX/2):int(x+w+adding_dimensionsX/2)]

            # Save the face with a unique filename
            cv2.imwrite(f"faces/{name_given}.jpg", cropped_face) 
            # cv2.imwrite(f"Current/{name_given}.jpg", cropped_face) 
            global name
            # name = f"test-{name_counter}.jpg"
            # name_counter += 1
            global exit
            exit = True
            # Introduce a delay after saving the face
            # time.sleep(1)  # Adjust the sleep duration as needed

            # Reset take_screenshot after the delay
    return


# def main(name_given):
def save_name(name_given):


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

    while 1:
        capture = k4a.get_capture()
        # if first_frame is None and np.any(capture.color):
        #     first_frame = capture.color[:, :, :3]
        #     break
        # if np.any(capture.color):
        #     cv2.imshow("k4a", capture.color[:, :, :3])
            
        #     cv2.destroyAllWindows()
        #     break
        detect_bounding_box(capture.color[:,:,:3],name_given)
        if exit:
            break
    k4a.stop()

# if __name__ == "__main__":
#     main("TestName")




