import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
import time
import RPi.GPIO as GPIO
from adafruit_mcp3xxx.analog_in import AnalogIn
from datetime import datetime

spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)
mcp = MCP.MCP3008(spi, cs)
channel = AnalogIn(mcp, MCP.P0)

#GPIO.setmode(GPIO.BCM)
#GPIO.setup(17,  GPIO.OUT)
try:
  while True:
#    print('Raw ADC Value: ', channel.value) 
    print('ADC Voltage: ' + str(channel.voltage)[0:5] + ' V')
    current_val = str(channel.voltage/10)[0:5]
    print('ADC Current: ' + current_val+ ' A')
    #if channel.voltage > 2.0:
      #GPIO.output(17, True)
    #else:
      #GPIO.output(17, False)
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    #with open('test.csv', 'a') as fd:
    volt = str(channel.voltage)[0:5]
    with open('currentNumsSmallShopVac.csv', 'a') as fd:
     # fd.write(current_time + ',' + current_val + '\n')
      fd.write(f"{channel.value},{volt},{current_val}\n")
    time.sleep(0.25)



# format will be: RAWADC,VOLATGE,CURRENT

#filename = "/home/pi/Desktop/data.txt"
#f = open(filename, "a")
#volt=str(channel.voltage)[0:5]
#f.writelines(f"{channel.value},{volt},{current_val}")










except KeyboardInterrupt:
  exit
