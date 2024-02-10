import speech_recognition as sr 

def stt(languageCode):
    lang_code = languageCode
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

            text = r.recognize_google(audio, language=lang_code)
            print("You said:", text)
            
        except sr.UnknownValueError:
            x = stt(languageCode)
            return x

            
        except sr.RequestError as e:
            text="Could not request results from Google Speech Recognition service; {0}".format(e)
            print(text)
            # self.open_mic()
        return text

