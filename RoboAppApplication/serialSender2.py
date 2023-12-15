import serial
import time
import flask
ser2 = serial.Serial('COM19', baudrate=9600, timeout=0.1)
def head_movement(command):
    ser2.write(command.encode())
    print("executed cOMMAND")
    


# code = "#1P2000T1000\r\n"

# head_movement(code)
  