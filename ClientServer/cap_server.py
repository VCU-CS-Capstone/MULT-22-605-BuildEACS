#Server side test program
#Will await connection from client side
#Once connection is made, will read in data sent from client,
#data should consist of member id number. We can get ip address from the tcp packet
#using that data we will run the query on the ip address to get the cert needed
#and will then check to see if that user had that cert. 
#if so, we send true back to client, false if not.

#Last update: 02MAR22
import socket
import datetime
import threading
import os
import sys
from mysql.connector import (connection)

#Get host/server ip address
HOST = socket.gethostbyname(socket.gethostname()) #Gets ip automatically *Can use loopback for testing on same machine
#declare port number
PORT = 12001    #Any port that is not reserved will work *Client and server must use the same port
FORMAT = 'utf-8' #Used for encode/decode across network

#the query used to check if a user is certified
query = ("SELECT userID FROM CertUser WHERE certID = (SELECT certID FROM EqCert WHERE equipID = (SELECT equipID FROM Equipment WHERE wifi_Address = %s))")

#create socket object
serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#assign ip and port to socket
serv.bind((HOST,PORT))

#define date object
currDate = datetime.date.today()

dbpw = sys.argv[1]

if int(str(currDate).split('-')[2][0:2]) < 15:
    logPath = '/Users/blattmt/Desktop/python/school/' + str(currDate).split('-')[0] + str(currDate).split('-')[1] + '-01.txt'
else:
    logPath = '/Users/blattmt/Desktop/python/school/' + str(currDate).split('-')[0] + '-' + str(currDate).split('-')[1] + '-15.txt'

#Function to handle connections, get data from client, check against query and return results
def handle_client(conn, addr):
    #Display which address of new connection
    print(f'[NEW CONNECTION] {addr} connected.')
    
    #Create database connection
    cnx = connection.MySQLConnection(user='root', password=dbpw, host='127.0.0.1', database='sys')
    
    #Cursor object to let us run query
    cursor = cnx.cursor()
    
    #Loop condition variable
    connected = True
    while connected:
        #Read member number from client
        mID = conn.recv(32).decode(FORMAT)
        
        #Display member number sent from address
        print(f'[{addr}] Sent member ID: {mID}')

        #Run db query using address of machine sending request
        cursor.execute(query, (addr,))

        #based on return of the query,
        #decline or allow based on member ID having req certification
        response = 'True'

        # print(cursor.fetchall())
        check = cursor.fetchall()
        # if check.rowcount == 0:
        if not check:
            response = 'False'
            print('Unverified User')
            print('\n'+logPath+'\n')
            conn.send(response.encode(FORMAT))
            logFile = open(logPath, 'a')
            #Write to file in sequence 'Denied/id/machine/date and time
            logFile.write('DENIED,' + mID + ',' + addr + ',' + str(datetime.datetime.now()).split('.')[0] +'\n')
            logFile.close()
        else:
            a_tuple = ()
            for userID in check:
                #Display user ID
                #if mID is allowed and in list, send True and log...
                a_tuple = a_tuple + userID
            print(a_tuple)
            #print(userID)
            if int(mID) in userID:
                print("Here is the mID " + mID + "\n")
                print('Verified User')
                conn.send(response.encode(FORMAT))
                logFile = open(logPath, 'a')
                #Write to file in sequence 'Granted/id/ip/date and time
                logFile.write('GRANTED,' + mID +' ,' + addr + ',' + str(datetime.datetime.now()).split('.')[0] + '\n')
                logFile.close()            
                #if not, send false and log
            else:
                #response = 'False'
                print('Unverified User')
                conn.send(response.encode(FORMAT))
                logFile = open(logPath, 'a')
                #Write to file in sequence 'Denied/id/machine/date and time
                logFile.write('DENIED,' + mID + ',' + addr + ',' + str(datetime.datetime.now()).split('.')[0] +'\n')
                logFile.close()
        connected = False

    #close cursor object
    cursor.close()
    #close database connection
    cnx.close()
    #close connection
    conn.close()
#Function to begin listening on network 
def start():
    #begin listening for connections on socket
    serv.listen()
    #print confirmation of socket listening and on what address
    print(f'[LISTENING] Server is listening on {HOST}')
    runLoop = True
    while runLoop :
        #accept the connection
        conn, addr = serv.accept()
        #grap ip
        addr = addr[0]
        #Create and start new thread to handle the connection
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

        print(f'[ACTIVE CONNECTIONS] {threading.active_count() - 1}')

#Run driver function - Currently only requires calling of start()
start()