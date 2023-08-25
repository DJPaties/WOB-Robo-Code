import socket
import json
response1 = {'known': True, 'name': "Mohammad Dghaily"}
response2 = {'known': False, 'name': ""}


server_ip = '192.168.16.157'
server_port = 12345     # Change this to the server's port

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
server_address = (server_ip, server_port)
client_socket.connect(server_address)

# Send a message to the server
message = json.dumps(response1)
client_socket.send(message.encode())

# # Receive and decode the response from the server
response = client_socket.recv(1024).decode()
print("Received from server:", response)
response_name=client_socket.recv(1024).decode()
print("received name from the server:",response_name)


# Close the connection
client_socket.close()

