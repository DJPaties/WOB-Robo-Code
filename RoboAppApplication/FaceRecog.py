import cv2
import pvporcupine
import pyaudio
import numpy as np
from multiprocessing import Process, Event
import cv2
from simple_facerec_FORFACERECOG import SimpleFacerec
import ExtraMicrophone
import pyaudio
import pvporcupine
import numpy as np
from multiprocessing import Process, Event, Manager, Lock
import ExtraTTS
import string
import os
import random
name_frame_lock = Lock()


def start(known_names,exit_event,get_frame, name_frame):
    cap = cv2.VideoCapture(0)
    sfr = SimpleFacerec()
    sfr.load_encoding_images("images/")
    
    while True:
        ret, frame = cap.read()
        # Detect Faces
        face_locations, face_names = sfr.detect_known_faces(frame)
        for face_loc, name in zip(face_locations, face_names):
            y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

            cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
            # known_face = name
            known_names[:] = face_names
        print(known_names)
        # Check if get_frame is True and capture a screenshot
        # print(known_names)
        # if get_frame.value:
        #     # with name_frame.get_lock():
        #     with name_frame_lock:
        #         current_value = name_frame.value.decode('utf-8')
        #     capture_and_save_screenshot(sfr,frame, f"images/{current_value}.jpg")
        #     get_frame.value = False
        if get_frame.value:
            with name_frame_lock:
                current_value = name_frame.value.decode('utf-8')
            # Capture the screenshot only around detected faces
            frame_copy = frame.copy()
            face_locations, _ = sfr.detect_known_faces(frame_copy)
            for face_loc in face_locations:
                y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
                # Adjust the margin to include more or less of the surrounding area
                margin = 20
                y1 = max(0, y1 - margin)
                x1 = max(0, x1 - margin)
                y2 = min(frame_copy.shape[0], y2 + margin)
                x2 = min(frame_copy.shape[1], x2 + margin)
                # Crop the frame around the detected face
                face_frame = frame_copy[y1:y2, x1:x2]
                # Save the cropped frame to an image file
                # cv2.imwrite(f"images/{current_value}.jpg", face_frame)
                file_path=f"images/{current_value}.jpg"
                if os.path.exists(file_path):
                    characters = string.ascii_letters + string.digits
                    characters =  ''.join(random.choice(characters) for _ in range(3))
                    cv2.imwrite(f"images/{characters}-{current_value}.jpg",face_frame)
                else:
                    cv2.imwrite(f"images/{current_value}.jpg", face_frame)
            get_frame.value = False 


        cv2.imshow("Frame", frame)

        key = cv2.waitKey(1)
        if key == ord('q') or exit_event.is_set():
            break
        elif key == ord('s'):
            get_frame = True
        

def get_input(exit_event,known_names, get_frame, name_frame):
    import NameExtract
    # while True:
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
    
    # msg = ExtraMicrophone.stt('en-US')
    # if msg == "hello":
    print(known_names)
    if len(known_names)>1:
        for n in known_names:
            reply_message = ""
            count_unknown = known_names.count('Unknown')
            new_known_list = [item for item in known_names if item != 'Unknown']
            for index, n in enumerate(new_known_list):
                if index == len(new_known_list) - 1:
                    reply_message += f"{n}"
                else:
                    reply_message += f"{n},and"
            if count_unknown >=2: 
                reply_message+= "and there are people i don't know. I will get to know you when we speak alone."
            elif count_unknown == 1:
                reply_message += "and there is one person i don't know.I will get to know you when we speak alone."
    elif len(known_names)==1:
        if known_names[0]=="Unknown":
            reply_message = "Hey there, what is your name"
            print(reply_message)
            check_name = name_frame.value.decode('utf-8')
            while not check_name:
                msg = ExtraMicrophone.stt('en-US')
                name= NameExtract.get_name(msg,"en-US")
                with name_frame_lock:
                    name_frame.value = name.encode('utf-8')
                    check_name = name
                print(name_frame)
            reply_message = f"{check_name}"
            get_frame.value = True
        else :
            reply_message = f"{known_names[0]}"
            
    else:
        reply_message = "How are you"
    reply_message = "Hello, "+ reply_message
    print(reply_message)
    ExtraTTS.tts(reply_message,"en-US")
    exit_event.set()


def run():
    exit_event = Event()
    manager = Manager()

    # Use the manager to create shared variables
    get_frame = manager.Value('b', False)
    name_frame = manager.Value('c', b"")
    known_names = manager.list([])
    # start(known_names,exit_event,get_frame, name_frame)
    p = Process(target=start, args=(known_names,exit_event,get_frame,name_frame,))
    p.start()
    # get_input(exit_event,known_names, get_frame, name_frame)
        # Start the input process
    p_input = Process(target=get_input, args=(exit_event, known_names, get_frame, name_frame))
    p_input.start()
    
    p.join()
    p_input.join()
    print("After Process")

if __name__ == "__main__":
    run()
