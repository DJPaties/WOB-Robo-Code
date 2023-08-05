import tkinter as tk
import os
import pyaudio
from google.cloud import texttospeech
import pygame
import glob
from google.cloud import speech
import io
import sounddevice as sd
import numpy as np
import soundfile as sf
from concurrent.futures import ThreadPoolExecutor
import pvporcupine
import time
import botConnecter

class VoiceAssistant:
    def __init__(self):
        self.detection = False
        self.msg = ""
        self.screen_width = None
        self.screen_height = None
        self.label = None
        self.wake_label = None
        self.generate_button = None
        self.executor = ThreadPoolExecutor()
        self.is_closed = False
        self.root = None
    def open_mic(self):
        if self.detection:
            self.generate_button.invoke()
        else:
            print("Machine is idle")
    def on_close(self):
        print("Closing...")
        self.is_closed = True
        self.executor.shutdown(wait=True)
        self.root.destroy()
    def wake_check(self):
        keyword_path = 'C:/Users/dghai/OneDrive/Desktop/RoboApp/Hey-Jack_en_windows_v2_2_0.ppn'
        access_key = 'kFYBTDtUiBn8PUPOWm8jtm7kNhRqZ67YAgjaKOlX2B8H7160vxfspA=='
        
        self.detection= False
        def audio_callback(in_data, frame_count, time_info, status):
            pcm = np.frombuffer(in_data, dtype=np.int16)
            keyword_index = handle.process(pcm)
            if keyword_index >= 0:
                self.detection = True
                print("Keyword Detected!")
                print("Hello Human")
            
            return None, pyaudio.paContinue

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

        while not self.detection:
            pass

        audio_stream.stop_stream()
        audio_stream.close()

        pa.terminate()

        print("All CLEAR")
        print(self.detection)
        pygame.mixer.init()
        pygame.mixer.music.load('dummy.mp3')
        pygame.mixer.music.load('hey_response.mp3')
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.2)  # Wait a second before checking again
        self.open_mic()

    def tts(self):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'tts.json'

        client = texttospeech.TextToSpeechClient()

        text = '<speak>'+""+self.label.cget("text")+""+'</speak>'
        synthesis_input = texttospeech.SynthesisInput(ssml=text)

        voice = texttospeech.VoiceSelectionParams(
            language_code='en-US',
            ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
        )

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
        )

        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config,
        )

        filename = 'audio.mp3'

        with open(filename, 'wb') as out:
            out.write(response.audio_content)

        pygame.mixer.init()
        pygame.mixer.music.load('dummy.mp3')

        files = glob.glob('audio*.mp3')
        for f in files:
            try:
                os.remove(f)
            except OSError as e:
                print("Error: %s - %s." % (e.filename, e.strerror))

        filename = 'audio' + str(pygame.time.get_ticks()) + '.mp3'
        with open(filename, 'wb') as out:
            out.write(response.audio_content)

        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.2)  # Wait a second before checking again
        if botConnecter.InputType():
            print("Opening Mic...")
            self.open_mic()
        else:
            self.detection=False
            print("Machine is at idle again DETECTION IS ",self.detection)
            self.wake_check()


    def stt(self, speech_label):

       if self.detection:
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'stt.json'
            fs = 8000  # Sample rate
            duration = 2  # Duration of each chunk
            silence_threshold = 4  # Adjust this value based on your requirements
            recording = []  # List to hold the recording chunks
            silence_counter = 0  # Counter to check for consecutive silence
            
            while True:
                print("Recording chunk")
                myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1) 
                sd.wait()  # Wait until recording is finished

                # If the recorded chunk is "silent", increment the silence counter
                print(np.abs(myrecording).mean()*100)
                if np.abs(myrecording).mean()*100 < silence_threshold:
                    silence_counter += 1
                else:  # Otherwise, reset the counter
                    silence_counter = 0

                # Add the recorded chunk to the list of chunks
                recording.append(myrecording)

                # If we have 5 seconds of consecutive silence, stop recording
                if silence_counter > 0:
                    print("Silence detected, stopping recording")
                    break

            # Combine all chunks into one recording
            myrecording = np.concatenate(recording, axis=0)

            # Normalize to 16-bit range
            myrecording *= 32767 / np.max(np.abs(myrecording))
            # Convert to 16-bit data
            myrecording = myrecording.astype(np.int16)

            # Save as WAV file
            sf.write('output.wav', myrecording, fs)

            client = speech.SpeechClient()
            file_name = "output.wav"

            if not os.path.exists(file_name):
                print(f"The file {file_name} does not exist.")
                return

            with io.open(file_name, "rb") as audio_file:
                content = audio_file.read()

            audio = speech.RecognitionAudio(content=content)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=8000,
                language_code="en-US",
            )
            global msg
            msg=""
            response = client.recognize(config=config, audio=audio)

            if not response.results:
                print("The API did not return any results.")
                self.detection = False
                print("No mic detected idiling the app")
                self.wake_check()
        
            for result in response.results:
                msg = result.alternatives[0].transcript
            speech_label.config(text=msg)
            
            self.label.config(text= botConnecter.main(msg))
            self.tts()    
       else:
            speech_label.config(text="Machine Still at Idle")


    def gui_setup(self):
        root = tk.Tk()
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()
        root.geometry(f"{self.screen_width}x{self.screen_height}")
        
        frame = tk.Frame(root, width=self.screen_width//2, height=self.screen_height//2)
        frame.pack(pady=20)
        self.wake_label = tk.Label(frame, text="WakeUp Word detection:"+str(self.detection), font=("Arial", 22))
        self.wake_label.pack(pady=10)
        self.label = tk.Label(frame, text="", font=("Arial", 12))
        self.label.pack(pady=10)
        button = tk.Button(frame, text="Text to Speech", font=("Arial", 12), command=lambda: self.tts())
        button.pack(pady=10)
        right_frame = tk.Frame(frame, width=200, height=200)
        right_frame.pack(side=tk.RIGHT)
        result_label = tk.Label(right_frame, text="Result:", font=("Arial", 12))
        result_label.pack(pady=10)
        speech_label = tk.Label(right_frame, text="Your speech to text is generated here", font=("Arial", 12), width=100, height=20, relief=tk.SOLID, wraplength=350)
        speech_label.pack(pady=10)
        self.generate_button = tk.Button(right_frame, text="Generate Speech", font=("Arial", 12), command=lambda: self.stt(speech_label))
        self.generate_button.pack(pady=10)
        button.configure(height=2, width=20)
        self.generate_button.configure(height=2, width=20)
        root.mainloop()

    def run(self):
        future = self.executor.submit(self.wake_check)
        future3 = botConnecter.connectToBot()
        future2 = self.executor.submit(self.gui_setup)
        return_value = future.result()
        self.wake_label.config(text="WakeUp Word detection:"+str(self.detection))
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)


