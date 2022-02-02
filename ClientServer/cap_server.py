#Server side test program
#Will await connection from client side
#Once connection is made, will read in data sent from client,
# split it into ip adress and member address based on delimiter '|'
#Once split, will run query and return a true or false, based on response
#from the query

#Last update: 02FEB22

import socket

#declare host ip and port number
HOST = '127.0.0.1'
PORT = 22222

#create socket object
serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#assign ip and port to socket
serv.bind((HOST,PORT))
#begin listing for connections on socket
serv.listen()

#begin loop to continue listening on socket
while True:
    #read socket object and address from client
    connection_socket, addr = serv.accept()
    print('accepted')

    #Take in data from client
    rData = connection_socket.recv(1024).decode()

    #Data should be in form of <ipv4>|<memberID>
    #split based on delimiter
    addr, mID = rData.split('|')
    #print ipv4 and memberID
    print('Machine address:', addr)
    print('Member ID:', mID)

    #Simple if else to check if data matches abitrary test data or not
    #Sends back true if it does, false otherwise
    if addr == '192.168.1.103' and mID == '111222':
        connection_socket.send('True'.encode())
    else:
        connection_socket.send('False'.encode())

    #close connection to that client
    connection_socket.close()