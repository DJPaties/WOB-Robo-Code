import socket
import json
response1 = {'known': True, 'name': "Mohammad Dghaily"}
response2 = {'known': False, 'name': ""}
response3 = "new_user Mohammad Dghaily"
response4 = "None of the above"

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('192.168.0.105', 12345)
client_socket.connect(server_address)

try:
    while True:
        message = input("Enter a message: ")
        if message == '1':
            client_socket.send((json.dumps(response1)).encode())
        elif message == '2':
            client_socket.send((json.dumps(response2)).encode())
        elif message == '3':
            client_socket.send(response3.encode())
        elif message == '4':
            client_socket.send(response4.encode())
        else:
            client_socket.send(str(message).encode())

        response = client_socket.recv(1024).decode()
        print(response)
except KeyboardInterrupt:
    pass

finally:
    client_socket.close()
