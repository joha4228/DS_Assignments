import threading

def process():
    #not implemented
    pass

def main():
    global numbers_list

    numbers_list = [random.randint(1,100) for _ in range(5)]
    print(numbers_list)

    # lock = threading.Lock()

    num_clients = int(input("Enter the number of clients to initiate: "))

    client_threads = []
    for _ in range(num_clients):
        thread = threading.Thread(target=process)
        client_threads.append(thread)
        thread.start()

    for thread in client_threads:
        thread.join()

if __name__ == "__main__":
    main()