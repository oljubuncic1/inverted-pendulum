import time
from math import pi
import serial
from fuzzy_controller import get_controller as fake_ctrl
import signal
import logging
import sys

def normalize_theta(theta):
    return theta * pi / 180.0

ser = serial.Serial('/dev/ttyACM0', 115200)

while ser.isOpen() == False:
    ser.open()

print 'Connection established, sleeping 10 sec...'
time.sleep(10)
print 'Woke up (not like Fake)'

def graceful_shutdown(signal, frame):
    print "Shutting down gracefully, as BAKI deserved..."
    for i in range(10):
        ser.write('0')
    ser.close()
    sys.exit(0)

signal.signal(signal.SIGINT, graceful_shutdown)
signal.signal(signal.SIGTERM, graceful_shutdown)

sleep_time = 0.03

ctrl = fake_ctrl()

prev_theta = 0
theta = 'A0'
last_time = 0
while True:
    try:
        temp_time = time.time()
        dtime = temp_time - last_time
        last_time = temp_time

        theta = float(theta[1:])
        print theta
        theta = normalize_theta(theta)
        dtheta = (theta - prev_theta) / dtime

        original_output_force = ctrl.output({'theta': theta, 'dtheta': dtheta})['force']
        original_output_force = original_output_force
        if original_output_force == -1024:
            print 'Error: Fuzzy controller calculated 0 area'
            continue
        
        output_force = abs(original_output_force) * 100
        prev_theta = theta

        # print '(output_force, theta, dtheta) = (', output_force, theta * 180.0 / pi, dtheta, ');'

        if original_output_force < 0:
            output_force = output_force + 100
        output_force = int(output_force)
        
        print('Sending force...')
        ser.write(str(output_force))
        if ser.inWaiting():
            theta = ser.readline()
        else:
            theta = 'A0'
            print 'Did not receive anything'

        time.sleep(sleep_time)
    except Exception as e:
            print 'Error: An Exception has occured', e
            break
