# coding: utf-8
# A serial transport demo

import serial

# Open and setup COM5,
# speed: 19200
# bytesize: 8
# stopbits: 1
ser = serial.Serial('COM5', 19200, bytesize=8, stopbits=1)

# String sent to COM5
outlabel = '66 01 01 05 00 05 00 55'

# Send String
try:
    result = ser.write(bytes.fromhex(outlabel))
except:
    # I don't know what kind of Error to fetch
    # If something is wrong, remove the try-except block to investigate
    print('Something is wrong.')
finally:
    # Close COM5 safely
    ser.close()
