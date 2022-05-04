# Build-EACS
Build-EACS was initially designed for the Build Forward Foundation in Richmond, VA and was decided that it should be open source so makerspaces all over could experience a little piece of mind when it came to their hardware. EACS stands for Equiptment Access Control System, and it functions as a buffer between the user and the machine. This system works by reading a members RFID signal and seeing if they have been granted access to use the tool that they are trying to swipe for. If the system recognizes the user, then it will log the user into a log file and allow power to the machine. If the system does not recognize the user, it will log them into an access denied log file and prevent power from reaching the machine.

	This Machine was built using:
	1x Raspberry Pi 3B
	1x songle relay srd-05vdc-sl-c
	1x ACEIRMC XL6019 5A High Power Current DC to DC Step-up
	1x Potter & Brumfield T9AS1D22-12 relay 
	1x Mean Well RS 15-5 220V to 5V power supply
	1x Gravity 50A current sensor
	1x RFID sensor (depends on frequency of card)
	1x Analog to Digital Converter (ADC) MCP3008 IC

Note that the current sensor provides an anolog data output, and the Raspberry Pi reads digital input. Consequently, the ADC is needed convert that ADC data into a digital signal that the Pi can read.
