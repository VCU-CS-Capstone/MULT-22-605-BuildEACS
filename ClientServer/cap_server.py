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
from mysql.connector import (connection)

#------can use this(loopback) for testing on same machine
HOST = '127.0.0.1'
#Get host/server ip address
#HOST = socket.gethostbyname(socket.gethostname())
#declare port number
PORT = 12001
HEADER = 64
FORMAT = 'utf-8'
#the query used to check if a user is certified
query = ("SELECT userID FROM CertUser WHERE certID = (SELECT certID FROM EqCert WHERE equipID = (SELECT equipID FROM Equipment WHERE wifi_Address = %s))")

#create socket object
serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#assign ip and port to socket
serv.bind((HOST,PORT))
#define date object
currDate = datetime.date.today()
# -------------------UPDATE to filepath desired on server system when installed
logPath = '/Users/blattmt/Desktop/python/school/' + str(currDate).split('-')[0] + '-' + str(currDate).split('-')[1] + '.txt'

#Function to handle connections, get data from client, check against query
#and return results
def handle_client(conn, addr):
    #Display which address of new connection
    print(f'[NEW CONNECTION] {addr} connected.')
    #Create database connection
    cnx = connection.MySQLConnection(user='root', password='CapstonePassword', host='127.0.0.1', database='sys')
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
            for userID in check:
                #Display user ID
                #if mID is allowed and in list, send True and log...
                print(userID)
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
        # connected = False
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
        conn, addr = serv.accept()
        addr = addr[0]
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f'[ACTIVE CONNECTIONS] {threading.active_count() - 1}')

##MAIN###########################
#Run driver function
start()