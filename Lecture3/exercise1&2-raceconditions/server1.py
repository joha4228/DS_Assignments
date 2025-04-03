import socket
import threading

def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, num):
        if num % i == 0:
            return False
    return True

def handle_client(clientConnection, clientAddress):
    print("Connected client:", clientAddress)

    while True:
        data = clientConnection.recv(1024).decode()
        if not data:
            break
        print(f"Received from {clientAddress}: {data}")

        if data == 'bye':
            clientConnection.send('Goodbye!'.encode())
            break
        elif data.isdigit():
            number = int(data)
            if is_prime(number):
                clientConnection.send(f"{number} is a prime number.".encode())
            else:
                clientConnection.send(f"{number} is not a prime number.".encode())
        else:
            clientConnection.send("Invalid input. Please send an integer number or 'bye' to exit.".encode())

    clientConnection.close()
    print(f"Connection with {clientAddress} closed.")

# Constants
LOCALHOST = "127.0.0.1"
PORT = 8080

# Create a server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((LOCALHOST, PORT))
server.listen()
print("Server started")
print("Waiting for client requests...")

while True:
    clientConnection, clientAddress = server.accept()
    client_thread = threading.Thread(target=handle_client, args=(clientConnection, clientAddress))
    client_thread.start()
