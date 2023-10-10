import os
from google.cloud import texttospeech
import pygame
import glob
import time
from mutagen.mp3 import MP3
import wave
from concurrent.futures import ThreadPoolExecutor
from serialSender import mouth, talking_scenario, Ser
serialExecuter = ThreadPoolExecutor()
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
            mouth(float(audio.info.length))
            serialExecuter.submit(talking_scenario(audio.info.length))
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
            mouth(duration_seconds)
            serialExecuter.submit(talking_scenario(duration_seconds))
            while pygame.mixer.music.get_busy():
                time.sleep(0.2)  # Wait a second before checking again
    except Exception as e:
        print("Error occured ", e)


# tts("باااي باااي, أِزا بَدَّكْ يانِي ,رْجَاعْ عيِّطْلي", 'ar-LB')