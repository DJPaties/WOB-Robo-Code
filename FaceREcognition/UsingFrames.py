
import face_recognition
import os
import cv2
import numpy as np
import math
import pvporcupine
import pyaudio
from concurrent.futures import ThreadPoolExecutor
from ExtraTTS import tts
from ExtraMicrophone import stt
import NameExtract
import pyk4a
from pyk4a import Config, PyK4A
import numpy as np
import math
from testpyk4a import save_name

execute = ThreadPoolExecutor()

face_classifier = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_alt.xml"
    )
    #_______________________________________________________________________________

for currentImg in os.listdir("Current"):
    os.remove(os.path.join('Current',currentImg))


def get_input():
    # while True:
        #_______________________________________________________________________________
    known_face_encodings = []
    known_face_names = []
    for image in os.listdir('faces'):
        try:
            face_image = face_recognition.load_image_file(f'faces/{image}')
            face_encoding = face_recognition.face_encodings(face_image)[0]
            known_face_encodings.append(face_encoding)
            known_face_names.append(image)
        except IndexError as e:
            os.remove(os.path.join('faces',image))
    print(known_face_names)
    #_______________________________________________________________________________
    detection = False
    reply_message = ""
    keyword_path = 'C:/Users/WOB/Desktop/WOB-Robo-Code-main/RoboAppApplication/HeySam.ppn'
    access_key = 'hnVEQNTuN7caCisx8/8byB5z3xT1zsJ+ANs/NuVK2ZLWO9WNAJThdQ=='
    print("Entered stop check")

    def audio_callback(in_data, frame_count, time_info, status):
        nonlocal detection
        pcm = np.frombuffer(in_data, dtype=np.int16)
        keyword_index = handle.process(pcm)
        if keyword_index >= 0:
            detection = True
            print("Keyword Detected!")

        return None, pyaudio.paContinue

    print("1")

    handle = pvporcupine.create(keyword_paths=[keyword_path], access_key=access_key)

    pa = pyaudio.PyAudio()

    audio_stream = pa.open(
        rate=handle.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=handle.frame_length,
        stream_callback=audio_callback
    )

    audio_stream.start_stream()
    print("2")
    while not detection:
        pass

    audio_stream.stop_stream()
    audio_stream.close()

    pa.terminate()
    print("3")
    # exit_event.set()
    main("TestName",known_face_encodings,known_face_names)











def face_confidence(face_distance, face_match_threshold=0.6):
    range = (1.0 - face_match_threshold)
    linear_val = (1.0- face_distance) / (range *2.0)
    if face_distance > face_match_threshold:
        return str(round(linear_val * 100, 2)) + ''
    else:
        value = (linear_val + ((1.0- linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))) * 100
        return str(round(value, 2)) + ''
#_______________________________________________________________________________


exit = False

def detect_bounding_box(vid,name_given,known_face_encodings,known_face_names):
    global take_screenshot
    name_counter = 0
    # gray_image = cv2.cvtColor(vid, cv2.COLOR_BGR2GRAY)
    gray_image = vid.copy()
    faces = face_classifier.detectMultiScale(gray_image, 1.1, 5, minSize=(40, 40))
    if len(faces) >0:
        name_counter = 0
        for (x, y, w, h) in faces:
            # cv2.rectangle(vid, (x, y), (x + w, y + h), (0, 255, 0), 4)

           
            frame_copy = gray_image.copy()
            remaining_dimensionX = (x+w) - x
            remaining_dimensionY  = (y+h) - y
            # adding_dimensionsX = 250 - remaining_dimensionX
            # adding_dimensionsY = 250 - remaining_dimensionY            
            adding_dimensionsX = 250 - remaining_dimensionX
            adding_dimensionsY = 250 - remaining_dimensionY
            cropped_face = frame_copy[int(y - adding_dimensionsY/2):int(y+h+adding_dimensionsY/2),
                                    int(x - adding_dimensionsX/2):int(x+w+adding_dimensionsX/2)]

            # Save the face with a unique filename
            # cv2.imwrite(f"faces/{name_given}.jpg", cropped_face) 
            cv2.imwrite(f"Current/{name_given}{name_counter}.jpg", cropped_face) 
            global name
            name = f"test-{name_counter}.jpg"
            name_counter += 1
            global exit
            exit = True
            # Introduce a delay after saving the face
            # time.sleep(1)  # Adjust the sleep duration as needed

            # Reset take_screenshot after the delay
    #_______________________________________________________________________________
        face_names = []
        count_unknown = 0
        for imgs in os.listdir("Current"):
            x=face_recognition.load_image_file(os.path.join("Current",imgs))
            face_locations = face_recognition.face_locations(x)
            face_encodings = face_recognition.face_encodings(x,face_locations)
            # print("HI again")
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = 'Unknown'
                confidence = ''
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                    confidence = face_confidence(face_distances[best_match_index])
                face_names.append(f'{name} {confidence}')    
        
        print(face_names)
        response = ""
        count_unknown = 0
        if len(face_names)>1:
            for index,img in enumerate(face_names):
                img = img.split(" ")
                if img[0] == "Unknown":
                    count_unknown +=1
                elif index == len(face_names)-1 and float(img[1])>88:
                    response+=img[0]
                elif float(img[1])>88:
                    response+=img[0] + "and"
                else:
                    count_unknown+=1
        elif len(face_names)==1:
            checkName = face_names[0].split(" ")
            if checkName[0] == "Unknown" or float(checkName[1])<88:
                tts("Hey what is you name?","en-US")
                newName = stt("en")
                newName = NameExtract.get_name(newName,"en-US")
                if len(newName)==0:
                    while len(newName)==0:
                        tts("I didn't get your name Can you repeat?","en-US")
                        newName = stt("en")
                        newName = NameExtract.get_name(newName,"en-US")
                    
                    response += newName
                else:
                    response += newName
                    execute.submit(save_name(newName))
            else:
                response += checkName[0]    
        if count_unknown>1:
            print("Hey",response.replace(".jpg",""),"and there are people i don't know.") 
            tts("Hey"+response.replace(".jpg","")+"and there are people i don't know.", "en-US")        
        elif count_unknown== 1:
            print("Hey",response.replace(".jpg",""),"there is a person i dont't know I'll meet him later") 
            tts("Hey"+response.replace(".jpg","")+"there is a person i dont't know I'll meet him later", "en-US")        
        elif count_unknown == 0:
            print("Hey",response.replace(".jpg","")) 
            tts("Hey"+response.replace(".jpg",""), "en-US")        
       
                        
                        
    #_______________________________________________________________________________

    return


def main(name_given,known_face_encodings,known_face_names):


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
        detect_bounding_box(capture.color[:,:,:3],name_given,known_face_encodings,known_face_names)
        if exit:
            break
    k4a.stop()

if __name__ == "__main__":
    get_input()




