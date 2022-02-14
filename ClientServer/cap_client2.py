#Client side base program. 
#Will connect to server side, send test data consisting
#of ip address and member address as a string delimited by a '|'
#Upon response from server: 
# will check the response and either deny or allow access

#Last update: 09FEB22
from socket import *

#Declaring ip and port number for socket
serverName = '127.0.0.1'
serverPort = 12000

#Create socket object
client = socket(AF_INET, SOCK_STREAM)

#Connection request
client.connect((serverName, serverPort))

#Prompt for input ----------Make this the member ID
#testData = raw_input()
#testData = '192.442.456.813|1235'
testData = '0003248329'

#send date to server
client.send(testData)

#Receive server response and decode
servResponse = client.recvfrom(2048)
servResponse = servResponse[0].decode()

#print data from server
print (servResponse)

#close socket
client.close()