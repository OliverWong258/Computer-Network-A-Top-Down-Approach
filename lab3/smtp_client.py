from socket import * 
import pdb
import base64
import ssl

msg = "\r\n I love computer networks!" 
endmsg = "\r\n.\r\n" 
# Choose a mail server (e.g. Google mail server) and call it mailserver
server = "smtp.gmail.com" 
mailserver = (server, 587) #Fill in start   #Fill in end 
# Create socket called clientSocket and establish a TCP connection with mailserver 
#Fill in start   
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(mailserver)
#Fill in end 
recv = clientSocket.recv(1024).decode() 
print(recv) 
if recv[:3] != '220': 
    print('220 reply not received from server.') 
# Send HELO command and print server response. 
heloCommand = 'HELO localhost\r\n' 
clientSocket.send(heloCommand.encode()) 
recv = clientSocket.recv(1024).decode() 
print(recv) 
if recv[:3] != '250': 
    print('250 reply not received from server.') 
    
# Start TSL
starttlsCommand = "STARTTLS\r\n"
clientSocket.send(starttlsCommand.encode())
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '220':
    print('220 reply not received from server.')
    
context = ssl.create_default_context()
tlsSocket = context.wrap_socket(clientSocket, server_hostname=server)

# Resend HELO command
tlsSocket.send(heloCommand.encode())
recv = tlsSocket.recv(1024).decode()
print(recv) 
if recv[:3] != '250': 
    print('250 reply not received from server.') 
    
# Send AUTH command
authCommand = 'AUTH LOGIN\r\n'
tlsSocket.send(authCommand.encode())
recv = tlsSocket.recv(1024).decode() 
print(recv) 
if recv[:3] != '334': 
    print('334 reply not received from server.') 

email = ''
encoded_bytes = base64.b64encode(email.encode('utf-8'))
userName = encoded_bytes.decode()+"\r\n"
tlsSocket.send(userName.encode())
recv = tlsSocket.recv(1024).decode() 
print(recv) 
if recv[:3] != '334': 
    print('334 reply not received from server.') 

passWord = ""
encoded_bytes = base64.b64encode(passWord.encode('utf-8'))
passWord = encoded_bytes.decode()+"\r\n"
tlsSocket.send(passWord.encode())
recv = tlsSocket.recv(1024).decode() 
print(recv) 

# Send MAIL FROM command and print server response. 
# Fill in start 
mailCommand = 'MAIL FROM:<>\r\n'
tlsSocket.send(mailCommand.encode())
recv = tlsSocket.recv(1024).decode()
print(recv)
if recv[:3] != '250':
    print('250 reply not received from server.')
# Fill in end 
# Send RCPT TO command and print server response.  
# Fill in start 
recptCommand = 'RCPT TO:<>\r\n'
tlsSocket.send(recptCommand.encode())
recv = tlsSocket.recv(1024).decode()
print(recv)
if recv[:3] != '250':
    print('250 reply not received from server.')
# Fill in end 
# Send DATA command and print server response.  
# Fill in start 
dataCommand = "DATA\r\n"
tlsSocket.send(dataCommand.encode())
recv = tlsSocket.recv(1024).decode()
print(recv)
if recv[:3] != '354':
    print('354 reply not received from server.')
# Fill in end 
# Send message data. 
# Fill in start 
tlsSocket.send(msg.encode())
# Fill in end 
# Message ends with a single period. 
# Fill in start 
tlsSocket.send(endmsg.encode())
recv = tlsSocket.recv(1024).decode()
print(recv)
if recv[:3] != '250':
    print('250 reply not received from server.')
# Fill in end 
# Send QUIT command and get server response. 
# Fill in start 
quitCommand = "QUIT\r\n"
tlsSocket.send(quitCommand.encode())
recv = tlsSocket.recv(1024).decode()
print(recv)
if recv[:3] != '221':
    print('221 reply not received from server.')
# Fill in end