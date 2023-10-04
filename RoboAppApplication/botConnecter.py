import RazaBot
import socket
import json
import time
import subprocess
from botconnecterTTS import tts
import serial

# def talking_movement(delay):
#     counter=0
#     while counter < delay:
#         print("Command1")
#         servo_command="#1P1500#2P1500#3P1500#4P1500#5P1500#6P500#7P1500#8P1500#9P1500#10P1852#11P1367#12P1600#13P1567#14P1449#15P2133#16P1400#17P1500#18P1500#19P1500#20P1500#21P1500#22P1500#23P1500#24P1500#25P1500#26P2500#27P1500#28P1500#29P1500#30P2472#31P1500#32P1500T1000D1000\r\n"
#         ser.write(servo_command.encode())
#         time.sleep(0.3)
#         print("Command2")
#         servo_command = "#13P1400#14P1110#15P1867T1000D1000\r\n"
#         ser.write(servo_command.encode())
#         time.sleep(0.3)
#         print("Command3")
#         servo_command = "#13P1333#14P1381T1000D1000\r\n"
#         ser.write(servo_command.encode())
#         time.sleep(0.3)
#         # counter+=1
#         print("Command4")
#         servo_command = "#8P1467#9P1667#10P1856#11P1567#12P2500#13P1733#14P873#15P1867#16P1333T1000D1000\r\n"
#         ser.write(servo_command.encode())
#         time.sleep(0.3)
#         print("Command5")
#         servo_command = "#9P1600#10P1788#12P1067#13P1433#14P1449#15P2033#16P1667T1000D1000\r\n"
#         ser.write(servo_command.encode())
#         time.sleep(0.3)
#         print("Command6")
#         servo_command = "#12P1200#13P1567#14P1255#15P1967#16P1467#27P1700#28P1467#29P1633T1000D1000\r\n"
#         ser.write(servo_command.encode())
#         time.sleep(0.3)
#         # counter+=1

Name = ""
# Name = "Farah hawwari"
New_User = False
false_detecion = False
denied_name = False
# name_callback_update = None

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

            print(response1)
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
        print(response1)
        print("before return")
        return response1['text']
        
        
    else:
        
        expecting_input_detection = True

        return response1
        
        

# def initialize_client():
    
#     try:
#         global client_socket
#         global Name
#         server_ip = '192.168.0.3'
#         server_port = 12345

#         # Create a socket object
#         client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#         # Connect to the server
#         server_address = (server_ip, server_port)
#         client_socket.connect(server_address)
#         print("before loop")
#         while True:

#             print(" Server is on")
#             message = client_socket.recv(1024).decode()
#             if not message:
#                 break
#             json_data = json.loads(message)
#             print(json_data)
#             try:
#                 if json_data['known'] == True:
#                     Name = json_data['name']
#                     print("Name recieved: "+ Name)
#                     client_socket.send(Name.encode())
#                 else:
#                 # elif json_data['known'] == False:
#                     Name=json_data['Name']
#                     print("Name: "+ Name)
#                     print("Unknown name")
#                     while not New_User:
#                         print("Entering LOOP")
#                         time.sleep(1)
#                     client_socket.send(Name.encode())
#                     set_Name_deny_False()
#             except ValueError as e:
#                 print(e)
#     except KeyboardInterrupt:
#         client_socket.close()

#     finally:
#         client_socket.close()

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
                        Name=received_json['name']
                        print("Name: "+ Name)
                        print("Unknown name")
                        while not New_User:
                            print("Entering LOOP")
                            time.sleep(1)
                        client_socket.send(Name.encode())
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