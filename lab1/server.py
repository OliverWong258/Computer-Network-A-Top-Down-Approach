#import socket module 
from socket import * 
import sys # In order to terminate the program 
serverSocket = socket(AF_INET, SOCK_STREAM) 
#Prepare a sever socket 
#Fill in start 
serverSocket.bind(('localhost', 12345))
serverSocket.listen(5)
serverSocket.settimeout(2) 
#Fill in end 
try:
    while True: 
        #Establish the connection 
        print("begin loop")
        try:
            print('Ready to serve...') 
            connectionSocket, addr = serverSocket.accept()
            connectionSocket.settimeout(2)
        except:
            print("serverSocket timeout")
            continue
        try:
            try: 
                message =   connectionSocket.recv(1024)              
            except:
                print("connectionSocket timeout")
                continue
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
            connectionSocket.send("\r\n".encode())
            #Close client socket 
            connectionSocket.close()
except(KeyboardInterrupt):
    print("\nServer is shutting down.")
finally: 
    print("\nExitting")            
    serverSocket.close() 
    sys.exit() #Terminate the program after sending the corresponding data         