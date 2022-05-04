Place cap_server.py into desire path. Once there, the following information can help with modification and startup

Adjust following values as needed/desired
- Port number - for use in socket connection
- logpath - location for log file
- Database information - likely only change database and password

Run with terminal using the following command
python3 cap_server.py <database_password>
- Can change <cap_server.py> to whatever you need/desire the filename to be

Required Libraries:
- socket 
- datetime
- threading
- sys


Once running, the client will be able to connect
