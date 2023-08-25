import json
import requests



def send_message(msg):

    payload = {

                    "sender": "user1",
                    "message": msg
                }
    print("Payload done")
    r = requests.post('https://3f1f-185-127-125-57.ngrok.io/webhooks/rest/webhook', json=payload)
    print("Request done")
    data = r.json()
    # print(type(data))
    # Process the response from the Rasa chatbot
    response = None
    for message in data:
        # print(message["text"])
        response = message["text"]

    # print(response)
    try:
        return_Message = json.loads(response)
        x = (return_Message)
        print(x)
        return return_Message
    except ValueError as e :
        print("Response is not a json")
        
        return response
    # print(type(return_Message))
    # return return_Message
    
    # return data
# print(send_message("yes"))s


