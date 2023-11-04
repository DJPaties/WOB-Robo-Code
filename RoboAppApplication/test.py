import io
import queue
import threading
import wave
import os
import librosa
import numpy as np
import pyaudio

from google.cloud import speech_v1 as speech

class SpeechToTextStreamer:
    def __init__(self, sample_rate=16000, channels=1, buffer_size=2048):
        self.sample_rate = sample_rate
        self.channels = channels
        self.buffer_size = buffer_size
        self.stream = pyaudio.PyAudio().open(format=pyaudio.paInt16, channels=channels, rate=sample_rate, input=True)
        self.queue = queue.Queue()
        self.thread = threading.Thread(target=self.process_audio)
        self.thread.start()

    def process_audio(self):
        while True:
            data = self.stream.read(self.buffer_size)
            self.queue.put(data)

    def get_transcript(self):
        transcript = ""
        while True:
            data = self.queue.get()

            # Convert the audio data from int16 to float32.
            audio_data_float32 = np.frombuffer(data, dtype=np.int16).astype(np.float32)

            # Compute the MFCCs of the audio data.
            features = librosa.feature.mfcc(y=audio_data_float32, sr=self.sample_rate)
            features = features.T
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'text.json'
            # Send the features to the Google Cloud Speech-to-Text API.
            client = speech.SpeechClient()
            config = speech.types.RecognitionConfig(
                encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=self.sample_rate,
                language_code="en-US",
            )

            content = speech.types.RecognitionAudio(content=features)

            response = client.recognize(config, content)

            # Get the transcript from the response.
            for result in response.results:
                transcript += result.alternatives[0].transcript

            # If there is no more audio data, break out of the loop.
            if data is None:
                break

        return transcript

    def stop(self):
        self.stream.stop_stream()
        self.stream.close()
        self.thread.join()

# Create a speech to text streamer.
streamer = SpeechToTextStreamer()

# Start streaming audio.
streamer.stream.start_stream()

# Get the transcript.
transcript = streamer.get_transcript()

# Print the transcript.
print(transcript)

# Stop streaming audio.
streamer.stop()
