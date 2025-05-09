import time
import threading
import RPi.GPIO as GPIO
from stepper_motor import StepperMotor
from ir_sensor import IRSensor

# Initialize IR sensor and stepper motor
ir_sensor = IRSensor(pin=17)
motor = StepperMotor(in1=18, in2=23, in3=24, in4=25)

# Shared state
current_angle = 0

# ---------- Persistence Functions ----------

def save_current_angle(angle):
    try:
        with open("angle_state.txt", "w") as f:
            f.write(str(angle))
    except Exception as e:
        print(f"Error saving angle: {e}")

def load_last_angle():
    try:
        with open("angle_state.txt", "r") as f:
            return int(f.read())
    except:
        return 0  # Default to 0 if file missing or unreadable

# ---------- Motor Thread Logic ----------

def motor_thread_func():
    global current_angle
    object_was_previously_detected = False

    while True:
        detected = ir_sensor.is_object_detected()

        if detected and not object_was_previously_detected:
            print("New object detected!")

            # Go from 0 to 90
            current_angle = motor.go_to_angle(current_angle, 90)
            save_current_angle(current_angle)
            time.sleep(3)

            # Go from 90 to 180
            current_angle = motor.go_to_angle(current_angle, 180)
            save_current_angle(current_angle)
            time.sleep(2)

            # Go from 180 to 270
            current_angle = motor.go_to_angle(current_angle, 270)
            save_current_angle(current_angle)
            time.sleep(3)

            # Return to 0
            current_angle = motor.go_to_angle(current_angle, 0)
            save_current_angle(current_angle)
            time.sleep(2)

            # Prevent retrigger until object is removed
            object_was_previously_detected = True

        elif not detected:
            # Reset detection state when object leaves
            object_was_previously_detected = False

        time.sleep(0.1)

# ---------- Startup ----------

try:
    # Load last known angle from file
    current_angle = load_last_angle()

    if current_angle != 0:
        print(f"Restoring motor to 0° from {current_angle}°...")
        current_angle = motor.go_to_angle(current_angle, 0)
        save_current_angle(current_angle)
        time.sleep(2)

    # Start motor thread
    motor_thread = threading.Thread(target=motor_thread_func)
    motor_thread.start()

except KeyboardInterrupt:
    print("Exiting...")
    GPIO.cleanup()
