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
import server
import subprocess
import threading
from serialSender import mouth, talking_scenario, Ser
import ExtraMicrophone
import ExtraTTS
import threading
class VoiceAssistant:
    def __init__(self):

        self.recognizedFace = ""
        self.lang_change = False
        self.detection = False
        self.msg = ""       
        self.screen_width = None
        self.screen_height = None 
        self.label = None
        self.wake_label = None
        self.generate_button = None
        self.executor = ThreadPoolExecutor()
        self.serialExecuter = ThreadPoolExecutor()
        self.is_closed = False
        self.root = None
        self.response_message = ""
        self.speech_label = None
        self.lang_code = "ar-LB"
        self.counter = 1
        self.script_process = None
        self.script_thread = None
        self.getNewName = False

    def run_face(self):
        self.script_process = subprocess.Popen(["python", r"C:\Users\wot\Desktop\python_vision\main_old.py"])
        self.script_process.communicate()

    def close_face(self):
        if self.script_process:
            self.script_process.terminate()
            # print("closed Face")
    
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
        #language logic to change the speech to text
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

        self.is_closed = True
        self.executor.shutdown(wait=False)
        self.serialExecuter.shutdown(wait=False)
        self.root.destroy()
        print("Application closed")
        exit(0)

    def updateface(self):
        self.recognizedFace=botConnecter.get_Name()


    #WakeUp Word function it detects hey jack then moves on to the tts function
    def wake_check(self):
        self.script_thread= threading.Thread(target=self.run_face)
        self.script_thread.start()
        servo_command_2 = "#1P1500#2P1500#3P1500#4P1500#5P1500#6P500#7P1500#8P1500#9P1500#10P1852#11P1367#12P1600#13P1900#14P1076#15P1467#16P1300#17P1500#18P1500#19P1500#20P1500#21P1500#22P1500#23P1500#24P1500#25P1500#26P2500#27P1500#28P1500#29P1500#30P2472#31P1500#32P1500T1000D1000\r\n"  # Move servo 2 to position 2000 in 2 seconds

        Ser(servo_command_2)
        keyword_path = r'C:\Users\wot\Desktop\RoboAppApplication\Hey-Jack_en_windows_v2_2_0.ppn'
        keyword_path_arabic = "C:/Users/wot/Desktop/RoboAppApplication/مرحبا-جاك_ar_windows_v2_2_0.ppn"
        access_key = '4HceBz+B5ZnPRKTBlanhYjuwZxWZVG5RBuE9V9Fa7FY66pQs0M57MA=='
        model_path = 'C:/Users/wot/Desktop/RoboAppApplication/porcupine_params_ar.pv'
        print("Entered wake check")
        self.detection= False
        def audio_callback(in_data, frame_count, time_info, status):
            pcm = np.frombuffer(in_data, dtype=np.int16)
            keyword_index = handle.process(pcm)
            if keyword_index >= 0:
                self.detection = True
                print("Keyword Detected!")
            
            return None, pyaudio.paContinue


        if self.lang_code == "en-US":

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



            self.updateface()
            self.lang_change = False

            if len(self.recognizedFace) == 0:
                self.getNewName = True
                self.response_message = "hey,"+ botConnecter.main("name not recognized")
                self.speech_label.config(text=self.response_message)
                self.tts()
            else:
                self.close_face()
                self.response_message = "Hey, " + self.recognizedFace + "."
                print( "Hey, " + self.recognizedFace + ".")
                self.speech_label.config(text=self.response_message)
                self.tts() 
        if self.lang_code == "ar-LB":
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

            while not self.detection:
                pass
            print("after detect keyword")

            audio_stream.stop_stream()
            audio_stream.close()

            pa.terminate()



            self.updateface()
            self.lang_change = False

            servo_command_2 = "#1P1500#2P1500#3P1500#4P1500#5P1500#6P500#7P1500#8P1500#9P1500#10P1852#11P1500#12P1500#13P1500#14P1500#15P2367#16P1500#17P1500#18P1500#19P1500#20P1500#21P1500#22P1500#23P1500#24P1500#25P1500#26P2500#27P1500#28P1500#29P1500#30P2472#31P1500#32P1500T500D500\r\n"
            time.sleep(1)
            # ser.write(servo_command_2.encode())
            Ser(servo_command_2)  
            if len(self.recognizedFace) == 0:
                self.getNewName = True
                self.response_message = " مرحبا شو أِسْمَكْ"
                self.speech_label.config(text=self.response_message)
                self.tts()

                # self.response_message = "مرحبا,"+ botConnecter.main("الاسم منو  موجود")
                # self.speech_label.config(text=self.response_message)
                # self.tts()
            else:
                self.close_face()
                self.response_message = "مرحبا"+self.recognizedFace
                print( "مرحبا"+self.recognizedFace + ".")
                self.speech_label.config(text=self.response_message)
                self.tts()
 
        

    #its simple job is to only read the words that are results
    def tts(self):
   
        # print("TTS")
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'text.json'
        try:        
            
            client = texttospeech.TextToSpeechClient()
            print("Client created successfully.")
        except Exception as e:
            print("Error:", str(e))
        # print("TTS")
        text = '<speak>'+""+self.response_message+""+'</speak>'
        synthesis_input = texttospeech.SynthesisInput(ssml=text)
        
        try:
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
                # try:
                #     self.executor.submit(botConnecter.talking_movement(float(audio.info.length)))
                # except Exception as e:
                #     print(e)
                pygame.mixer.music.load(filename)
                pygame.mixer.music.play()
                mouth(float(audio.info.length))
                # self.executor.submit(talking_scenario(audio.info.length))
                ttsThread = threading.Thread(target=talking_scenario, args=(audio.info.length,))
                ttsThread.start()
                while pygame.mixer.music.get_busy():
                    time.sleep(0.15)  # Wait a second before checking again
        
        #if lamguage is arabic then a whole new process is written 
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
                # try:    
                #      self.executor.submit(botConnecter.talking_movement(float(duration_seconds)))
                # except Exception as e:
                #     print(e) 
                  
                mouth(duration_seconds)
                # self.serialExecuter.submit(talking_scenario(duration_seconds))
                ttsThreadArabic = threading.Thread(target=talking_scenario, args=(duration_seconds,))
                ttsThreadArabic.start()
                             
                while pygame.mixer.music.get_busy():
                    time.sleep(0.15)  # Wait a second before checking again

        except Exception as e:
            print("Error occured ", e)
        if self.lang_change:
            self.wake_check()
        else:
            self.stt(self.speech_label)




    
    #this function is where the user speaks and handles its requests
    def stt(self, speech_label):
        if self.detection:
            # if self.getNewName:

            if botConnecter.denied_name:
                self.response_message = botConnecter.main("name not recognized")
                botConnecter.set_Name_deny_False()
                self.tts()
            else:
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
                        if self.getNewName:
                            new_name = botConnecter.save_new_name(text)
                            print("New NAME IS ")
                            if self.lang_code == "ar-LB":
                                # self.tts("أَكِيدْ اِسْمَكْ " + new_name)
                                ExtraTTS.tts(f"أَكِيدْ اِسْمَكْ {new_name}" ,"ar-LB")
                                confirmation = ExtraMicrophone.stt()
                                if confirmation:
                                    botConnecter.set_new_name(new_name)
                                    botConnecter.set_New_user()
                                    self.getNewName = False
                                    self.response_message = "مرحبا"+ new_name
                                    self.tts()
                                else:
                                    self.response_message = "رْجاعْ أُلِّيْ اِسْمَكْ"
                                    self.tts()
                        else:
                            self.response_message = botConnecter.main(text) 

                        

                    
                    except sr.UnknownValueError:
                        #TODO here in future time is where will we implement the sleep function that turns microphoneoff
                        # when there is no one talking to him
                        if self.counter == 1:
                            
                            if self.lang_code == "en-US":
                                self.response_message = "could not understand audio please repeat and be clear"
                            else:
                                self.response_message = "مش عم بِفْهَمْ عَلَيْك عيد"
                            self.speech_label.config(text=self.response_message) 
                            print("loop- number 1")   
                            self.counter += 1 
                            self.tts()
                            
                        elif self.counter <= 5:
                            print("opened mic again")
                            self.counter += 1
                            self.stt(self.speech_label)
                        
                        else:
                            print("SLEEPING")
                            self.counter = 1
                            self.wake_check()

                        
                    except sr.RequestError as e:
                        x="Could not request results from Google Speech Recognition service; {0}".format(e)
                        print(x)
                        self.open_mic()
                self.speech_label.config(text=self.response_message)
                self.tts()
    

    #this is the Tkinter setup for main interface and the application window
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
    #Tاread theruns multiple functions at once
    def run(self):
        future = self.executor.submit(server.start_server)
        future3 = self.executor.submit(self.gui_setup)
        future4 = self.executor.submit(botConnecter.initialize_client)
        future2 = self.executor.submit(self.wake_check)
        return future,future2, future3, future4
        

#this starts the application
if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.run()




