import socket
import threading
import json
def handle_client(client_socket, client_id, clients):
    try:
        while True:
            message = client_socket.recv(1024).decode()
            if not message:
                break

            for other_id, other_socket in clients.items():
                if other_id != client_id:
                    other_socket.send(message.encode())
    except Exception as e:
        print(f"Error handling client {client_id}: {e}")

    del clients[client_id]
    client_socket.close()
    print(f"Connection with client {client_id} closed")





def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('0.0.0.0', 12345)
    server_socket.bind(server_address)
    server_socket.listen()

    print("Server started. Waiting for connections...")

    clients = {}
    client_id = 1

    while client_id <= 2:
        try:
            client_socket, client_address = server_socket.accept()
            print(f"Connection established with client {client_id}: {client_address}")

            clients[client_id] = client_socket

            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_id, clients))
            client_thread.start()

            client_id += 1
        except Exception as e:
            print("Error accepting connection:", e)

start_server()
