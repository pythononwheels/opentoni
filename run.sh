#!/bin/sh
sleep 10
cd /home/pi/opentoni/Adafruit_Python_SSD1306/examples
sudo python stats.py &
cd /home/pi/opentoni/opentoni
sudo python opentoni_1.py
