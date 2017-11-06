#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522
import signal
import os, time
from subprocess import Popen, PIPE, STDOUT
continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
print "Welcome to the MFRC522 data read example"
print "Press Ctrl-C to stop."

playing=False
current_uid=0
status2count=0
last_status = 2
# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    # Scan for cards
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    #print "status: " + str(status) + "  last_status: " + str(last_status) + " status2count: " + str(status2count) 
    # If a card is found
    (status,uid) = MIFAREReader.MFRC522_Anticoll()
    if status == 2 and last_status==2:
        # card removed:
        status2count += 1
        if status2count > 10 and playing == True:
            music.terminate()
            playing = False
            status2count = 0
    else:
        if playing == False:
            if uid[0]==98:
                music = Popen("mpg321 /home/pi/wir_sind_gross.mp3".split(" ",1), stdout=PIPE, stderr=STDOUT, close_fds=True)
            elif uid[0]==243:
                music = Popen("mpg321 /home/pi/maedchen_gegen_jungs.mp3".split(" ",1), stdout=PIPE, stderr=STDOUT, close_fds=True)
        playing = True
    last_status=status
