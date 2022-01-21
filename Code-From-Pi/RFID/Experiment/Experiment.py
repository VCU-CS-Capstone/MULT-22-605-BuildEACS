import sys
import csv
import datetime
import os
import subprocess
from gpiozero import LED
from time import sleep
from RPLCD.gpio import CharLCD
from RPi import GPIO
import collections
#import wiringpi

print("define LCD")
GPIO.setwarnings(False)
lcd = CharLCD(cols=16, rows=2, pin_rs=26, pin_rw=24, pin_e=19, pins_data=[13, 6, 5, 11],numbering_mode=GPIO.BCM)
#lcd = CharLCD(cols=16, rows=2, pin_rs=37, pin_rw=18, pin_e=35, pins_data=[33, 31, 29, 23], numbering_mode=GPIO.BOARD)
print('lcd defined')

###Define Variables-------------------------------------------------------------------------------------------------------------------

import RPi.GPIO as GPIO
from gpiozero import OutputDevice

relay = OutputDevice(17)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)

global relayState
relayState = 0

def access_granted():
        GPIO.output(17, True)
        print('Welcome ' + nicknames_list[pos])
        lcd.clear()
        lcd.cursor_pos = (0,1)
        lcd.write_string('Access Granted')
        log_file = open('/home/pi/Desktop/RFID/log-door.csv', 'r')
        new_line = (time.strftime('%a %Y-%m-%d,%H:%M:%S') + ',' + rfid_number + ',' + names_list[pos] + ',Approved \n')
        contents = log_file.readlines()
        contents.insert(0, new_line)
        log_file.close()
        log_file = open('/home/pi/Desktop/RFID/log-door.csv', 'w')
        log_file.writelines(contents)
        log_file.close()

def access_denied():
        GPIO.output(17, False)
        print('Unauthorized User')
        lcd.clear()
        lcd.cursor_pos = (0,3)
        lcd.write_string('Go to class')
        sleep(3)
        lcd.clear()
        log_file = open('/home/pi/Desktop/RFID/log-door.csv', 'r')
        new_line = (time.strftime('%a %Y-%m-%d,%H:%M:%S') + ',' + rfid_number + ',' +' Unknown ID,DENIED \n')
        print(new_line)
        contents = log_file.readlines()
        contents.insert(0, new_line)
        log_file.close()
        log_file = open('/home/pi/Desktop/RFID/log-door.csv', 'w')
        log_file.writelines(contents)
        log_file.close()

def machine_turnoff():
        GPIO.output(17, False)
        print('Machine turned off by ' + nicknames_list[pos])
        lcd.clear()
        lcd.cursor_pos = (0,3)
        lcd.write_string('Goodbye')
        sleep(5)
        lcd.clear()

#def Switch():
#    wiringpi.pinMode(25,0)
#    wiringpi.digitalRead(25)
#    gpio17state = wiringpi.digitalRead(25)
#    if gpio17state:
#        wiringpi.pinMode(25,1)
#        wiringpi.digitalWrite(25,0)
#    else:
#        wiringpi.pinMode(25,0)
#        wiringpi.digitalWrite(25,1)

###Define Whitelist-------------------------------------------------------------------------------------------------------------------

with open('/home/pi/Desktop/RFID/members_list') as whitelist:
    csv_reader = csv.reader(whitelist, delimiter=',')
    line_count = 0
    ID_list = []
    names_list = []
    nicknames_list = []
    member_type_list = []
    for row in csv_reader:
        ID = row[0]
        first_name = row[2]
        last_name = row[1]
        nickname = row[3]
        member_type = row[4]
        full_name = first_name+' '+last_name
        ID_list.append(ID)
        names_list.append(full_name)
        nicknames_list.append(nickname)
        member_type_list.append(member_type)
    print(ID_list)

hid = { 4: 'a', 5: 'b', 6: 'c', 7: 'd', 8: 'e', 9: 'f', 10: 'g', 11: 'h', 12: 'i', 13: 'j', 14: 'k', 15: 'l', 16: 'm', 17: 'n', 18: 'o', 19: 'p', 20: 'q', 21: 'r', 22: 's', 23: 't', 24: 'u', 25: 'v', 26: 'w', 27: 'x', 28: 'y', 29: 'z', 30: '1', 31: '2', 32: '3', 33: '4', 34: '5', 35: '6', 36: '7', 37: '8', 38: '9', 39: '0', 44: ' ', 45: '-', 46: '=', 47: '[', 48: ']', 49: '\\', 51: ';' , 52: '\'', 53: '~', 54: ',', 55: '.', 56: '/'  }
hid2 = { 4: 'A', 5: 'B', 6: 'C', 7: 'D', 8: 'E', 9: 'F', 10: 'G', 11: 'H', 12: 'I', 13: 'J', 14: 'K', 15: 'L', 16: 'M', 17: 'N', 18: 'O', 19: 'P', 20: 'Q', 21: 'R', 22: 'S', 23: 'T', 24: 'U', 25: 'V', 26: 'W', 27: 'X', 28: 'Y', 29: 'Z', 30: '!', 31: '@', 32: '#', 33: '$', 34: '%', 35: '^', 36: '&', 37: '*', 38: '(', 39: ')', 44: ' ', 45: '_', 46: '+', 47: '{', 48: '}', 49: '|', 51: ':' , 52: '"', 53: '~', 54: '<', 55: '>', 56: '?'  }
fp = open('/dev/hidraw0', 'rb')
rfid_number = ""
shift = False
done = False

###Running the loop-------------------------------------------------------------------------------------------------------------------

while True:
    ### Wait for RFID
    while not done:			## Get the character from the HID
        lcd.clear()
        lcd.cursor_pos = (0,3)
        lcd.write_string('Swipe Chip')

        buffer = fp.read(8)
        for c in buffer:
            if ord(c) > 0:	##  40 is carriage return which signifies we are done looking for characters
                if int(ord(c)) == 40:
                    done = True
                    break;	##  If we are shifted then we have to  use the hid2 characters.
                if shift: 	## If it is a '2' then it is the shift key
                    if int(ord(c)) == 2 :
                        shift = True
                    else:	# if not a 2, lookup mapping
                        rfid_number += hid2[ int(ord(c)) ]
                        shift = False
                else:		# if not shifted, use the hid characters
                    if int(ord(c)) == 2 :	# if 2, then it is the shift key
                        shift = True
                    else:	# If not a 2, lookup mapping
                        rfid_number += hid[ int(ord(c)) ]
    print rfid_number
    time = datetime.datetime.now()

    if ID_list.count(rfid_number) > 0:
        pos = ID_list.index(rfid_number)
        if member_type_list[pos] == 'keyed_membership' > 0 and relayState == 0:
            access_granted()
            relayState = 1
        elif member_type_list[pos] == 'keyed_membership' > 0 and relayState == 1:
            machine_turnoff()
            relayState = 0
    if ID_list.count(rfid_number) == 0:
            access_denied()
            relayState = 0
    rfid_number = ''
    done = False
