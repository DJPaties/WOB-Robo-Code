import pvporcupine
import numpy as np
import pyaudio
from TTS import tts
detection = False
def wake_check():

    keyword_path = r'C:\Users\WOB\Desktop\RoboAppApplication\stop_mimick.ppn'

    access_key = 'O+T89wqaNBxf3FBKU7VmQA7xHHHxUO13pChq3tUtziLLZ27FXcCwBQ=='

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

    # updateface()
    # lang_change = False
    tts("Okay I'm stopping counting your finger")
    exit(0)

wake_check()