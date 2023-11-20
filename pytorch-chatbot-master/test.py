import json
import requests

def send_message(msg):

    
    print(msg)
    url = 'http://127.0.0.1:5000/receive'
    data = {'message': msg}
    response = requests.post(url, json=data)
    data = response.json()
    if data["intent"] == "conversation":
        return data['gpt_response']
    else :
        return data['text']
    # if data['message'] == False:
    #     time.sleep(1)
    #     send_message(data['intent'])
    # else:
    
while True:
    x = send_message(input(">"))
    print(x)