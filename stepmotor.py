import RPi.GPIO as GPIO
import time

# Pin setup for ULN2003
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

# Half-step sequence (8 steps)
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

STEPS_PER_REV = 4096           # 360 degrees = 4096 steps
STEPS_PER_90 = STEPS_PER_REV // 4  # 90 degrees = 1024 steps

def move_steps(steps, direction=1, delay=0.001):
    """Move motor a number of steps. direction=1 for forward, -1 for reverse."""
    seq = halfstep_seq if direction == 1 else list(reversed(halfstep_seq))
    for _ in range(steps):
        for halfstep in seq:
            for pin in range(4):
                GPIO.output(control_pins[pin], halfstep[pin])
            time.sleep(delay)

try:
    while True:
        # Rotate forward in 90° increments with 3s pause
        for _ in range(4):
            move_steps(STEPS_PER_90, direction=1)
            time.sleep(3)

        # Return to 0° in reverse (entire 360°)
        move_steps(STEPS_PER_REV, direction=-1)
        time.sleep(1)

except KeyboardInterrupt:
    print("\nInterrupted. Cleaning up GPIO...")
    GPIO.cleanup()
