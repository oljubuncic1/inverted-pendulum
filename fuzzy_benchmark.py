from baki_fuzzy_inference import get_controller as get_fake
from  fuzzy import get_controller as get_lib

import time, random

fake_ctrl = get_fake()
lib_ctrl = get_lib()

fake_sum = 0
lib_sum = 0

for i in range(0, 100):
    theta = random.random() * 3.14
    dtheta = random.random() * 3.14
    theta = 0.139277274309 
    dtheta = 5.48033385126
    

    print 'ins', theta, dtheta

    temp = time.time()
    lib_ctrl.input['theta'] = theta
    lib_ctrl.input['dtheta'] = dtheta
    lib_ctrl.compute()
    lib_ctrl.print_state()
    lib_out = lib_ctrl.output['force']
    lib_sum = lib_sum + (time.time() - temp)

    print '\tlib', lib_out

    temp = time.time()
    fake_out = fake_ctrl.output({'theta': theta, 'dtheta': dtheta})['force']
    fake_sum = fake_sum + (time.time() - temp)
    
    print '\tfake', fake_out
    print 'sums', lib_sum, fake_sum
    break


