import threading
import socket
import json
import time
import subprocess
from serialSender import talking_scenario
from botconnecterTTS import tts
from NameExtract import get_name
import RazaBot
# import exampleBodyTracking

# eye_tracking_process = None


def run_eye():
    # run_thread()
    global eye_tracking_process
    eye_tracking_process = subprocess.Popen(["python", "exampleBodyTracking.py"])
    eye_tracking_process.communicate()


def close_eye():
    if eye_tracking_process:
        eye_tracking_process.terminate()

def run_thread():

    threa = threading.Thread(target=run_eye)
    threa.start()
    threa = None


# Name = ""
Name = "Mohammad"
new_name = ""
New_User = False
false_detecion = False
denied_name = False

run_thread()

def get_New_User_detected():
    return New_User


def set_New_user():
    global New_User
    New_User = True


def save_new_name(text):
    temp_name = get_name(text)
    return temp_name


def set_new_name(new):
    global new_name
    new_name = new


def checkForSwitch(msg):
    keyword_list = ["change", "talk", "switch"]
    keyword_list_arabic = ["حول", "غير", "احكي", "تكلم"]
    words = msg.lower().split()

    if "انجليزي" in words:
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


def get_denied_Name():
    return denied_name


def set_Name_deny_False():
    global denied_name
    denied_name = False


