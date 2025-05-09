import RPi.GPIO as GPIO
import time

# Setup GPIO pins for ULN2003 (modify if using other GPIOs)
IN1 = 17
IN2 = 18
IN3 = 27
IN4 = 22

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

control_pins = [IN1, IN2, IN3, IN4]
for pin in control_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

# Half-step sequence for smoother motion
halfstep_seq = [
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
    [1, 0, 0, 1]
]

# Constants
STEPS_PER_REV = 4096       # 360 degrees
STEPS_90_DEG = 1024        # 90 degrees

def step_motor(steps, direction=1, delay=0.001):
    """
    Move motor a given number of steps in a direction (1 = CW, -1 = CCW).
    """
    sequence = halfstep_seq if direction == 1 else list(reversed(halfstep_seq))
    for _ in range(steps):
        for halfstep in sequence:
            for pin in range(4):
                GPIO.output(control_pins[pin], halfstep[pin])
            time.sleep(delay)

try:
    while True:
        # Move 90° steps forward, with 3-second pause after each
        step_motor(STEPS_90_DEG, direction=1)
        time.sleep(3)

        step_motor(STEPS_90_DEG, direction=1)
        time.sleep(3)

        step_motor(STEPS_90_DEG, direction=1)
        time.sleep(3)

        step_motor(STEPS_90_DEG, direction=1)
        time.sleep(3)

        # Return to 0° (rotate 360° in reverse direction)
        step_motor(STEPS_PER_REV, direction=-1)
        time.sleep(1)

except KeyboardInterrupt:
    print("Interrupted. Cleaning up GPIO...")
    GPIO.cleanup()
