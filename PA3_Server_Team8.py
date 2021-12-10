# We need to use multithreading to support multiple clients so that
# each client has its own thread and we can listen for input 
# concurrently from both clients. Additionally, multithreading
# allows us to share data between client threads so that we 
# can print the final message to the clients
 
from socket import *
from threading import Thread
import time

# global variables 
serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(2)
print ('The server is ready to receive 2 connections...')
threads = []
messages = []
# create dictionary to store message times with name of sender
messageTimes = {'X': 0.0, 'Y': 0.0}

# thread function that receives connectionSocket and name of thread
# waits to receive a message from the client
def thread_fcn(socket, name):
	while True:
		data = socket.recv(1024)
		# if no data received, break
		if not data: break
		# otherwise append message data to messages array and messageTime dict
		else:
			messages.append(data.decode())
			messageTimes[name] = time.time()
			# print message to server
			print ('Client ' + name + ' sent message' + str(len(messages)) + ': ' + data.decode())
		break

# main function
if __name__ == "__main__":
	# for client 'X':
	# first, accept the connection, populate connectionSocketX and addrX
	connectionSocketX, addrX = serverSocket.accept()
	# create new thread using thread_fcn, pass in connectionSocketX, and name 'X'
	newThreadX = Thread(target=thread_fcn, args=(connectionSocketX, 'X',))
	# start the thread
	newThreadX.start()
	# append new thread to threads array
	threads.append(newThreadX)
	# send message to client that X has connected successfully
	serverMessageX = 'X connected'
	connectionSocketX.send(serverMessageX.encode())
	# print message to server that X has connected successfully
	print ('Received first connection. Calling it Client X')

	# for client 'Y'
	# accept the second connection, populate connectionSocketY and addrY
	connectionSocketY, addrY = serverSocket.accept()
	# create new thread using thread_fcn
	newThreadY = Thread(target=thread_fcn, args=(connectionSocketY, 'Y',))
	# start new thread
	newThreadY.start()
	# append new thread to threads array
	threads.append(newThreadY)
	# send message to client that Y has connected successfully
	serverMessageY = 'Y connected'
	connectionSocketY.send(serverMessageY.encode())
	# print message to server that Y has connected successfully
	print ('Received second connection. Calling it Client Y')
	
	print ('Waiting to receive messages from Client X and Client Y')
	
#join threads
for t in threads:
	t.join()
# create final message to client by comparing times that messages were received
if (messageTimes['X'] < messageTimes['Y']):
	finalMessage = 'X: ' + messages[0] + ' received before Y: ' + messages[1]
else:
	finalMessage = 'Y: ' + messages[0] + ' received before X: ' + messages[1]

# send final message to both clients
connectionSocketX.send(finalMessage.encode())
connectionSocketY.send(finalMessage.encode())

print ('Waiting a bit for clients to close their connections')

# close connections
connectionSocketX.close()
connectionSocketY.close()

print ('Done')
