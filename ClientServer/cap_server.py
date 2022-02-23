#Server side test program
#Will await connection from client side
#Once connection is made, will read in data sent from client,
#data should consist of member id number. We can get ip address from the tcp packet
#using that data we will run the query on the ip address to get the cert needed
#and will then check to see if that user had that cert. 
#if so, we send true back to client, false if not.

#Last update: 23FEB22
import socket
import datetime
import threading
from mysql.connector import (connection)

#------can use this(loopback) for testing on same machine
HOST = '127.0.0.1'
#Get host/server ip address
#HOST = socket.gethostbyname(socket.gethostname())
#declare port number
PORT = 12000
DISCONNECT_MSG = '!DISCONNECT'
HEADER = 64
FORMAT = 'utf-8'

#create database connection
cnx = connection.MySQLConnection(user='root', password='CapstonePassword', host='127.0.0.1', database='sys')
#create cursor object to allow running of query
cursor = cnx.cursor()
#the query used to check if a user is certified
query = ("SELECT userID FROM CertUser WHERE certID = (SELECT certID FROM EqCert WHERE equipID = (SELECT equipID FROM Equipment WHERE wifi_Address = %s))")

#create socket object
serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#assign ip and port to socket
serv.bind((HOST,PORT))

#Function to handle connections, get data from client, check against query
#and return results
def handle_client(conn, addr):
    #Display which address of new connection
    print(f'[NEW CONNECTION] {addr} connected.')
    
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
        for userID in cursor:
            #Display user ID
            #print('{}'.format(userID))
            #if mID is allowed list, send True and log...
            if int(mID) in userID:
                print('Verified User')
                conn.send(response.encode(FORMAT))
                #logFile = open(logPath, 'a')
                #Write to file in sequence 'Granted/id/machine/date and time
                #logFile.write('ACCESS GRANTED   ' + mID)....
                #logFile.close()
            #if not, send false and log
            else:
                response = 'False'
                print('Unverified User')
                conn.socket.send(response.encode(FORMAT))
                #logFile = open(logPath, 'a')
                #Write to file in sequence 'Denied/id/machine/date and time
                #logFile.write('ACCESS GRANTED   ' + mID)....
                #logFile.close()
        connected = False
    #close connection
    conn.close()
#Function to begin listening on network 
def start():
    #begin listening for connections on socket
    serv.listen()
    #print confirmation of socket listening and on what address
    print(f'[LISTENING] Server is listening on {HOST}')
    #print('[ENTER "quit" TO TERMINATE')
    while True:
        conn, addr = serv.accept()
        addr = addr[0]
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f'[ACTIVE CONNECTIONS] {threading.active_count() - 1}')

##MAIN###########################

#define date object
currDate = datetime.date.today()
#define filepath for log
logPath = '/Users/blattmt/Desktop/python/school/' + str(currDate).split('-')[0] + '-' + str(currDate).split('-')[1] + '.txt'

###Run driver function
start()

#close cursor object
cursor.close()
#close database connection
cnx.close()