if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.run()



'''import tkinter as tk
import os
import pyaudio
from google.cloud import texttospeech
import pygame
import glob
from google.cloud import speech
import io
import sounddevice as sd
import numpy as np
import soundfile as sf
from concurrent.futures import ThreadPoolExecutor
import pvporcupine
import time
import botConnecter
detection = False
def openMic():
    if detection:
        generate_button.invoke()
    else:
        print("Machine is idle")
def Wake_check():
    keyword_path = 'C:/Users/dghai/OneDrive/Desktop/RoboApp/Hey-Jack_en_windows_v2_2_0.ppn'
    access_key = 'kFYBTDtUiBn8PUPOWm8jtm7kNhRqZ67YAgjaKOlX2B8H7160vxfspA=='
    global detection 
    detection= False
    def audio_callback(in_data, frame_count, time_info, status):
        pcm = np.frombuffer(in_data, dtype=np.int16)
        keyword_index = handle.process(pcm)
        if keyword_index >= 0:
            global detection
            detection = True
            print("Keyword Detected!")
            print("Hello Human")
           
        return None, pyaudio.paContinue

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

    while not detection:
        pass

    audio_stream.stop_stream()
    audio_stream.close()

    pa.terminate()

    print("All CLEAR")
    print(detection)
    pygame.mixer.init()
    pygame.mixer.music.load('dummy.mp3')
    pygame.mixer.music.load('hey_response.mp3')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(0.5)  # Wait a second before checking again
    openMic()


def TTS():
    
        
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'tts.json'

        client = texttospeech.TextToSpeechClient()

        text = '<speak>'+""+label.cget("text")+""+'</speak>'
        synthesis_input = texttospeech.SynthesisInput(ssml=text)

        voice = texttospeech.VoiceSelectionParams(
            language_code='en-US',
            ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
        )

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
        )

        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config,
        )

        filename = 'audio.mp3'

        with open(filename, 'wb') as out:
            out.write(response.audio_content)

        pygame.mixer.init()
        pygame.mixer.music.load('dummy.mp3')

        files = glob.glob('audio*.mp3')
        for f in files:
            try:
                os.remove(f)
            except OSError as e:
                print("Error: %s - %s." % (e.filename, e.strerror))

        filename = 'audio' + str(pygame.time.get_ticks()) + '.mp3'
        with open(filename, 'wb') as out:
            out.write(response.audio_content)

        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.5)  # Wait a second before checking again
        if botConnecter.InputType():
            print("Opening Mic...")
            openMic()
        else:
            detection=False
            print("Machine is at idle again DETECTION IS ",detection)
            Wake_check()

    


def STT(speech_label):
    global detection
    if detection:
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'stt.json'
        fs = 8000  # Sample rate
        duration = 2  # Duration of each chunk
        silence_threshold = 4  # Adjust this value based on your requirements
        recording = []  # List to hold the recording chunks
        silence_counter = 0  # Counter to check for consecutive silence
        time.sleep(1)
        while True:
            print("Recording chunk")
            myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1) 
            sd.wait()  # Wait until recording is finished

            # If the recorded chunk is "silent", increment the silence counter
            print(np.abs(myrecording).mean()*100)
            if np.abs(myrecording).mean()*100 < silence_threshold:
                silence_counter += 1
            else:  # Otherwise, reset the counter
                silence_counter = 0

            # Add the recorded chunk to the list of chunks
            recording.append(myrecording)

            # If we have 5 seconds of consecutive silence, stop recording
            if silence_counter > 1:
                print("Silence detected, stopping recording")
                break

        # Combine all chunks into one recording
        myrecording = np.concatenate(recording, axis=0)

        # Normalize to 16-bit range
        myrecording *= 32767 / np.max(np.abs(myrecording))
        # Convert to 16-bit data
        myrecording = myrecording.astype(np.int16)

        # Save as WAV file
        sf.write('output.wav', myrecording, fs)

        client = speech.SpeechClient()
        file_name = "output.wav"

        if not os.path.exists(file_name):
            print(f"The file {file_name} does not exist.")
            return

        with io.open(file_name, "rb") as audio_file:
            content = audio_file.read()

        audio = speech.RecognitionAudio(content=content)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=8000,
            language_code="en-US",
        )
        global msg
        msg=""
        response = client.recognize(config=config, audio=audio)

        if not response.results:
            print("The API did not return any results.")
            detection = False
            print("No mic detected idiling the app")
            Wake_check()
       
        for result in response.results:
            msg = result.alternatives[0].transcript
        speech_label.config(text=msg)
        
        label.config(text= botConnecter.main(msg))
        TTS()
        
       
      
    
        
    else:
        speech_label.config(text="Machine Still at Idle")

def main():
    
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}")
    
    frame = tk.Frame(root, width=screen_width//2, height=screen_height//2)
    frame.pack(pady=20)
    global wake_label
    wake_label = tk.Label(frame, text="WakeUp Word detection:"+str(detection), font=("Arial", 22))
    wake_label.pack(pady=10)
    global label
    label = tk.Label(frame, text="", font=("Arial", 12))
    label.pack(pady=10)
   

    button = tk.Button(frame, text="Text to Speech", font=("Arial", 12), command=lambda: TTS())
    button.pack(pady=10)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
    right_frame = tk.Frame(frame, width=200, height=200)
    right_frame.pack(side=tk.RIGHT)
    
    result_label = tk.Label(right_frame, text="Result:", font=("Arial", 12))
    result_label.pack(pady=10)



    speech_label = tk.Label(right_frame, text="Your speech to text is generated here", font=("Arial", 12), width=100, height=20, relief=tk.SOLID, wraplength=350)
    speech_label.pack(pady=10)
    global generate_button
    generate_button = tk.Button(right_frame, text="Generate Speech", font=("Arial", 12), command=lambda: STT(speech_label))
    generate_button.pack(pady=10)

    button.configure(height=2, width=20)

    generate_button.configure(height=2, width=20)
    # Using ThreadPoolExecutor to manage threads and get return values
    
    root.mainloop()

with ThreadPoolExecutor() as executor:
        
        future = executor.submit(Wake_check)
        future3 = botConnecter.connectToBot()
        future2 = executor.submit(main)
        return_value = future.result()
        wake_label.config(text="WakeUp Word detection:"+str(detection))

        
'''