def main(x):
    global expecting_input_detection
    global eye_tracking_thread
    print("THE MESSAGE SENT IS", x)

    # print("recieving the message")
    response1 = RazaBot.send_message(x)
    # response1 = "test"
    # print("Before IF")

    if isinstance(response1, dict):
        
        if response1["intent"] == 'raise_hand':
            tts(response1["text"], "en-US")
            if response1["entities"]["side"] == "right":
                servo_commandr = "#1P2500#2P2432#3P2367#4P2367#5P2400#6P500#7P1500#8P1500#9P1500#10P1852#11P1500#12P1500#13P1500#14P1500#15P1500#17P1500#18P1500#19P1500#21P2200#22P2200#23P2200#24P2500#25P2200#26P2500#27P1200#28P1500#29P2251#30P2472#31P1500#32P1500T500D500\r\n"
                # serialSender.Ser(servo_commandr)
                talking_scenario(5, "any", servo_commandr)
                print("Raised Right")
            elif response1["entities"]["side"] == "left":
                servo_commandl = "#1P2333#2P2398#3P2400#4P2367#5P2400#6P500#7P710#8P1460#9P2220#10P1852#11P1500#12P1500#13P1500#14P1500#15P1500#17P1500#18P1500#19P1500#21P2200#22P2200#23P2200#24P2500#25P2200#26P2500#27P1500#28P1500#29P1500#30P2472#31P1500#32P1500T500D500\r\n"
                # serialSender.Ser(servo_commandl)
                talking_scenario(5, "any", servo_commandl)
                print("Raised Left")
            else:
                servo_commandb = "#1P2500#2P2500#3P2500#4P2500#5P2500#6P500#7P710#8P1460#9P2200#10P1852#11P1500#12P1500#13P1500#14P1500#15P1500#17P1500#18P1500#19P1500#21P2200#22P2200#23P2200#24P2500#25P2200#26P2300#27P1223#28P1500#29P2160#30P2472#31P1500#32P1500T500D500\r\n"
                # serialSender.Ser(servo_commandb)
                talking_scenario(5, "any", servo_commandb)
                print("Raised both")
            time.sleep(5)
            reset_command = "#1P2200#2P2200#3P2500#4P2500#5P2500#6P500#7P2000#8P1400#9P1500#10P1852#11P1500#12P1500#13P1400#14P1500#15P1500#16P1470#17P1500#18P1500#19P1500#21P2200#22P2200#23P2200#24P2500#25P2200#26P2500#27P1400#28P1500#29P1650#30P2472#31P1500#32P1500T500D500\r\n"
            # serialSender.Ser(reset_command)
            talking_scenario(5, "any", reset_command)
            return "Im tired I will put my arms down now."
        elif response1["intent"] == 'raise_hand_ar':
            tts(response1["text"], "ar-LB")
            if response1["entities"]["side"] == "right":
                servo_commandr = "#1P2500#2P2432#3P2367#4P2367#5P2400#6P500#7P1500#8P1500#9P1500#10P1852#11P1500#12P1500#13P1500#14P1500#15P1500#17P1500#18P1500#19P1500#21P2200#22P2200#23P2200#24P2500#25P2200#26P2500#27P1200#28P1500#29P2251#30P2472#31P1500#32P1500T500D500\r\n"
                # serialSender.Ser(servo_commandr)
                talking_scenario(5, "any", servo_commandr)
                print("Raised Right")
            elif response1["entities"]["side"] == "left":
                servo_commandl = "#1P2333#2P2398#3P2400#4P2367#5P2400#6P500#7P710#8P1460#9P2220#10P1852#11P1500#12P1500#13P1500#14P1500#15P1500#17P1500#18P1500#19P1500#21P2200#22P2200#23P2200#24P2500#25P2200#26P2500#27P1500#28P1500#29P1500#30P2472#31P1500#32P1500T500D500\r\n"
                # serialSender.Ser(servo_commandl)
                talking_scenario(5, "any", servo_commandl)
                print("Raised Left")
            else:
                servo_commandb = "#1P2500#2P2500#3P2500#4P2500#5P2500#6P500#7P710#8P1460#9P2200#10P1852#11P1500#12P1500#13P1500#14P1500#15P1500#17P1500#18P1500#19P1500#21P2200#22P2200#23P2200#24P2500#25P2200#26P2300#27P1223#28P1500#29P2160#30P2472#31P1500#32P1500T500D500\r\n"
                # serialSender.Ser(servo_commandb)
                talking_scenario(5, "any", servo_commandb)
                print("Raised both")
            time.sleep(5)
            reset_command = "#1P2200#2P2200#3P2500#4P2500#5P2500#6P500#7P2000#8P1400#9P1500#10P1852#11P1500#12P1500#13P1400#14P1500#15P1500#16P1470#17P1500#18P1500#19P1500#21P2200#22P2200#23P2200#24P2500#25P2200#26P2500#27P1400#28P1500#29P1650#30P2472#31P1500#32P1500T500D500\r\n"
            # serialSender.Ser(reset_command)
            talking_scenario(5, "any", reset_command)
            return "حَنَزِّلْ إيدَيِّ هَلّْلَءْ لأَنّي تْعِبِتْ."
        elif response1["intent"] == "take selfie":
            tts(response1['text'], "en-US")
            selfie_command = "#1P2500#2P2500#3P2500#4P2500#5P2500#6P500#7P1500#8P1500#9P1500#10P1852#11P1500#12P1500#13P1500#14P1500#15P1500#17P1500#18P1500#19P1500#21P600#22P600#23P2200#24P2500#25P600#26P2500#27P2240#28P780#29P1790#30P2482#31P1500#32P1500T500D500\r\n"
            # serialSender.Ser(selfie_command)
            talking_scenario(5, "any", selfie_command)
            print("Took selfie")
            time.sleep(6)
            reset_command = "#1P2200#2P2200#3P2500#4P2500#5P2500#6P500#7P2000#8P1400#9P1500#10P1852#11P1500#12P1500#13P1400#14P1500#15P1500#16P1470#17P1500#18P1500#19P1500#21P2200#22P2200#23P2200#24P2500#25P2200#26P2500#27P1400#28P1500#29P1650#30P2472#31P1500#32P1500T500D500\r\n"
            # serialSender.Ser(reset_command)
            talking_scenario(5, "any", reset_command)
            return "I hope it was a nice selfie send it to me when you can."
        elif response1["intent"] == "take selfie ar":
            tts(response1['text'], "ar-LB")
            selfie_command = "#1P2500#2P2500#3P2500#4P2500#5P2500#6P500#7P1500#8P1500#9P1500#10P1852#11P1500#12P1500#13P1500#14P1500#15P1500#17P1500#18P1500#19P1500#21P600#22P600#23P2200#24P2500#25P600#26P2500#27P2240#28P780#29P1790#30P2482#31P1500#32P1500T500D500\r\n"
            # serialSender.Ser(selfie_command)
            talking_scenario(5, "any", selfie_command)
            print("Took selfie")
            time.sleep(6)
            reset_command = "#1P2200#2P2200#3P2500#4P2500#5P2500#6P500#7P2000#8P1400#9P1500#10P1852#11P1500#12P1500#13P1400#14P1500#15P1500#16P1470#17P1500#18P1500#19P1500#21P2200#22P2200#23P2200#24P2500#25P2200#26P2500#27P1400#28P1500#29P1650#30P2472#31P1500#32P1500T500D500\r\n"
            # serialSender.Ser(reset_command)
            talking_scenario(5, "any", reset_command)
            return "أكيد الصُورى حَتْكُونْ حِلْوِ لأَنُّو أَنَا فِيَا. بْعَتْلِي الصُورَى عَلْ خَاصْ"
        elif response1["intent"] == "greeting":
            tts(response1["text"], "en-US")
            greet_command = "#1P2500#2P2500#3P2500#4P2500#5P2500#6P500#7P500#8P1500#9P1430#10P1852#11P1500#12P1500#13P1500#14P1500#15P1500#17P1500#18P1500#19P2500#21P1000#22P1100#23P1133#24P1267#25P2200#26P2500#27P1667#28P1030#29P1820#30P2192#31P1500#32P1500T500D500\r\n"
            # serialSender.Ser(greet_command)
            talking_scenario(5, "any", greet_command)
            return "Nice to meet you"
        elif response1["intent"] == "greeting_ar":
            tts(response1["text"], "ar-LB")
            greet_command = "#1P2500#2P2500#3P2500#4P2500#5P2500#6P500#7P500#8P1500#9P1430#10P1852#11P1500#12P1500#13P1500#14P1500#15P1500#17P1500#18P1500#19P2500#21P1000#22P1100#23P1133#24P1267#25P2200#26P2500#27P1667#28P1030#29P1820#30P2192#31P1500#32P1500T500D500\r\n"
            # serialSender.Ser(greet_command)
            talking_scenario(5, "any", greet_command)
            return "تْشَرّْرَفِتْ فِيْكْ حَبِيْبِيْ"
        elif response1['intent'] == "like":
            tts(response1['text'], "en-US")
            like_command = "#1P1500#2P1500#3P1500#4P1500#5P1500#6P500#7P1500#8P1500#9P1500#10P1852#11P1500#12P1500#13P1500#14P1500#15P1500#17P1500#18P1500#19P1500#21P500#22P500#23P500#24P500#25P2200#26P2500#27P1977#28P1167#29P1750#30P2472#31P1500#32P1500T500D500\r\n"
            # serialSender.Ser(like_command)
            talking_scenario(5, "any", like_command)
            time.sleep(3)
            return "Nice Like"
        elif response1['intent'] == "like_ar":
            tts(response1['text'], "ar-LB")
            like_command = "#1P1500#2P1500#3P1500#4P1500#5P1500#6P500#7P1500#8P1500#9P1500#10P1852#11P1500#12P1500#13P1500#14P1500#15P1500#17P1500#18P1500#19P1500#21P500#22P500#23P500#24P500#25P2200#26P2500#27P1977#28P1167#29P1750#30P2472#31P1500#32P1500T500D500 \r\n"
            # serialSender.Ser(like_command)
            talking_scenario(5, "any", like_command)
            time.sleep(3)
            return "حِلُوْ"
        elif response1["intent"] == 'new_user':
            global New_User
            global Name
            Name = response1['name']
            print("NEW USER IS FOUND", Name)

            New_User = True

            # client_socket.send(Name)

        elif response1["intent"] == 'denied name':
            global denied_name
            denied_name = True

            # print(response1)
        elif response1["intent"] == 'rock_paper_seaser':
            tts(response1['text'], "en-US")
            close_eye()
            subprocess.run([r"C:/Users/WOB/AppData/Local/Programs/Python/Python311/python.exe",
                           "RockPaperScissors.py"], check=True, text=True, shell=True)
            run_thread()
            return "I had fun playin with you"
        elif response1["intent"] == 'rock_arabic':
            tts(response1['text'], "ar-LB")
            close_eye()
            subprocess.run([r"C:/Users/WOB/AppData/Local/Programs/Python/Python311/python.exe",
                           "RockPaperScissorsArabic.py"], check=True, text=True, shell=True)
            run_thread()
            return "لِّعْبِهْ حِلوَى. اتْسَلّيْنا فِيَا"
        elif response1["intent"] == "finger_count":
            tts(response1['text'], "en-US")
            close_eye()
            subprocess.run([r"C:/Users/WOB/AppData/Local/Programs/Python/Python311/python.exe",
                           "FingerCounter.py"], check=True, text=True, shell=True)
            run_thread()
            return "Okay I'm stopping counting your finger"
        elif response1["intent"] == "finger_count_arabic":
            tts(response1['text'], "ar-LB")
            close_eye()
            subprocess.run([r"C:/Users/WOB/AppData/Local/Programs/Python/Python311/python.exe",
                           "FingerCounterArabic.py"], check=True, text=True, shell=True)
            run_thread()
            return "ماشِيْ حَوَئّْئِفْ عِدْ أَصابِيعَكْ"
        elif response1["intent"] == 'object_detection':
            tts(response1['text'], "en-US")
            close_eye()
            subprocess.run([r"C:/Users/WOB/AppData/Local/Programs/Python/Python311/python.exe",
                           "object_tracking.py"], check=True, text=True, shell=True)
            # return " "
            run_thread()
            return "Correct me if i didn't see the object correctly"
        elif response1["intent"] == 'object_detection_arabic':
            tts(response1['text'], "ar-LB")
            close_eye()
            subprocess.run([r"C:/Users/WOB/AppData/Local/Programs/Python/Python311/python.exe",
                           "object_tracking_ar.py"], check=True, text=True, shell=True)
            # return ""
            run_thread()
            return "خَبِّرني إِزَا شِفِتْ شِي غَلَط"

        elif response1["intent"] == 'mimic_my_hand':
            tts(response1['text'], "en-US")
            close_eye()
            subprocess.run([r"C:/Users/WOB/AppData/Local/Programs/Python/Python311/python.exe",
                           "handTrackingModule.py"], check=True, text=True, shell=True)
            return "okay stopped mimicking your hand"
        elif response1["intent"] == 'mimic_my_hand_ar':
            tts(response1['text'], "ar-LB")
            close_eye()
            subprocess.run([r"C:/Users/WOB/AppData/Local/Programs/Python/Python311/python.exe",
                           "handTrackingModuleAR.py"], check=True, text=True, shell=True)
            print("done mimick")
            run_thread()
            return "ماشي حَوَئّْئِفْ  تَئْليدْ إِيْدَكْ"
        elif response1["intent"] == 'beard_detection_arabic':
            tts(response1['text'], "ar-LB")
            close_eye()
            subprocess.run([r"C:/Users/WOB/AppData/Local/Programs/Python/Python311/python.exe",
                           "FindBeardArabic.py"], check=True, text=True, shell=True)
            run_thread()
            # return "ماشي حَوَءِّفْ  تَءْليدْ أِيْدَكْ"
            return "شُو هَلْ مَنْظَرْ لِأِدَّامِيْ"
        elif response1["intent"] == 'beard_detection':
            tts(response1['text'], "en-US")
            close_eye()
            subprocess.run([r"C:/Users/WOB/AppData/Local/Programs/Python/Python311/python.exe",
                           "FindBeardArabic.py"], check=True, text=True, shell=True)
            run_thread()
            return "You look ugly."
        elif response1["intent"] == "conversation":
            return response1['gpt_response']
        elif response1['intent'] == "dance":
            tts(response1["text"], "en-US")
            close_eye()
            subprocess.run([r"C:/Users/WOB/AppData/Local/Programs/Python/Python311/python.exe",
                           "dance.py"], check=True, text=True, shell=True)
            run_thread()
            return "I hope you like my ammazing dance"
        elif response1['intent'] == "dance_ar":
            tts(response1["text"], "ar-LB")
            close_eye()
            subprocess.run([r"C:/Users/WOB/AppData/Local/Programs/Python/Python311/python.exe",
                           "dance.py"], check=True, text=True, shell=True)
            run_thread()
            return "بِشَرَفَكْ, عَجْبِتَكْ شِي رَئِصْتِي"
        elif response1['intent'] == "distance":
            tts(response1["text"], "en-US")
            close_eye()
            subprocess.run([r"C:/Users/WOB/AppData/Local/Programs/Python/Python311/python.exe",
                           "detect_distance.py"], check=True, text=True, shell=True)
            run_thread()
            return "I will stop calculating distance"
        elif response1['intent'] == "distance_arabic":
            tts(response1["text"], "ar-LB")
            close_eye()
            subprocess.run([r"C:/Users/WOB/AppData/Local/Programs/Python/Python311/python.exe",
                           "detect_distance_ar.py"], check=True, text=True, shell=True)
            run_thread()
            return "ماشي"
        elif response1['intent'] == "intent_count_ar":
            tts(response1["text"], "ar-LB")
            close_eye()
            subprocess.run([r"C:/Users/WOB/AppData/Local/Programs/Python/Python311/python.exe",
                           "count7_ar.py"], check=True, text=True, shell=True)
            run_thread()
            return "سَهْلِ كانِتْ"
        elif response1['intent'] == "intent_count":
            tts(response1["text"], "en-US")
            close_eye()
            subprocess.run([r"C:/Users/WOB/AppData/Local/Programs/Python/Python311/python.exe",
                           "count7.py"], check=True, text=True, shell=True)
            run_thread()
            return "It was Easy"
        elif response1['intent'] == "intent_not_count":
            close_eye()
            subprocess.run([r"C:/Users/WOB/AppData/Local/Programs/Python/Python311/python.exe",
                           "notcount.py"], check=True, text=True, shell=True)
            run_thread()
            return response1['text']
        elif response1['intent'] == "intent_not_count_ar":
            close_eye()
            subprocess.run([r"C:/Users/WOB/AppData/Local/Programs/Python/Python311/python.exe",
                           "notcount_ar.py"], check=True, text=True, shell=True)
            run_thread()
            return response1['text']
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
                        print("Name recieved: " + Name)
                        client_socket.send(Name.encode())

                    else:
                        New_User = False
                        Name = received_json['name']
                        # print("Name: "+ Name)
                        print("Unknown name")
                        while not New_User:
                            print("Entering LOOP")
                            time.sleep(1)
                        client_socket.send(new_name.encode())
                        set_Name_deny_False()

                else:
                    print("No data received from the client")
                    break  # Break out of the loop if no data is received
        except Exception as e:
            print(f"Error: {str(e)}")
        finally:
            # Close the client socket
            client_socket.close()

