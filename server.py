# Author - Brett Sullivan
# sullbret@oregonstate.edu
# Developed - 3-13-24
# References : https://realpython.com/python-sockets/#echo-client-and-server
# https://www.anthonymorast.com/blog/2020/03/21/a-client-and-server-chat-application-in-python/ 
# https://www.geeksforgeeks.org/socket-programming-python/ 
# https://python.plainenglish.io/python-networking-101-building-a-simple-chat-app-with-socket-b69389702b9d

# Python program to implement server side of chat room. 
import socket 
import threading
import random

# Global flag to indicate if the server should keep running
server_running = True
 
def handle_client(client_socket):
    global server_running
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        message = data.decode('utf-8')
        print(f"Received message from client: {message}")

        # Check if the client sent "/q" to quit or requested to play a game
        if message.strip() == "/q":
            server_running = False
            print("shutting down")
        elif message.strip() == "/game":
            play_game(client_socket)
        else:
            response = input("Enter your response: ")  # Get response from server user
            client_socket.sendall(response.encode('utf-8'))

    # Shutdown and close the client socket
    client_socket.shutdown(socket.SHUT_RDWR)
    client_socket.close() 
   
   
def play_game(client_socket):
    options = ["rock", "paper", "scissors"]
    server_choice = random.choice(options)

    client_socket.sendall("Let's play Rock-Paper-Scissors! Enter your choice (rock/paper/scissors): ".encode('utf-8'))
    client_choice = client_socket.recv(1024).decode('utf-8').strip().lower()

    if client_choice in options:
        if client_choice == server_choice:
            result = "It's a tie!"
        elif (client_choice == "rock" and server_choice == "scissors") or \
             (client_choice == "paper" and server_choice == "rock") or \
             (client_choice == "scissors" and server_choice == "paper"):
            result = "You win!"
        else:
            result = "You lose!"
    else:
        result = "Invalid choice. Please choose rock, paper, or scissors."

    client_socket.sendall(result.encode('utf-8'))
    
        
def main():
    global server_running
        
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'
    port = 12345
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")

    while server_running:
        # Accept incoming connection from client
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")
        
        # Start a new thread to handle communication with the client
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()
        if not server_running:
            break  # Exit the loop if server_running is False
        
    # Close the server socket after all clients are handled
    print("Shutting down server")
    server_socket.shutdown(socket.SHUT_RDWR)
    server_socket.close()
        

if __name__ == "__main__":
    main()    