import RazaBot
import socket
import json
from concurrent.futures import ThreadPoolExecutor


# import server


name_detected = False
nanme_Recognized = ""
send_New_Name = False
name_callback_update = None
def send_delay(delay_time):

    pass

def process_input(input):
    try:
        # Attempt to parse the input as JSON
        response = json.loads(input)
        if "known" in response and response["known"] :
            try:
                print("Name found: ", response['name'])
                global name_detected
                name_detected = True
                return response['name']
            except Exception as e:
                return e
        else:
            
            name_detected = False
    except json.JSONDecodeError:
        pass

    # If JSON parsing failed or the type is not "new_user", treat it as a regular string
    parts = input.split(" ", 1)
    if parts[0] == "new_user" and len(parts) > 1:
        rest_of_sentence = parts[1]
        return rest_of_sentence
    else:
        return "None of the above expected results came" 

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
    return nanme_Recognized
    

def set_Name(name):
    global nanme_Recognized
    nanme_Recognized = name

  
    
def main(x):
    global expecting_input_detection

    print("THE MESSAGE SENT IS",x)

    
    print("recieving the message")
    response1 = RazaBot.send_message(x)


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
            print("anything")



        print("before return")
        return response1['text']
        
        
    else:
        
        expecting_input_detection = True

        return response1
        
        
def initialize_client():
    global client_socket
    server_ip = '192.168.0.105'
    server_port = 12345

    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    server_address = (server_ip, server_port)
    client_socket.connect(server_address)
    try:
        while True:
            message = client_socket.recv(1024).decode()
            # print(message)
            if not message:
                break
            response = process_input(str(message))
            global name_detected
            global send_New_Name
            if name_detected and not send_New_Name:
                print("Image is known,"+response)
                name_detected = False
                set_Name(response)
                client_socket.send(response.encode())


            elif not name_detected and not send_New_Name:
                msg = "Aborted Commmand"
                client_socket.send(msg.encode())
            elif name_detected and send_New_Name:
                client_socket.send(response.encode())
            
            
    except KeyboardInterrupt:
        pass

    finally:
        client_socket.close()





# def send_message(msg):
#     client_socket.send(msg.encode())
executer = ThreadPoolExecutor()
executer.submit(initialize_client())
# send_message("Testing")

# def InputType():
#     global expecting_input_detection
#     return expecting_input_detection

# while True:
#     msg = input('')
# print(main(response1))