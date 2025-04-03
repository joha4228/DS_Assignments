# The asyncio module is a way to use asynchronous in Python 
import asyncio
import random

numbers_list = []

# Important: Generally, “async” defines an async coroutine, and “await” suspends or yields execution to another coroutine from within a coroutine
# (await is used for the pre-implemented functions in the module)
async def client(lock):
    SERVER = "127.0.0.1"
    PORT = 8080

    # Here we use asyncio to open_connection with the specified server and port
    # We have a reader that reads the socket and a writer that writes to the socket
    # These are part of the asyncio module and they offer several functions that can be used for asynchronous
    reader, writer = await asyncio.open_connection(SERVER, PORT)

    try:
        async with lock: # Use lock object to make sure a thread is the only one operating on the list in the current moment. 
            # Select a random integer from 1 to 100
            number = random.randint(1, 100)

            # Use the writer to write to the server (Remember to typecast the number to string and encode it)
            writer.write(str(number).encode())

            # "Drain" the socket using the writer 
            await writer.drain()

            # Use the reader to read the data from the server
            data = await reader.read(1024) # You have to specify this unless you know that you will get an EOF character('\n') at some point.

            # Decode the data and print the response
            print(data.decode())

        # Add a 5-second delay with asyncio
        await asyncio.sleep(5)

    finally:
        # Close the writer 
        writer.close()
        # Wait until the stream is closed.
        # Call wait_closed(), after close() to wait until the underlying connection is closed, ensuring that all data has been flushed before e.g. exiting the program.
        await writer.wait_closed()

async def main():
    global numbers_list
    # initialise list with 5 random numbers
    numbers_list = [random.randint(1,100) for _ in range(5)]


    # Get the number of threads 
    num_clients = int(input("Enter the number of clients to initiate: "))

    lock = asyncio.Lock()
    
    # The logic is similar to the synchronous implementation for the main function
    tasks = []
    for _ in range(num_clients):
        # Now we create tasks for the threads 
        task = asyncio.create_task(client(lock))
        # Append the empty list with the tasks
        tasks.append(task)

    # Produce the results as soon as they are done
    # Note: An asterisk * denotes iterable unpacking. Its operand must be an iterable one. 
    # The iterable is expanded into a sequence of items, which are included in the new tuple, list, or set, at the site of the unpacking.
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    # Run the main with asyncio
    asyncio.run(main())
