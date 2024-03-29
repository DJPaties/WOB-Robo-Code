import os
from concurrent.futures import ThreadPoolExecutor
import pyaudio
from google.cloud import texttospeech
import pygame
import glob
import numpy as np
import pvporcupine
import time
import botConnecter
import speech_recognition as sr
import wave
from mutagen.mp3 import MP3
import server
import subprocess
import threading
from serialSender import mouth, talking_scenario
import ExtraMicrophone
import threading
import greetings

class VoiceAssistant:
    def __init__(self):
        self.recognizedFace = ""
        self.lang_change = False
        self.detection = True
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
        self.eye_tracking_process = None
        self.eye_tracking_thread = None
        self.getNewName = False

    def run_face(self):
        # self.script_process = subprocess.Popen([r"C:\Users\WOB\AppData\Local\Programs\Python\Python38\python.exe", r"C:\Users\WOB\Desktop\WOB-Robo-Code-main\python_vision\main_old.py"])
        # self.script_process.communicate()
        if self.lang_code == "en-US":
            # self.script_process = subprocess.Popen([r"python", r"FaceRecog.py"])
            
            self.script_process = subprocess.Popen([r"c:/Users/WOB/Desktop/WOB-Robo-Code-main/FaceREcognition/venv/Scripts/python.exe", r"c:/Users/WOB/Desktop/WOB-Robo-Code-main/FaceREcognition/UsingFrames.py"])
            
            self.script_process.communicate()
        else:
            self.script_process = subprocess.Popen([r"c:/Users/WOB/Desktop/WOB-Robo-Code-main/FaceREcognition/venv/Scripts/python.exe", r"c:/Users/WOB/Desktop/WOB-Robo-Code-main/FaceREcognition/UsingFramesAr.py"])
            self.script_process.communicate()

    def close_face(self):
        if self.script_process:
            self.script_process.terminate()
    # #To reopen microphone
    # def open_mic(self):t
    #     if self.detection:
    #         self.generate_button.invoke()
    #     else:
    #         print("Machine is idle")

    #Check For language
    def selectLangauge(self, msg):
        x = botConnecter.checkForSwitch(msg)
        print("Language code is", x)
        #language logic to change the speech to text
        if x is not None:
            self.lang_code = x
            if self.lang_code == "en-US":
                self.response_message = "Okay I will speak in english from now on."

              
            elif self.lang_code == "ar-LB":
                self.response_message = " ماشي حاءحْكي معكْ بالعربي  هَلّْاأْ"
               
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

