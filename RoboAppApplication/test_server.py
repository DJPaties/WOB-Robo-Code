import socket
import json
def server():
    # Define the server host and port
    host = 'localhost'  # Use 'localhost' for the local machine, or use an IP address
    port = 12345       # Choose a port number

    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the host and port
    server_socket.bind((host, port))

    # Listen for incoming connections
    server_socket.listen(5)

    print(f"Server is listening on {host}:{port}")

    while True:
        # Accept a connection from a client
        client_socket, client_address = server_socket.accept()
        
        print(f"Accepted connection from {client_address}")
        
        try:
            while True:
                # Receive data from the client
                print("Waiting for data")
                data = client_socket.recv(1024).decode('utf-8')
            
                if data:
                    print(f"Received JSON data from client: {data}")
                    
                    # Parse the received JSON data
                    received_json = json.loads(data)
                    
                    # Check if the received JSON contains a "known" key
                    if received_json['known']:
                        Name = received_json['name']
                        print("Received Name is: " + Name)
                        client_socket.send(Name.encode())
                    else:
                        print("Unknown Name")
                        name = input("Enter Name: ")
                        client_socket.send(name.encode('utf-8'))
                else:
                    print("No data received from the client")
                    break  # Break out of the loop if no data is received
        except Exception as e:
            print(f"Error: {str(e)}")
        finally:
            # Close the client socket
            client_socket.close()
