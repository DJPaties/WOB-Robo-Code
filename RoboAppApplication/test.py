# import cv2
# import pvporcupine
# import pyaudio
# import numpy as np
# from multiprocessing import Process, Event
# import cv2
# from simple_facerec_FORFACERECOG import SimpleFacerec
# import ExtraMicrophone
# import pyaudio
# import pvporcupine
# import numpy as np
# from multiprocessing import Process, Event, Manager, Lock
# import ExtraTTS

# detection = False
# name_frame_lock = Lock()


# def capture_and_save_screenshot(sfr,frame, filename):
#     num_of_images = 5
#     img_nb = 0
#     # Create a copy of the frame to avoid modifying the original frame
#     frame_copy = frame.copy()

#     # Detect Faces
#     while img_nb<num_of_images:
#         face_locations, face_names = sfr.detect_known_faces(frame_copy)
#         for face_loc, name in zip(face_locations, face_names):
#             y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

#             # Draw rectangles on the copy of the frame
#             # cv2.rectangle(frame_copy, (x1, y1), (x2, y2), (0, 0, 200), 4)

#         # Save the copy without rectangles
#         cv2.imwrite(f"{filename}-{img_nb}", frame_copy)
#         img_nb+=1



# def start(known_names,exit_event,get_frame, name_frame):
#     cap = cv2.VideoCapture(0)
#     sfr = SimpleFacerec()
#     sfr.load_encoding_images("images/")
    
#     while True:
#         ret, frame = cap.read()
#         # Detect Faces
#         face_locations, face_names = sfr.detect_known_faces(frame)
#         for face_loc, name in zip(face_locations, face_names):
#             y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

#             cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
#             # known_face = name
#             known_names[:] = face_names
#         #print(known_names)
#         # Check if get_frame is True and capture a screenshot
#         # #print(known_names)
#         # if get_frame.value:
#         #     # with name_frame.get_lock():
#         #     with name_frame_lock:
#         #         current_value = name_frame.value.decode('utf-8')
#         #     capture_and_save_screenshot(sfr,frame, f"images/{current_value}.jpg")
#         #     get_frame.value = False
#         if get_frame.value:
#             with name_frame_lock:
#                 current_value = name_frame.value.decode('utf-8')
#             # Capture the screenshot without using a separate function
#                 num_of_images = 5
#                 img_nb = 0
#                 # Create a copy of the frame to avoid modifying the original frame
#                 frame_copy = frame.copy()

#                 # Detect Faces
#                 while img_nb<num_of_images:
#                     face_locations, face_names = sfr.detect_known_faces(frame_copy)
#                     for face_loc, name in zip(face_locations, face_names):
#                         y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

#                         # Draw rectangles on the copy of the frame
#                         # cv2.rectangle(frame_copy, (x1, y1), (x2, y2), (0, 0, 200), 4)

#                     # Save the copy without rectangles
#                     cv2.imwrite(f"{current_value}-{img_nb}", frame_copy)
#                     img_nb+=1

#         cv2.imshow("Frame", frame)

#         key = cv2.waitKey(1)
#         if key == ord('q') or exit_event.is_set():
#             break
#         elif key == ord('s'):
#             get_frame = True
        

# def get_input(exit_event,known_names, get_frame, name_frame):
#     import NameExtract
#     # while True:
#     detection = False
#     reply_message = ""
#     keyword_path = 'C:/Users/WOB/Desktop/WOB-Robo-Code-main/RoboAppApplication/HeySam.ppn'
#     access_key = 'zBapjwgbd0M1f7jDBHxkKG52DLToh8gCLuo06ffIom43uhFNJhLPpw=='
#     #print("Entered stop check")

#     def audio_callback(in_data, frame_count, time_info, status):
#         nonlocal detection
#         pcm = np.frombuffer(in_data, dtype=np.int16)
#         keyword_index = handle.process(pcm)
#         if keyword_index >= 0:
#             detection = True
#             #print("Keyword Detected!")

#         return None, pyaudio.paContinue

#     #print("1")

#     handle = pvporcupine.create(keyword_paths=[keyword_path], access_key=access_key)

#     pa = pyaudio.PyAudio()

#     audio_stream = pa.open(
#         rate=handle.sample_rate,
#         channels=1,
#         format=pyaudio.paInt16,
#         input=True,
#         frames_per_buffer=handle.frame_length,
#         stream_callback=audio_callback
#     )

