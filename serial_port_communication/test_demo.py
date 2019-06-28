# coding: utf-8

import serial

ser = serial.Serial('COM5', 19200)

outlabel = '66 01 01 05 00 05 00 55'

try:
    result = ser.write(bytes.fromhex(outlabel))
except:
    print('Something is wrong.')
finally:
    ser.close()
