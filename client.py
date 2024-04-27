# Author - Brett Sullivan
# sullbret@oregonstate.edu
# Developed - 3-13-24
# References : https://realpython.com/python-sockets/#echo-client-and-server

# Python program to implement client side of chat room.
import socket
import threading


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'
    port = 12345
    client_socket.connect((host, port))

    while True:
        message = input("Enter your message ('/q' to quit, '/game' to play rock-paper-scissors): ")
        client_socket.sendall(message.encode('utf-8'))

        if message.strip() == "/q":
            print("Exiting...")
            break
        elif message.strip() == "/game":
            play_game(client_socket)
        else:
            data = client_socket.recv(1024)
            response = data.decode('utf-8')
            if data.strip() == "/q":
                print("server requests exit, shutting down")
                client_socket.close()
            print(f"Server response: {response}")

    client_socket.close()    

def play_game(client_socket):
    data = client_socket.recv(1024)
    print(data.decode('utf-8'))
    choice = input().strip().lower()
    client_socket.sendall(choice.encode('utf-8'))

    result = client_socket.recv(1024).decode('utf-8')
    print(f"Game result: {result}")

if __name__ == "__main__":
    main()
