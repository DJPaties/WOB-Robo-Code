import RazaBot
import socket
import json
import time
import subprocess
from botconnecterTTS import tts


Name = "محمد"
# Name = "Mohammad Dghaily"
New_User = False
false_detecion = False
denied_name = False
# name_callback_update = None
def send_delay(delay_time):
    pass

def get_New_User_detected():
    return New_User    
    
def set_get_New_User_detected_False():
    New_User = False 
          


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

def get_Name():
    print("The get name function returned :", Name)
    return Name
    
def get_denied_Name ():
    return denied_name
def set_Name_deny_False():
    global denied_name
    denied_name=False




  
    
def main(x):
    global expecting_input_detection

    print("THE MESSAGE SENT IS",x)

    
    print("recieving the message")
    response1 = RazaBot.send_message(x)

    print("Before IF")
    if isinstance(response1,dict):
        
        inputHint = response1.get('inputHint')
        if inputHint:
            if response1['inputHint'] == 'acceptingInput':

                intent = response1.get('intent')
                entities = response1.get('entities')

                if intent and entities:
                    payload = {
                        "intent": intent,
                        "side": entities["side"],
                        "degree_value": entities["degree_value"],
                        "time_value": int(entities["time_value"].split(":")[-1])
                    }

                    print(payload)
                elif intent:
                    payload={
                            "intent": intent
                        }
                    print(payload)
                expecting_input_detection = False
            

        elif response1["intent"] == 'new_user':
            global New_User
            global Name
            Name = response1['name']
            print("NEW USER IS FOUND", Name)
 
            New_User = True
            
            
            # client_socket.send(Name)         

        elif response1["intent"] ==  'denied name':
            global denied_name
            denied_name = True
            # msg = ("denied name")
            print(response1)
        elif response1["intent"] ==  'rock_paper_seaser':
            tts(response1['text'], "en-US") 
            subprocess.run([r"C:/Users/wot/AppData/Local/Programs/Python/Python311/python.exe", "RockPaperScissors.py"], check=True, text=True, shell=True)
            return "Nice Game I had fun playin with you"
        elif response1["intent"] ==  '':#TODO fix rock paper scissor arabic version
            tts(response1['text'], "en-US") 
            subprocess.run([r"C:/Users/wot/AppData/Local/Programs/Python/Python311/python.exe", "RockPaperScissors.py"], check=True, text=True, shell=True)
            return "Nice Game I had fun playin with you"
        elif response1["intent"] == "finger_count":
            tts(response1['text'],"en-US") 
            subprocess.run([r"C:/Users/wot/AppData/Local/Programs/Python/Python311/python.exe", "FingerCounter.py"], check=True, text=True, shell=True)
            return "Okay I'm stopping counting your finger"
        elif response1["intent"] == "finger_count_arabic":
            tts(response1['text'],"ar-LB") 
            subprocess.run([r"C:/Users/wot/AppData/Local/Programs/Python/Python311/python.exe", "FingerCounterArabic.py"], check=True, text=True, shell=True)
            return "Okay I'm stopping counting your finger"
        elif response1["intent"] ==  'object_detection':
            tts(response1['text'],"en-US") 
            subprocess.run([r"C:/Users/wot/AppData/Local/Programs/Python/Python311/python.exe", "object_tracking.py"], check=True, text=True, shell=True)
            return "Okay I'm stopping counting your finger"
        elif response1["intent"] ==  'object_detection_arabic':
            tts(response1['text'],"ar-LB") 
            subprocess.run([r"C:/Users/wot/AppData/Local/Programs/Python/Python311/python.exe", "object_tracking_ar.py"], check=True, text=True, shell=True)
            return "Okay I'm stopping counting your finger"
        elif response1["intent"] ==  'mimic_my_hand':
            tts(response1['text'],"en-US") 
            subprocess.run([r"C:/Users/wot/AppData/Local/Programs/Python/Python311/python.exe", "handTrackingModule.py"], check=True, text=True, shell=True)    
            return "okay stopped mimicking your hand"
        elif response1["intent"] ==  'mimic_my_hand_ar':
            print("After if")
            tts(response1['text'],"ar-LB") 
            subprocess.run([r"C:/Users/wot/AppData/Local/Programs/Python/Python311/python.exe", "handTrackingModuleAR.py"], check=True, text=True, shell=True)    
            return "ماشي حَوَءِّفْ  تَءْليدْ أِيْدَكْ"
        print(response1)
        print("before return")
        return response1['text']
        
        
    else:
        
        expecting_input_detection = True

        return response1
        
        

def initialize_client():
    
    try:
        global client_socket
        global Name
        server_ip = '192.168.16.166'
        server_port = 12345

        # Create a socket object
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to the server
        server_address = (server_ip, server_port)
        client_socket.connect(server_address)
        print("before loop")
        while True:

            print(" Server is on")
            message = client_socket.recv(1024).decode()
            if not message:
                break
            json_data = json.loads(message)
            print(json_data)
            if json_data['known'] == True:
                Name = json_data['name']
                client_socket.send(Name.encode())
            elif json_data['known'] == False:
                while not New_User:
                    print("Entering LOOP")
                    time.sleep(1)
                client_socket.send(Name.encode())
                set_Name_deny_False()
    except KeyboardInterrupt:
        client_socket.close()

    finally:
        client_socket.close()


# while True:
#     msg = input('')
# print(main(response1))