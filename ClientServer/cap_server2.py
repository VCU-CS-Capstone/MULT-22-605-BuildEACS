from socket import *
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print ("The server is ready to receive")
while 1:
    print ("Waiting ...")
    connectionSocket, addr = serverSocket.accept()
    print ("accept")
    sentence = connectionSocket.recv(2048)
    print ("Message Received: " + sentence)

    if sentence == '0003248329':
        modifiedSentence = 'True'
    else:
        modifiedSentence = 'False'
    
    connectionSocket.send(modifiedSentence)
    connectionSocket.close()