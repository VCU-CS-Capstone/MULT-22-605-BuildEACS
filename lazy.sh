sudo mount /dev/sda1 /mnt/usb

cp /mnt/usb/BuildTACS-v03.py ~/Desktop/RFID/

sudo umount /mnt/usb

sudo python ~/Desktop/RFID/BuildTACS-v03.py
