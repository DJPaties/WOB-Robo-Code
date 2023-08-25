import socket
import json
import botConnecter
# def start_server():
#     def send_name_Vision(msg):
#         connection.send(msg.encode())

sendName = False
response_rasa=""
def setSendNameTrue():
    sendName==True

def start_server():
        # Create a socket object
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to a specific IP address and port
        server_address = ('0.0.0.0', 12345)  # Use 0.0.0.0 to listen on all available interfaces
        server_socket.bind(server_address)

        # Listen for incoming connections
        server_socket.listen(1)

        print("Waiting for a connection...")
        # response = server_socket.recv(1024).decode()
        # print("Received from server:", response)
        while True:
            connection, client_address = server_socket.accept()

            try:
                print("Connection established with:", client_address)
            
                while True:
                    data = connection.recv(1024).decode()
                    if not data:
                        break

                    print("Received:", data)
                    print(type(data))
                    response = json.loads(data)

                    if "known" in response and response["known"] :
                        print("Name found: ", response['name'])
                        botConnecter.set_Name(response['name'])
                    else:
                         if sendName:
                            print("send the name to a client")
                            connection.send(botConnecter.get_Name().encode())




            finally:
                connection.close()
        # Close the server socket (this will never be reached in an infinite loop)
        server_socket.close()

     

# message = "Hello, client!"
# server_socket.send(message.encode())


    # while True:
    #     connection, client_address = server_socket.accept()

    #     try:
    #         print("Connection established with:", client_address)
        
    #         while True:
    #             data = connection.recv(1024)
    #             if not data:
    #                 break
    #             print("Received:", data.decode())
    #             json_msg = data.decode()
    #             response = json.loads(json_msg)
    #             print(response['known']," ",type(response['known']))

    #             if "known" in response and response["known"] :
    #                 message = "stop"
    #                 for key in response:
    #                     name=response[key]
    #                     #send_name_Vision(message)
    #                     print("true")
    #             else:
    #                 message = "name is not recognized"
    #                 # send_name_Vision(message)
    #                 print("false")
    #                 print(botConnecter.main(message))
    #                 user_input=input("enter your name:")
    #                 send_name_Vision(user_input)
                
                
    #     finally:
    #         connection.close()
    #     # Close the server socket (this will never be reached in an infinite loop)
    #     server_socket.close()






