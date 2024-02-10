import face_recognition
import os, sys
import cv2
import numpy as np
import math
from multiprocessing import Process, Event, Manager, Lock
import pvporcupine
import pyaudio

def get_input(exit_event):
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
    exit_event.set()


def face_confidence(face_distance, face_match_threshold=0.6):
    range = (1.0 - face_match_threshold)
    linear_val = (1.0- face_distance) / (range *2.0)
    if face_distance > face_match_threshold:
        return str(round(linear_val * 100, 2)) + '%'
    else:
        value = (linear_val + ((1.0- linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))) * 100
        return str(round(value, 2)) + '%'
    
class FaceRecognition:
    face_locations = []
    face_encodings = []
    face_names = []
    known_face_encodings = []
    known_face_names = []
    process_current_frame = True
    def __init__(self):
        self.encode_faces()
        
        
    def encode_faces(self):

        for image in os.listdir('faces'):
            face_image = face_recognition.load_image_file(f'faces/{image}')
            face_encoding = face_recognition.face_encodings(face_image)[0]
            self.known_face_encodings.append(face_encoding)
            self.known_face_names.append(image)
        print(self.known_face_names)
        
    def run_recognition(self,exit_event):
        video_capture = cv2.VideoCapture(0)
        if not video_capture.isOpened():
            sys.exit('Video source not found ... ')
        while True:
            ret, frame = video_capture.read()
            if self.process_current_frame:
                # print("HI")
            # Resize and change the frame to RGB
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                rgb_small_frame = small_frame[:, :, ::- 1]
                # Find all faces in the current frame
                self.face_locations = face_recognition.face_locations(rgb_small_frame)
                self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)
                self.face_names = []
                # print("HI again")
                for face_encoding in self.face_encodings:
                    matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                    name = 'Unknown'
                    confidence = 'Unknown'
                    face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = self.known_face_names[best_match_index]
                        confidence = face_confidence(face_distances[best_match_index])
                    self.face_names.append(f'{name} ({confidence})')
            self.process_current_frame = not self.process_current_frame
            # Display annotations
            for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), -1)
                cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)
            cv2.imshow('Face Recognition', frame)
            # print("hello")
            if cv2.waitKey(1) == ord('q'):
                
                break
        video_capture.release()
        cv2.destroyAllWindows()
        return self.face_names
        
if __name__ == '__main__':
    exit_event = Event()
    manager = Manager()
    fr = FaceRecognition()
    
    stop_frame = manager.Value('b',False)
    
    p = Process(target=fr.run_recognition,args=(exit_event,))
    p.start()
    
    p_input = Process(target=get_input, args=(exit_event,))
    p_input.start()
    print(p)