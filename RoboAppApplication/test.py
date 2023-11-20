import json
import requests
import speech_recognition as sr 
import time
import os
from google.cloud import texttospeech
import pygame
import glob
import time
from mutagen.mp3 import MP3
import wave
from concurrent.futures import ThreadPoolExecutor
from serialSender import mouth, talking_scenario
from RazaBot import send_message
def tts(response_message,lang_code):

    print("TTS")
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'tts.json'
    try:        
        
        client = texttospeech.TextToSpeechClient()
        print("Client created successfully.")
    except Exception as e:
        print("Error:", str(e))
    print("TTS")
    text = '<speak>'+""+response_message+""+'</speak>'
    synthesis_input = texttospeech.SynthesisInput(ssml=text)
    
    try:
        if lang_code == "en-US":
            voice = texttospeech.VoiceSelectionParams(
            language_code=lang_code ,
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
            # mouth(float(audio.info.length))
            # serialExecuter.submit(talking_scenario(audio.info.length,"talking","any"))
            while pygame.mixer.music.get_busy():
                time.sleep(0.2)  # Wait a second before checking again
    
    #if lamguage is arabic then a whole new process is written 
        else:

            name = "ar-XA-Standard-B"
            text_input = texttospeech.SynthesisInput(text=response_message)
            voice_params = texttospeech.VoiceSelectionParams(
                language_code="ar-XA", name=name
            )
            audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.LINEAR16)

            response = client.synthesize_speech(
                input=text_input,
                voice=voice_params,
                audio_config=audio_config,
            )
            

            filename = f"botConnecterarabic.wav"
            print(filename)
            with open(filename, "wb") as out:
                out.write(response.audio_content)
                print(f'Generated speech saved to "{filename}"')
            with wave.open(filename) as mywav:
                duration_seconds = mywav.getnframes() / mywav.getframerate()
                print(f"Length of the WAV file: {duration_seconds:.1f} s")
            pygame.mixer.init()
            pygame.mixer.music.load('dummy.mp3')
            files = glob.glob('botConnecterarabic*.mp3')
            for f in files:
                try:
                    os.remove(f)
                except OSError as e:
                    print("Error: %s - %s." % (e.filename, e.strerror))
            filename = 'botConnecterarabic' + str(pygame.time.get_ticks()) + '.wav'
            with open(filename, 'wb') as out:
                out.write(response.audio_content)
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
            #mouth(duration_seconds)
            # serialExecuter.submit(talking_scenario(duration_seconds,"talking","any"))
            while pygame.mixer.music.get_busy():
                time.sleep(0.2)  # Wait a second before checking again
    except Exception as e:
        print("Error occured ", e)


def stt():
    lang_code = "ar-LB"
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
            text = r.recognize_google(audio, language=lang_code)
            print("You said:", text)
            x = send_message(text)
            if x['message'] == False:
                send_message(x['intent'])
            else:
                tts(x['message'],"ar-LB")
                stt()

            

        
        except sr.UnknownValueError:
            
            stt()

            
        except sr.RequestError as e:
            x="Could not request results from Google Speech Recognition service; {0}".format(e)
            print(x)
            stt()

def send_input():
    msg = input(">")
    resposne = send_message(msg)
    if resposne['message'] == False:
        send_message(resposne['intent'])
    else:
        tts(resposne['message'],"ar-LB")
        send_input()
        
send_input()
    