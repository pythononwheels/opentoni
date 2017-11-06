#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522
import signal
import os, time
from subprocess import Popen, PIPE, STDOUT
from random import randint
import glob

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
print "Welcome to OpenToni."
print "Press Ctrl-C to stop."


# build the playlists once on every new run
musicdir="/home/pi/music"
d=musicdir
subdirs = [os.path.join(d, o) for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))]

for elem in subdirs:
    playlist=glob.glob(elem + "/*.mp3")




playing=False
current_uid=0
status2count=0
last_status = 2

MUSICDIR="/home/pi/music"
# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    # Scan for cards
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    #print "status: " + str(status) + "  last_status: " + str(last_status) + " status2count: " + str(status2count) 
    # If a card is found
    (status,uid) = MIFAREReader.MFRC522_Anticoll()
    if status2count > 2:
        status2count = 0
    if status == 2 and last_status==2:
        # card removed:
        status2count += 1
        if status2count > 2 and playing == True:
            music.terminate()
            playing = False
            status2count = 0
    else:
        if playing == False:
            if uid[0]==98:
                #songlist = []
                #for file in os.listdir(MUSICDIR+"/nieke"):
                #    if file.endswith(".mp3"):
                #        songlist.append(os.path.join(MUSICDIR+"/nieke", file))
                #songnum = randint(0,len(songlist))-1
                #for idx,elem in enumerate(songlist):
                #    print str(idx) + " : " + elem
                #print str(songlist)
                #print "randonly chosen song number: " + str(songnum)
                #print " ........ " + str(songlist[songnum])
                #openstr= songlist[songnum]
                #print "trying to play: " + openstr
                openstr="/home/pi/music/nieke"
                music = Popen("mpg321 -Z /home/pi/music/nieke/", stdout=PIPE, stdin=PIPE, stderr=STDOUT)
                #music.stdin.write("LOAD " + openstr)
            elif uid[0]==243:
                songlist = []
                for file in os.listdir(MUSICDIR+"/meck"):
                    if file.endswith(".mp3"):
                        songlist.append(os.path.join(MUSICDIR+"/meck", file))
                songnum = randint(0,len(songlist))-1
                for idx,elem in enumerate(songlist):
                    print str(idx) + " : " + elem
                #print str(songlist)
                print "randonly chosen song number: " + str(songnum)
                print " ........ " + str(songlist[songnum])
                openstr=songlist[songnum]
                print "trying to play: " + openstr
                music = Popen(["mpg321", "-R", "testPlayer"], stdin=PIPE)
                music.stdin.write("LOAD " + openstr)
        playing = True
    last_status=status
