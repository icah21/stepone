# ir_sensor.py
import RPi.GPIO as GPIO
import time

class IRSensor:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)

    def detected(self):
        return GPIO.input(self.pin) == 0  # Assuming LOW when object detected
