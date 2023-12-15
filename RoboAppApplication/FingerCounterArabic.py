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
    keyword_path_arabic = "C:/Users/WOB/Desktop/WOB-Robo-Code-main/RoboAppApplication/stopArabic.ppn"
    access_key = 'KT8J7GHX3ohRwP3c/W/TyovUX0ceYDL0g8U01PTb3q7ARhHDOgYD9w=='
    model_path = 'C:/Users/WOB/Desktop/WOB-Robo-Code-main/RoboAppApplication/porcupine_params_ar.pv'
    print("language is arabic")
    def audio_callback(in_data, frame_count, time_info, status):
        pcm = np.frombuffer(in_data, dtype=np.int16)
        keyword_index = handle.process(pcm)
        if keyword_index >= 0:
            global detection
            detection = True    
            print("Keyword Detected!")
        
        return None, pyaudio.paContinue


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
    exit_flag =  False
    print("All CLEAR")
    print(detection)
    print('exit')
    exit(-1)

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
                responses = ["هَلَّءْ فِينِيْ شُوفْ", "اِنْتَ رافِعْ", "هولي",""]
                if upCount == 0:
                    tts("مِشْ رافِعْ وَلا أُصْبَعْ", "ar-LB")
                else:
                    number = ""
                    if upCount == 1:
                        number = "أُصْبَعْ واحِدْ"
                    if upCount == 2:
                        number = "أُصْبَعانْ"
                    if upCount == 3:
                        number = " تْلاتْ أَصابِعْ"
                    if upCount == 4:
                        number = " أَرْبَعْ أَصابِعْ"
                    if upCount == 5:
                        number = " خَمْسَةْ أَصابِعْ"


                    index = random.randint(0,3)
                    tts(responses[index] + " "+ number ,"ar-LB")
        else:
            break
            


    cv2.imshow("Finger detection :", image)
    cv2.waitKey(1)