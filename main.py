import time
import threading
from stepper_motor import StepperMotor
from ir_sensor import IRSensor

# Initialize IR sensor and stepper motor
ir_sensor = IRSensor(pin=17)
motor = StepperMotor(in1=18, in2=23, in3=24, in4=25)

# Shared state
current_angle = 0
motion_lock = threading.Lock()
new_trigger = False

# IR watcher thread
def ir_watchdog():
    global new_trigger
    while True:
        if ir_sensor.is_object_detected():
            with motion_lock:
                new_trigger = True
            time.sleep(0.1)  # Debounce delay
        time.sleep(0.01)

# Motor motion thread
def motor_thread_func():
    global current_angle, new_trigger
    while True:
        if new_trigger:
            with motion_lock:
                new_trigger = False  # Reset the trigger

            print("Bean detected! Starting motion")

            # Perform motion steps
            current_angle = motor.go_to_angle(current_angle, 90)
            time.sleep(3)

            current_angle = motor.go_to_angle(current_angle, 180)
            time.sleep(3)

            current_angle = motor.go_to_angle(current_angle, 270)
            time.sleep(3)

            current_angle = motor.go_to_angle(current_angle, 0)
            time.sleep(0.5)

        time.sleep(0.01)

try:
    # Start threads
    threading.Thread(target=ir_watchdog, daemon=True).start()
    threading.Thread(target=motor_thread_func, daemon=True).start()

    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("Exiting...")
    motor.cleanup()
