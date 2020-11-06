import serial
import time

puerto = '/dev/ttyACM0'
arduino = serial.Serial(puerto, 115200)

print("ENCENDIENDO LED...")
arduino.write(b'Q')
time.sleep(10000)
print("APAGANDO LED...")
arduino.write(b'W')
