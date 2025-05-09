import RPi.GPIO as GPIO

class IRSensor:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.pin, GPIO.IN)

    def is_object_detected(self):
        return GPIO.input(self.pin) == 0  # Adjust to 1 if using a normally-open sensor
