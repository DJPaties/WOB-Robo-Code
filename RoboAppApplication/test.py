import speech_recognition as sr
import os
import time
import glob
import pygame
from google.cloud import texttospeech 

import os

from google.cloud import speech
import io
import sounddevice as sd
import numpy as np
import soundfile as sf


# def tts(text):
#     os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'tts.json'
#     client = texttospeech.TextToSpeechClient()

#     # Detect the language of the input text
#     language_code = detect(text)

#     ssml_text = '<speak>' + text + '</speak>'
#     synthesis_input = texttospeech.SynthesisInput(ssml=ssml_text)
#     voice = texttospeech.VoiceSelectionParams(
#         language_code=language_code,
#         ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
#     )
#     audio_config = texttospeech.AudioConfig(
#         audio_encoding=texttospeech.AudioEncoding.MP3,
#     )
#     response = client.synthesize_speech(
#         input=synthesis_input, voice=voice, audio_config=audio_config,
#     )
#     filename = 'audio' + str(int(time.time())) + '.mp3'
#     with open(filename, 'wb') as out:
#         out.write(response.audio_content)

#     pygame.mixer.init()
#     pygame.mixer.music.load(filename)
#     pygame.mixer.music.play()
#     while pygame.mixer.music.get_busy():
#         time.sleep(0.2)  # Wait a second before checking again

#     # Clean up the generated audio files
#     files = glob.glob('audio*.mp3')
#     for f in files:
#         try:
#             os.remove(f)
#         except OSError as e:
#             print("Error: %s - %s." % (e.filename, e.strerror))
      
def speech_to_text():
    start = time.time()
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
            # Use the Google Web Speech API to recognize the speech in Arabic
            text = r.recognize_google(audio, language='en-US')
            print("You said:", text)
            end = time.time()
            elapsed = (end - start)*1000
            print("Function time", elapsed)
            # tts(text)
            return text
        
        except sr.UnknownValueError:
            x = "Speech recognition could not understand audio"
            print(x)
            # tts(x)
            
        except sr.RequestError as e:
            x="Could not request results from Google Speech Recognition service; {0}".format(e)
            print(x)
            # tts(x)
            
speech_to_text()