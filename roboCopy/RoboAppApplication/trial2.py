import os
from google.cloud import texttospeech
import pygame
import glob
import time

lang_code = "ar-LB"
response_message = "مش عم بِفْهَمْ عَلَيْك عيد"

def tts():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'tts.json'
    client = texttospeech.TextToSpeechClient()
    text = '<speak>' + "" + response_message + "" + '</speak>'
    synthesis_input = texttospeech.SynthesisInput(ssml=text)

    if lang_code == "en-US":
        voice = texttospeech.VoiceSelectionParams(
            language_code=lang_code,
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

        # Create the "audio_files" directory if it doesn't exist
        if not os.path.exists("audio_files"):
            os.mkdir("audio_files")

        filename = os.path.join("audio_files", f"{name}.wav")
        with open(filename, "wb") as out:
            out.write(response.audio_content)
            print(f'Generated speech saved to "{filename}"')

    pygame.mixer.init()
    pygame.mixer.music.load('dummy.mp3')
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(0.2)  # Wait a second before checking again


while True:
    msg = input("enter 1:")
    if msg == "1":
        tts()
