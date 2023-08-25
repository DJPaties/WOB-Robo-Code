import RazaBot
import socket
import server
server_ip = '192.168.16.157'
server_port = 12345     # Change this to the server's port
name_to_server=""

expecting_input_detection = None
nanme_Recognized = ""
def send_delay(delay_time):

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

def get_Name():
    return nanme_Recognized

def set_Name(name):
    global nanme_Recognized
    nanme_Recognized = name
  
    
def main(x):
    global expecting_input_detection

    print("THE MESSAGE SENT IS",x)

    
    print("recieving the message")
    # response1 = RazaBot.send_message(x)
    response1 = {
    "text":"Hello mohammad Dghaily",
    "name": "Mohammad Dghaily",
    "intent": "new_user",
    "inputHint": ""
}

    if isinstance(response1,dict):
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
            # print(payload)
            server.setSendNameTrue()
        print("before return")
        return response1['text']
        
        
    else:
        
        expecting_input_detection = True

        return response1
        
        
# def set_name(received_name):
#     global name_to_server
#     name_to_server=received_name
# def get_name():
#     return name_to_server
    
def InputType():
    global expecting_input_detection
    return expecting_input_detection

# while True:
#     msg = input('')
print(main("a"))