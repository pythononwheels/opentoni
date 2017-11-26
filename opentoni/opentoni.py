#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522
import signal
import os, time
from subprocess import Popen, PIPE, STDOUT, call
import random
import json


#class MyRand(object):
#    def __init__(self):
#        self.last = None
#    def __call__(self, start=0,end=10 ):
#        r = random.randint(start, end)
#        while r == self.last:
#            r = random.randint(0, end)
#        self.last = r
#        return r

#randint = MyRand()
continue_reading = True
FNULL=FNULL = open(os.devnull, 'w')

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
#print "Welcome to the MFRC522 data read example"
#print "Press Ctrl-C to stop."

playing=False
current_uid=0
status2count=0
last_status=2
last_rand = 1

MUSICDIR="/home/pi/music/"

#
# Welcome Message
#
messages = json.load(open("opentoni_messages.json"))
for elem in messages["welcome"]:
    call(["espeak", "-v", "de", elem])
skip_intro = messages["skip_intro"]
if not skip_intro:
    for elem in messages["intro"]:
        call(["espeak", "-v", "de", elem])

data = json.load(open("opentoni.json"))
def get_song_from_path(songpath):
    try:
        return os.path.splitext(os.path.basename(songpath))[0]
    except:
        return "konnte den song nicht finden"

def say_songname(path):
    call(["espeak", "-v", "de", messages["song_pre"]])
    call(["espeak", "-v", "de", get_song_from_path(path)])

def play_random(path, last_rand):
    songlist = []
    for file in os.listdir(MUSICDIR+path):
        if file.endswith(".mp3"):
            songlist.append(os.path.join(MUSICDIR+path, file))
    if len(songlist) >1:
        r = random.randint(0, len(songlist)-1)
        while r == last_rand:
            r = random.randint(0, len(songlist)-1)
        songnum = r
    else:
        print "len songlist <=1"
        songnum = 0
    for idx,elem in enumerate(songlist):
        print str(idx) + " : " + elem
    #print str(songlist)
    print "randonly chosen song number: " + str(songnum)
    print " ........ " + str(songlist[songnum])
    openstr = songlist[songnum]
    #print "trying to play: " + openstr
    #if music:
    #    music.terminate()
    #music = Popen(["mpg321", "-R", "opentoni"], stdin=PIPE)
    #music.stdin.write("LOAD " + openstr)
    return openstr,songnum

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
        if status2count > 1 and playing == True:
            music.terminate()
            #music.stdin.write("STOP")
            playing = False
            status2count = 0
    else:
        if playing == False:
            for elem in data:
                if uid[0] == int(elem):
                    songpath, last_rand = play_random(data[elem]["path"], last_rand)
                    print "last_rand:" + str(last_rand)
                    say_songname(songpath)
                    music = Popen(["mpg321", "-q", "-R", "opentoni"], stdin=PIPE, stdout=FNULL)
                    music.stdin.write("LOAD " + songpath)
            #if uid[0]==98:
            #    songpath = play_random("/nieke")
            #    say_songname(songpath)
            #    music = Popen(["mpg321", "-R", "opentoni"], stdin=PIPE)
            #    music.stdin.write("LOAD " + songpath)
            
        playing = True
    time.sleep(0.3)
    last_status=status