#     audio_stream.start_stream()
#     #print("2")
#     while not detection:
#         pass

#     audio_stream.stop_stream()
#     audio_stream.close()

#     pa.terminate()
#     #print("3")
    
#     # msg = ExtraMicrophone.stt('en-US')
#     # if msg == "hello":
#     #print(known_names)
#     if len(known_names)>1:
#         for n in known_names:
#             reply_message = ""
#             count_unknown = known_names.count('Unknown')
#             new_known_list = [item for item in known_names if item != 'Unknown']
#             for n in new_known_list:
#                 reply_message += f"{n},and "
#             if count_unknown >=2: 
#                 reply_message+= "and there are people i don't know. I will get to know you when we speak alone."
#             elif count_unknown == 1:
#                 reply_message += "and there is one person i don't know.I will get to know you when we speak alone."
#     elif len(known_names)==1:
#         if known_names[0]=="Unknown":
#             reply_message = "Hey there, what is your name"
#             #print(reply_message)       
#             ExtraTTS.tts(reply_message,"en-US")
#             check_name = name_frame.value.decode('utf-8')
#             while not check_name:
#                 msg = ExtraMicrophone.stt('en-US')
#                 name= NameExtract.get_name(msg,"en-US")
#                 with name_frame_lock:
#                     name_frame.value = name.encode('utf-8')
#                     check_name = name
#                 #print(name_frame)
#             reply_message = f"{check_name}"
#             get_frame.value = True
#         else :
#             reply_message = f"{known_names[0]}"
            
#     else:
#         reply_message = "How are you"
#     reply_message = "Hello, "+ reply_message
#     #print(reply_message)
#     ExtraTTS.tts(reply_message,"en-US")
#     exit_event.set()


# def run():
#     exit_event = Event()
#     manager = Manager()

#     # Use the manager to create shared variables
#     get_frame = manager.Value('b', False)
#     name_frame = manager.Value('c', b"")
#     known_names = manager.list([])
#     # start(known_names,exit_event,get_frame, name_frame)
#     p = Process(target=start, args=(known_names,exit_event,get_frame,name_frame,))
#     p.start()
#     # get_input(exit_event,known_names, get_frame, name_frame)
#         # Start the input process
#     p_input = Process(target=get_input, args=(exit_event, known_names, get_frame, name_frame))
#     p_input.start()
    
#     p.join()
#     p_input.join()
#     #print("After Process")

# if __name__ == "__main__":
#     run()
import cv2
import time

def capture_enlarged_face_screenshots(camera_index=0, num_screenshots=5, save_path="screenshots", haarcascade_path="haarcascade_frontalface_default.xml", enlargement_factor=1.5):
    # Load the Haar Cascade classifier for face detection
    face_cascade = cv2.CascadeClassifier(haarcascade_path)

    # Open the camera
    cap = cv2.VideoCapture(camera_index)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    # Create the save path if it doesn't exist
    import os
    os.makedirs(save_path, exist_ok=True)

    screenshot_count = 0

    while screenshot_count < num_screenshots:
        ret, frame = cap.read()

        if not ret:
            print(f"Error: Could not read frame {screenshot_count + 1}.")
            break

        # Convert the frame to grayscale for face detection
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces using the Haar Cascade classifier
        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5)

        # Save the first detected face as the screenshot
        if len(faces) > 0:
            x, y, w, h = faces[0]

            # Enlarge the bounding box
            x = max(0, int(x - (enlargement_factor - 1) * w / 2))
            y = max(0, int(y - (enlargement_factor - 1) * h / 2))
            w = int(w * enlargement_factor)
            h = int(h * enlargement_factor)

            # Draw the enlarged bounding box on the frame
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Show the preview
            cv2.imshow("Preview", frame)

            # Save the enlarged face as the screenshot
            face_roi = gray_frame[y:y+h-10, x:x+w-10]
            screenshot_path = os.path.join(save_path, f"screenshot_{screenshot_count + 1}.jpg")
            cv2.imwrite(screenshot_path, face_roi)
            print(f"Enlarged Face Screenshot {screenshot_count + 1} saved at {screenshot_path}")
            screenshot_count += 1

        # Add a short delay between frames
        time.sleep(0.01)

        # Break the loop if the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and destroy the window
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_enlarged_face_screenshots()




