import requests
def send_message(msg):

    
    print(msg)
    url = 'http://127.0.0.1:5000/receive'
    data = {'message': msg}
    response = requests.post(url, json=data)
    data = response.json()
    print(data)
    return (data)

