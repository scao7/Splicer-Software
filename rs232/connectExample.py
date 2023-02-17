# connect rs232 tutorial
# 
import serial
import time 

ser = serial.Serial(
    port="COM3",  
    baudrate=4800,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=None,
    xonxoff=0,
    rtscts=0,
)

ser.isOpen()
ser.write(b'\xa1')
time.sleep(1)

SPEED = b'\xa3\x30\x30\x32\x31'
ser.write(SPEED)
time.sleep(1)
print(ser.read())

time.sleep(5)
ser.write(b'\xaa')


# READINCLINE = b'\xc2'
# SETINCLINE = b'\xa3\x30\x33\x35\x30'
# ser.write(SETINCLINE)
# time.sleep(1)
# print(ser.read())
# time.sleep(60)
# ser.write(READINCLINE)
# time.sleep(1)
# print(ser.read())

ser.close()

 