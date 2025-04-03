import zmq
import sys


# Provide two ports of two different servers to connect to simultaneously.
port = "5556"
if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)

if len(sys.argv) > 2:
    port1 =  sys.argv[2]
    int(port1)


# Client is created with a socket type “zmq.REQ”. 
# Notice that the same socket can connect to two different servers.
context = zmq.Context()
print("Connecting to server...") 
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:%s" % port)
if len(sys.argv) > 2:
    #  The "Unbound variable"-error occurs bc this port doesn't exist if only 1 argument is given when running the program.
    #  And u can't use a variable that does not exist. Because of the if statements, it's not a problem. 
    socket.connect("tcp://localhost:%s" % port1)

#  Do 10 requests, waiting each time for a response
for request in range(1,10):
    print("Sending request ", request,"...")
    socket.send_string(f"Hello{request}")  # The 0MQ library has this method so u don'thave to .encode() or (b"Hello")
    # Get the reply. 
    message = socket.recv(1024).decode()
    print("Received reply ", request, "[", message, "]")