from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
import numpy as np
import cv2
import cvlib as cv
from scipy.spatial import distance
from ExtraTTS import tts
import random
 # load model
model = load_model(r"C:\Users\WOB\Desktop\WOB-Robo-Code-main\RoboAppApplication\gender_detection.model")

def detect_gender(language_code):

    # open webcam
    webcam = cv2.VideoCapture(0)

    classes = ['Man', 'Woman'] #the gender in english 
    if language_code == "en-US":
        result_label = {
                        "Man": ["You are a man","What a handsome man"] ,
                        "Woman": ["You are a women","Based on my experience you are a lovely women"]
                        }
    else:
        result_label = {
                        "Man": [" شو هَلْ زَلمي الحْلِوى هيْدَا","شَبْ حِلو إنْتَ ","يا هَلا بِأَبو الشَّباب"] ,
                        "Woman": ["إِنْتِ بِنِتْ زَيْ الأَمَرْ","ِْيا هَلا بالبَنُوت","إِنْتِ بِنِتْ"]
                        }
    

    label_frequency = {label: 0 for label in classes}

    # classes = ['ِزَلَمِي', 'بِنِتْ'] #the gender in arabic 
    
    new_label = ""

    # loop through frames
    while webcam.isOpened():
        

        # read frame from webcam
        status, frame = webcam.read()

        # apply face detection
        faces, confidences = cv.detect_face(frame)

        # track the closest face
        closest_face_idx = None
        min_distance = float('inf')

        for idx, f in enumerate(faces):
            # get corner points of face rectangle
            (startX, startY) = f[0], f[1]
            (endX, endY) = f[2], f[3]

            # calculate the centroid of the face rectangle
            face_center = (startX + endX) // 2, (startY + endY) // 2

            # calculate the Euclidean distance from the center of the frame (assuming camera is at the center)
            dist = distance.euclidean((frame.shape[1] // 2, frame.shape[0] // 2), face_center)

            # update closest face if the current face is closer
            if dist < min_distance:
                min_distance = dist
                closest_face_idx = idx

        # loop through detected faces
        for idx, f in enumerate(faces):
            if idx == closest_face_idx:
                # draw rectangle over the closest face
                (startX, startY) = f[0], f[1]
                (endX, endY) = f[2], f[3]
                cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)

                # crop the detected face region
                face_crop = np.copy(frame[startY:endY, startX:endX])

                if (face_crop.shape[0]) < 10 or (face_crop.shape[1]) < 10:
                    continue

                # preprocessing for gender detection model
                face_crop = cv2.resize(face_crop, (96, 96))
                face_crop = face_crop.astype("float") / 255.0
                face_crop = img_to_array(face_crop)
                face_crop = np.expand_dims(face_crop, axis=0)

                # apply gender detection on face
                conf = model.predict(face_crop)[0]

                # get label with max accuracy
                idx = np.argmax(conf)
                label = classes[idx]
                label_frequency[label] += 1
                label = "{}: {:.2f}%".format(label, conf[idx] * 100)

                Y = startY - 10 if startY - 10 > 10 else startY + 10

                # write label and confidence above face rectangle
                cv2.putText(frame, label, (startX, Y), cv2.FONT_HERSHEY_SIMPLEX,
                            0.7, (0, 255, 0), 2)
                print("Label Frequencies:", label_frequency)
                print("Total Frames Processed:", sum(label_frequency.values()))
        if sum(label_frequency.values())>=10:
        # Find the emotion with the maximum frequency
            max_label = max(label_frequency, key=label_frequency.get)
            max_frequency = label_frequency[max_label]
            print("Gender with the Largest Frequency:", max_label, "(", max_frequency, "times)")
            chosen_value = random.choice(result_label[max_label])
            tts(chosen_value,"ar-LB")    
    # label_frequency = {label: 0 for label in emotion_labels}
            break
                # if new_label != label:  # test if the previos emotion is the same as the current to not repeat the speech said
                #     new_label = label
                #   # understand , create , and start the audio taken in the language needed to be spoken and the word
                #     if label in result_label:
                #         chosen_value = random.choice(result_label[label])
                #         tts(chosen_value, "ar-LB")
                
                

        # display output
        cv2.imshow("gender detection", frame)
       

        # press "Q" to stop
        if cv2.waitKey(1) & 0xFF == ord('q') :
            break

    # release resources
    webcam.release()
    cv2.destroyAllWindows()

# if __name__ == "__main__":
#     detect_gender()
