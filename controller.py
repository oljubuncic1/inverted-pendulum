# NOT TESTED
import fuzzy
import serial

controller = fuzzy.get_controller()

def scale_output(x, factor=1.):
    return x * factor

while 1:
#    theta = ser.readline()
#    dtheta = ser.readline()
    theta = float(raw_input('theta: '))
    dtheta = float(raw_input('dtheta: '))

    controller.input['theta'] = theta
    controller.input['dtheta'] = dtheta
    controller.compute()

    output_force = controller.output['force']
    output_force = scale_output(output_force, 1)

    N = 3
    print output_force
