import socket
import sys

if len(sys.argv) != 4:
    print("Usage: python client.py server_host server_port filename")
    sys.exit(1)

server_host = sys.argv[1]
server_port = int(sys.argv[2])  # 注意转换为整型
filename = sys.argv[3]

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

clientSocket.connect((server_host, server_port))

clientSocket.sendall(f"GET /{filename} HTTP/1.1\r\n".encode())
clientSocket.send("\r\n".encode())

while True:
    message = clientSocket.recv(1024).decode()
    if len(message) == 0:
        break
    print(message)
    
clientSocket.close()