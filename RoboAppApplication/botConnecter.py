# from direct_line_api_helper import DirectLineAPI
import RazaBot
import serial
import time

expecting_input_detection = None
# arduino = serial.Serial(port='COM10', baudrate= 9600, timeout=.1)      

def send_delay(delay_time):
    # arduino.write(str(delay_time).encode('utf-8'))
    # time.sleep(0.65)
    pass

def checkForSwitch(msg):
    keyword_list = ["change", "talk", "switch"]
    keyword_list_arabic = ["حول", "غير", "احكي", "تكلم"]
    words = msg.lower().split()
 
    if "انجليزي" in words :
        for keyword in keyword_list_arabic:
            if keyword in words:
                print("Switching to English")
                lang = "en-US"
                return lang
        print("No action needed for English")
        return None
    elif "arabic" in words:
        for keyword in keyword_list:
            if keyword in words:
                print("Switching to Arabic")
                lang = "ar-LB"
                return lang
        print("No action needed for Arabic")
        return None
    else:
        print("No action needed")
        return None



# def translateToEnglish(message):
#     tr = Translator()
#     out = tr.translate(message, dest="en")
#     return out.text


# def translateToArabic(message):
#     tr = Translator()
#     out = tr.translate(message, dest="ar")
#     print("After Translating", out.text)
#     return out.text


# def connectToBot():
#     global api
#     api=DirectLineAPI("taz30Qet5pA.vi8qB12H0Vf_0_25pvUlu3y9FRVa2hNZnfYBbywVGcI")
#     api.set_headers()
#     api.start_conversation() 
    
    
def main(x):
    global expecting_input_detection

    print("THE MESSAGE SENT IS",x)
    # api.send_message(x)
    
    print("recieving the message")
    response1 = RazaBot.send_message(x)
    
    # print("THIS IS RESPONSE ONE:"+ response1) 
    if isinstance(response1,dict):
        if response1['inputHint'] == 'acceptingInput':
            #print("ACCEPTING INPUT: THE MESSAGE IS:" + response1['text'])
            intent = response1.get('intent')
            entities = response1.get('entities')

            if intent and entities:
                payload = {
                    "intent": intent,
                    "side": entities["side"],
                    "degree_value": entities["degree_value"],
                    "time_value": int(entities["time_value"].split(":")[-1])
                }
                # full_entity = ""
                # for key, value in entities.items():
                #     full_entity += key + " " + str(value) + " "
                # print(intent, " full_entity " + full_entity)
                print(payload)
            elif intent:
                payload={
                    "intent": intent
                }
                print(payload)
            expecting_input_detection = False


            # if  lang_code == "ar-LB":
            #     msg = translateToArabic(response1['text'])
            #     return msg
            return response1['text']
        
    else:
        
        expecting_input_detection = True

        #print("EXPECTING INPUT: THE MESSAGE IS:" + response1['text'])

        # if lang_code == "ar-LB":
        #     x = translateToArabic(response1['text'])
        #     return x
        return response1
        
        


    
def InputType():
    global expecting_input_detection
    return expecting_input_detection

# while True:
#     msg = input('')
#     print(main(msg))