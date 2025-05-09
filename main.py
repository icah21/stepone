import time
import threading
from stepper_motor import StepperMotor
from ir_sensor import IRSensor

# Initialize IR sensor and stepper motor
ir_sensor = IRSensor(pin=17)
motor = StepperMotor(in1=18, in2=23, in3=24, in4=25)

# Shared state
current_angle = 0

# Helper: interruptible delay
def interruptible_sleep(seconds, check_interval=0.1):
    for _ in range(int(seconds / check_interval)):
        if not ir_sensor.is_object_detected():
            return False  # interrupted
        time.sleep(check_interval)
    return True

def motor_thread_func():
    global current_angle
    while True:
        if ir_sensor.is_object_detected():
            print("Object detected!")

            while ir_sensor.is_object_detected():
                current_angle = motor.go_to_angle(current_angle, 90)
                if not interruptible_sleep(3):
                    break

                current_angle = motor.go_to_angle(current_angle, 180)
                if not interruptible_sleep(2):
                    break

                current_angle = motor.go_to_angle(current_angle, 270)
                if not interruptible_sleep(5):
                    break

                current_angle = motor.go_to_angle(current_angle, 0)
                if not interruptible_sleep(2):
                    break

            print("Object no longer detected, waiting...")
        else:
            time.sleep(0.1)

try:
    motor_thread = threading.Thread(target=motor_thread_func)
    motor_thread.daemon = True
    motor_thread.start()

    while True:
        time.sleep(1)  # Keep main thread alive

except KeyboardInterrupt:
    print("Exiting...")
    motor.cleanup()
