#Server side test program
#Will await connection from client side
#Once connection is made, will read in data sent from client,
# split it into ip adress and member address based on delimiter '|'
#Once split, will run query and return a true or false, based on response
#from the query

#Last update: 02FEB22

import socket
from mysql.connector import (connection)

#create database connection
cnx = connection.MySQLConnection(user='root', password='CapstonePassword', host='127.0.0.1', database='sys')

cursor = cnx.cursor()
#the query used to check if a user is certified
query = ("SELECT userID FROM CertUser WHERE certID = (SELECT certID FROM EqCert WHERE equipID = (SELECT equipID FROM Equipment WHERE wifi_Address = %s))")



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

    cursor.execute(query, (addr,))

    for userID in cursor:
        print('{}'.format(userID))
        if int(mID) in userID:
            print('Verified User')
            connection_socket.send('True'.encode())
        else:
            print('Unverified User')
            connection_socket.send('False'.encode())

    cursor.close()
    cnx.close()
    #close connection to that client
    connection_socket.close()