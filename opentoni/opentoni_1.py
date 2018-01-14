#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522
import signal
import os, time
from subprocess import Popen, PIPE, STDOUT, call
import random
import json
import codecs
from random import shuffle

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

# load the opentoni.json data
data = json.load(open("opentoni.json"))
MUSICDIR=data["999"]["music_path"]
PLAYLISTDIR=os.path.join(MUSICDIR, "playlists")

#
# Load Messages from opentoni_messages.json
#
messages = json.load(open("opentoni_messages.json"))
for elem in messages["welcome"]:
    call(["espeak", "-v", "de", elem])
skip_intro = messages["skip_intro"]

#
# say welcome intro
#
if not skip_intro:
    for elem in messages["intro"]:
        call(["espeak", "-v", "de", elem])

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
        #print "len songlist <=1"
        songnum = 0
    for idx,elem in enumerate(songlist):
        print str(idx) + " : " + elem
    #print str(songlist)
    #print "randonly chosen song number: " + str(songnum)
    #print " ........ " + str(songlist[songnum])
    openstr = songlist[songnum]
    #print "trying to play: " + openstr
    #if music:
    #    music.terminate()
    #music = Popen(["mpg321", "-R", "opentoni"], stdin=PIPE)
    #music.stdin.write("LOAD " + openstr)
    return openstr,songnum

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
out = None
while continue_reading:
    # Scan for cards
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    #print "status: " + str(status) + "  last_status: " + str(last_status) + " status2count: " + str(status2count) 
    # If a card is found
    (status,uid) = MIFAREReader.MFRC522_Anticoll()
    if out:
        print "out: " +str(out.read())
    if status2count > 2:
        status2count = 0
    if status == 2 and last_status==2:
        # card removed:
        status2count += 1
        if status2count > 1 and playing == True:
            try:
                music.terminate()
            #music.stdin.write("STOP")
            except:
                pass
            finally:
                playing = False
                status2count = 0
    else:
        if playing == False:
            for elem in data:
                if uid[0] == int(elem):
                    if data[elem]["type"] == "song":
                        say_songname(data[elem]["info"])
                        songpath=os.path.join(MUSICDIR, data[elem]["path"])
                        music = Popen(["mpg321", "-q", "-R", "opentoni"], stdin=PIPE, stdout=FNULL)
                        music.stdin.write("LOAD " + songpath)
                    elif data[elem]["type"] == "random_playlist":
                        import os
                        import glob
                        dir = os.path.join(MUSICDIR,data[elem]["path"])
                        plname=os.path.join(PLAYLISTDIR, data[elem]["name"] +  ".m3u") 
                        songlist=[]
                        _m3u = codecs.open( plname , "w", encoding="utf-8" )
                        for file in os.listdir(dir):
                            filename, file_ext = os.path.splitext(file)
                            if file_ext== ".mp3" :
                                songlist.append(file)
                        shuffle(songlist)
                        say_songname(data[elem]["info"])

                        for s in songlist:
                            _m3u.write(os.path.join(dir,s) + os.linesep)
                        _m3u.close()
                        #print("now playing:" + plname)
                        #say_songname("playlists muss der onkel erst noch programmieren")
                        #say_songname(data[elem]["info"])
                        music = Popen(["mpg321", "--list", plname], stdin=PIPE, stdout=FNULL)
                        #music.stdin.write("LOAD " + songpath)
                    elif data[elem]["type"] == "recursive":
                        say_songname(data[elem]["info"])
                        songpath = os.path.join(MUSICDIR, data[elem]["path"])
                        #print "last_rand:" + str(last_rand)
                        music = Popen(["mpg321", "-q", "-B", songpath], stdin=PIPE, stdout=FNULL)
                    else:
                        songpath, last_rand = play_random(data[elem]["path"], last_rand)
                        #print "last_rand:" + str(last_rand)
                        say_songname(songpath)
                        music = Popen(["mpg321", "-q", "-R", "opentoni"], stdin=PIPE, stdout=FNULL)
                        music.stdin.write("LOAD " + songpath)
        else:
            print "out: "+ str(out)
        playing = True
    time.sleep(0.3)
    last_status=status

