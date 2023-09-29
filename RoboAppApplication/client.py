import json
import time
import socket
from botConnecter import get_New_User_detected
from botConnecter import set_Name_deny_False

def initialize_client():
    
    try:

        
        
        global client_socket
        global Name
        server_ip = '192.168.16.166'
        server_port = 12345

        # Create a socket object
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to the server
        server_address = (server_ip, server_port)
        client_socket.connect(server_address)
        
        while True:

            print(" Server is on")
            message = client_socket.recv(1024).decode()
            # print(message)
            if not message:
                break
            # response = process_input(str(message))
            # print("THIS IS THE RESPONSE:"+response)
            json_data = json.loads(message)
            if json_data['known'] == True:
                Name = json_data['name']
                client_socket.send(Name.encode())
            elif json_data['known'] == False:
                # Name = input("Enter the new name")
                while not get_New_User_detected:
                    print("Entering LOOP")
                    time.sleep(1)
                client_socket.send(Name.encode())
                set_Name_deny_False()
    except KeyboardInterrupt:
        client_socket.close()

    finally:
        client_socket.close()
