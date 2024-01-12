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
            # Use the Google Web Speech API to recognize the speech 
            # if languageCode == "ar-LB":
            #     yes_list = ["اي", "اي هيدا اسمي","اي هيدا", "نعم","ايه هذا اسمي","نعم هذا اسمي","ايه اسمي","ايه اكيد","اكيد"]
            #     no_list = ["لأ", "لأ مش اسمي"]
            #     if text in yes_list:
            #         return True
            #     elif text in no_list:
            #         return False
            #     else:
            #         TTS.tts("إِلّلِي اِزا اِيهْ أَوْ لَْأ", "ar-LB")
            #         stt(lang_code)
            # else:
            #     yes_list = ["Yes", "Yes that's my name","Yes it is", "Yeah","that is my name","Yeah it is","You are correct"]
            #     no_list = ["No", "No it is not","No it isn't", "Nope","That's not my name"]
            #     if text in yes_list:
            #         return True
            #     elif text in no_list:
            #         return False
            #     else:
            #         TTS.tts("Tell me if yes or no", "en-US")
            #         stt(lang_code)
            
            

        
        except sr.UnknownValueError:
            #TODO here in future time is where will we implement the sleep function that turns microphoneoff
            # when there is no one talking to him
            stt('ar-LB')

            
        except sr.RequestError as e:
            text="Could not request results from Google Speech Recognition service; {0}".format(e)
            print(text)
            # self.open_mic()
        return text
# print(stt())
# def check_response(text):
#     yes_list = ["اي", "اي هيدا اسمي", "اي هيدا", "نعم", "ايه هذا اسمي", "نعم هذا اسمي", "ايه اسمي", "ايه اكيد", "اكيد"]
#     no_list = ["لأ", "لأ مش اسمي"]

#     # Convert the text to lowercase for case-insensitive matching
#     lower_text = text.lower()

#     # Check if the text contains any of the words from the yes_list
#     for word in yes_list:
#         if word in lower_text:
#             return "Positive Response"

#     # Check if the text contains any of the words from the no_list
#     for word in no_list:
#         if word in lower_text:
#             return "Negative Response"

#     return "Uncertain Response"

# # Example usage
# user_input = input("Enter a text: ")
# result = stt("ar-LB")

# print(f"The response is: {result}")
