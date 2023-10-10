import RazaBot
import socket
import json
import time
import subprocess
from botconnecterTTS import tts
import serial
from NameExtract import get_name



Name = "Mohammad"
# Name = "Farah hawwari"
new_name = ""
New_User = False
false_detecion = False
denied_name = False
# name_callback_update = None

def get_New_User_detected():
    return New_User    
def set_New_user():
    global New_User
    New_User = True

# def set_get_New_User_detected_False():
#     global New_User
#     New_User = False 
          

def save_new_name(text):
    temp_name= get_name(text)
    return temp_name

def set_new_name(new):
    global new_name
    new_name = new




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

    
    # print("recieving the message")
    response1 = RazaBot.send_message(x)

    # print("Before IF")
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

                    # print(payload)
                elif intent:
                    payload={
                            "intent": intent
                        }
                    # print(payload)
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

            # print(response1)
        elif response1["intent"] ==  'rock_paper_seaser':
            tts(response1['text'], "en-US") 
            subprocess.run([r"C:/Users/wot/AppData/Local/Programs/Python/Python311/python.exe", "RockPaperScissors.py"], check=True, text=True, shell=True)
            return "Nice Game I had fun playin with you"
        elif response1["intent"] ==  'rock_arabic':
            tts(response1['text'], "ar-LB") 
            subprocess.run([r"C:/Users/wot/AppData/Local/Programs/Python/Python311/python.exe", "RockPaperScissorsArabic.py"], check=True, text=True, shell=True)
            return "لِّعْبِهْ حِلوِى  تْسَلِّيْتْ فِيَا"
        elif response1["intent"] == "finger_count":
            tts(response1['text'],"en-US") 
            subprocess.run([r"C:/Users/wot/AppData/Local/Programs/Python/Python311/python.exe", "FingerCounter.py"], check=True, text=True, shell=True)
            return "Okay I'm stopping counting your finger"
        elif response1["intent"] == "finger_count_arabic":
            tts(response1['text'],"ar-LB") 
            subprocess.run([r"C:/Users/wot/AppData/Local/Programs/Python/Python311/python.exe", "FingerCounterArabic.py"], check=True, text=True, shell=True)
            return "ماشِيْ حَوَءِّفْ  شوفْ أَصابِيعَكْ"
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
            tts(response1['text'],"ar-LB") 
            subprocess.run([r"C:/Users/wot/AppData/Local/Programs/Python/Python311/python.exe", "handTrackingModuleAR.py"], check=True, text=True, shell=True)    
            return "ماشي حَوَءِّفْ  تَءْليدْ أِيْدَكْ"
        elif response1["intent"] ==  'beard_detection_arabic':
            tts(response1['text'],"ar-LB") 
            subprocess.run([r"C:/Users/wot/AppData/Local/Programs/Python/Python311/python.exe", "FindBeardArabic.py"], check=True, text=True, shell=True)    
            # return "ماشي حَوَءِّفْ  تَءْليدْ أِيْدَكْ"
            return "شُو هَلْ مَنزَرْ لِأِدَّامِيْ"
        elif response1["intent"] ==  'beard_detection_':
            tts(response1['text'],"en-US") 
            subprocess.run([r"C:/Users/wot/AppData/Local/Programs/Python/Python311/python.exe", "FindBeardArabic.py"], check=True, text=True, shell=True)    
            return "I will stop looking at you now"
        elif response1["intent"] == "conversation":
            return response1['gpt_response']
        elif response1['intent'] == 'face_vecog':
            pass
        elif response1['intent']== "face_vecog_arabic":
            pass
        elif response1['intent'] == 'Do':
            return response1['text']
        elif response1['intent'] == "byejack":
            pass
        elif response1['intent'] == "byejack_arabic":
            pass
        print(response1)
        # print("before return")
        return response1['text']
        
        
    else:
        
        expecting_input_detection = True

        return response1
        
        
def initialize_client():
    # Define the server host and port
    host = 'localhost'  # Use 'localhost' for the local machine, or use an IP address
    port = 12345       # Choose a port number

    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the host and port
    server_socket.bind((host, port))

    # Listen for incoming connections
    server_socket.listen(5)

    print(f"Server is listening on {host}:{port}")

    while True:
        # Accept a connection from a client
        client_socket, client_address = server_socket.accept()
        
        print(f"Accepted connection from {client_address}")
        
        try:
            while True:
                # Receive data from the client
                global Name
                global new_name
                global New_User
                print("Waiting for data")
                data = client_socket.recv(1024).decode('utf-8')
            
                if data:
                    print(f"Received JSON data from client: {data}")
                    
                    # Parse the received JSON data
                    received_json = json.loads(data)
                    print(received_json)
                    # Check if the received JSON contains a "known" key
                    if received_json['known']:

                        Name = received_json['name']
                        print("Name recieved: "+ Name)
                        client_socket.send(Name.encode())
                        # Name = received_json['name']
                        # print("Received Name is: " + Name)
                        # client_socket.send(Name.encode())
                    else:
                        New_User = False
                        Name=received_json['name']
                        # print("Name: "+ Name)
                        print("Unknown name")
                        while not New_User:
                            print("Entering LOOP")
                            time.sleep(1)
                        client_socket.send(new_name.encode())
                        set_Name_deny_False()
                            # print("Unknown Name")
                            # name = input("Enter Name: ")
                            # client_socket.send(name.encode('utf-8'))
                else:
                    print("No data received from the client")
                    break  # Break out of the loop if no data is received
        except Exception as e:
            print(f"Error: {str(e)}")
        finally:
            # Close the client socket
            client_socket.close()
# while True:
#     msg = input('')
# print(main(response1))