
import RPi.GPIO as GPIO
import time
buzz_pin=4
pir_pin=14
door_pin=17
button_pin=18

GPIO.setmode(GPIO.BCM)
GPIO.setup(pir_pin, GPIO.IN)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(door_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(buzz_pin,GPIO.OUT)
try:
  while True:
    if GPIO.input(pir_pin):
        GPIO.output(buzz_pin, GPIO.HIGH)

    if GPIO.input(door_pin):
        GPIO.output(buzz_pin, GPIO.HIGH)
    if not GPIO.input(button_pin):
        GPIO.output(buzz_pin, GPIO.LOW)
except KeyboardInterrupt:
  print "voce usou Ctrl+C!"
finally:
  GPIO.cleanup()
