#import socket module 
from socket import * 
import sys # In order to terminate the program 
from threading import Thread
import threading
import signal

stop_event = threading.Event()
threads = []

def listen(serverSocket):
    serverSocket.listen(5)
    serverSocket.settimeout(1)
    while not stop_event.is_set():
        try:
            connectionSocket, _ = serverSocket.accept()
        except:
            continue
        t = Thread(target=connect, args=(connectionSocket,))
        t.start()
        print("subThread created")
        threads.append(t)
    
def connect(connectionSocket):
    try:
        message = connectionSocket.recv(1024)
        filename = message.split()[1]                  
        f = open(filename[1:])                    
        outputdata = f.read()              
        #Send one HTTP header line into socket 
        connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
        connectionSocket.send("\r\n".encode())    
        #Send the content of the requested file to the client 
        for i in range(0, len(outputdata)):            
            connectionSocket.send(outputdata[i].encode()) 
        connectionSocket.send("\r\n".encode())
        connectionSocket.close()
    except IOError: 
        #Send response message for file not found        
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n".encode())
        #Close client socket 
        connectionSocket.close()
        
def sigint_handler(signum, frame):
    print("\nprepare to exit...")
    stop_event.set()
        
def main():
    serverSocket = socket(AF_INET, SOCK_STREAM) 
    #Prepare a sever socket 
    serverSocket.bind(('localhost', 12345))
    serverSocket.listen(5)
    mainThread = Thread(target=listen, args=(serverSocket,))
    mainThread.start()
    print("mainThread created")

    signal.signal(signal.SIGINT, sigint_handler)

    print("server is running, press Ctrl+C to stop...")

    while not stop_event.wait(1):
        pass
    
    # 等待子线程终止
    print("waiting for sub-thread to stop...")
    for t in threads:
        t.join()
    mainThread.join()
    print("server stopped")
    serverSocket.close() 
    sys.exit() #Terminate the program after sending the corresponding data         
    
if __name__ == "__main__":
    main()