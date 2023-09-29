import socket
import threading

def handle_client(client_socket, clients):
    try:
        while True:
            message = client_socket.recv(1024).decode()
            if not message:
                break

            # Send the message to all connected clients except the sender
            for other_socket in clients:
                if other_socket != client_socket:
                    other_socket.send(message.encode())
    except Exception as e:
        print(f"Error handling client: {e}")

    clients.remove(client_socket)
    client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('0.0.0.0', 12345)
    server_socket.bind(server_address)
    server_socket.listen()

    print("Server started. Waiting for connections...")

    connected_clients = []

    while True:
        try:
            client_socket, client_address = server_socket.accept()
            print(f"Connection established with client: {client_address}")

            connected_clients.append(client_socket)

            client_thread = threading.Thread(target=handle_client, args=(client_socket, connected_clients))
            client_thread.start()
        except Exception as e:
            print("Error accepting connection:", e)

if __name__ == "__main__":
    start_server()

