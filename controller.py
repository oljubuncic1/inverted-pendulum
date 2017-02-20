from fuzzy import get_controller as get_lib
import time
from math import pi
import serial
from baki_fuzzy_inference import get_controller as fake_ctrl

#controller = fuzzy.get_controller()

def scale_output(x, factor=1.):
    return x * factor

ser = serial.Serial('/dev/ttyACM0', 115200)
while ser.isOpen() == False:
    ser.open()

def normalize_theta(theta):
    return theta * pi / 180.0

print 'Connection established'

ctrl = fake_ctrl()
time.sleep(10)
prev_theta = 0
while 1:
    try: 
        theta = ser.readline()
        theta = float(theta[1:])
        theta = normalize_theta(theta)
        dtheta = (theta - prev_theta) / 0.01
#        ctrl.input['theta'] = theta
#        ctrl.input['dtheta'] = dtheta
#        ctrl.compute()

        original_output_force = ctrl.output({'theta': theta, 'dtheta': dtheta})['force']
        original_output_force = original_output_force * 100.0 / 66.0
        if original_output_force == -1024:
            print 'belaj', theta, dtheta
            continue
        prev_theta = theta
        output_force = abs(original_output_force) * 100
        if original_output_force > 0:
            output_force = output_force + 100
    
        output_force = int(output_force)
        print output_force, theta, prev_theta, dtheta
        ser.write(str(output_force))
    except Exception as e:
        print 'Exception', e
