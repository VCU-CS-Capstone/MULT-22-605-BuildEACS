#Client side test program
#Will connect to server side, send test data consisting
#of ip address and member address as a string delimited by a '|'
#Upon response from server: 
# will check the response and either deny or allow access

#Last update: 02FEB22

import socket

#declare host ip and port number
HOST = '127.0.0.1'
PORT = 22222

#create socket object
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#attempt to connect to server
client.connect((HOST,PORT))

#test data in form of <ip address>|<member ID>
testData = '192.168.1.103|112222'

#send test data
client.send(testData.encode())

#
response = client.recvfrom(1024)
response = response[0].decode()

if response == 'True':
    print('Member certified, access granted.')
else:
    print('Member not certified, access denied')

client.close()