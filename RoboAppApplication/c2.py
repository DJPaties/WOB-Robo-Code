import socket
import json
import RazaBot
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('192.168.16.166', 12345)
client_socket.connect(server_address)

def process_input(input):
    try:
        # Attempt to parse the input as JSON
        response = json.loads(input)
        if "known" in response and response["known"] :
            print("Name found: ", response['name'])
            return response['name']
        else:
            pass
    except json.JSONDecodeError:
        pass

    # If JSON parsing failed or the type is not "new_user", treat it as a regular string
    parts = input.split(" ", 1)
    if parts[0] == "new_user" and len(parts) > 1:
        rest_of_sentence = parts[1]
        return rest_of_sentence
    else:
        return "None of the above expected results came"    




try:
    while True:
        message = client_socket.recv(1024).decode()
        print(message)


        if not message:
            break
        response = process_input(str(message))
        client_socket.send(response.encode())
except KeyboardInterrupt:
    pass

finally:
    client_socket.close()
