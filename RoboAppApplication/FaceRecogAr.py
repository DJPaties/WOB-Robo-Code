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


name_frame_lock = Lock()


def capture_and_save_screenshot(sfr,frame, filename):
    # Create a copy of the frame to avoid modifying the original frame
    frame_copy = frame.copy()

    # Detect Faces
    face_locations, face_names = sfr.detect_known_faces(frame_copy)
    for face_loc, name in zip(face_locations, face_names):
        y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

        # Draw rectangles on the copy of the frame
        # cv2.rectangle(frame_copy, (x1, y1), (x2, y2), (0, 0, 200), 4)

    # Save the copy without rectangles
    cv2.imwrite(filename, frame_copy)



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
            # Capture the screenshot without using a separate function
            frame_copy = frame.copy()
            face_locations, _ = sfr.detect_known_faces(frame_copy)
            for face_loc in face_locations:
                y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
                # cv2.rectangle(frame_copy, (x1, y1), (x2, y2), (0, 0, 200), 4)
            cv2.imwrite(f"images/{current_value}.jpg", frame_copy)
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
    keyword_path_arabic = "C:/Users/WOB/Desktop/WOB-Robo-Code-main/RoboAppApplication/HeySamar.ppn"

    access_key = 'zBapjwgbd0M1f7jDBHxkKG52DLToh8gCLuo06ffIom43uhFNJhLPpw=='
    model_path = 'C:/Users/WOB/Desktop/WOB-Robo-Code-main/RoboAppApplication/porcupine_params_ar.pv'
    print("Entered wake check")
    detection= False
    def audio_callback(in_data, frame_count, time_info, status):
        pcm = np.frombuffer(in_data, dtype=np.int16)
        keyword_index = handle.process(pcm)
        if keyword_index >= 0:
            nonlocal detection
            detection = True
            print("Keyword Detected!")
        
        return None, pyaudio.paContinue


    print("language is arabic")
    handle = pvporcupine.create(keyword_paths=[keyword_path_arabic], access_key=access_key,model_path=model_path)
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

    while not detection:
        pass
    print("after detect keyword")

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
            for n in new_known_list:
                reply_message += f"{n},و"
            if count_unknown >=2: 
                reply_message+= "في أَشْخاَصْ مَا بَعْرِفَ. بِتْعَرَّفْ عَلَيَ لَمَّا نْكُونْ لَحالْنَا."
            elif count_unknown == 1:
                reply_message += "في شَخِصْ مَا بَعْرِفُ. بِتْعَرَّفْ عَلِىْ لَمَّا نْكُونْ لَحالْنَا."
    elif len(known_names)==1:
        if known_names[0]=="Unknown":
            reply_message = " حبيبي  شو اسمك؟"
            print(reply_message)
            ExtraTTS.tts(reply_message,"ar-LB")
            check_name = name_frame.value.decode('utf-8')
            while not check_name:
                msg = ExtraMicrophone.stt('ar-LB')
                name= NameExtract.get_name(msg,"ar-LB")
                with name_frame_lock:
                    name_frame.value = name.encode('utf-8')
                    check_name = name
                print(name_frame)
            reply_message = f"{check_name}"
            get_frame.value = True
        else :
            reply_message = f"{known_names[0]}"
            
    else:
        reply_message = "يا هلَا"
    reply_message = "مرحبَ, "+ reply_message
    print(reply_message)
    ExtraTTS.tts(reply_message,"ar-LB")
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
