import cv2
import mediapipe as mp
import pvporcupine
import pyaudio
import numpy as np
from multiprocessing import Process, Event
from serialSender import talking_scenario
import time 

detection = False

def wake_check(exit_event):
    global detection
    keyword_path = 'C:/Users/WOB/Desktop/WOB-Robo-Code-main/RoboAppApplication/SamStop.ppn'
    access_key = 'hnVEQNTuN7caCisx8/8byB5z3xT1zsJ+ANs/NuVK2ZLWO9WNAJThdQ=='
    print("Entered stop check")

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
    exit_event.set()
    print('exit', exit_event.is_set())
    exit(-1)

print('reset moves')
reset_moves = "#1P2500#2P2500#3P2500#4P1900#5P1500#6P1570#7P1506#8P1500#9P1842#10P1380#11P1500#12P1900#13P1540#14P1540#15P2140#16P1200#17P1500#18P1500#19P1500#20P1500#21P2340#22P2420#23P2340#24P2380#25P2500#26P1360#27P1810#28P1660#29P2500#30P1500#31P1500#32P1500T500D500\r\n"
talking_scenario(5, "any", reset_moves)

def start(exit_event):
    x, y, width, height = 300, 000, 700, 700
    cap = cv2.VideoCapture(0)
    mp_Hands = mp.solutions.hands
    hands = mp_Hands.Hands()
    mpDraw = mp.solutions.drawing_utils
    finger_Coord = [(8, 6), (12, 10), (16, 14), (20, 18)]
    thumb_Coord = (4, 2)
    old_code = ""
    while not exit_event.is_set():
        success, image = cap.read()
        image_height = image.shape[0]
        image = image[y:y + height, x:x + width]
        RGB_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(RGB_image)
        multiLandMarks = results.multi_hand_landmarks
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
            # pointer finger
            if handList[finger_Coord[0][0]][1] < handList[finger_Coord[0][1]][1]:
                pointer_finger = 1
            else:
                pointer_finger = 0
            # middle finger
            if handList[finger_Coord[1][0]][1] < handList[finger_Coord[1][1]][1]:
                middle_finger = 1
            else:
                middle_finger = 0
            # ring finger
            if handList[finger_Coord[2][0]][1] < handList[finger_Coord[2][1]][1]:
                ring_finger = 1
            else:
                ring_finger = 0
            # pinky finger
            if handList[finger_Coord[3][0]][1] < handList[finger_Coord[3][1]][1]:
                pinky_finger = 1
            else:
                pinky_finger = 0
            # thumb_finger
            if handList[thumb_Coord[0]][0] > handList[thumb_Coord[1]][0]:
                thumb_finger = 1
            else:
                thumb_finger = 0
            msg = [pinky_finger, ring_finger, middle_finger, pointer_finger, thumb_finger]
            #        21             22             23         24             25
            cv2.putText(image, str(msg), (150, 150), cv2.FONT_HERSHEY_PLAIN, 4, (0, 255, 0), 6)
            print("inside cam exit flag", exit_event.is_set())
            if not exit_event.is_set():
                code = ""
                counter = 21
                for i in msg:
                    if counter ==22 or  counter == 24 or counter == 25:
                        if i == 1:
                            value = 2400
                        else:
                            value = 600
                    
                    else:
                        if i == 1:
                            value = 2400
                        else:
                            value = 600

                    code += f"#{counter}P{value}"
                    counter += 1
                code += "T500D500\r\n"

                if old_code != code:
                    print(code)
                    old_code = code 
                    talking_scenario(5, "any", code)
                    time.sleep(0.5)
            else:
                print("broken")
                break

        cv2.imshow("Finger detection :", image)
        cv2.waitKey(1)

def run():
    exit_event = Event()
    p = Process(target=wake_check, args=(exit_event,))
    p.start()
    start(exit_event)

if __name__ == "__main__":
    run()
