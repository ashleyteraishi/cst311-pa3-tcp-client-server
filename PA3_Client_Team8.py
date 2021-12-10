from socket import *

serverName = 'localhost'
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

serverMessage = clientSocket.recv(1024)
print ('From Server:', serverMessage.decode())

sentence = input('Enter message to send to server:')
clientSocket.send(sentence.encode())

clientSocket.close()
