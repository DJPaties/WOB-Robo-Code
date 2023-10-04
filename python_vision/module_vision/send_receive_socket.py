import socket
import json


def send_name_socket( ip_server , port_server ,name ,known ,client_socket):
# def send_name_socket( ip_server , port_server ,name ,known ):





    # Prepare JSON data
    data = {'known': known , 'name ':name }

    json_data = json.dumps(data).encode('utf-8')
    print(f"the data sended is {json_data}")

    # Send JSON data
    client_socket.send(json_data)



def receive_socket(client_socket):
    # Receive response from the server (if applicable)
    response = client_socket.recv(1024).decode('utf-8')
    # response_json = json.loads(response)
    print("Received response:", response)
    return response

if __name__ =="__main__":
    
    
    # # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"socket created .. ")
    ip_server,port_server = "192.168.16.157" ,12345
    # Connect to the server
    server_address = (ip_server,port_server )  # Replace with the server address and port
    client_socket.connect(server_address)
    print(f"print client socket connected to {ip_server} at port {port_server} ")
    send_name_socket(ip_server ,port_server ,"hello" ,True ,client_socket )



# import socket
# import json
# response1 = {'known': True, 'name': "Mohammad Dghaily"}
# response5 = {'known': True, 'name': "Adnan Abdulla"}
# response2 = {'known': False, 'name': ""}
# response3 = "new_user Mohammad Dghaily"
# response4 = "None of the above"

# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_address = ('192.168.16.157', 12345)
# client_socket.connect(server_address)

# try:
#     while True:
#         message = input("Enter a message: ")
#         if message == '1':
#             client_socket.send((json.dumps(response1)).encode())
#         elif message == '2':
#             client_socket.send((json.dumps(response2)).encode())
#         elif message == 'new':
#             client_socket.send(response3.encode())
#         elif message == '4':
#             client_socket.send(response4.encode())
#         elif message == 'name':
#             client_socket.send((json.dumps(response5)).encode())
#         else:
#             client_socket.send(str(message).encode())

#         response = client_socket.recv(1024).decode()
#         print(response)
# except KeyboardInterrupt:
#     pass

# finally:
#     client_socket.close()
