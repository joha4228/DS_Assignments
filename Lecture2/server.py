import socket
import time
from threading import Thread

def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, num):
        if num % i == 0:
            return False
    return True


def waiting(s, t=5):
    print("Waiting for 5 secunds...")
    for i in range(t): 
        current_step = str(i+1) 
        s.send(current_step.encode())
        print(current_step)
        time.sleep(1)
    s.send(b"Great nap! Now I'm back. :)\n")
    print("Awake again.\n")


def handle_client(c, addr):
    print("Connection from " + str(addr))  # Display who is connecting.  
    client_socket.send(b"Thank you for connecting " + str(addr).encode())  # Confirm to client that it is connected.   

    while True:
        data = c.recv(1024).decode()
        if not data:
            break
        print(f"Received from {addr}: {data}")

        if data == "bye":
            c.send('Goodbye!'.encode())
            break
        elif data == "wait":
            waiting(c)
        elif data.isdigit():
            if is_prime(int(data)):
                print(f"{addr}: {data} is prime")
                c.send(f'{data} is prime.'.encode())
            else:
                print(f"{addr}: {data} is not prime")
                c.send(f'{data} is not prime.'.encode())
            break
        else:
            c.send(b"'" + data.encode() + b"'")
    
    c.close()
    print(f"Connection with {addr} closed.")



#-----------------------------------------------------------------------------------------------------------------------#
# set up server with constant port and ip.
PORT = 5000
hostName = socket.gethostname()  # Get host name (dsvm1)
HOST_IP  = socket.gethostbyname(hostName)  # Get the IP matching the hostname (10.92.1.60)
print(f'Server address : {HOST_IP}')

# Call socket method, to create server socket.
# - socket.AF_INET refers to the IPv4 address family.
# - socket.SOCK_STREAM refers to connection oriented TCP protocol. 
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
# Listen to incomming requests on this address and port.     
server_socket.bind((HOST_IP, PORT))
    
# Configure how many clients the server can listen to simultainiously.
server_socket.listen(10)
print("Server started")
print("Waiting for client requests...")


while True:    
    # Get socket-object and address from a connecting client.
    client_socket, client_address = server_socket.accept()
     
    # Handle the clients requests on seperate thread 
    # to allow other clients to access this server simoultaniously. 
    Thread(target=handle_client, args=(client_socket, client_address)).start()

