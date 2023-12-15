import json
import requests

# def send_message(msg):
#     print(msg)
#     url = 'http://127.0.0.1:50001/command'
#     data = {'message': msg}
#     requests.post(url, json=data)
#     # if data['message'] == False:
#     #     time.sleep(1)
#     #     send_message(data['intent'])
#     # else:
def send_message(msg):
    
    print(msg)
    url = 'http://127.0.0.1:5000/receive'
    data = {'message': msg}
    response = requests.post(url, json=data)
    data = response.json()
    print(data)
    # if data['message'] == False:
    #     time.sleep(1)
    #     send_message(data['intent'])
    # else:
    return (data)
while True:
    x = send_message(input(">"))
    print(x)