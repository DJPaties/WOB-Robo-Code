import tkinter as tk
import os
import pyaudio
from google.cloud import texttospeech
import pygame
import glob
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import pvporcupine
import time
import botConnecter
import speech_recognition as sr
import wave
from mutagen.mp3 import MP3

class VoiceAssistant:
    def __init__(self):
        self.lang_change = False
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
        self.response_message = ""
        self.speech_label = None
        self.lang_code = "en-US"
    #To reopen microphone
    def open_mic(self):
        if self.detection:
            self.generate_button.invoke()
        else:
            print("Machine is idle")

    #Check For language
    def selectLangauge(self, msg):
        x = botConnecter.checkForSwitch(msg)
        print("Language code is", x)
        if x is not None:
            self.lang_code = x
            if self.lang_code == "en-US":
                self.response_message = "Okay I will speak in english from now on."
                self.speech_label.config(text="Okay I will speak in english from now on.")
                
              
            elif self.lang_code == "ar-LB":
                self.response_message = " ماشي حاءحْكي معكْ بالعربي  هَلّْاأْ"
                self.speech_label.config(text=" ماشي حاءحْكي معكْ بالعربي  هَلّْاأْ")
               
            self.lang_change = True
            self.tts()

        
    #Properly close application        
    def on_close(self):
        print("Closing...")
        self.is_closed = True
        self.executor.shutdown(wait=False)
        self.root.destroy()
        print("Application closed")
        exit(0)

    
    #WakeUp Word function
    def wake_check(self):
        keyword_path = 'C:/Users/dghai/OneDrive/Desktop/RoboApp/Hey-Jack_en_windows_v2_2_0.ppn'
        access_key = 'kFYBTDtUiBn8PUPOWm8jtm7kNhRqZ67YAgjaKOlX2B8H7160vxfspA=='
        print("Entered wake check")
        self.detection= False
        def audio_callback(in_data, frame_count, time_info, status):
            pcm = np.frombuffer(in_data, dtype=np.int16)
            keyword_index = handle.process(pcm)
            if keyword_index >= 0:
                self.detection = True
                print("Keyword Detected!")
            
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
        self.lang_change = False
        if self.lang_code == "en-US":
            self.response_message = "Hey how can i assist you?"
            self.speech_label.config(text=self.response_message)
            self.tts()   
        else:
            self.response_message = "مرحبا كِيفْ فِيِّ ساعْدَكْ "
            self.speech_label.config(text=self.response_message)
            self.tts()
        


    def tts(self):

        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'tts.json'
        client = texttospeech.TextToSpeechClient()
        text = '<speak>'+""+self.response_message+""+'</speak>'
        synthesis_input = texttospeech.SynthesisInput(ssml=text)
        if self.lang_code == "en-US":
            voice = texttospeech.VoiceSelectionParams(
                language_code=self.lang_code ,
                ssml_gender=texttospeech.SsmlVoiceGender.MALE,
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
            audio = MP3(filename)
            
            print("MP3 audio length is ",audio.info.length)
            try:
                botConnecter.send_delay(float(audio.info.length))
            except Exception as e:
                print(e)
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(0.2)  # Wait a second before checking again
        else:

            name = "ar-XA-Standard-B"
            text_input = texttospeech.SynthesisInput(text=self.response_message)
            voice_params = texttospeech.VoiceSelectionParams(
                language_code="ar-XA", name=name
            )
            audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.LINEAR16)

            response = client.synthesize_speech(
                input=text_input,
                voice=voice_params,
                audio_config=audio_config,
            )
            

            filename = f"{name}.wav"
            print(filename)
            with open(filename, "wb") as out:
                out.write(response.audio_content)
                print(f'Generated speech saved to "{filename}"')
            with wave.open(filename) as mywav:
                duration_seconds = mywav.getnframes() / mywav.getframerate()
                print(f"Length of the WAV file: {duration_seconds:.1f} s")
            try:    
                botConnecter.send_delay(float(duration_seconds))
            except Exception as e:
                print(e)
            pygame.mixer.init()
            pygame.mixer.music.load('dummy.mp3')
            files = glob.glob('ar-XA-Standard-*.mp3')
            for f in files:
                try:
                    os.remove(f)
                except OSError as e:
                    print("Error: %s - %s." % (e.filename, e.strerror))
            filename = 'ar-XA-Standard-B' + str(pygame.time.get_ticks()) + '.wav'
            with open(filename, 'wb') as out:
                out.write(response.audio_content)
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(0.2)  # Wait a second before checking again

        if self.lang_change:
            self.wake_check()
        else:
            self.stt(self.speech_label)



    

    def stt(self, speech_label):
        if self.detection:
            self.lang_change = False
            # Create a recognizer object
            r = sr.Recognizer()

            # Open the microphone for capturing the speech
            with sr.Microphone() as source:
                print("Listening...")   
                
                # Adjust the energy threshold for silence detection
                r.energy_threshold = 4000

                # Listen for speech and convert it to text
                audio = r.listen(source)

                try:
                    
                    # Use the Google Web Speech API to recognize the speech 
                    text = r.recognize_google(audio, language=self.lang_code)
                    print("You said:", text)
                    self.selectLangauge(text)
                    self.response_message = botConnecter.main(text) 
                    

                
                except sr.UnknownValueError:
                    x = "could not understand audio please repeat and be clear"
                    print(x)
                    if self.lang_code == "en-US":
                        self.response_message = "could not understand audio please repeat and be clear"
                    else:
                        self.response_message = "مش عم بِفْهَمْ عَلَيْك عيد"
                    self.speech_label.config(text=self.response_message)    
                    self.tts()
                    
                except sr.RequestError as e:
                    x="Could not request results from Google Speech Recognition service; {0}".format(e)
                    print(x)
                    self.open_mic()
            self.speech_label.config(text=self.response_message)
            self.tts()
    


    def gui_setup(self):
        self.root = tk.Tk()
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{self.screen_width}x{self.screen_height}")
        
        frame = tk.Frame(self.root, width=self.screen_width//2, height=self.screen_height//2)
        frame.pack(pady=20)
        self.wake_label = tk.Label(frame, text="WakeUp Word detection:"+str(self.detection), font=("Arial", 22))
        self.wake_label.pack(pady=10)
        self.label = tk.Label(frame, text="", font=("Arial", 12))
        self.label.pack(pady=10)
        right_frame = tk.Frame(frame, width=200, height=200)
        right_frame.pack(side=tk.RIGHT)
        result_label = tk.Label(right_frame, text="Result:", font=("Arial", 12))
        result_label.pack(pady=10)
        self.speech_label = tk.Label(right_frame, text="Machine is at Idle.", font=("Arial", 12), width=100, height=20, relief=tk.SOLID, wraplength=350)
        self.speech_label.pack(pady=10)
        self.generate_button = tk.Button(right_frame, text="Generate Speech", font=("Arial", 12), command=lambda: self.stt(self.speech_label))
        self.generate_button.pack(pady=10)
        
        self.generate_button.configure(height=2, width=20)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()

    def run(self):
        future = self.executor.submit(self.wake_check)
        future2 = self.executor.submit(botConnecter.connectToBot)
        future3 = self.executor.submit(self.gui_setup)
        return future, future2, future3
        


if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.run()

