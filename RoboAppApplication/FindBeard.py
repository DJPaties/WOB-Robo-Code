import cv2
from objectLogic import analyze_image
from time import sleep
# Initialize the camera
cap = cv2.VideoCapture(0)
x, y, width, height = 300, 000, 700, 700  # Example values, adjust these as needed

import os
import os, io
from google.cloud import vision
from google.cloud.vision_v1 import types
import json

beard_detect = False
#the JSON file you downloaded in step 5 above
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'object.json'

# Instantiates a client
client = vision.ImageAnnotatorClient()

#set this thumbnail as the url
# image = types.Image()
# image.source.image_uri = 'https://i.ytimg.com/vi/UQQHSbeIaB0/maxresdefault.jpg'

with open('names.json', 'r') as json_file:
    data = json.load(json_file)
    object_names = data['object_names']

def analyze_image(request_from_object):
    file_name = 'sample.jpg'
    image_path = os.path.join('', file_name)

    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()

    image =types.Image(content=content)
    #### LABEL DETECTION ######
    detected_objects = ""
    response_label = client.label_detection(image=image)

    if request_from_object == "FindBeard":
        
        for label in response_label.label_annotations:
            print({'label': label.description, 'score': label.score})
            if label.description == "Beard" or label.description == "Facial hair":
                # print("yes, I see that you have a nice beard.")
                global beard_detect
                beard_detect = True
                break
        if beard_detect:
            print("Yes I can see you have a nice beard.")
        else:
            print("No i don't see you have a beard or any signs of it.")


# Capture a frame from the camera
ret, frame = cap.read()
frame_height = frame.shape[0]

# Adjust the Y-coordinate to invert the Y-axis
# y = frame_height - y - height
# print(y)
# Crop the frame to the ROI
frame = frame[y:y+height, x:x+width]
# Display the camera preview

# cv2.imshow('Camera Preview', frame)
if ret:
     # Save the screenshot as "screenshot.png"
    cv2.imwrite('sample.jpg', frame)
    print("Screenshot saved as 'screenshot.png'")
    analyze_image("FindBeard")
# Wait for a key press 
    # analyze_image()
# # If 'q' is pressed, quit the program
#     key = cv2.waitKey(1)
#     if key & 0xFF == ord('q'):
#         break

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
