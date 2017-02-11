# NOT TESTED
import fuzzy
import serial

ser = serial.Serial('/dev/ttyACM0', 9600)
controller = fuzzy.get_controller()

def scale_output(x, factor=1.):
    return x * factor

while 1:
    theta = ser.readline()
    dtheta = ser.readline()

    controller.input['theta'] = theta
    controller.input['dtheta'] = dtheta
    controller.compute()

    output_force = controller.output['force']
    output_force = scale_output(output_force, 10)

    N = 3
    ser.write(str(output_force)[0:N])
