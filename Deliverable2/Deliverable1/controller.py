# This module translates the serial input from the capacitive touchpad

import serial, time

dataDic = {'\xbe\xef':'Wake Up', '\xde\xad':'Sleep', '\x80\x80': 'Center'}

touch = serial.Serial()
touch.port = '/dev/ttyACM0'
touch.baudrate = 9600
touch.open()

if touch.isOpen():    
    try:
        touch.flushInput()
        touch.flushOutput()
        time.sleep(1)
    except:
        pass    
    for i in range(0,10):
        print "Is the device readable? ", touch.readable()
    #time.sleep(3)
        try:
            data = touch.read(size=2)
        except:
            print "failed"
            continue
        try:
            print dataDic[data]
        except:
            print data
        time.sleep(1)
touch.close()
