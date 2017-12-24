import RPi.GPIO as gpio
import time

pin = 15
gpio.setmode(gpio.BOARD)
gpio.setup(pin, gpio.IN, pull_up_down = gpio.PUD_UP)

prev_state = 1

try:
  while True:
    cur_state = gpio.input(pin)
    if gpio.input(pin) != prev_state:
      if prev_state == 1:
        print "Der Taster wurde geschlossen."
      else:
        print "Der Taster wurde geoeffnet."
      prev_state = cur_state
    time.sleep(0.1)
finally:
    gpio.cleanup()
