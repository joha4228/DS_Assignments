# Client
import socket

def client_program():
    vm_address = '10.92.1.60'
    port = 5000  # The server is listening on this port 

    # Instanciate socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connection to hostname on the port.
    try:
        print("Trying to connect...")
        client_socket.connect((vm_address, port))
    except:
        print("Connection failed. :(")
        raise
        

    # receive data from the server
    data = client_socket.recv(1024)

    # print the data received
    print(data.decode())

    print("Send a message and hear the echo! (the string 'bye' closes connection) \n")

    # send data to the server
    while(True):
        message = input(" -> ")
        #if message.lower().strip() == "prime":
        #    pass

        client_socket.send(message.encode())
        
        if message.lower().strip() == "bye":
            # close the client socket
            client_socket.close()


if __name__ == '__main__':
    client_program()