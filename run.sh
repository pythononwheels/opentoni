#!/bin/sh
sleep 10
cd /home/pi/Adafruit_Python_SSD1306/examples
sudo python stats.py &
cd /home/pi/MFRC522-python
sudo python Read_khz3.py
