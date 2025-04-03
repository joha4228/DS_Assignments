import zmq
import socket
import sys
import time


# Keep addresses of all nodes in the network (including itself)
ALL_NODES = []


# Class describing the properties of a node
class node:
    def __init__(self, id, address) -> None:
        self.id = id
        self.active = True
        self.address = address
        self.role = "follower"

# Make class for holding Election relevant function 
class Election:
    def __init__(self) -> None:
        pass


def realize_network(configFilePath):
    global ALL_NODES
    # Path to config file is a .txt file provided by user.
    # The config file should contain the id and address for each node in the network
    #   - id and address seperated by comma, each node seperated by newline. 
    with open(configFilePath, 'r') as conf:
        lines = conf.read().splitlines()
        for line in lines:
            id, addr = line.split(',')
            ALL_NODES.append(node(id, addr))

# Create funktionallity for recieving heartbeats
#use zmq
def server_part():
    print(zmq.HEARTBEAT_IVL)



# Create funktionallity for starting election heartbeats
def client_part():
    pass





def main():
    # Get host ip address
    HOST_IP  = socket.gethostbyname(socket.gethostname())
    PORT = '8000'  # set port
    MY_ADDR = "tcp://" + HOST_IP + ":" + PORT
    
    
    if len(sys.argv) < 1:
        realize_network(sys.argv[1])
    else: 
        print("No config file, no node, no fun. Sorry...\n\n \
              ---------------Goodbye!---------------")
        quit()

    
    
if __name__ == "__main__":
    main()


    


