Final Working code from the Pi and Documentation


hidbash - Need to run on pi start up to find the hidraw port of the RFID reader
Equipment Access Code - Need to make sure the "fp = open('dev/hidraw0', 'rb)" is set to the right hidraw port that is found with the hidbash shell
    need to change line 100 "serverName = "xxx.xxx.xxx.xxx"" to the point to the IP address of back end server
    need to change line 101 "serverPort = "######"" to point to the port on the back end server
