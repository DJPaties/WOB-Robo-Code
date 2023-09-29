import cv2
import random
import mediapipe as mp
from TTS import tts
import pvporcupine
import pyaudio
import numpy as np
from concurrent.futures import ThreadPoolExecutor
executor = ThreadPoolExecutor()
detection = False
exit_flag = True
def wake_check():
    global exit_flag
    keyword_path = r'C:\Users\wot\Desktop\RoboAppApplication\stop_mimick.ppn'
    access_key = '+VvLL7ztuNRvOkGOd6ou3qjp3t7emg4tBUuyTkChlQjOZL6ugCLblw=='

    print("Entered stop check")
    # detection= False
    def audio_callback(in_data, frame_count, time_info, status):
        global detection
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
    print("All CLEAR")
    print(detection)
    exit_flag = False
    # updateface()
    # lang_change = False
    # tts("Okay I'm stopping counting your finger")
    print('exit')
    exit(0)

executor.submit(wake_check)



x, y, width, height = 300, 000, 700, 700 
cap = cv2.VideoCapture(0)
mp_Hands = mp.solutions.hands
hands = mp_Hands.Hands()
mpDraw = mp.solutions.drawing_utils
finger_Coord = [(8, 6), (12, 10), (16, 14), (20, 18)]
thumb_Coord = (4,2)
newUpcount = 0

while True:
    
    success, image = cap.read()
    image_height = image.shape[0]
    image = image[y:y+height, x:x+width]
    RGB_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(RGB_image)
    multiLandMarks = results.multi_hand_landmarks 
    # if exit_flag:
    #         break
    if multiLandMarks:
        handList = []
        for handLms in multiLandMarks:
            mpDraw.draw_landmarks(image, handLms, mp_Hands.HAND_CONNECTIONS)
            for idx, lm in enumerate(handLms.landmark):
              h, w, c = image.shape
              cx, cy = int(lm.x * w), int(lm.y * h)
              handList.append((cx, cy))
        for point in handList:
            cv2.circle(image, point, 10, (255, 255, 0), cv2.FILLED)
        upCount = 0
        for coordinate in finger_Coord:
            if handList[coordinate[0]][1] < handList[coordinate[1]][1]:
                upCount += 1
        
        if handList[thumb_Coord[0]][0] > handList[thumb_Coord[1]][0]:
            upCount+= 1

        cv2.putText(image, str(upCount), (150,150), cv2.FONT_HERSHEY_PLAIN, 4, (0,255,0), 6)
       
        if exit_flag:
            if newUpcount != upCount:
                newUpcount = upCount
                responses = ["Now I can see", "You are holding up", "These are",""]
                index = random.randint(0,3)
                tts(responses[index] + " "+ str(upCount) +"Fingers")
        else:
            break
            


    cv2.imshow("Finger detection :", image)
    cv2.waitKey(1)