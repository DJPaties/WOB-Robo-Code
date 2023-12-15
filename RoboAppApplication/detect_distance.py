import cv2
import numpy as np
import pyk4a
from helpers import colorize
from pyk4a import Config, PyK4A
from TTS import tts
import pvporcupine
import pyaudio
from concurrent.futures import ThreadPoolExecutor
executor = ThreadPoolExecutor()

def main():
    global message
    global new_message
    global exit_flag 
    exit_flag = False
    message = ""
    new_message = ""

    def wake_check():
        
        keyword_path_arabic = "C:/Users/WOB/Desktop/WOB-Robo-Code-main/RoboAppApplication/stop_mimick.ppn"
        access_key = 'KT8J7GHX3ohRwP3c/W/TyovUX0ceYDL0g8U01PTb3q7ARhHDOgYD9w=='
        print("language is arabic")
        def audio_callback(in_data, frame_count, time_info, status):
            pcm = np.frombuffer(in_data, dtype=np.int16)
            keyword_index = handle.process(pcm)
            if keyword_index >= 0:
                global detection
                detection = True    
                print("Keyword Detected!")
                global exit_flag
                exit_flag =  True 
                print("All CLEAR")
                print(exit_flag)
            
            return None, pyaudio.paContinue


        handle = pvporcupine.create(keyword_paths=[keyword_path_arabic], access_key=access_key)
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

        # pyautogui.press('a')

        print('exit')
        exit(0)

    executor.submit(wake_check)

    point = (400,300)
    k4a = PyK4A(
        Config(
            color_resolution=pyk4a.ColorResolution.OFF,
            depth_mode=pyk4a.DepthMode.NFOV_UNBINNED,
            synchronized_images_only=False,
        )
    )
    k4a.start()

    # getters and setters directly get and set on device
    k4a.whitebalance = 4500
    assert k4a.whitebalance == 4500
    k4a.whitebalance = 4510
    assert k4a.whitebalance == 4510

    while True:
        capture = k4a.get_capture()
        if np.any(capture.depth):

            cv2.circle(capture.depth, point,20,(0,0,255))
            cv2.imshow("k4a", colorize(capture.depth, (None, 5000), cv2.COLORMAP_HSV))
            depth_data = capture.depth[point[1],point[0]]
            print(depth_data)

            if depth_data > 2000:
                print("Over 2 meters far")
                new_message ="The distance between you and me is more than two metres."
            elif 2000>depth_data and depth_data>1500:
                print("Between 1.5 to 2 meters")  
                new_message = "The distance between you and me, is from two meters to a meter and a half."
            elif 1500>depth_data and depth_data>1000:
                print("Between 1.5 and 1 meters")
                new_message = "The distance between you and me, is from a meter and a half to a meter."
            elif 1000>depth_data and depth_data>500:
                print("Between 0.5 to 1 meter far")
                new_message = "The distance between you and me, is from a meter to a half a meter."
            elif 500>depth_data:
                print("Your too close to me stay back")
                new_message = "You are really close to me, please go back a bit"

            if message != new_message:
                message = new_message
                tts(new_message,"en-US")
            # key = cv2.waitKey(10)
            # if key != -1:
            #     cv2.destroyAllWindows()
            #     break
            print("INSIDE CAMERA:",exit_flag)
            if exit_flag:
                cv2.destroyAllWindows()
                break      
    k4a.stop()


main()