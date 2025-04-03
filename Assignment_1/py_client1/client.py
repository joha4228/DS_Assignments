import glob
import threading
import logging
import os
import re

import grpc
import myfirstproto_pb2 as pb2
import myfirstproto_pb2_grpc as pb2_grpc


word_list = []


def count_words(id, file, lock, stub):
    global word_list
    text = ""
    with open(file, 'r') as f:
        text = f.read()

    #  Send off the job of counting the words using gRPC stub
    response = stub.Calculate(pb2.Textk(text=text))
    
    #  Then unpack and append the recveived result to a list.
    try: # Acquire lock and avoid race conditions 
        lock.acquire()   
        # Append in here.
        word_list.extend(response.wordcountlist)
    except:
        print("didn't work")   
    finally:
        lock.release() 
        f.close()


def main():
    threadList = {}
    lock = threading.Lock()

    with grpc.insecure_channel('localhost:9000') as channel:
        stub = pb2_grpc.FrequencyCalculatorStub(channel)
        #   C:\Users\johan\VScodeProjects\Distributed_systems_exercises\Assignment_1\input\file1.txt
        #   C:\Users\johan\VScodeProjects\Distributed_systems_exercises\Assignment_1\py_client1\client.py 
    
        dir_path = os.path.dirname(os.path.realpath(__file__))
        input_paths = glob.glob(os.path.join(dir_path, "../input/*.txt")) 
        
        for id, file_path in enumerate(input_paths):
            print("Starting thread that handles", file_path[-9:])
            fileKthread = threading.Thread(target=count_words, args=(id, file_path, lock, stub,))
            threadList[id] = fileKthread
            fileKthread.start()
            
        for t in threadList.keys():
            threadList[t].join()
        print("All threads finished")

        # Synchronously streaming the elements of word_list (i.e. client call waits for the server to respond.)
        combinedLists = stub.Combine(iter(word_list))  #  Create iterator from iterable list before parsing it.

        # Make the returned list pretty and print
        pretty = {}
        #re.sub(r'(?<!\n)\n(?!\n)', '', str(combinedLists.wordcountlist)).replace('\n', ', ')
        for obj in combinedLists.wordcountlist:
            pretty[obj.word] = obj.count   
        pretty = re.sub(r'[{}]', lambda x: '[' if x.group() == '{' else ']', str(pretty)) 
        print("\nOutput:", pretty)
    

if __name__=="__main__":
    print("\n\t**début**\n")
    logging.basicConfig()
    main()
    print("\n\t**fin**")
