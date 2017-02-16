import serial, time
from math import pi

print "Establishing connection"

ser = serial.Serial('/dev/ttyACM0', 9600)
while(ser.isOpen() == False):
    ser.open()

print "Connection established"

def normalize_theta(x):
    return ((17 * pi * x) /12420) - ((59*pi)/138)

count = 20
i = 0
prev_val = 0
prev_force = 0
ser.write('5')
print 'Waiting message...'
last_time = time.time()
while 1:
    try:
        i = i + 1
        line = ser.readline()
        print 'got', line
        theta = int(line[1:])
        #x = int(line[line.index('T')+1:]) * 100
        x = time.time() - last_time
        last_time = time.time()
        theta = normalize_theta(theta)
        dtheta = (theta - prev_val) / x
        f = 200
        if abs(theta) < 0.01:
            f = 0
        elif theta < 0:
            f = 99
        print "Applying force ", f
        ser.write(str(f))
    except Exception as e:
        print e
        ser.write(str(prev_force))
        pass