#==========================================================================================================================================================================================================================================================================================================================================================================================#
    #WakeUp Word function it detects hey jack then moves on to the tts function
    # def wake_check(self):
    #     self.script_thread= threading.Thread(target=self.run_face)
    #     self.script_thread.start()
    #     servo_command_2 = "#1P2467#2P2500#3P2400#4P2100#5P2300#6P500#7P500#8P1500#9P1410#10P1762#11P1367#12P1600#13P1200#14P1415#15P1500#16P1500#17P1500#18P1500#19P1500#20P1500#21P2200#22P2200#23P2200#24P2200#25P2200#26P2500#27P600#28P1500#29P1600#30P2472#31P1500#32P1500T1000D1000\r\n"  # Move servo 2 to position 2000 in 2 seconds

    #     talking_scenario(5,"any",servo_command_2)
    #     # keyword_path = 'C:/Users/WOB/Desktop/WOB-Robo-Code-main/RoboAppApplication/Hey-Jack_en_windows_v2_2_0.ppn'
    #     keyword_path = "C:/Users/WOB/Desktop/WOB-Robo-Code-main/RoboAppApplication/HeySam.ppn"
    #     # keyword_path_arabic = "C:/Users/WOB/Desktop/WOB-Robo-Code-main/RoboAppApplication/مرحبا-جاك_ar_windows_v2_2_0.ppn"
    #     keyword_path_arabic = "C:/Users/WOB/Desktop/WOB-Robo-Code-main/RoboAppApplication/HeySamar.ppn"

    #     access_key = 'hnVEQNTuN7caCisx8/8byB5z3xT1zsJ+ANs/NuVK2ZLWO9WNAJThdQ=='
    #     model_path = 'C:/Users/WOB/Desktop/WOB-Robo-Code-main/RoboAppApplication/porcupine_params_ar.pv'
    #     print("Entered wake check")
    #     self.detection= False
    #     def audio_callback(in_data, frame_count, time_info, status):
    #         pcm = np.frombuffer(in_data, dtype=np.int16)
    #         keyword_index = handle.process(pcm)
    #         if keyword_index >= 0:
    #             self.detection = True
    #             print("Keyword Detected!")
            
    #         return None, pyaudio.paContinue

    #     print("test")
    #     if self.lang_code == "en-US":

    #         handle = pvporcupine.create(keyword_paths=[keyword_path], access_key=access_key)

    #         pa = pyaudio.PyAudio()

    #         audio_stream = pa.open(
    #             rate=handle.sample_rate,
    #             channels=1,
    #             format=pyaudio.paInt16,
    #             input=True,
    #             frames_per_buffer=handle.frame_length,
    #             stream_callback=audio_callback
    #         )

    #         audio_stream.start_stream()

    #         while not self.detection:
    #             pass

    #         audio_stream.stop_stream()
    #         audio_stream.close()

    #         pa.terminate()



    #         self.updateface()
    #         self.lang_change = False

    #         if len(self.recognizedFace) == 0:
    #             self.getNewName = True
    #             self.response_message = "Hello. what's your name?"
    #             self.tts()


    #         else:
    #             self.close_face()
    #             self.response_message = "Hey, " + self.recognizedFace + "."
    #             print( "Hey, " + self.recognizedFace + ".")
                # TTS.tts(self.response_message, "en-US")
    #             greet_command = "#1P2500#2P2500#3P2500#4P2500#5P2500#6P500#7P500#8P1500#9P1430#10P1852#11P1500#12P1500#13P1500#14P1500#15P1500#16P1510#17P1500#18P1500#19P2500#20P1510#21P2200#22P2200#23P2200#24P2200#25P2400#26P2500#27P933#28P1200#29P1820#30P2192#31P1500#32P1500T500D500\r\n"
    #             talking_scenario(5,"any",greet_command)
    #             time.sleep(0.5)
    #             greetings.hand_shaking(self.lang_code)
    #             self.stt(self.speech_label)


    #     if self.lang_code == "ar-LB":
    #         print("language is arabic")
    #         handle = pvporcupine.create(keyword_paths=[keyword_path_arabic], access_key=access_key,model_path=model_path)
    #         pa = pyaudio.PyAudio()

    #         audio_stream = pa.open(
    #             rate=handle.sample_rate,
    #             channels=1,
    #             format=pyaudio.paInt16,
    #             input=True,
    #             frames_per_buffer=handle.frame_length,
    #             stream_callback=audio_callback
    #         )

    #         audio_stream.start_stream()

    #         while not self.detection:
    #             pass
    #         print("after detect keyword")

    #         audio_stream.stop_stream()
    #         audio_stream.close()

    #         pa.terminate()



    #         self.updateface()
    #         self.lang_change = False


    #         time.sleep(1)

    #         if len(self.recognizedFace) == 0:
    #             self.getNewName = True
    #             self.response_message = " مرحبَا, شو أِسْمَكْ"
    #             self.tts()
    #         else:
    #             self.close_face()

    #             self.response_message = "مرحبا"+self.recognizedFace
    #             print( "مرحبا"+self.recognizedFace + ".")
    #             TTS.tts(self.response_message, "ar-LB")
    #             greet_command = "#1P2500#2P2500#3P2500#4P2500#5P2500#6P500#7P500#8P1500#9P1430#10P1852#11P1500#12P1500#13P1500#14P1500#15P1500#16P1510#17P1500#18P1500#19P2500#20P1510#21P2200#22P2200#23P2200#24P2200#25P2400#26P2500#27P933#28P1200#29P1820#30P2192#31P1500#32P1500T500D500\r\n"
    #             talking_scenario(5,"any",greet_command)
    #             time.sleep(0.5)
    #             greetings.hand_shaking("ar-LB")
    #             print("done wake")
    #             self.stt(self.speech_label)
 
    def wake_check(self):
        servo_command_2 = "#1P2500#2P2500#3P2500#4P1900#5P1500#6P1570#7P1486#8P1500#9P1842#10P1380#11P1500#12P1900#13P1540#14P1540#15P2140#16P1200#17P1500#18P1500#19P1500#20P1500#21P2340#22P2420#23P2340#24P2380#25P2500#26P1360#27P1500#28P1660#29P2500#30P1500#31P1500#32P1500T500D500\r\n"  # Move servo 2 to position 2000 in 2 seconds
        talking_scenario(5,"any",servo_command_2)
        self.run_face()
        time.sleep(0.5)
        botConnecter.run_thread()
        greet_command = "#1P2500#2P2500#3P2500#4P1900#5P1500#6P830#7P1476#8P1440#9P1842#10P1380#11P1500#12P1900#13P2500#14P1540#15P2140#16P1200#17P1500#18P1500#19P1500#20P1500#21P2340#22P2420#23P2340#24P2380#25P2500#26P1350#27P1700#28P1660#29P2500#30P1500#31P1500#32P1500T500D500\r\n"
        talking_scenario(5,"any",greet_command)
        greetings.hand_shaking(self.lang_code)
        self.stt(self.speech_label)








