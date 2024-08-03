import serial
port = "/dev/ttyACM0"
ser = serial.Serial(port, baudrate=9600)
ser.flushInput()

while True:
    if(ser.inWaiting() > 0):
        in_msg = ser.read()
        print(ord(in_msg))