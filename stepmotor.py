import time
import RPi.GPIO as GPIO

# GPIO pin setup
IN1 = 17
IN2 = 18
IN3 = 27
IN4 = 22

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
control_pins = [IN1, IN2, IN3, IN4]
for pin in control_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

# Half-step sequence for 28BYJ-48
halfstep_seq = [
    [1,0,0,0],
    [1,1,0,0],
    [0,1,0,0],
    [0,1,1,0],
    [0,0,1,0],
    [0,0,1,1],
    [0,0,0,1],
    [1,0,0,1]
]

# Constants
DEGREES_PER_STEP = 360 / 4096  # approx 0.0879
STEPS_PER_90_DEGREES = int(90 / DEGREES_PER_STEP)  # ≈1024 steps

def step_motor(steps, delay=0.001):
    for _ in range(steps):
        for halfstep in halfstep_seq:
            for pin in range(4):
                GPIO.output(control_pins[pin], halfstep[pin])
            time.sleep(delay)

try:
    while True:
        for i in range(4):  # 0 -> 90 -> 180 -> 270 -> 360
            step_motor(STEPS_PER_90_DEGREES)
            time.sleep(3)
        # Return to 0 (reverse)
        for i in range(4 * len(halfstep_seq) * STEPS_PER_90_DEGREES // 8):
            for halfstep in reversed(halfstep_seq):
                for pin in range(4):
                    GPIO.output(control_pins[pin], halfstep[pin])
                time.sleep(0.001)
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
