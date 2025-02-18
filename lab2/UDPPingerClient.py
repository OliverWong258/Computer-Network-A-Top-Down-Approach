from socket import *
import time

clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(2)

for i in range(10):
    timeStamp = time.time()
    message = f"Ping {i} {timeStamp}"
    clientSocket.sendto(message.encode(), ("localhost", 12000))
    try:
        returnMsg, serverAddr = clientSocket.recvfrom(1024)
        print(f"received: {returnMsg.decode()}")
        print(f"RTT: {time.time()-timeStamp:.4f}s")
    except:
        print("Request timed out")