import socket
#Import threading to use threads in our python code
from threading import Thread
import random
import time


def client_thread():
    SERVER = "10.92.1.60"  # Switch to "127.0.0.1" for localhost when running server & client on the same machine.
    PORT = 5000

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER, PORT))

    try:
        number = random.randint(1, 100)
        client.send(str(number).encode())
        response = client.recv(1024).decode()
        print(f"Server Response: {response}")
        time.sleep(5)  # Add a 5-second delay to see the response
    finally:
        client.close()


def main():
    # Get input for the number of clients to initiate. 
    number_of_clients = '' 
    while True:
        try:
            number_of_clients = int(input(' -> '))
            break
        except ValueError:
            print("Invalid input. Please enter an integer.")
    
    # Create an empty list that we will append to later on to carry the threads
    threads = []

    # We are not interested in how many times the loop will be run, but it will be run a specific amount of times (input) so use for _
    for _ in range(number_of_clients):
        # Declare the thread
        thread = Thread(target=client_thread) 
        # Append the list
        threads.append(thread)
        #Start the thread
        thread.start()
        
    # Wait for all client threads to finish
    for t in threads:
        t.join()  # the join function makes the program halt until all joint threads have finished.

if __name__ == "__main__":
    main()
