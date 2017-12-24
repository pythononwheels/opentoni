import RPi.GPIO as gpio
import time
from subprocess import Popen, PIPE, call

pin = 21
gpio.setmode(gpio.BOARD)
gpio.setup(pin, gpio.IN, pull_up_down = gpio.PUD_UP)
PRESSED = 0
prev_state = 1
pressed_time = 0.1
skip_mode = False
pause_mode = False
continue_mode = False
VOICE = "-vde"
try:
  while True:
    cur_state = gpio.input(pin)
    if cur_state == PRESSED:
        pressed_time += 0.1 
        print "pressed : " + str( pressed_time)
        if pressed_time > 2:
            #shut down
            call(["espeak", VOICE, "opentoni schaltet sich aus"])
            pause_mode = False
            continue_mode = False
            skip_mode=False
        elif pressed_time > 0.1 and pressed_time< 1:
            # skip
            skip_mode = True
            call(["espeak", VOICE, "skip"])

        elif pressed_time == 0.1:
           if continue_mode:
               call(["espeak", VOICE, "weiter"])
               pause_mode = False
               continue_mode = False
           else:
               pause_mode = True
    else:
        pressed_time = 0
        if pause_mode == True:
            call(["espeak", VOICE, "pause"])
            continue_mode = True
        elif skip_mode:
            call(["espeak", VOICE, "skippe"])

    time.sleep(0.1)
finally:
    gpio.cleanup()
