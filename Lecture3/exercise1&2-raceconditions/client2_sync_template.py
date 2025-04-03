import socket
#Import threading to use threads in our python code
import threading
import random
import time

numbers_list = []

def client_thread(lock):
    SERVER = "127.0.0.1"
    PORT = 8080

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER, PORT))

    try:
        lock.acquire() # Get the lock 
        # Choose number from list
        number = random.choice(numbers_list)
        # Remove the chosen number from list
        numbers_list.remove(number)
        lock.release() # Open lock for other threads
        # Send the number to server & get response
        client.send(str(number).encode())
        response = client.recv(1024).decode()
        print(f"Server Response: {response}")
        time.sleep(5)  # Add a 5-second delay to see the response. This puts the thread in the 'wait' stage of its lifecycle, allowing 
    finally:
        client.close()


def main():
    global numbers_list
    # initialise list with 5 random numbers
    numbers_list = [random.randint(1,100) for _ in range(5)]
    print(numbers_list)
    # Create lock for the threads to use
    lock = threading.Lock()

    # Get input for the number of clients to initiate. 
    num_clients = int(input("Enter the number of clients to initiate: "))

    # Create an empty list that we will append later on to carry the threads
    client_threads = []
    # We are not interested in how many times the loop will be run, but it will be run a specific amount of times (input) so use for _
    for _ in range(num_clients):
        # Declare the thread
        thread = threading.Thread(target=client_thread, args=(lock,))
        # Append the list
        client_threads.append(thread)
        #Start the thread
        thread.start()

    # Wait for all client threads to finish
    for thread in client_threads:
        thread.join()

if __name__ == "__main__":
    main()
