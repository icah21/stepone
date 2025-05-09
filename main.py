# main.py
import threading
import time
import RPi.GPIO as GPIO
from stepmotor import StepperMotor
from ir_sensor import IRSensor

# Pin configuration
MOTOR_PINS = [17, 18, 27, 22]
IR_PIN = 23

motor = StepperMotor(MOTOR_PINS)
sensor = IRSensor(IR_PIN)

running_flag = threading.Event()

def motor_thread():
    while True:
        running_flag.wait()
        motor.execute_sequence()
        running_flag.clear()

def sensor_thread():
    while True:
        if sensor.detected() and not running_flag.is_set():
            print("Object detected! Starting motor sequence.")
            running_flag.set()
        time.sleep(0.2)

try:
    t1 = threading.Thread(target=motor_thread, daemon=True)
    t2 = threading.Thread(target=sensor_thread, daemon=True)
    t1.start()
    t2.start()

    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("Shutting down...")
    motor.cleanup()
    GPIO.cleanup()
