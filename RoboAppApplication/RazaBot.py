import json
import requests
def send_message(msg):
    payload = {

                    "sender": "user1",
                    "message": msg
                }
    print("Payload done")
    # r = requests.post('http://localhost:5005/webhook/rest/webhook', json=payload)
    r = requests.post('http://f516-185-127-125-53.ngrok.io/webhooks/rest/webhook', json=payload)
    print("Request done")
    data = r.json()
    print(data)
    # Process the response from the Rasa chatbot
    response = None
    for message in data:

        response = message["text"]
    # print("Enter try")
    try:
        return_Message = json.loads(response)
        x = (return_Message)
        print(x)
        return return_Message
    except ValueError as e :
        # print("Response is not a json")

        print(response)
        return response

# while True:
#     msg = input("الاسم منو موجود")
#     print(send_message(msg))    


