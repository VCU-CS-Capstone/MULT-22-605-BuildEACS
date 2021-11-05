# Build-EACS
Build-EACS was initially designed for the Build Forward Foundation in Richmond, VA and was decided that it should be open source so makerspaces all over could experience a little piece of mind when it came to their hardware. Build-EACS stands for Equiptment Access Control System, and functions as a buffer between the user and the machine. This system works by reading a members RFID signal and seeing if they have been granted access to use the tool that they are trying to swipe for. If the system recognizes the user, then it will log the user into a log file and allow power to the machine. If the system does not recognize the user, it will log them into an access denied log file and prevent further use from that machine by that user until certification. 

	This Machine was built using:
	1x Raspberry Pi 3B
	1x songle relay srd-05vdc-sl-c
	1x ACEIRMC XL6019 5A High Power Current DC to DC Step-up
	1x Potter & Brumfield T9AS1D22-12 relay 
	1x Arduino Uno
	1x Mean Well RS 15-5 220V to 5V power supply
	1x Gravity 50A current sensor
	1x RFID sensor (depends on frequency of card)

As seen in the parts list, there are two boards, the raspberry pi and the arduino uno. At the time of developement, the idea that all functionality could be achieved using the raspbery pi was believed, but the op-amp of the uno was needed for processing the current signal from the wall. For future iterations, a self contained Arduino system in C could be used. If you do not need current readings, the raspberry pi 3B can be used without the addition of the Arduino. 