#====================================================================================================================================================================================================================================================================================================================================
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

                pygame.mixer.music.load(filename)
                pygame.mixer.music.play()
                mouth(float(audio.info.length))
                ttsThread = threading.Thread(target=talking_scenario, args=(audio.info.length,"talking","any"))
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
                mouth(duration_seconds)
                # ttsThreadArabic = threading.Thread(target=talking_scenario, args=(duration_seconds,"talking","any"))
                # ttsThreadArabic.start()
                talking_scenario(duration_seconds,"talking","any")
                while pygame.mixer.music.get_busy():
                    time.sleep(0.15)  # Wait a second before checking again

        except Exception as e:
            print("Error occured ", e)
        if self.lang_change:
            self.stt(self.speech_label)
        else:
            self.stt(self.speech_label)




    
    #this function is where the user speaks and handles its requests
    def stt(self, speech_label):
        if self.detection:


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
                        # print(self.getNewName)
                        # if self.getNewName:
                        #     print("entering the get name")
                        #     new_name = botConnecter.save_new_name(text, self.lang_code)
                        #     print("New NAME IS ")
                        #     if self.lang_code == "ar-LB":
                        #         # ExtraTTS.tts(f"أَكِيدْ اِسْمَكْ {new_name}" ,"ar-LB")
                        #         # confirmation = ExtraMicrophone.stt(self.lang_code)
                        #         confirmation = True
                        #         if confirmation:
                                    
                        #             botConnecter.set_new_name(new_name)
                        #             botConnecter.set_New_user()
                        #             self.getNewName = False
                        #             self.response_message = "مرحبا"+ new_name
                        #             self.tts()
                        #         else:
                        #             self.response_message = "رْجاعْ أُلِّيْ اِسْمَكْ"
                        #             self.tts()
                        #     else:
                        #         ExtraTTS.tts(f"Are you sure your name is {new_name}" ,"en-US")
                        #         confirmation = ExtraMicrophone.stt(self.lang_code,"en-US")
                        #         if confirmation:
                        #             botConnecter.set_new_name(new_name)
                        #             botConnecter.set_New_user()
                        #             self.getNewName = False
                        #             self.response_message = "Hello"+ new_name
                        #             self.tts()
                        #         else:
                        #             self.response_message = "What's your name again"
                        #             self.tts()
                       
                        # else:
                        self.response_message = botConnecter.main(text) 

                        

                    
                    except sr.UnknownValueError:
                        # if self.counter == 1:
                            
                        #     if self.lang_code == "en-US":
                        #         self.response_message = "could not understand audio please repeat and be clear"
                        #     else:
                        #         self.response_message = "مش عم بِفْهَمْ عَلَيْك عيد"
                        #     #self.speech_label.config(text=self.response_message) 
                        #     print("loop- number 1")   
                        #     self.counter += 1 
                        #     self.tts()
                            
                        if self.counter <= 7:
                            print("opened mic again")
                            self.counter += 1
                            self.stt(self.speech_label)
                        
                        else:
                            print("SLEEPING")
                            self.counter = 1
                            botConnecter.close_eye()
                            self.wake_check()

                        
                    except sr.RequestError as e:
                        x="Could not request results from Google Speech Recognition service; {0}".format(e)
                        print(x)
                        # self.open_mic()
                #self.speech_label.config(text=self.response_message)
                self.tts()
    

    # #Tاread theruns multiple functions at once
    def run(self):
        # future = self.executor.submit(server.start_server)
        # future4 = self.executor.submit(botConnecter.initialize_client)
        future2 = self.executor.submit(self.wake_check)
        # return future,future2, future4
        return future2
        

#this starts the application
if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.run()




