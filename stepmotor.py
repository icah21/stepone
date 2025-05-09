# stepmotor.py
import RPi.GPIO as GPIO
import time

class StepperMotor:
    def __init__(self, pins, delay=0.001):
        self.pins = pins
        self.delay = delay
        self.seq = [
            [1,0,0,0],
            [1,1,0,0],
            [0,1,0,0],
            [0,1,1,0],
            [0,0,1,0],
            [0,0,1,1],
            [0,0,0,1],
            [1,0,0,1],
        ]
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        for pin in self.pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, 0)
        self.steps_90 = 1024
        self.steps_360 = 4096

    def move_steps(self, steps, direction=1):
        seq = self.seq if direction == 1 else list(reversed(self.seq))
        for _ in range(steps):
            for halfstep in seq:
                for pin, val in zip(self.pins, halfstep):
                    GPIO.output(pin, val)
                time.sleep(self.delay)

    def execute_sequence(self):
        # Rotate 0 -> 360 in 90° steps
        for _ in range(4):
            self.move_steps(self.steps_90, direction=1)
            time.sleep(3)
        # Rotate 360 -> 0
        self.move_steps(self.steps_360, direction=-1)
        time.sleep(1)

    def cleanup(self):
        GPIO.cleanup()
