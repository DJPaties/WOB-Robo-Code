import cv2
from simple_facerec import SimpleFacerec
import numpy as np
from keras.models import load_model
from keras.preprocessing.image import img_to_array
from ExtraTTS import tts
import random
# Encode faces from a folder
sfr = SimpleFacerec()
classifier = load_model("model.h5")
face_classifier = cv2.CascadeClassifier(
    r"C:\Users\WOB\Desktop\WOB-Robo-Code-main\RoboAppApplication\haarcascade_frontalface_default.xml"
)
# sfr.load_encoding_images("images/")
# Load Camera
cap = cv2.VideoCapture(1)

def mood(languageCode):
    if languageCode == "en-US":
        result_label = {
                        "Angry": ["Bro why are you angry","Why are you angry?","You look mad."] ,
                        "Discusted": ["Why are you discusted"] ,
                        "Afraid": ["ْWhy are you afraid","You look so afraid","Calm down you look afraid"],
                        "Happy": ["What a beautiful smile","You have a lovely smile","You look lovely with that smile"],
                        "Neutral": ["Why  the neutral face be happy","Show some emotions"],
                        "Sad": ["Who made you sad","Who made you feel sad","Don't be sad try to smile"],
                        "Shocked": ["Why are you shocked","WHat did you see you look shocked"],
                        }
    else: 
        result_label = {
                        "Angry": [" خَيِّيِ لِيِ مْعَصِّب"," شو مَالَكْ مْعَصِّب","إِنْتَ كتير مْعَصِبْ"] ,
                        "Discusted": ["ْْ أُفْ شُو أَرْفيِن","لي أَرْفينْ","شُو بيك أَرْفين يا خِيِّ"] ,
                        "Afraid": ["ْ حَبِبي  لِيِ خَيْفيِن","ِخَيْفيِنْ إِِنْتَ شي ","ما تخَافْ حَبيبيِ"],
                        "Happy": ["شو هَلْ بَسميِ الحِلوي يا حلُو","يٌأبُرني هل بَسْمي","خَيْ شُو مَبْصُوطْ"],
                        "Neutral": ["ضَحَكْلَكْ نِتْفِي يا حِلو","شو ميلَكْ مْنَشفا", "إِنْتَ شُبيكْ نِشِفْ"],
                        "Sad": ["بَدِيش شوفَكْ زَعْلينْ","ْلي الحِلو زَعْلِين","ما دَلَّكْ زَعْلِيِنْ حَبِبِي"],
                        "Shocked": ["لي مَصْضُوم فِيَّ","حاجْتَكْ مَصضُوم لُوُوُوُوُوُوُوُو", "شُو بِيك مَصْضُومْ"],
                        }
    emotion_labels = [
        "Angry",
        "Discusted",
        "Afraid",
        "Happy",
        "Neutral",
        "Sad",
        "Shocked"
    ]

    # Initialize a dictionary to store label frequencies
    label_frequency = {label: 0 for label in emotion_labels}

    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray)

        # Detect Faces
        face_locations, face_names = sfr.detect_known_faces(frame)
        for face_loc, name in zip(face_locations, face_names):
            y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

            cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)
            roi_gray = gray[y1: y1 + x1, x1: y2 + x2]
            roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)
            if np.sum([roi_gray]) != 0:
                roi = roi_gray.astype("float") / 255.0
                roi = img_to_array(roi)
                roi = np.expand_dims(roi, axis=0)

                prediction = classifier.predict(roi)[0]
                label = emotion_labels[prediction.argmax()]

                # Increment the frequency count for the detected label
                label_frequency[label] += 1

                print(label)

        print("Label Frequencies:", label_frequency)
        print("Total Frames Processed:", sum(label_frequency.values()))
        if sum(label_frequency.values())>=5:
            # Find the emotion with the maximum frequency
            max_label = max(label_frequency, key=label_frequency.get)
            max_frequency = label_frequency[max_label]
            print("Emotion with the Largest Frequency:", max_label, "(", max_frequency, "times)")
            chosen_value = random.choice(result_label[max_label])
            tts(chosen_value, languageCode)    
            # label_frequency = {label: 0 for label in emotion_labels}
            break

        cv2.imshow("Frame", frame)

        key = cv2.waitKey(1)
        if key == 27:
            break
        
    cap.release()
    cv2.destroyAllWindows()

# mood()