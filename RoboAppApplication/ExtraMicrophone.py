import speech_recognition as sr 
import TTS 

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
            yes_list = ["اي", "اي هيدا اسمي","اي هيدا", "نعم","ايه هذا اسمي","نعم هذا اسمي","ايه اسمي"]
            no_list = ["لأ", "لأ مش اسمي"]
            if text in yes_list:
                return True
            elif text in no_list:
                return False
            else:
                TTS.tts("إِلّلِي اِزا اِيهْ أَوْ لَْأ", "ar-LB")
                stt()
            

        
        except sr.UnknownValueError:
            #TODO here in future time is where will we implement the sleep function that turns microphoneoff
            # when there is no one talking to him
            stt()

            
        except sr.RequestError as e:
            x="Could not request results from Google Speech Recognition service; {0}".format(e)
            print(x)
            # self.open_mic()

# print(stt())