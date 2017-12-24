import RPi.GPIO as GPIO
import time

MYGPIO=23
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(MYGPIO,GPIO.OUT)
GPIO.setup(18,GPIO.OUT)
print "LED blink"
while 1:
    GPIO.output(23,GPIO.LOW)
    GPIO.output(18,GPIO.LOW)
    time.sleep(1)
    GPIO.output(23,GPIO.HIGH)
    GPIO.output(18,GPIO.HIGH)
    time.sleep(1)
